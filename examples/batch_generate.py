"""批量生成示例 — 脚本化自由度的用法演示。

用法:
    uv run python examples/batch_generate.py

等价于 CLI: vh batch --file examples/batch.toml
但这里展示的是"内核即可编程库":你可以随意改造本脚本——
从 Excel/数据库/爬虫读文案、自定义参数模板、接自己的调度循环。
"""

from vh_core.api import run_batch
from vh_core.models import JobSpec

# 公共参数:所有 job 共用(参考音频/素材视频/样式等)
COMMON = {
    "avatar_video": "assets/avatar.mp4",  # 换成你自己的口播素材视频路径
    # "ref_audio": "...",          # 换成你自己的参考音频;不指定则用 CosyVoice 自带示例音色
    "avatar": {"batch_size": 8},   # provider 级参数经子 dict 透传
    "postprocess": {"bgm_volume": 0.12},
}

TEXTS = [
    "孩子突然厌学,背后藏着什么秘密?家长别慌,这三个信号一定要看懂。",
    "为什么越省钱越穷?普通人逆袭的第一步,是换一种思维方式。",
    "每天十分钟,坚持一个月,你的身体会发生惊人的变化。",
]


def main() -> None:
    specs = [
        JobSpec(job_id=f"demo-{i:03d}", params={**COMMON, "text": t})
        for i, t in enumerate(TEXTS, 1)
    ]
    report = run_batch(specs)
    for j in report["jobs"]:
        print(j)
    print(f"成功 {report['succeeded']}/{report['total']}")


if __name__ == "__main__":
    main()
