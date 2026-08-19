"""后期处理子模块:静音切除 / 水印 / 封面。

包内只做相对 import,无模块级副作用,路径全参数化;
ffmpeg 调用统一走 vh_core.ffmpeg_utils.run_ffmpeg。
"""

from .cover import add_multicolor_text, extract_frame
from .silence import cut_silence, detect_silences, probe_video
from .watermark import add_ai_watermark, add_text_watermark, pick_font_file

__all__ = [
    "add_ai_watermark",
    "add_multicolor_text",
    "add_text_watermark",
    "cut_silence",
    "detect_silences",
    "extract_frame",
    "pick_font_file",
    "probe_video",
]
