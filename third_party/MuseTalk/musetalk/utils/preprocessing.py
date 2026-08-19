"""[vh2 补丁] MuseTalk 预处理:去 mmpose/mmcv 化。

原版用 mmpose dwpose 推理全身关键点再取 [23:91] 作为 68 点脸部 landmark,
在 Windows + 新 torch 环境下 mmcv 系依赖装不上。本补丁将 landmark 来源替换为
mediapipe FaceMesh(468 点,模型随 wheel 内置,无需下载,dwpose 权重不再需要)。

下游消费约定保持不变:
- 返回 68x2 数组,其中 [28]/[29]/[30] 为鼻梁竖列三点(上→下);
- min(x)/max(x)/max(y) 由脸部轮廓点给出,用于裁剪框计算。
"""
import sys
from face_detection import FaceAlignment, LandmarksType
from os import listdir, path
import subprocess
import numpy as np
import cv2
import pickle
import os
import json
import torch
from tqdm import tqdm

# initialize the face detection model
device = "cuda" if torch.cuda.is_available() else "cpu"
fa = FaceAlignment(LandmarksType._2D, flip_input=False, device=device)

# maker if the bbox is not sufficient
coord_placeholder = (0.0, 0.0, 0.0, 0.0)


class _MediapipeLandmarker:
    """mediapipe FaceMesh → 伪 68 点 landmark(满足下游消费约定)。"""

    # 鼻梁竖列三点(上→下),对应 68 点方案的 28/29/30
    IDX_NOSE = (6, 195, 4)

    def __init__(self):
        import mediapipe as mp
        self._mesh = mp.solutions.face_mesh.FaceMesh(
            static_image_mode=True, max_num_faces=1, refine_landmarks=False,
        )
        from mediapipe.python.solutions.face_mesh_connections import FACEMESH_FACE_OVAL
        self._oval_idx = sorted({i for pair in FACEMESH_FACE_OVAL for i in pair})

    def get(self, frame_bgr) -> np.ndarray | None:
        """返回 68x2 float32 landmark;检测不到人脸返回 None。"""
        h, w = frame_bgr.shape[:2]
        rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        res = self._mesh.process(rgb)
        if not res.multi_face_landmarks:
            return None
        pts = np.array(
            [[p.x * w, p.y * h] for p in res.multi_face_landmarks[0].landmark],
            dtype=np.float32,
        )
        out = np.tile(pts[self._oval_idx], (2, 1))[:68]  # 轮廓点填满,提供 min/max 范围
        out[28], out[29], out[30] = pts[list(self.IDX_NOSE)]
        return out


_landmarker = _MediapipeLandmarker()


def _get_face_landmark(frame) -> np.ndarray | None:
    return _landmarker.get(frame)


def resize_landmark(landmark, w, h, new_w, new_h):
    w_ratio = new_w / w
    h_ratio = new_h / h
    landmark_norm = landmark / [w, h]
    landmark_resized = landmark_norm * [new_w, new_h]
    return landmark_resized

def read_imgs(img_list):
    frames = []
    print('reading images...')
    for img_path in tqdm(img_list):
        frame = cv2.imread(img_path)
        frames.append(frame)
    return frames

def get_bbox_range(img_list,upperbondrange =0):
    frames = read_imgs(img_list)
    batch_size_fa = 1
    batches = [frames[i:i + batch_size_fa] for i in range(0, len(frames), batch_size_fa)]
    coords_list = []
    landmarks = []
    if upperbondrange != 0:
        print('get key_landmark and face bounding boxes with the bbox_shift:',upperbondrange)
    else:
        print('get key_landmark and face bounding boxes with the default value')
    average_range_minus = []
    average_range_plus = []
    for fb in tqdm(batches):
        face_land_mark = _get_face_landmark(np.asarray(fb)[0])
        if face_land_mark is None:
            coords_list += [coord_placeholder]
            continue
        face_land_mark = face_land_mark.astype(np.int32)

        # get bounding boxes by face detetion
        bbox = fa.get_detections_for_batch(np.asarray(fb))

        # adjust the bounding box refer to landmark
        # Add the bounding box to a tuple and append it to the coordinates list
        for j, f in enumerate(bbox):
            if f is None: # no face in the image
                coords_list += [coord_placeholder]
                continue

            half_face_coord =  face_land_mark[29]#np.mean([face_land_mark[28], face_land_mark[29]], axis=0)
            range_minus = (face_land_mark[30]- face_land_mark[29])[1]
            range_plus = (face_land_mark[29]- face_land_mark[28])[1]
            average_range_minus.append(range_minus)
            average_range_plus.append(range_plus)
            if upperbondrange != 0:
                half_face_coord[1] = upperbondrange+half_face_coord[1] #手动调整  + 向下（偏29）  - 向上（偏28）

    text_range=f"Total frame:「{len(frames)}」 Manually adjust range : [ -{int(sum(average_range_minus) / len(average_range_minus))}~{int(sum(average_range_plus) / len(average_range_plus))} ] , the current value: {upperbondrange}"
    return text_range


def get_landmark_and_bbox(img_list,upperbondrange =0):
    frames = read_imgs(img_list)
    batch_size_fa = 1
    batches = [frames[i:i + batch_size_fa] for i in range(0, len(frames), batch_size_fa)]
    coords_list = []
    landmarks = []
    if upperbondrange != 0:
        print('get key_landmark and face bounding boxes with the bbox_shift:',upperbondrange)
    else:
        print('get key_landmark and face bounding boxes with the default value')
    average_range_minus = []
    average_range_plus = []
    for fb in tqdm(batches):
        face_land_mark = _get_face_landmark(np.asarray(fb)[0])
        if face_land_mark is None:
            coords_list += [coord_placeholder]
            continue
        face_land_mark = face_land_mark.astype(np.int32)

        # get bounding boxes by face detetion
        bbox = fa.get_detections_for_batch(np.asarray(fb))

        # adjust the bounding box refer to landmark
        # Add the bounding box to a tuple and append it to the coordinates list
        for j, f in enumerate(bbox):
            if f is None: # no face in the image
                coords_list += [coord_placeholder]
                continue

            half_face_coord =  face_land_mark[29]#np.mean([face_land_mark[28], face_land_mark[29]], axis=0)
            range_minus = (face_land_mark[30]- face_land_mark[29])[1]
            range_plus = (face_land_mark[29]- face_land_mark[28])[1]
            average_range_minus.append(range_minus)
            average_range_plus.append(range_plus)
            if upperbondrange != 0:
                half_face_coord[1] = upperbondrange+half_face_coord[1] #手动调整  + 向下（偏29）  - 向上（偏28）
            half_face_dist = np.max(face_land_mark[:,1]) - half_face_coord[1]
            min_upper_bond = 0
            upper_bond = max(min_upper_bond, half_face_coord[1] - half_face_dist)

            f_landmark = (np.min(face_land_mark[:, 0]),int(upper_bond),np.max(face_land_mark[:, 0]),np.max(face_land_mark[:,1]))
            x1, y1, x2, y2 = f_landmark

            if y2-y1<=0 or x2-x1<=0 or x1<0: # if the landmark bbox is not suitable, reuse the bbox
                coords_list += [f]
                w,h = f[2]-f[0], f[3]-f[1]
                print("error bbox:",f)
            else:
                coords_list += [f_landmark]

    print("********************************************bbox_shift parameter adjustment**********************************************************")
    print(f"Total frame:「{len(frames)}」 Manually adjust range : [ -{int(sum(average_range_minus) / len(average_range_minus))}~{int(sum(average_range_plus) / len(average_range_plus))} ] , the current value: {upperbondrange}")
    print("*************************************************************************************************************************************")
    return coords_list,frames


if __name__ == "__main__":
    img_list = ["./results/lyria/00000.png","./results/lyria/00001.png","./results/lyria/00002.png","./results/lyria/00003.png"]
    crop_coord_path = "./coord_face.pkl"
    coords_list,full_frames = get_landmark_and_bbox(img_list)
    with open(crop_coord_path, 'wb') as f:
        pickle.dump(coords_list, f)

    for bbox, frame in zip(coords_list,full_frames):
        if bbox == coord_placeholder:
            continue
        x1, y1, x2, y2 = bbox
        crop_frame = frame[y1:y2, x1:x2]
        print('Cropped shape', crop_frame.shape)

    print(coords_list)
