# models/ — 模型权重目录(不进 git)

> 本目录存放运行所需的模型权重,**一律不进 git**(见根目录 `.gitignore`)。
> 下载统一用仓库根目录的 `download_weights.py`(requests 直连 + 断点续传):
>
> ```bash
> uv run python download_weights.py [ms|hf|all]
> ```

## 权重清单

| 目录 | 来源 | 许可 | 用途 |
|---|---|---|---|
| `Fun-CosyVoice3-0.5B-2512/` | ModelScope [`FunAudioLLM/Fun-CosyVoice3-0.5B-2512`](https://modelscope.cn/models/FunAudioLLM/Fun-CosyVoice3-0.5B-2512) | 见模型页 | TTS 默认(CosyVoice3,声音克隆) |
| `SenseVoiceSmall/` | ModelScope [`iic/SenseVoiceSmall`](https://modelscope.cn/models/iic/SenseVoiceSmall) | Apache-2.0 | ASR 默认(字幕时间轴对齐) |
| `IndexTTS-2/`(可选) | HuggingFace [`IndexTeam/IndexTTS-2`](https://huggingface.co/IndexTeam/IndexTTS-2)(经 hf-mirror) | **bilibili Model Use License** | TTS 备选,受 bilibili 模型协议约束(月活 >1 亿或年收入 >10 亿需单独授权;每份拷贝须附协议全文——下载脚本会自动把 `third_party/index-tts/LICENSE` 复制进来) |

## MuseTalk 配套权重

MuseTalk(默认数字人引擎)的权重不在本目录,而是放在 `third_party/MuseTalk/models/` 下,由 `download_weights.py` 经 hf-mirror(<https://hf-mirror.com>)拉取:

- `musetalk/`、`musetalkV15/`:MuseTalk V1.0 / V1.5 UNet(HF `TMElyralab/MuseTalk`)
- `sd-vae/`(HF `stabilityai/sd-vae-ft-mse`)、`whisper/`(HF `openai/whisper-tiny`)、`syncnet/`(HF `ByteDance/LatentSync`)、`face-parse-bisent/`(HF `ManyOtherFunctions/face-parse-bisent`)

另有一个 S3FD 人脸检测权重 `s3fd.pth`(约 86MB),随 `download_weights.py` 从官方源
(face-alignment 项目)下载到 `third_party/MuseTalk/musetalk/utils/face_detection/detection/sfd/`;
漏下载时引擎首次运行也会自动拉取到 torch hub 缓存。

## LstmSync 权重

LstmSync 为授权制自备引擎,权重**无公开下载来源**,本脚本不提供下载。
获取方式见 `third_party/README.md` 末尾的"LstmSync(可选,自备)"一节。
