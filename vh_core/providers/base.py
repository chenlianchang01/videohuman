"""三个吃 GPU 环节的 Provider 协议。

local/ 下的实现遵循同一组协议;stage 只面向协议编程,
由 get_provider 按 engine 选择具体实现。
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class ASRProvider(Protocol):
    """语音转写。local: SenseVoice-Small。"""

    def transcribe(self, audio: Path, **kwargs: Any) -> dict:
        """返回带时间轴的字幕 JSON(dict)。"""
        ...


@runtime_checkable
class TTSProvider(Protocol):
    """语音合成。local: CosyVoice3(默认)/IndexTTS2(备选)。"""

    def synthesize(self, text: str, out_path: Path, ref_audio: Path | None = None, **kwargs: Any) -> Path:
        """合成语音写入 out_path，返回该路径。"""
        ...


@runtime_checkable
class AvatarProvider(Protocol):
    """数字人生成。local: MuseTalk 1.5(默认)/LstmSync(可选,引擎需自备)。"""

    def generate(self, video: Path, audio: Path, out_path: Path, **kwargs: Any) -> Path:
        """以 video 为形象、audio 为驱动音频生成数字人视频，返回 out_path。"""
        ...
