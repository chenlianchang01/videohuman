# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller 打包配置 — videohuman Windows onedir(非便携)版。

构建: pyinstaller videohuman.spec
产物: dist/videohuman/videohuman.exe + dist/videohuman/_internal/

设计要点:
- onedir 模式(用户要求非便携版,启动比 onefile 快)
- torch CUDA 12.8 全套 dll 必须 collect_all,否则运行时缺 cudnn/cublas
- third_party(CosyVoice/MuseTalk/...)整体作为数据打包,运行时 sys.path 注入后 import
- web/dist 前端构建产物必须先 npm run build 再打包
- 模型权重(约16GB)不打包,首次运行 videohuman.exe download-weights 下载
"""
import os
import sys

from PyInstaller.utils.hooks import (
    collect_all,
    collect_data_files,
    collect_dynamic_libs,
    collect_submodules,
)

block_cipher = None
ROOT = SPECPATH  # PyInstaller 内置变量:spec 文件所在目录 = 项目根

# ============================================================
# 1. 收集依赖
# ============================================================
datas = []
binaries = []
hiddenimports = []


def _safe_collect_all(pkg):
    """collect_all 的容错包装(包不存在时跳过)。"""
    try:
        d, b, h = collect_all(pkg)
        return d, b, h
    except Exception as e:
        print(f"[spec] collect_all({pkg}) 跳过: {e}", flush=True)
        return [], [], []


# ---- 必须完整收集的 AI 框架(CUDA dll / 动态导入 / 数据文件) ----
for pkg in [
    "torch",
    "torchaudio",
    "torchvision",
    "transformers",
    "diffusers",
    "funasr",
    "mediapipe",
    "insightface",
    "modelscope",
    "accelerate",
]:
    d, b, h = _safe_collect_all(pkg)
    datas += d
    binaries += b
    hiddenimports += h

# ---- 只收集二进制/dll 的包 ----
# 注意: onnxruntime-gpu 安装后 import 名为 onnxruntime,无需单独收集 onnxruntime_gpu
for pkg in [
    "onnxruntime",
    "numba",
    "llvmlite",
    "pyworld",
    "soundfile",
    "cv2",
    "scipy",
    "sklearn",
    "kornia",
]:
    try:
        binaries += collect_dynamic_libs(pkg)
    except Exception:
        pass

# ---- 只收集数据文件的包 ----
for pkg in [
    "imageio_ffmpeg",       # 内置 ffmpeg.exe
    "librosa",              # 示例音频/配置
    "PIL",                  # 字体等
    "fonttools",            # 字体数据
    "pydantic",             # 可能有 .json
    "omegaconf",
    "hydra",
    "biliup",
    "playwright",           # driver 脚本(不含浏览器二进制)
    "x_transformers",
    "conformer",
    "HyperPyYAML",
]:
    try:
        datas += collect_data_files(pkg)
    except Exception:
        pass

# ---- 子模块(hidden import) ----
for pkg in [
    "torch", "torchaudio", "torchvision",
    "transformers", "diffusers", "funasr",
    "mediapipe", "insightface", "modelscope",
    "accelerate", "datasets", "evaluate",
    "librosa", "numba", "sklearn",
    "scipy", "PIL", "cv2", "kornia",
    "pyarrow", "cryptography", "openai",
    "fastapi", "uvicorn", "starlette",
    "pydantic", "typer", "click",
    "loguru", "omegaconf", "hydra",
    "biliup", "playwright", "einops",
    "inflect", "regex", "tqdm",
    "x_transformers", "conformer",
    "imageio", "imageio_ffmpeg",
    "soundfile", "pyworld",
    "onnxruntime",
]:
    try:
        hiddenimports += collect_submodules(pkg)
    except Exception:
        pass

# ============================================================
# 2. 项目资源文件(打包到 _internal/ 下对应路径)
# ============================================================
# third_party 整体打包(CosyVoice/MuseTalk/LatentSync/index-tts)
# 注意:这些是 vendored 代码,通过 sys.path 注入后 import,
# 必须以原始 .py 文件存在(不能只进 PYZ),否则 __file__ 定位失效。
for sub in ["CosyVoice", "MuseTalk", "LatentSync", "index-tts"]:
    src = os.path.join(ROOT, "third_party", sub)
    if os.path.isdir(src):
        datas.append((src, os.path.join("third_party", sub)))

# 配置 / 素材 / 示例 / 前端
_resource_dirs = [
    ("configs", "configs"),
    ("assets", "assets"),
    ("examples", "examples"),
    ("web/dist", "web/dist"),
]
for src_rel, dst_rel in _resource_dirs:
    src = os.path.join(ROOT, src_rel)
    if os.path.isdir(src):
        datas.append((src, dst_rel))

# 根目录文件
for fname in ["download_weights.py", "README.md", "LICENSE", "NOTICE", "使用说明.txt"]:
    src = os.path.join(ROOT, fname)
    if os.path.isfile(src):
        datas.append((src, "."))

# models 目录占位(运行时下载权重;空目录也需要存在)
models_dir = os.path.join(ROOT, "models")
os.makedirs(models_dir, exist_ok=True)
datas.append((models_dir, "models"))

# ============================================================
# 3. Hidden imports — third_party 代码动态导入的模块
# ============================================================
hiddenimports += [
    # --- CosyVoice 运行时导入 ---
    "cosyvoice",
    "cosyvoice.cli",
    "cosyvoice.cli.cosyvoice",
    "cosyvoice.cli.frontend",
    "cosyvoice.cli.model",
    "cosyvoice.flow",
    "cosyvoice.flow.DiT",
    "cosyvoice.hifigan",
    "cosyvoice.utils",
    "matcha",
    "matcha.models",
    "matcha.utils",
    "matcha.text",
    "matcha.hifigan",
    # --- MuseTalk 运行时导入 ---
    "musetalk",
    "musetalk.utils",
    "musetalk.utils.audio_processor",
    "musetalk.utils.audio_utils",
    "musetalk.utils.face_parsing",
    "musetalk.utils.utils",
    "musetalk.utils.preprocessing",
    "musetalk.utils.blending",
    "musetalk.utils.face_detection",
    "musetalk.utils.face_detection.detection",
    "musetalk.utils.face_detection.detection.sfd",
    "musetalk.utils.dwpose",
    # --- transformers 动态模型 ---
    "transformers.models",
    "transformers.models.whisper",
    "transformers.models.whisper.modeling_whisper",
    "transformers.models.bert",
    "transformers.models.gpt2",
    "transformers.models.clip",
    "transformers.pipelines",
    "transformers.pipelines.audio_classification",
    "transformers.pipelines.automatic_speech_recognition",
    "transformers.feature_extraction_utils",
    "transformers.processing_utils",
    # --- funasr ---
    "funasr.models",
    "funasr.datasets",
    "funasr.train",
    "funasr.utils",
    "funasr.register",
    # --- insightface ---
    "insightface.app",
    "insightface.model_zoo",
    "insightface.utils",
    "insightface.data",
    # --- onnxruntime ---
    "onnxruntime.capi",
    "onnxruntime.capi.onnxruntime_pybind11_state",
    # --- 其他常见遗漏 ---
    "charset_normalizer",
    "hpack",
    "hyperframe",
    "priority",
    "sklearn.metrics",
    "sklearn.neighbors",
    "sklearn.cluster",
    "sklearn.tree",
    "sklearn.utils",
    "sklearn.preprocessing",
    "sklearn.neighbors._partition_nodes",
    "email.mime",
    "email.mime.multipart",
    "email.mime.text",
    "email.mime.application",
    "pkg_resources",
    "setuptools",
    "setuptools.version",
    # --- uvicorn / fastapi ---
    "uvicorn.logging",
    "uvicorn.loops",
    "uvicorn.loops.auto",
    "uvicorn.protocols",
    "uvicorn.protocols.http",
    "uvicorn.protocols.http.auto",
    "uvicorn.protocols.websockets",
    "uvicorn.protocols.websockets.auto",
    "uvicorn.lifespan",
    "uvicorn.lifespan.on",
    "starlette.routing",
    "starlette.middleware",
    "starlette.staticfiles",
    # --- mediapipe ---
    "mediapipe.python",
    "mediapipe.python.solutions",
    "mediapipe.python.solutions.face_mesh",
    "mediapipe.python.solutions.face_detection",
    # --- pyarrow ---
    "pyarrow.lib",
    "pyarrow.compute",
    # --- cryptography ---
    "cryptography.hazmat",
    "cryptography.hazmat.primitives",
    "cryptography.hazmat.backends",
    # --- modelscope ---
    "modelscope.hub",
    "modelscope.metainfo",
    "modelscope.utils",
    "modelscope.models",
    "modelscope.pipelines",
    "modelscope.preprocessors",
    # --- kornia ---
    "kornia.feature",
    "kornia.geometry",
    "kornia.enhance",
    "kornia.filters",
    # --- diffusers ---
    "diffusers.models",
    "diffusers.schedulers",
    "diffusers.pipelines",
    # --- accelerate ---
    "accelerate.utils",
    "accelerate.commands",
    # --- librosa ---
    "librosa.feature",
    "librosa.beat",
    "librosa.effects",
    "librosa.filters",
    "librosa.sequence",
    "librosa.util",
    "librosa.core",
    "librosa.core.spectrum",
    # --- scipy ---
    "scipy.signal",
    "scipy.fft",
    "scipy.linalg",
    "scipy.spatial",
    "scipy.special",
    "scipy.stats",
    "scipy.interpolate",
    "scipy.optimize",
    "scipy.ndimage",
    # --- PIL ---
    "PIL.Image",
    "PIL.ImageDraw",
    "PIL.ImageFont",
    "PIL.ImageFilter",
    "PIL.ImageOps",
    # --- cv2 ---
    "cv2",
    "cv2.gapi",
    # --- numpy ---
    "numpy",
    "numpy.core",
    "numpy.fft",
    "numpy.linalg",
    "numpy.random",
    "numpy.polynomial",
    # --- typing / typing_extensions ---
    "typing_extensions",
    # --- pydantic ---
    "pydantic.deprecated",
    "pydantic.v1",
    # --- click / typer ---
    "click.core",
    "click.termui",
    "click.utils",
    "click.parser",
    # --- loguru ---
    "loguru._colorama",
    # --- openai ---
    "openai._types",
    "openai._base_client",
    "openai.resources",
    # --- requests ---
    "requests",
    "urllib3",
    "httpcore",
    "httpx",
    # --- tqdm ---
    "tqdm.auto",
    "tqdm.gui",
    "tqdm.notebook",
    # --- einops ---
    "einops.layers",
    # --- inflect ---
    "inflect",
    # --- regex ---
    "regex",
    # --- HyperPyYAML ---
    "hyperpyyaml",
    # --- conformer ---
    "conformer",
    "conformer.conv",
    # --- x_transformers ---
    "x_transformers",
    "x_transformers.x_transformers",
    # --- pyworld ---
    "pyworld",
    # --- soundfile ---
    "soundfile",
    # --- imageio ---
    "imageio",
    "imageio.plugins",
    # --- omegaconf ---
    "omegaconf",
    "omegaconf._utils",
    # --- hydra ---
    "hydra",
    "hydra.utils",
    "hydra.conf",
    # --- biliup ---
    "biliup",
    "biliup.common",
    "biliup.plugins",
    # --- playwright ---
    "playwright.sync_api",
    "playwright.async_api",
    "playwright._impl",
    # --- python_multipart ---
    "multipart",
    # --- anyio ---
    "anyio",
    "anyio._backends",
    # --- h11 ---
    "h11",
    # --- websockets ---
    "websockets",
    # --- aiofiles ---
    "aiofiles",
    # --- watchfiles ---
    "watchfiles",
    # --- certifi ---
    "certifi",
    # --- idna ---
    "idna",
    # --- sniffio ---
    "sniffio",
    # --- annotated_types ---
    "annotated_types",
    # --- mdurl ---
    "mdurl",
    # --- pygments ---
    "pygments",
    # --- rich ---
    "rich",
    # --- shellingham ---
    "shellingham",
]

# ============================================================
# 4. 排除不需要的模块(减小体积)
# ============================================================
excludes = [
    # GUI 框架(本项目纯 CLI + Web,不需要桌面 GUI)
    "tkinter",
    "Tkinter",
    "PyQt5",
    "PyQt6",
    "PySide2",
    "PySide6",
    "wx",
    "gtk",
    "cairo",
    # 交互式环境
    "IPython",
    "ipykernel",
    "ipywidgets",
    "jupyter",
    "jupyter_client",
    "jupyter_core",
    "notebook",
    "sphinx",
    "numpydoc",
    # 测试框架
    "pytest",
    "doctest",
    "unittest.mock",
    # 绘图(如被间接依赖会自动保留,这里只排除顶层)
    "matplotlib",
    "seaborn",
    "plotly",
    "bokeh",
    "altair",
    # 符号计算
    "sympy",
    # 文档生成
    "pydoc",
    # 其他
    "conda",
    "lib2to3",
    "test",
    "tests",
]

# ============================================================
# 5. Analysis / EXE / COLLECT
# ============================================================
a = Analysis(
    ["vh_entry.py"],
    pathex=[ROOT],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=excludes,
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="videohuman",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name="videohuman",
)
