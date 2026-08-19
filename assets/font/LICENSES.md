# assets/font/ — 字体来源与许可

本目录字体用于字幕烧录与封面绘制(流水线自动扫描本目录,见 `vh_core/stages/postprocess.py`)。
逐个来源与许可如下:

| 字体文件 | 名称 | 许可 | 来源 |
|---|---|---|---|
| `AlibabaPuHuiTi-3-*.ttf` | 阿里巴巴普惠体 3.0 | 官方免费商用 | <https://www.alibabafonts.com> |
| `ZhanKuWenYiTi-2.ttf` | 站酷文艺体 | 免费商用 | <https://www.zcool.com.cn/special/zcoolfonts/> |
| `ShangguSerif-*.ttf` | 尙古明體 | SIL Open Font License (OFL) | 见下方 OFL 说明 |
| `XiaoheSimplifySerif-*.ttf` | 小合简化体 | SIL Open Font License (OFL) | 见下方 OFL 说明 |
| `TaipeiSansTCBeta-Bold.ttf` | 思源黑体衍生(Taipei Sans TC Beta) | SIL Open Font License (OFL) | 见下方 OFL 说明 |
| `CooperZhengKai-1.2.ttf` | Cooper ZhengKai | SIL Open Font License (OFL) | 见下方 OFL 说明 |

## OFL 协议要点(SIL Open Font License)

- 允许自由使用、研究、修改、再分发,**可商用**,可嵌入文档/视频/应用;
- 字体不得**单独出售**;
- 修改后再分发时,若原作者保留了名称(Reserved Font Name),必须改名;
- 再分发时必须连同 OFL 协议原文一起提供。

协议全文:<https://openfontlicense.org>

## 添加自己的字体

可以直接往本目录放 `.ttf` / `.otf` / `.ttc` 字体文件——字幕与封面会自动扫描本目录
(字幕取按文件名排序后第一个可用字体;封面按文案缺字情况挑选能覆盖全部字符的字体)。
也可用 job 参数 `subtitle_font` 指定具体字体文件。请自行确认所加字体的许可。
