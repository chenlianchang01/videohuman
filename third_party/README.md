# third_party/ — 随仓库分发的开源组件源码

> 本目录存放流水线依赖的开源项目源码(浅克隆,`--depth 1`)。
> 模型权重一律不进 git,需用仓库根目录的 `download_weights.py` 单独下载(见 `models/README.md`)。
>
> 已克隆版本(2026-08-07):MuseTalk `0a89dec`(2025-09-26)、CosyVoice `074ca6d`(2026-05-26)、index-tts `90ca4d6`(2026-08-05)、LatentSync `a229c39`(2025-06-20)

## Vendor 清单与许可

| 目录 | 上游仓库 | 许可 | 用途 |
|---|---|---|---|
| `MuseTalk/` | [TMElyralab/MuseTalk](https://github.com/TMElyralab/MuseTalk) | MIT(Tencent Music) | 数字人引擎(默认),v1.5。实时唇形同步,配合 `models/` 外置权重使用 |
| `CosyVoice/` | [FunAudioLLM/CosyVoice](https://github.com/FunAudioLLM/CosyVoice) | Apache-2.0 | TTS(默认),配合 Fun-CosyVoice3-0.5B-2512 权重,支持声音克隆 |
| `LatentSync/` | [bytedance/LatentSync](https://github.com/bytedance/LatentSync) | Apache-2.0(ByteDance) | 数字人引擎(备选),v1.6,512×512 训练,画质优先场景使用 |
| `index-tts/` | [index-tts/index-tts](https://github.com/index-tts/index-tts) | **bilibili Model Use License**(非 OSI 标准协议,见目录内 `LICENSE`/`LICENSE_ZH.txt`) | TTS(备选),IndexTTS2,情绪控制 + 时长精确控制 |

**IndexTTS-2 协议要点(bilibili Model Use License):**

- 你或你关联公司的产品/服务**月活跃用户超过 1 亿**,或上一自然年**年收入超过 10 亿元人民币**,须向 bilibili 单独申请授权,否则无权使用;
- 每份模型或其衍生作品的拷贝中**必须保留原始版权声明及协议全文**(因此 `download_weights.py` 在下载 IndexTTS-2 权重后会自动把 `third_party/index-tts/LICENSE` 复制到 `models/IndexTTS-2/`);
- 不得用该模型改进除 IndexTTS-2 自身及其衍生作品以外的商业 AI 模型。

## 本地修改清单(许可证合规声明)

为适配本项目的运行环境,对 vendor 源码做过以下修改,**每处修改在对应文件内均有
`[vh2]` / `[vh2 补丁]` 注释标记**(Apache-2.0 §4(b) 要求的修改声明):

- `MuseTalk/`(MIT):
  - `musetalk/utils/preprocessing.py`:landmark 来源由 mmpose/dwpose 替换为 mediapipe FaceMesh(去 mmcv 系依赖,dwpose 权重不再需要);
  - `musetalk/models/unet.py`、`musetalk/utils/face_detection/detection/sfd/sfd_detector.py`、`musetalk/utils/face_parsing/__init__.py`、`musetalk/utils/face_parsing/resnet.py`:`torch.load` 显式 `weights_only=False`(适配 torch ≥ 2.6 的新默认值,加载官方旧权重)。
- `CosyVoice/`(Apache-2.0):
  - `cosyvoice/utils/file_utils.py`:`load_wav` 改用 soundfile 读取(绕开 torchaudio 2.9 在 Windows 上的 torchcodec 依赖),重采样仍走 torchaudio。
- `index-tts/`、`LatentSync/`:**未做任何修改**。

## 不需要克隆的组件

- **FunASR / SenseVoice-Small(ASR)**:`pip install funasr` 即可,模型走 ModelScope 按需下载
- **faster-whisper(ASR 备选)**:pip 包

## LstmSync(可选,自备)

LstmSync 是可选的第二个数字人引擎,**授权制**,其引擎代码与权重**不随本仓库分发**。

- 上游仓库:<https://github.com/oneCodeSuperman/LstmSync>
- 授权与 api_key:<https://lstmsync.andclaw.cn/>
- 获取方式:按上游指引取得授权后,将引擎放入 `third_party/lstmsync/`(或修改 `configs/default.toml` 中的 `lstmsync_dir` 指向实际位置),并在配置中填入 api_key。
- 所需文件:
  - 引擎代码:`lstmsync_func.py` 等
  - 权重:`checkpoints/` 目录,含 `256.onnx`、`256_m.onnx`、`repair.npy`、`chinese-hubert-large/`、`auxiliary/`

只有 `avatar_engine = "lstmsync"` 时才需要;默认引擎为 MuseTalk,无此依赖。
