from __future__ import annotations

import re
import subprocess
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

import yaml

EXPECTED_COUNTS: dict[str, int] = {"core": 8, "social": 8, "other": 10}
SECTION_ORDER = ("core", "social", "other")
SECTION_TITLES_JA = {
    "core": "政治・経済・主要ニュース",
    "social": "社会を読む",
    "other": "科学・文化・都市、そのほか",
}
SECTION_DESCRIPTIONS_JA = {
    "core": "全国的な政策、経済、安全保障、統計、重大災害を扱う8本。",
    "social": "公共サービス、家族、労働、医療、教育、地方行政、生活条件から日本社会を読む8本。",
    "other": "科学、文化、教育、都市、スポーツ、映画、出版、地域社会を記録する10本。",
}
MANIFEST_RE = re.compile(r"^japanese/edition-(\d{4}-\d{2}-\d{2})\.ya?ml$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


class EditionError(RuntimeError):
    pass


@dataclass(frozen=True)
class MarkdownPost:
    path: Path
    data: dict[str, Any]
    body: str
    raw_front_matter: str


def parse_markdown(path: Path) -> MarkdownPost:
    text = path.read_text(encoding="utf-8")
    parts = re.split(r"^---\s*$\n?", text, maxsplit=2, flags=re.MULTILINE)
    if len(parts) != 3:
        raise EditionError(f"{path}: invalid YAML front matter")
    try:
        data = yaml.safe_load(parts[1]) or {}
    except yaml.YAMLError as exc:
        raise EditionError(f"{path}: YAML error: {exc}") from exc
    if not isinstance(data, dict):
        raise EditionError(f"{path}: front matter must be a mapping")
    return MarkdownPost(path=path, data=data, body=parts[2].strip(), raw_front_matter=parts[1])


def normalized_date(value: Any) -> str:
    return str(value).strip()


def discover_edition_dates(root: Path) -> list[str]:
    dates: list[str] = []
    for path in (root / "japanese").glob("edition-*.yml"):
        match = re.fullmatch(r"edition-(\d{4}-\d{2}-\d{2})\.yml", path.name)
        if match:
            dates.append(match.group(1))
    return sorted(set(dates))


def latest_edition_date(root: Path) -> str:
    dates = discover_edition_dates(root)
    if not dates:
        raise EditionError("No japanese/edition-YYYY-MM-DD.yml manifest found")
    return dates[-1]


def collect_posts(root: Path, language: str, edition_date: str) -> list[MarkdownPost]:
    if not DATE_RE.fullmatch(edition_date):
        raise EditionError(f"Invalid edition date: {edition_date}")
    if language == "zh":
        paths = sorted((root / "_posts").glob("*.md"))
    elif language == "ja":
        paths = sorted((root / "japanese" / "posts").glob("*.md"))
    else:
        raise EditionError(f"Unsupported language: {language}")

    posts: list[MarkdownPost] = []
    for path in paths:
        post = parse_markdown(path)
        value = post.data.get("edition_date", post.data.get("news_date"))
        if normalized_date(value) == edition_date:
            posts.append(post)
    return sorted(posts, key=lambda item: int(item.data.get("importance", 999999)))


def parse_changed_edition_dates(root: Path, changed_paths: Iterable[str]) -> list[str]:
    dates: set[str] = set()
    for raw_path in changed_paths:
        rel = raw_path.strip().lstrip("./")
        if not rel:
            continue
        match = MANIFEST_RE.fullmatch(rel)
        if match:
            dates.add(match.group(1))
            continue
        path = root / rel
        if path.suffix.lower() not in {".md", ".markdown", ".yml", ".yaml"} or not path.exists():
            continue
        if rel.startswith("japanese/posts/") or rel.startswith("japanese/daily/") or rel.startswith("_posts/") or rel.startswith("daily/"):
            try:
                post = parse_markdown(path)
            except EditionError:
                continue
            value = post.data.get("edition_date", post.data.get("news_date"))
            if value and DATE_RE.fullmatch(normalized_date(value)):
                dates.add(normalized_date(value))
    return sorted(dates)


def git_changed_paths(root: Path, base: str, head: str) -> list[str]:
    if not base or set(base) == {"0"}:
        command = ["git", "show", "--pretty=", "--name-only", head]
    else:
        command = ["git", "diff", "--name-only", base, head]
    completed = subprocess.run(command, cwd=root, text=True, capture_output=True, check=False)
    if completed.returncode != 0:
        raise EditionError(completed.stderr.strip() or "git diff failed")
    return [line.strip() for line in completed.stdout.splitlines() if line.strip()]


def _yaml_list(values: Iterable[str], indent: int = 0) -> str:
    prefix = " " * indent
    def scalar(value: str) -> str:
        return yaml.safe_dump(value, allow_unicode=True, default_flow_style=True).splitlines()[0]
    return "\n".join(f"{prefix}- {scalar(value)}" for value in values)


def _quoted(value: str) -> str:
    return yaml.safe_dump(value, allow_unicode=True, default_flow_style=True).strip()


def render_chinese_daily(
    *,
    edition_date: str,
    coverage_start: str,
    coverage_end: str,
    published_at: str,
) -> str:
    return f'''---
layout: page
title: "日本新闻早报｜{edition_date}"
date: '{published_at}'
news_date: '{edition_date}'
edition_date: '{edition_date}'
edition_type: morning
coverage_start: '{coverage_start}'
coverage_end: '{coverage_end}'
permalink: /daily/{edition_date}/
description: "截至日本时间{coverage_end[11:16]}，过去24小时内26篇日本新闻：8篇政治经济与重大事件、8篇社会观察、10篇科学文化城市及其他新闻。"
seo_title: "{edition_date}日本新闻早报｜26篇双语独立报道"
meta_description: "截至日本时间{coverage_end[11:16]}的日本新闻早报，共26篇：8篇政治经济与重大事件、8篇社会观察、10篇科学文化城市及其他新闻。"
---

<div class="daily-meta">Morning edition · {edition_date} JST · 26 reports</div>

本期收录截至日本时间 **{coverage_end[11:16]}** 的过去24小时日本新闻，共26篇独立报道。候选只来自可信新闻媒体和权威机构正式发布，不以社交媒体热度、搜索趋势或点击排行榜作为入选依据。

<div class="daily-summary">
<strong>选题结构：</strong>8篇政治经济与重大事件、8篇社会观察、10篇科学文化城市与其他新闻。每篇文章均重新检索官方资料和可信独立报道后写作。
</div>

{{% assign all_daily_posts = site.posts | where: "news_date", page.news_date %}}
{{% assign core_posts = all_daily_posts | where: "daily_section", "core" | sort: "importance" %}}
{{% assign social_posts = all_daily_posts | where: "daily_section", "social" | sort: "importance" %}}
{{% assign other_posts = all_daily_posts | where: "daily_section", "other" | sort: "importance" %}}

<section class="daily-section daily-section--core" id="politics-economy">
<div class="daily-section__header">
<p class="section-kicker">Core · {{{{ core_posts | size }}}} reports</p>
<h2>政治经济与重大事件</h2>
<p>全国性政治、经济、外交、安全、统计、重大灾害与公共风险。</p>
</div>
<ol class="daily-list">
{{% for post in core_posts %}}
<li>
<h2><a href="{{{{ post.url | relative_url }}}}">{{{{ post.title }}}}</a></h2>
<p>{{{{ post.excerpt | strip_html | strip_newlines }}}}</p>
{{% include tag-list.html tags=post.tags limit=6 compact=true %}}
</li>
{{% endfor %}}
</ol>
</section>

<section class="daily-section daily-section--social" id="social-observation">
<div class="daily-section__header">
<p class="section-kicker">Society · {{{{ social_posts | size }}}} reports</p>
<h2>社会观察</h2>
<p>公共服务、医疗、家庭、劳动、教育、地方治理与生活条件。</p>
</div>
<div class="social-grid">
{{% for post in social_posts %}}
<article class="social-card">
<div class="post-meta">{{{{ post.categories | join: " / " }}}}</div>
<h3><a href="{{{{ post.url | relative_url }}}}">{{{{ post.title }}}}</a></h3>
<p>{{{{ post.excerpt | strip_html | strip_newlines }}}}</p>
{{% include tag-list.html tags=post.tags limit=6 compact=true %}}
</article>
{{% endfor %}}
</div>
</section>

<section class="daily-section daily-section--other" id="science-culture-city">
<div class="daily-section__header">
<p class="section-kicker">Elsewhere · {{{{ other_posts | size }}}} reports</p>
<h2>科学、文化、城市与其他</h2>
<p>科学、文化、教育、城市、体育、电影、出版与地方社会新闻。</p>
</div>
<div class="brief-grid">
{{% for post in other_posts %}}
<article class="brief-card">
<div class="post-meta">{{{{ post.categories | join: " / " }}}}</div>
<h3><a href="{{{{ post.url | relative_url }}}}">{{{{ post.title }}}}</a></h3>
<p>{{{{ post.excerpt | strip_html | strip_newlines }}}}</p>
{{% include tag-list.html tags=post.tags limit=4 compact=true %}}
</article>
{{% endfor %}}
</div>
</section>

## 编辑说明

本期按事件聚类，通讯社转载和重复报道只计算一次。重要性依据公共影响、制度意义、后果持续性、新事实强度、来源可靠性和独立确认判断，不按照网络热度排序。
'''


def render_japanese_daily(
    *,
    edition_date: str,
    coverage_start: str,
    coverage_end: str,
    published_at: str,
    posts: list[MarkdownPost],
    wordpress_status: str,
    site_url: str = "https://shinkiji.com",
) -> str:
    counts = Counter(str(post.data.get("daily_section")) for post in posts)
    if counts != Counter(EXPECTED_COUNTS):
        raise EditionError(f"Japanese daily requires {EXPECTED_COUNTS}, got {dict(counts)}")
    tags = [
        edition_date.replace("-", "年", 1).replace("-", "月", 1) + "日",
        "日本ニュース",
        "政治",
        "経済",
        "社会",
        "科学",
        "文化",
        "都市",
        "防災",
        "医療",
        "労働",
        "地域",
    ]
    lines = [
        "---",
        f"story_id: {edition_date}-japan-daily",
        "lang: ja",
        "editorial_origin: japanese-sources",
        "translation_status: original",
        "publication_target: wordpress",
        f"title: 日本ニュース朝刊｜{edition_date}",
        f"date: '{published_at}'",
        f"news_date: '{edition_date}'",
        f"edition_date: '{edition_date}'",
        "edition_type: morning",
        f"coverage_start: '{coverage_start}'",
        f"coverage_end: '{coverage_end}'",
        f"slug: japan-daily-{edition_date}",
        f"excerpt: {edition_date}の日本ニュース朝刊。政治・経済8本、社会8本、科学・文化・都市など10本の計26本を収録し、各見出しから独立記事を読める。",
        "categories:",
        "- 日本",
        "- ニュース",
        "- デイリー",
        "tags:",
        *_yaml_list(tags).splitlines(),
        f"seo_title: 日本ニュース朝刊｜{edition_date}・全26本",
        f"meta_description: {edition_date}の日本を、政治・経済8本、社会8本、科学・文化・都市など10本の計26本で伝える朝刊。",
        f"source_checked_at: '{coverage_end}'",
        "wordpress:",
        f"  status: {wordpress_status}",
        "  post_type: post",
        "  comment_status: closed",
        "  categories:",
        "  - 日本",
        "  - ニュース",
        "  - デイリー",
        "  tags:",
        *_yaml_list(tags, indent=2).splitlines(),
        "---",
        "",
        f"日本時間の **{coverage_end[11:16]}** までに確認された過去24時間の日本ニュースを、26本の独立記事としてまとめた。候補は信頼できる報道機関と公的機関の正式発表に限定し、SNSの話題量や検索トレンドは選定基準にしていない。",
        "",
        "> **全26本**｜政治・経済・主要ニュース **8本**｜社会を読む **8本**｜科学・文化・都市、そのほか **10本**  ",
        "> 見出し、または「全文を読む」をクリックすると独立記事へ移動します。",
        "",
        "## 目次",
        "",
        "- [政治・経済・主要ニュース（8本）](#politics-economy)",
        "- [社会を読む（8本）](#society)",
        "- [科学・文化・都市、そのほか（10本）](#science-culture-city)",
    ]
    anchors = {"core": "politics-economy", "social": "society", "other": "science-culture-city"}
    number = 1
    for section in SECTION_ORDER:
        lines.extend(["", "---", "", f'<a id="{anchors[section]}"></a>', "", f"## {SECTION_TITLES_JA[section]}", "", SECTION_DESCRIPTIONS_JA[section], ""])
        section_posts = [post for post in posts if post.data.get("daily_section") == section]
        section_posts.sort(key=lambda item: int(item.data.get("importance", 999999)))
        for post in section_posts:
            slug = str(post.data["slug"])
            title = str(post.data["title"])
            excerpt = str(post.data["excerpt"])
            url = f"{site_url.rstrip('/')}/{slug}/"
            lines.extend([
                f"### {number:02d}｜[{title}]({url})",
                "",
                excerpt,
                "",
                f"[全文を読む →]({url})",
                "",
            ])
            number += 1
    lines.extend([
        "---",
        "",
        "## 編集方針",
        "",
        "同一通信社記事の転載は重複としてまとめ、公共への影響、制度的意味、結果の持続性、新事実の強さ、情報源の信頼性、独立確認の有無によって選定した。SNSの話題量、検索順位、閲覧数は選定基準にしていない。",
        "",
    ])
    return "\n".join(lines)

COMMON_REQUIRED_FIELDS = (
    "title",
    "date",
    "news_date",
    "daily_section",
    "slug",
    "excerpt",
    "categories",
    "tags",
    "article_type",
    "analysis_angle",
    "importance",
    "seo_title",
    "meta_description",
    "source_checked_at",
    "wordpress",
)
JAPANESE_REQUIRED_FIELDS = (
    "story_id",
    "lang",
    "editorial_origin",
    "translation_status",
    "publication_target",
)
LEGACY_MIN_PROSE = {
    "zh": {"core": 600, "social": 400, "other": 220},
    "ja": {"core": 900, "social": 700, "other": 500},
}
CURRENT_MIN_PROSE = {
    "zh": {"core": 900, "social": 650, "other": 400},
    "ja": {"core": 1000, "social": 750, "other": 550},
}
SOURCE_HEADINGS = {"zh": "## 资料来源", "ja": "## 参照資料"}
SOURCE_LINK_RE = re.compile(r"^\- \[[^\]]+\]\(https?://[^\)]+\)$", re.MULTILINE)


def load_manifest(root: Path, edition_date: str) -> dict[str, Any]:
    path = root / "japanese" / f"edition-{edition_date}.yml"
    if not path.exists():
        raise EditionError(f"Missing manifest: {path}")
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError as exc:
        raise EditionError(f"{path}: YAML error: {exc}") from exc
    if not isinstance(data, dict):
        raise EditionError(f"{path}: manifest must be a mapping")
    return data


def section_counts(posts: Iterable[MarkdownPost]) -> dict[str, int]:
    counter = Counter(str(post.data.get("daily_section", "")) for post in posts)
    return {section: counter.get(section, 0) for section in SECTION_ORDER}


def _post_errors(
    post: MarkdownPost,
    *,
    language: str,
    edition_date: str,
    schema_version: int,
    expected_status: str | None,
) -> list[str]:
    errors: list[str] = []
    data = post.data
    required = list(COMMON_REQUIRED_FIELDS)
    if language == "ja":
        required.extend(JAPANESE_REQUIRED_FIELDS)
    missing = [field for field in required if field not in data]
    if missing:
        errors.append(f"{post.path}: missing fields: {', '.join(missing)}")

    if normalized_date(data.get("edition_date", data.get("news_date"))) != edition_date:
        errors.append(f"{post.path}: edition/news date must be {edition_date}")
    section = str(data.get("daily_section", ""))
    if section not in EXPECTED_COUNTS:
        errors.append(f"{post.path}: invalid daily_section {section!r}")
    slug = str(data.get("slug", ""))
    if not slug or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug):
        errors.append(f"{post.path}: invalid slug {slug!r}")

    if language == "ja":
        if data.get("lang") != "ja":
            errors.append(f"{post.path}: lang must be ja")
        if data.get("editorial_origin") != "japanese-sources":
            errors.append(f"{post.path}: editorial_origin must be japanese-sources")
        if data.get("translation_status") != "original":
            errors.append(f"{post.path}: translation_status must be original")
        if data.get("publication_target") != "wordpress":
            errors.append(f"{post.path}: publication_target must be wordpress")
        if str(data.get("story_id", "")) != f"{edition_date}-{slug}":
            errors.append(f"{post.path}: story_id must be {edition_date}-{slug}")

    tags = [str(item) for item in data.get("tags") or []]
    categories = [str(item) for item in data.get("categories") or []]
    if not 12 <= len(tags) <= 25:
        errors.append(f"{post.path}: expected 12-25 tags, got {len(tags)}")
    if len(categories) < 2:
        errors.append(f"{post.path}: expected at least 2 categories")
    absent = [tag for tag in tags if tag not in post.body]
    if absent:
        errors.append(f"{post.path}: tags absent from body: {', '.join(absent)}")

    wordpress = data.get("wordpress") or {}
    if not isinstance(wordpress, dict):
        errors.append(f"{post.path}: wordpress must be a mapping")
        wordpress = {}
    status = str(wordpress.get("status", ""))
    if expected_status and status != expected_status:
        errors.append(f"{post.path}: wordpress.status must be {expected_status}, got {status!r}")
    elif status not in {"draft", "publish"}:
        errors.append(f"{post.path}: wordpress.status must be draft or publish")
    if wordpress.get("post_type") != "post":
        errors.append(f"{post.path}: wordpress.post_type must be post")
    if language == "ja" and wordpress.get("comment_status") != "closed":
        errors.append(f"{post.path}: wordpress.comment_status must be closed")
    if [str(item) for item in wordpress.get("categories") or []] != categories:
        errors.append(f"{post.path}: wordpress.categories mismatch")
    if [str(item) for item in wordpress.get("tags") or []] != tags:
        errors.append(f"{post.path}: wordpress.tags mismatch")

    if re.search(r"(?:&id\d+|\*id\d+)", post.raw_front_matter):
        errors.append(f"{post.path}: YAML aliases are not allowed")
    heading = SOURCE_HEADINGS[language]
    if heading not in post.body:
        errors.append(f"{post.path}: missing source section {heading}")
        prose = post.body
    else:
        prose = post.body.split(heading, 1)[0]
    source_count = len(SOURCE_LINK_RE.findall(post.body))
    min_sources = 1
    if schema_version >= 2 and section in {"core", "social"}:
        min_sources = 2
    if source_count < min_sources:
        errors.append(f"{post.path}: expected at least {min_sources} linked sources, got {source_count}")

    min_table = CURRENT_MIN_PROSE if schema_version >= 2 else LEGACY_MIN_PROSE
    min_prose = min_table[language].get(section, 0)
    prose_length = len(re.sub(r"\s+", "", prose))
    if prose_length < min_prose:
        errors.append(f"{post.path}: prose too short ({prose_length} < {min_prose})")
    return errors


def validate_edition(root: Path, edition_date: str) -> dict[str, Any]:
    manifest = load_manifest(root, edition_date)
    errors: list[str] = []
    schema_version = int(manifest.get("schema_version", 1))
    if normalized_date(manifest.get("edition")) != edition_date:
        errors.append(f"manifest edition must be {edition_date}")
    expected_counts = {str(k): int(v) for k, v in (manifest.get("expected_counts") or {}).items()}
    if expected_counts != EXPECTED_COUNTS:
        errors.append(f"manifest expected_counts must be {EXPECTED_COUNTS}, got {expected_counts}")
    expected_status = manifest.get("wordpress_default_status")
    if schema_version >= 2:
        if expected_status not in {"draft", "publish"}:
            errors.append("schema_version 2 manifest requires wordpress_default_status draft or publish")
        for field in ("coverage_start", "coverage_end", "published_at", "edition_type"):
            if not manifest.get(field):
                errors.append(f"schema_version 2 manifest missing {field}")
    elif expected_status not in {None, "draft", "publish"}:
        errors.append("manifest wordpress_default_status must be draft or publish")

    zh_posts = collect_posts(root, "zh", edition_date)
    ja_posts = collect_posts(root, "ja", edition_date)
    if len(zh_posts) != 26:
        errors.append(f"expected 26 Chinese posts for {edition_date}, got {len(zh_posts)}")
    if len(ja_posts) != 26:
        errors.append(f"expected 26 Japanese posts for {edition_date}, got {len(ja_posts)}")
    if section_counts(zh_posts) != EXPECTED_COUNTS:
        errors.append(f"Chinese section counts mismatch: {section_counts(zh_posts)}")
    if section_counts(ja_posts) != EXPECTED_COUNTS:
        errors.append(f"Japanese section counts mismatch: {section_counts(ja_posts)}")

    for post in zh_posts:
        errors.extend(_post_errors(post, language="zh", edition_date=edition_date, schema_version=schema_version, expected_status=expected_status))
    for post in ja_posts:
        errors.extend(_post_errors(post, language="ja", edition_date=edition_date, schema_version=schema_version, expected_status=expected_status))

    zh_by_slug = {str(post.data.get("slug")): post for post in zh_posts}
    ja_by_slug = {str(post.data.get("slug")): post for post in ja_posts}
    if len(zh_by_slug) != len(zh_posts):
        errors.append("duplicate Chinese slugs")
    if len(ja_by_slug) != len(ja_posts):
        errors.append("duplicate Japanese slugs")
    if set(zh_by_slug) != set(ja_by_slug):
        errors.append(
            "Chinese/Japanese slug sets differ: "
            f"missing_ja={sorted(set(zh_by_slug) - set(ja_by_slug))}, "
            f"missing_zh={sorted(set(ja_by_slug) - set(zh_by_slug))}"
        )

    manifest_posts = manifest.get("posts") or []
    if not isinstance(manifest_posts, list) or len(manifest_posts) != 26:
        errors.append(f"manifest expected 26 posts, got {len(manifest_posts) if isinstance(manifest_posts, list) else 'non-list'}")
        manifest_posts = []
    manifest_slugs: list[str] = []
    for item in manifest_posts:
        if not isinstance(item, dict):
            errors.append("manifest post entry must be a mapping")
            continue
        slug = str(item.get("slug", ""))
        manifest_slugs.append(slug)
        post = ja_by_slug.get(slug)
        if post is None:
            errors.append(f"manifest references missing Japanese slug: {slug}")
            continue
        expected_path = str(post.path.relative_to(root))
        if str(item.get("path")) != expected_path:
            errors.append(f"manifest path mismatch for {slug}: {item.get('path')} != {expected_path}")
        mappings = {
            "story_id": post.data.get("story_id"),
            "section": post.data.get("daily_section"),
            "importance": int(post.data.get("importance")),
            "title": post.data.get("title"),
            "excerpt": post.data.get("excerpt"),
        }
        for key, value in mappings.items():
            item_value = item.get(key)
            if key == "importance" and item_value is not None:
                item_value = int(item_value)
            if item_value != value:
                errors.append(f"manifest {key} mismatch for {slug}")
    if set(manifest_slugs) != set(ja_by_slug):
        errors.append("manifest slug set differs from Japanese posts")
    importances = [int(item.get("importance", 999999)) for item in manifest_posts if isinstance(item, dict)]
    if importances != sorted(importances) or len(importances) != len(set(importances)):
        errors.append("manifest posts must have unique ascending importance")

    chinese_daily = root / "daily" / f"{edition_date}.md"
    japanese_daily = root / "japanese" / "daily" / f"{edition_date}.md"
    if not chinese_daily.exists():
        errors.append(f"missing Chinese daily: {chinese_daily}")
    else:
        daily = parse_markdown(chinese_daily)
        if normalized_date(daily.data.get("edition_date", daily.data.get("news_date"))) != edition_date:
            errors.append(f"{chinese_daily}: wrong edition date")
        if schema_version >= 2:
            if daily.data.get("coverage_start") != manifest.get("coverage_start"):
                errors.append(f"{chinese_daily}: coverage_start mismatch")
            if daily.data.get("coverage_end") != manifest.get("coverage_end"):
                errors.append(f"{chinese_daily}: coverage_end mismatch")

    if not japanese_daily.exists():
        errors.append(f"missing Japanese daily: {japanese_daily}")
    else:
        daily = parse_markdown(japanese_daily)
        if normalized_date(daily.data.get("edition_date", daily.data.get("news_date"))) != edition_date:
            errors.append(f"{japanese_daily}: wrong edition date")
        daily_status = str((daily.data.get("wordpress") or {}).get("status", ""))
        if expected_status and daily_status != expected_status:
            errors.append(f"{japanese_daily}: wordpress.status must be {expected_status}")
        if schema_version >= 2:
            if daily.data.get("coverage_start") != manifest.get("coverage_start"):
                errors.append(f"{japanese_daily}: coverage_start mismatch")
            if daily.data.get("coverage_end") != manifest.get("coverage_end"):
                errors.append(f"{japanese_daily}: coverage_end mismatch")
        for slug, post in ja_by_slug.items():
            title = str(post.data.get("title", ""))
            url = f"https://shinkiji.com/{slug}/"
            if title not in daily.body:
                errors.append(f"{japanese_daily}: missing title {title}")
            if url not in daily.body:
                errors.append(f"{japanese_daily}: missing link {url}")

    if errors:
        raise EditionError("\n".join(errors))
    return {
        "edition": edition_date,
        "schema_version": schema_version,
        "counts": EXPECTED_COUNTS,
        "chinese_posts": len(zh_posts),
        "japanese_posts": len(ja_posts),
        "wordpress_default_status": expected_status,
    }


def build_manifest(
    *,
    root: Path,
    edition_date: str,
    coverage_start: str,
    coverage_end: str,
    published_at: str,
    wordpress_status: str,
) -> dict[str, Any]:
    if wordpress_status not in {"draft", "publish"}:
        raise EditionError(f"Unsupported WordPress status: {wordpress_status}")
    zh_posts = collect_posts(root, "zh", edition_date)
    ja_posts = collect_posts(root, "ja", edition_date)
    if len(zh_posts) != 26 or len(ja_posts) != 26:
        raise EditionError(f"Need 26 Chinese and 26 Japanese posts, got zh={len(zh_posts)}, ja={len(ja_posts)}")
    if section_counts(zh_posts) != EXPECTED_COUNTS or section_counts(ja_posts) != EXPECTED_COUNTS:
        raise EditionError(f"Section counts must be {EXPECTED_COUNTS}")
    zh_slugs = {str(post.data.get("slug")) for post in zh_posts}
    ja_slugs = {str(post.data.get("slug")) for post in ja_posts}
    if zh_slugs != ja_slugs:
        raise EditionError(f"Chinese/Japanese slug mismatch: zh_only={sorted(zh_slugs-ja_slugs)}, ja_only={sorted(ja_slugs-zh_slugs)}")
    items = []
    for post in sorted(ja_posts, key=lambda item: int(item.data.get("importance", 999999))):
        slug = str(post.data["slug"])
        expected_story_id = f"{edition_date}-{slug}"
        if post.data.get("story_id") != expected_story_id:
            raise EditionError(f"{post.path}: story_id must be {expected_story_id}")
        current_status = str((post.data.get("wordpress") or {}).get("status", ""))
        if current_status != wordpress_status:
            raise EditionError(f"{post.path}: wordpress.status must be {wordpress_status}")
        items.append(
            {
                "story_id": expected_story_id,
                "slug": slug,
                "section": str(post.data["daily_section"]),
                "importance": int(post.data["importance"]),
                "title": str(post.data["title"]),
                "excerpt": str(post.data["excerpt"]),
                "path": str(post.path.relative_to(root)),
            }
        )
    return {
        "schema_version": 2,
        "edition": edition_date,
        "edition_type": "morning",
        "coverage_start": coverage_start,
        "coverage_end": coverage_end,
        "published_at": published_at,
        "lang": "ja",
        "editorial_origin": "japanese-sources",
        "publication_target": "wordpress",
        "wordpress_default_status": wordpress_status,
        "expected_counts": dict(EXPECTED_COUNTS),
        "posts": items,
    }


def write_generated_edition(
    *,
    root: Path,
    edition_date: str,
    coverage_start: str,
    coverage_end: str,
    published_at: str,
    wordpress_status: str,
) -> dict[str, Path]:
    manifest = build_manifest(
        root=root,
        edition_date=edition_date,
        coverage_start=coverage_start,
        coverage_end=coverage_end,
        published_at=published_at,
        wordpress_status=wordpress_status,
    )
    ja_posts = collect_posts(root, "ja", edition_date)
    manifest_path = root / "japanese" / f"edition-{edition_date}.yml"
    chinese_daily_path = root / "daily" / f"{edition_date}.md"
    japanese_daily_path = root / "japanese" / "daily" / f"{edition_date}.md"
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    chinese_daily_path.parent.mkdir(parents=True, exist_ok=True)
    japanese_daily_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(yaml.safe_dump(manifest, allow_unicode=True, sort_keys=False), encoding="utf-8")
    chinese_daily_path.write_text(
        render_chinese_daily(
            edition_date=edition_date,
            coverage_start=coverage_start,
            coverage_end=coverage_end,
            published_at=published_at,
        ),
        encoding="utf-8",
    )
    japanese_daily_path.write_text(
        render_japanese_daily(
            edition_date=edition_date,
            coverage_start=coverage_start,
            coverage_end=coverage_end,
            published_at=published_at,
            posts=ja_posts,
            wordpress_status=wordpress_status,
        ),
        encoding="utf-8",
    )
    return {
        "manifest": manifest_path,
        "chinese_daily": chinese_daily_path,
        "japanese_daily": japanese_daily_path,
    }
