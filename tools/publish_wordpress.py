#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Any


def normalize_password(value: str) -> str:
    return re.sub(r"\s+", "", value or "")


def exact_term_id(terms: list[dict[str, Any]], name: str) -> int | None:
    for term in terms:
        if str(term.get("name", "")) == name:
            return int(term["id"])
    return None


def normalize_wp_date(value: Any) -> str | None:
    if value is None:
        return None
    if isinstance(value, datetime):
        return value.isoformat()
    text = str(value).strip()
    for fmt in ("%Y-%m-%d %H:%M:%S %z", "%Y-%m-%dT%H:%M:%S%z"):
        try:
            return datetime.strptime(text, fmt).isoformat()
        except ValueError:
            pass
    return text


def make_post_payload(data: dict[str, Any], html: str, category_ids: list[int], tag_ids: list[int]) -> dict[str, Any]:
    wp = data.get("wordpress") or {}
    payload: dict[str, Any] = {
        "title": data["title"],
        "content": html,
        "excerpt": data.get("excerpt", ""),
        "slug": data["slug"],
        "status": wp.get("status", "draft"),
        "comment_status": wp.get("comment_status", "closed"),
        "categories": category_ids,
        "tags": tag_ids,
    }
    normalized_date = normalize_wp_date(data.get("date"))
    if normalized_date:
        payload["date"] = normalized_date
    return payload


def post_lookup_action(posts: list[dict[str, Any]]) -> tuple[str, int | None]:
    if not posts:
        return "create", None
    if len(posts) == 1:
        return "update", int(posts[0]["id"])
    raise RuntimeError("multiple posts found for the same slug")


def parse_markdown(path: Path) -> tuple[dict[str, Any], str]:
    import yaml

    text = path.read_text(encoding="utf-8")
    parts = re.split(r"^---\s*$", text, maxsplit=2, flags=re.MULTILINE)
    if len(parts) != 3:
        raise ValueError(f"Invalid front matter: {path}")
    data = yaml.safe_load(parts[1])
    if not isinstance(data, dict):
        raise ValueError(f"Invalid YAML mapping: {path}")
    return data, parts[2].strip()


def markdown_to_html(body: str) -> str:
    import markdown

    return markdown.markdown(body, extensions=["extra", "sane_lists"], output_format="html5")


class WordPressClient:
    def __init__(self, base_url: str, username: str, password: str, timeout: int = 45):
        import requests

        self.base_url = base_url.rstrip("/")
        self.api = f"{self.base_url}/wp-json/wp/v2"
        self.session = requests.Session()
        self.session.auth = (username, normalize_password(password))
        self.timeout = timeout

    def request(self, method: str, url: str, **kwargs: Any) -> Any:
        response = self.session.request(method, url, timeout=self.timeout, **kwargs)
        if response.status_code >= 400:
            detail = response.text[:1000]
            raise RuntimeError(f"WordPress {response.status_code}: {detail}")
        if not response.text:
            return None
        return response.json()

    def verify(self) -> dict[str, Any]:
        return self.request("GET", f"{self.api}/users/me", params={"context": "edit"})

    def ensure_term(self, taxonomy: str, name: str) -> int:
        endpoint = f"{self.api}/{taxonomy}"
        terms = self.request("GET", endpoint, params={"search": name, "per_page": 100, "context": "edit"})
        found = exact_term_id(terms, name)
        if found is not None:
            return found
        try:
            created = self.request("POST", endpoint, json={"name": name})
            return int(created["id"])
        except RuntimeError as exc:
            match = re.search(r'"term_id"\s*:\s*(\d+)', str(exc))
            if match:
                return int(match.group(1))
            raise

    def upsert(self, data: dict[str, Any], html: str) -> dict[str, Any]:
        wp = data.get("wordpress") or {}
        category_names = list(wp.get("categories") or data.get("categories") or [])
        tag_names = list(wp.get("tags") or data.get("tags") or [])
        category_ids = [self.ensure_term("categories", str(name)) for name in category_names]
        tag_ids = [self.ensure_term("tags", str(name)) for name in tag_names]
        posts = self.request(
            "GET",
            f"{self.api}/posts",
            params={"slug": data["slug"], "status": "any", "context": "edit", "per_page": 100},
        )
        action, post_id = post_lookup_action(posts)
        payload = make_post_payload(data, html, category_ids, tag_ids)
        if action == "create":
            result = self.request("POST", f"{self.api}/posts", json=payload)
        else:
            result = self.request("POST", f"{self.api}/posts/{post_id}", json=payload)
        return {
            "action": action,
            "id": int(result["id"]),
            "slug": result["slug"],
            "status": result["status"],
            "link": result.get("link"),
            "category_count": len(category_ids),
            "tag_count": len(tag_ids),
        }


def select_paths(root: Path, mode: str, slug: str | None) -> list[Path]:
    posts = sorted((root / "japanese" / "posts").glob("*.md"))
    if mode == "one":
        if not slug:
            raise ValueError("slug is required for mode=one")
        matched = [p for p in posts if parse_markdown(p)[0].get("slug") == slug]
        if len(matched) != 1:
            raise ValueError(f"Expected exactly one article for slug={slug}, got {len(matched)}")
        return matched
    if mode == "posts":
        return posts
    if mode == "daily":
        return [root / "japanese" / "daily" / "2026-07-31.md"]
    if mode == "all":
        return posts + [root / "japanese" / "daily" / "2026-07-31.md"]
    raise ValueError(f"Unsupported mode: {mode}")


def main() -> int:
    import yaml

    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument("--request", required=True)
    parser.add_argument("--report", default="wordpress-publish-report.json")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    request_data = yaml.safe_load(Path(args.request).read_text(encoding="utf-8")) or {}
    mode = str(request_data.get("mode", "one"))
    slug = request_data.get("slug")

    client = WordPressClient(
        os.environ["WP_BASE_URL"],
        os.environ["WP_USERNAME"],
        os.environ["WP_APP_PASSWORD"],
    )
    user = client.verify()
    results = []
    for path in select_paths(root, mode, slug):
        data, body = parse_markdown(path)
        if data.get("publication_target") != "wordpress":
            raise ValueError(f"Not a WordPress target: {path}")
        if (data.get("wordpress") or {}).get("status") != "draft":
            raise ValueError(f"Only draft publication is allowed: {path}")
        result = client.upsert(data, markdown_to_html(body))
        result["path"] = str(path.relative_to(root))
        results.append(result)

    report = {
        "site": client.base_url,
        "authenticated_user": {"id": user.get("id"), "name": user.get("name"), "slug": user.get("slug")},
        "mode": mode,
        "count": len(results),
        "results": results,
    }
    Path(args.report).write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"site": client.base_url, "mode": mode, "count": len(results), "results": results}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
