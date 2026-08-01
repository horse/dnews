import tempfile
import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))

from edition import (
    EXPECTED_COUNTS,
    collect_posts,
    latest_edition_date,
    parse_changed_edition_dates,
    render_japanese_daily,
    validate_edition,
    write_generated_edition,
)


def write_post(path: Path, *, date: str, slug: str, section: str, importance: int, lang: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if lang == 'ja':
        prefix = f"""story_id: {date}-{slug}
lang: ja
editorial_origin: japanese-sources
translation_status: original
publication_target: wordpress
"""
        source_heading = '## 参照資料'
        title = f'日本語 {slug}'
        excerpt = f'日本語要約 {slug}'
        categories = ['日本', '社会']
        tags = [f'タグ{i}' for i in range(12)]
    else:
        prefix = 'layout: post\n'
        source_heading = '## 资料来源'
        title = f'中文 {slug}'
        excerpt = f'中文摘要 {slug}'
        categories = ['日本', '社会']
        tags = [f'标签{i}' for i in range(12)]
    tag_lines = '\n'.join(f'- {tag}' for tag in tags)
    cat_lines = '\n'.join(f'- {cat}' for cat in categories)
    nested_tag_lines = '\n'.join(f'  - {tag}' for tag in tags)
    nested_cat_lines = '\n'.join(f'  - {cat}' for cat in categories)
    body_terms = (' '.join(tags) + ' ' + ('これは確認済みの新事実と公共的影響を説明する本文です。' if lang == 'ja' else '这是经过核验的新事实与公共影响说明。') * 120)
    path.write_text(
        f"""---
{prefix}title: {title}
date: '{date} 06:00:00 +0900'
news_date: '{date}'
daily_section: {section}
slug: {slug}
excerpt: {excerpt}
categories:
{cat_lines}
tags:
{tag_lines}
article_type: 事实报道型
analysis_angle: 公共影响
importance: {importance}
seo_title: {title}
meta_description: {excerpt}
source_checked_at: '{date}T05:30:00+09:00'
wordpress:
  status: publish
  post_type: post
  comment_status: closed
  categories:
{nested_cat_lines}
  tags:
{nested_tag_lines}
---

{body_terms}

{source_heading}

- [Source A](https://example.com/{slug}/a)
- [Source B](https://example.com/{slug}/b)
""",
        encoding='utf-8',
    )


class EditionLibraryTests(unittest.TestCase):
    def test_latest_edition_date_uses_manifest_filename(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'japanese').mkdir()
            (root / 'japanese' / 'edition-2026-08-01.yml').write_text('edition: 2026-08-01\n')
            (root / 'japanese' / 'edition-2026-08-03.yml').write_text('edition: 2026-08-03\n')
            self.assertEqual(latest_edition_date(root), '2026-08-03')

    def test_collect_posts_filters_by_requested_edition(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_post(root / '_posts' / '2026-08-01-a.md', date='2026-08-01', slug='a', section='core', importance=1, lang='zh')
            write_post(root / '_posts' / '2026-08-02-b.md', date='2026-08-02', slug='b', section='core', importance=1, lang='zh')
            posts = collect_posts(root, 'zh', '2026-08-02')
            self.assertEqual([post.data['slug'] for post in posts], ['b'])

    def test_parse_changed_dates_uses_manifest_and_front_matter(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_post(root / 'japanese' / 'posts' / '2026-08-02-a.md', date='2026-08-02', slug='a', section='core', importance=1, lang='ja')
            dates = parse_changed_edition_dates(
                root,
                ['japanese/edition-2026-08-03.yml', 'japanese/posts/2026-08-02-a.md', 'README.md'],
            )
            self.assertEqual(dates, ['2026-08-02', '2026-08-03'])

    def test_japanese_daily_contains_all_article_links(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            posts = []
            importance = {'core': 1, 'social': 101, 'other': 201}
            for section, count in EXPECTED_COUNTS.items():
                for index in range(count):
                    slug = f'{section}-{index + 1}'
                    path = root / 'japanese' / 'posts' / f'2026-08-02-{slug}.md'
                    write_post(path, date='2026-08-02', slug=slug, section=section, importance=importance[section] + index, lang='ja')
            posts = collect_posts(root, 'ja', '2026-08-02')
            text = render_japanese_daily(
                edition_date='2026-08-02',
                coverage_start='2026-08-01T06:00:00+09:00',
                coverage_end='2026-08-02T05:59:59+09:00',
                published_at='2026-08-02 06:00:00 +0900',
                posts=posts,
                wordpress_status='publish',
            )
            self.assertEqual(text.count('[全文を読む →]'), 26)
            self.assertIn('https://shinkiji.com/core-1/', text)
            self.assertIn('wordpress:\n  status: publish', text)

    def test_generated_edition_validates_as_one_dynamic_date(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            importance = {'core': 1, 'social': 101, 'other': 201}
            for section, count in EXPECTED_COUNTS.items():
                for index in range(count):
                    slug = f'{section}-{index + 1}'
                    write_post(root / '_posts' / f'2026-08-02-{slug}.md', date='2026-08-02', slug=slug, section=section, importance=importance[section] + index, lang='zh')
                    write_post(root / 'japanese' / 'posts' / f'2026-08-02-{slug}.md', date='2026-08-02', slug=slug, section=section, importance=importance[section] + index, lang='ja')
            write_generated_edition(
                root=root,
                edition_date='2026-08-02',
                coverage_start='2026-08-01T06:00:00+09:00',
                coverage_end='2026-08-02T05:59:59+09:00',
                published_at='2026-08-02 06:00:00 +0900',
                wordpress_status='publish',
            )
            report = validate_edition(root, '2026-08-02')
            self.assertEqual(report['chinese_posts'], 26)
            self.assertEqual(report['japanese_posts'], 26)
            self.assertEqual(report['wordpress_default_status'], 'publish')


if __name__ == '__main__':
    unittest.main()
