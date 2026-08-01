#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import time
from datetime import datetime
from pathlib import Path
from typing import Any

from edition import collect_posts, latest_edition_date, parse_markdown as parse_edition_markdown


def normalize_password(value: str) -> str:
    return re.sub(r"\s+", "", value or "")


def normalize_status_override(value: Any) -> str | None:
    if value is None or str(value).strip() == "":
        return None
    status = str(value).strip().lower()
    if status not in {"draft", "publish"}:
        raise ValueError(f"Unsupported status override: {status}")
    return status


def exact_term_id(terms: list[dict[str, Any]], name: str) -> int | None:
    for term in terms:
        if str(term.get("name", "")) == name:
            return int(term["id"])
    return None


def index_terms(terms: list[dict[str, Any]]) -> dict[str, int]:
    return {
        str(term.get("name", "")): int(term["id"])
        for term in terms
        if term.get("id") is not None
    }


def is_retryable_status(status_code: int) -> bool:
    return status_code in {408, 425, 429, 500, 502, 503, 504}


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


def make_post_payload(
    data: dict[str, Any],
    html: str,
    category_ids: list[int],
    tag_ids: list[int],
    status_override: str | None = None,
) -> dict[str, Any]:
    wp = data.get("wordpress") or {}
    payload: dict[str, Any] = {
        "title": data["title"],
        "content": html,
        "excerpt": data.get("excerpt", ""),
        "slug": data["slug"],
        "status": status_override or wp.get("status", "publish"),
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
    post = parse_edition_markdown(path)
    return post.data, post.body


def markdown_to_html(body: str) -> str:
    import markdown

    return markdown.markdown(
        body,
        extensions=["extra", "sane_lists"],
        output_format="html5",
    )


class WordPressClient:
    def __init__(
        self,
        base_url: str,
        username: str,
        password: str,
        timeout: int = 45,
        max_attempts: int = 6,
    ):
        import requests

        self.base_url = base_url.rstrip("/")
        self.api = f"{self.base_url}/wp-json/wp/v2"
        self.session = requests.Session()
        self.session.auth = (username, normalize_password(password))
        self.session.headers.update({"User-Agent": "dnews-wordpress-publisher/2.0"})
        self.timeout = timeout
        self.max_attempts = max_attempts
        self.term_cache: dict[str, dict[str, int]] = {}
        self.post_cache: dict[str, list[dict[str, Any]]] | None = None

    def request(self, method: str, url: str, **kwargs: Any) -> Any:
        import requests

        last_error: Exception | None = None
        for attempt in range(1, self.max_attempts + 1):
            try:
                response = self.session.request(method, url, timeout=self.timeout, **kwargs)
                if response.status_code >= 400:
                    detail = response.text[:1000]
                    error = RuntimeError(f"WordPress {response.status_code}: {detail}")
                    if is_retryable_status(response.status_code) and attempt < self.max_attempts:
                        last_error = error
                        time.sleep(min(2 ** (attempt - 1), 16))
                        continue
                    raise error
                if not response.text:
                    return None
                return response.json()
            except requests.RequestException as exc:
                last_error = exc
                if attempt >= self.max_attempts:
                    break
                time.sleep(min(2 ** (attempt - 1), 16))
        raise RuntimeError(
            f"WordPress request failed after {self.max_attempts} attempts: {last_error}"
        )

    def fetch_all(
        self,
        endpoint: str,
        params: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        items: list[dict[str, Any]] = []
        page = 1
        while True:
            page_params = dict(params or {})
            page_params.update({"per_page": 100, "page": page})
            batch = self.request("GET", endpoint, params=page_params)
            if not isinstance(batch, list):
                raise RuntimeError(f"Expected a list from {endpoint}")
            items.extend(batch)
            if len(batch) < 100:
                return items
            page += 1

    def verify(self) -> dict[str, Any]:
        return self.request("GET", f"{self.api}/users/me", params={"context": "edit"})

    def load_terms(self, taxonomy: str) -> dict[str, int]:
        if taxonomy not in self.term_cache:
            terms = self.fetch_all(f"{self.api}/{taxonomy}", {"context": "edit"})
            self.term_cache[taxonomy] = index_terms(terms)
        return self.term_cache[taxonomy]

    def ensure_term(self, taxonomy: str, name: str) -> int:
        cache = self.load_terms(taxonomy)
        if name in cache:
            return cache[name]
        endpoint = f"{self.api}/{taxonomy}"
        try:
            created = self.request("POST", endpoint, json={"name": name})
            term_id = int(created["id"])
        except RuntimeError as exc:
            match = re.search(r'"term_id"\s*:\s*(\d+)', str(exc))
            if not match:
                raise
            term_id = int(match.group(1))
        cache[name] = term_id
        return term_id

    def load_posts(self) -> dict[str, list[dict[str, Any]]]:
        if self.post_cache is None:
            posts = self.fetch_all(
                f"{self.api}/posts",
                {"status": "any", "context": "edit"},
            )
            cache: dict[str, list[dict[str, Any]]] = {}
            for post in posts:
                cache.setdefault(str(post.get("slug", "")), []).append(post)
            self.post_cache = cache
        return self.post_cache

    def upsert(
        self,
        data: dict[str, Any],
        html: str,
        status_override: str | None = None,
    ) -> dict[str, Any]:
        wp = data.get("wordpress") or {}
        category_names = list(wp.get("categories") or data.get("categories") or [])
        tag_names = list(wp.get("tags") or data.get("tags") or [])
        category_ids = [self.ensure_term("categories", str(name)) for name in category_names]
        tag_ids = [self.ensure_term("tags", str(name)) for name in tag_names]

        post_cache = self.load_posts()
        slug = str(data["slug"])
        action, post_id = post_lookup_action(post_cache.get(slug, []))
        payload = make_post_payload(
            data,
            html,
            category_ids,
            tag_ids,
            status_override=status_override,
        )
        if action == "create":
            result = self.request("POST", f"{self.api}/posts", json=payload)
        else:
            result = self.request("POST", f"{self.api}/posts/{post_id}", json=payload)
        post_cache[slug] = [result]
        return {
            "action": action,
            "id": int(result["id"]),
            "slug": result["slug"],
            "status": result["status"],
            "link": result.get("link"),
            "category_count": len(category_ids),
            "tag_count": len(tag_ids),
        }


def select_paths(
    root: Path,
    mode: str,
    slug: str | None,
    *,
    edition_date: str | None = None,
) -> list[Path]:
    date = edition_date or latest_edition_date(root)
    posts = [post.path for post in collect_posts(root, "ja", date)]
    daily = root / "japanese" / "daily" / f"{date}.md"
    if mode == "one":
        if not slug:
            raise ValueError("slug is required for mode=one")
        matched = [path for path in posts if parse_markdown(path)[0].get("slug") == slug]
        if len(matched) != 1:
            raise ValueError(
                f"Expected exactly one article for edition={date} slug={slug}, got {len(matched)}"
            )
        return matched
    if mode == "posts":
        return posts
    if mode == "daily":
        if not daily.exists():
            raise ValueError(f"Missing Japanese daily file: {daily}")
        return [daily]
    if mode == "all":
        if not daily.exists():
            raise ValueError(f"Missing Japanese daily file: {daily}")
        return posts + [daily]
    raise ValueError(f"Unsupported mode: {mode}")


def write_report(path: Path, report: dict[str, Any]) -> None:
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> int:
    import yaml

    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument("--request", required=True)
    parser.add_argument("--report", default="wordpress-publish-report.json")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    report_path = Path(args.report)
    request_data = yaml.safe_load(Path(args.request).read_text(encoding="utf-8")) or {}
    mode = str(request_data.get("mode", "all"))
    slug = request_data.get("slug")
    edition_date = request_data.get("edition_date") or latest_edition_date(root)
    status_override = normalize_status_override(
        request_data.get("status_override", request_data.get("status", "publish"))
    )

    client = WordPressClient(
        os.environ["WP_BASE_URL"],
        os.environ["WP_USERNAME"],
        os.environ["WP_APP_PASSWORD"],
    )
    user = client.verify()
    report: dict[str, Any] = {
        "site": client.base_url,
        "authenticated_user": {
            "id": user.get("id"),
            "name": user.get("name"),
            "slug": user.get("slug"),
        },
        "edition_date": str(edition_date),
        "mode": mode,
        "status_override": status_override,
        "count": 0,
        "results": [],
    }
    write_report(report_path, report)

    for path in select_paths(
        root,
        mode,
        slug,
        edition_date=str(edition_date),
    ):
        data, body = parse_markdown(path)
        if data.get("publication_target") != "wordpress":
            raise ValueError(f"Not a WordPress target: {path}")
        result = client.upsert(
            data,
            markdown_to_html(body),
            status_override=status_override,
        )
        result["path"] = str(path.relative_to(root))
        report["results"].append(result)
        report["count"] = len(report["results"])
        write_report(report_path, report)
        print(json.dumps(result, ensure_ascii=False))

    if status_override:
        mismatches = [
            item for item in report["results"] if item.get("status") != status_override
        ]
        if mismatches:
            raise RuntimeError(f"WordPress status mismatch: {mismatches}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
