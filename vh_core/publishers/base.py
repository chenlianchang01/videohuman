"""发布器协议 + 平台文案限制截断。

各平台 publisher 实现 PublisherBase 协议:
- validate_cookies(cookies_path):cookie 文件格式预检,不合格抛中文可排障异常
- upload(video, title, tags, cover, cookies_path, publish_date=None) -> dict
  返回 {"platform": str, "ok": bool, "detail": str}
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Protocol

# 平台文案限制(平台改版需维护点):标题按字符数截断,标签限制单条长度与条数
TITLE_MAX_LEN = {"bilibili": 80, "douyin": 55}
TAG_MAX_LEN = {"bilibili": 20, "douyin": 20}
TAG_MAX_COUNT = {"bilibili": 12, "douyin": 10}


def truncate_title(platform: str, title: str) -> str:
    """按平台标题长度上限截断(去首尾空白)。"""
    title = title.strip()
    limit = TITLE_MAX_LEN[platform]
    if len(title) > limit:
        return title[:limit]
    return title


def normalize_tags(platform: str, tags: list[str]) -> list[str]:
    """清洗并按平台限制截断标签:去 # 与空白、去空、去重(保序)、限长限条数。"""
    limit = TAG_MAX_LEN[platform]
    max_count = TAG_MAX_COUNT[platform]
    seen: set[str] = set()
    out: list[str] = []
    for raw in tags:
        tag = raw.strip().lstrip("#").strip()
        if not tag or tag in seen:
            continue
        seen.add(tag)
        out.append(tag[:limit])
        if len(out) >= max_count:
            break
    return out


class PublisherBase(Protocol):
    """平台发布器协议。"""

    platform: str

    def validate_cookies(self, cookies_path: Path) -> None:
        """cookie 文件格式预检。不存在/格式错误抛异常(中文、可排障)。"""
        ...

    def upload(
        self,
        video: Path,
        title: str,
        tags: list[str],
        cover: Path | None,
        cookies_path: Path,
        publish_date: datetime | None = None,
    ) -> dict:
        """上传视频,返回 {"platform", "ok", "detail}。失败也应返回 ok=False 而非抛错
        (cookie/参数问题除外,直接抛异常)。"""
        ...
