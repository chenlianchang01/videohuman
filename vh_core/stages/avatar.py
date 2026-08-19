"""avatar stage — 数字人生成,调 AvatarProvider(默认 MuseTalk,备选 LstmSync)。

音频取 tts 产物 speech.wav;素材视频来自 params.avatar_video(或 config 默认)。
params["avatar"] 透传 provider 级参数(batch_size/fps/extra_margin/use_float16 等)。
"""

from __future__ import annotations

from pathlib import Path

from ..pipeline import Stage, StageContext
from ..providers import get_provider


class AvatarStage(Stage):
    name = "avatar"

    def run(self, ctx: StageContext) -> dict[str, Path]:
        audio = ctx.job_dir / "tts" / "speech.wav"
        if not audio.exists():
            raise FileNotFoundError("avatar 需要 tts 产物 speech.wav,请先跑 tts stage")

        engine = ctx.params.get("avatar_engine")
        video = ctx.params.get("avatar_video") or ctx.settings.avatar_video
        if not video:
            raise ValueError("avatar 需要素材视频:params.avatar_video 或 config avatar_video")
        video = Path(video)
        if not video.is_absolute():
            video = (ctx.settings.abs_path(video))

        avatar_params = dict(ctx.params.get("avatar", {}))
        out = ctx.stage_dir / "avatar.mp4"
        provider = get_provider("avatar", ctx.settings, engine=engine)
        provider.generate(
            video=video, audio=audio, out_path=out,
            work_dir=ctx.stage_dir / "tmp",
            **avatar_params,
        )
        return {"avatar": out}
