from __future__ import annotations


def expected_publication_count(mode: str, post_count: int) -> int:
    if post_count < 0:
        raise ValueError("post_count must be non-negative")
    if mode == "all":
        return post_count + 1
    if mode == "posts":
        return post_count
    if mode in {"daily", "one"}:
        return 1
    raise ValueError(f"Unsupported mode: {mode}")
