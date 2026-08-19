# assets/bgm/ — 背景音乐目录(需自备)

本目录**初始为空**,不随仓库分发任何音乐。请自行放入背景音乐的副本:

- 支持格式:`.mp3` / `.wav` / `.m4a` / `.aac` / `.flac` / `.ogg`
- 建议使用免版税/可商用音乐,例如 YouTube Audio Library(<https://studio.youtube.com> 内音频库)、
  或其他已取得授权的音源;请自行确认许可。

## 流水线如何选取

postprocess 阶段的 BGM 混音(默认开启)按以下优先级选取(`vh_core/stages/postprocess.py`):

1. job 参数 `bgm_path`(或全局配置 `bgm_path`)指定的文件;
2. 否则取**本目录按文件名排序后的第一首**可用音频;
3. 目录为空时**不会报错**,只输出警告"未找到 BGM,输出仅含原音",成片仅保留人声。

混音音量由 `bgm_volume` 参数控制(默认见 `configs/default.toml`)。不需要 BGM 时可在 job 参数里设
`postprocess.bgm = false`。
