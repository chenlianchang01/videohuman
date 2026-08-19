# assets/background_images/ — 背景图目录(需自备)

本目录**初始为空**,不随仓库分发任何图片。请自行放入背景图:

- 支持格式:`.png` / `.jpg` / `.jpeg` / `.webp`
- 建议使用可商用图库,例如 Unsplash(<https://unsplash.com>)、Pexels(<https://www.pexels.com>),
  或自己制作的图片;请自行确认许可。

## 流水线如何选取

postprocess 阶段的背景图合成(`vh_core/stages/postprocess.py`)**默认关闭**,通过 job 参数
`postprocess.bg_image` 开启:

- `bg_image = true`:从本目录**随机**挑一张图,把口播视频缩小叠加到 1080×1920(可用
  `bg_canvas_w` / `bg_canvas_h` / `bg_fg_ratio` 调整)画布中央;
- `bg_image = "图片文件名或路径"`:使用指定图片(先按本目录内文件名找,再按绝对/相对路径找);
- 目录为空或指定文件不存在时**不会报错**,只输出警告并跳过背景图合成。
