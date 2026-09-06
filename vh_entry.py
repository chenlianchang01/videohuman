"""videohuman 统一入口(供 PyInstaller 打包为 videohuman.exe)。

在原 vh CLI 基础上增加 download-weights 子命令,使打包后无需 Python 环境
也能下载模型权重。

用法:
  videohuman.exe <CLI 子命令>          # 原 vh 全部功能(run/serve/batch/...)
  videohuman.exe download-weights [ms|hf|all]  # 下载模型权重
"""
from __future__ import annotations

import os
import sys


def _bootstrap_frozen() -> None:
    """PyInstaller 打包后把 _internal 目录加入 sys.path 头部。

    third_party 下的 CosyVoice/MuseTalk 等通过 sys.path 注入后动态 import,
    必须确保 _internal 在路径最前,避免命中外部同名包。
    """
    if not getattr(sys, "frozen", False):
        return
    exe_dir = os.path.dirname(sys.executable)
    internal = os.path.join(exe_dir, "_internal")
    if os.path.isdir(internal) and internal not in sys.path:
        sys.path.insert(0, internal)
    # 让 download_weights.py 的 __file__ 定位到 _internal(项目根)
    os.chdir(exe_dir)


def _run_download_weights() -> None:
    """转发到 download_weights 模块(打包后位于 _internal/download_weights.py)。"""
    which = sys.argv[2] if len(sys.argv) > 2 else "all"
    if which not in ("ms", "hf", "all"):
        print(f"未知参数: {which}(可选: ms / hf / all)", file=sys.stderr)
        sys.exit(2)

    import download_weights  # noqa: PLC0415

    os.makedirs(download_weights.MODELS_DIR, exist_ok=True)
    if which in ("ms", "all"):
        download_weights.download_ms()
    if which in ("hf", "all"):
        download_weights.download_hf()
        download_weights.download_s3fd()
    print("== 全部下载任务结束 ==", flush=True)


def main() -> None:
    _bootstrap_frozen()

    if len(sys.argv) > 1 and sys.argv[1] == "download-weights":
        _run_download_weights()
        return

    from vh_cli.main import app  # noqa: PLC0415
    app()


if __name__ == "__main__":
    main()
