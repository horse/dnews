#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POSTS = ROOT / "_posts"

core_files = [
    "2026-08-01-kumamoto-quake-supply-chain.md",
    "2026-08-01-boj-holds-rate-inflation-risk.md",
    "2026-08-01-japan-yen-intervention-estimate.md",
    "2026-08-01-us-treasury-yen-readiness.md",
    "2026-08-01-japan-national-intelligence-bureau.md",
    "2026-08-01-tokyo-cpi-july.md",
    "2026-08-01-japan-labor-june.md",
    "2026-08-01-japan-industrial-output-june.md",
]

social_files = [
    "2026-08-01-kumamoto-water-heat-evacuation.md",
    "2026-08-01-kumamoto-red-cross-emergency-care.md",
    "2026-08-01-kumamoto-public-facility-closures.md",
    "2026-08-01-tomoiku-end-solo-parenting.md",
    "2026-08-01-tokyo-skilled-trades-succession.md",
    "2026-08-01-tokyo-art-accessibility-exhibition.md",
    "2026-08-01-japan-environment-plan-review.md",
    "2026-08-01-tokyo-life-opinion-survey.md",
]

other_files = [
    "2026-08-01-kahaku-human-earth-exhibition.md",
    "2026-08-01-conrad-nagoya-opening.md",
    "2026-08-01-national-art-center-family-week.md",
    "2026-08-01-yoshimura-akira-yuonki.md",
    "2026-08-01-okayama-ponpon-boat-exhibition.md",
    "2026-08-01-japan-medical-education-conference.md",
    "2026-08-01-medical-physics-summer-seminar.md",
    "2026-08-01-japan-cinema-july31.md",
    "2026-08-01-npb-july31-roundup.md",
    "2026-08-01-kasai-sunflower-lighting.md",
]

for filename in core_files + social_files + other_files:
    path = POSTS / filename
    if not path.exists():
        raise RuntimeError(f"Expected post missing: {path}")

# Existing reports remain untouched except for section metadata.
for filename in core_files:
    path = POSTS / filename
    text = path.read_text(encoding="utf-8")
    marker = "news_date: '2026-07-31'\n"
    if "daily_section: core\n" not in text:
        if marker not in text:
            raise RuntimeError(f"news_date marker missing: {filename}")
        text = text.replace(marker, marker + "daily_section: core\n", 1)
        path.write_text(text, encoding="utf-8")

# Repair the first social writer's YAML indentation before parsing in CI.
for filename in social_files:
    path = POSTS / filename
    text = path.read_text(encoding="utf-8")
    before, wp_tail = text.split("wordpress:\n", 1)
    wp_front, body = wp_tail.split("---\n\n", 1)
    fixed_lines = [("  " + line if line.startswith("- ") else line) for line in wp_front.splitlines()]
    path.write_text(before + "wordpress:\n" + "\n".join(fixed_lines) + "\n---\n\n" + body, encoding="utf-8")

(ROOT / "daily/2026-07-31.md").write_text('''---
layout: page
title: "日本重要新闻日报｜2026年7月31日"
date: 2026-08-01 09:10:00 +0900
news_date: '2026-07-31'
permalink: /daily/2026-07-31/
description: "26篇独立报道呈现7月31日的日本：政治经济与灾害大事、社会生活的结构变化，以及科学、文化、城市和体育现场。"
seo_title: "2026年7月31日日本日报：26篇报道呈现政治经济、社会与文化"
meta_description: "2026年7月31日日本日报扩展为26篇独立报道：8篇政治经济大事、8篇社会观察、10篇科学文化城市与体育新闻。"
---

<div class="daily-meta">News date · 2026.07.31 JST · 26 reports</div>

本期以日本标准时间7月31日为事实截点，共收录26篇独立报道。八篇政治经济大事保留完整篇幅，继续解释熊本地震、日元、金融政策、国家情报体制与月末经济数据；八篇社会观察转向供水、医疗、公共服务、育儿、技能传承、无障碍文化、环境治理和城市民意；十篇其他新闻记录科学展览、文学空间、医学教育、城市更新、电影、棒球与夏季公共空间。

<div class="daily-summary">
<strong>今日主线：</strong>国家层面的风险管理和普通人的生活条件同时发生变化。熊本地震既冲击汽车与半导体，也让供水、急诊、育儿和公共设施成为问题；日元与利率决定家庭购买力；而美术馆、学校、研究机构和城市公园则展示日本社会如何处理教育、无障碍、技能接班与公共文化。
</div>

{% assign all_daily_posts = site.posts | where: "news_date", page.news_date %}
{% assign core_posts = all_daily_posts | where: "daily_section", "core" | sort: "importance" %}
{% assign social_posts = all_daily_posts | where: "daily_section", "social" | sort: "importance" %}
{% assign other_posts = all_daily_posts | where: "daily_section", "other" | sort: "importance" %}

<section class="daily-section daily-section--core" id="politics-economy">
<div class="daily-section__header">
<p class="section-kicker">Core · {{ core_posts | size }} reports</p>
<h2>政治经济大事</h2>
<p>全国性政策、经济、安全、统计与重大灾害进展。相近议题仍保持独立文章，但在版面中作为专题共同阅读。</p>
</div>
<ol class="daily-list">
{% for post in core_posts %}
<li>
<h2><a href="{{ post.url | relative_url }}">{{ post.title }}</a></h2>
<p>{{ post.excerpt | strip_html | strip_newlines }}</p>
{% include tag-list.html tags=post.tags limit=6 compact=true %}
</li>
{% endfor %}
</ol>
</section>

<section class="daily-section daily-section--social" id="social-observation">
<div class="daily-section__header">
<p class="section-kicker">Society · {{ social_posts | size }} reports</p>
<h2>社会观察</h2>
<p>不以类别配额填充版面，而选择能够说明公共服务、家庭、劳动、地方治理和生活条件的新闻。</p>
</div>
<div class="social-grid">
{% for post in social_posts %}
<article class="social-card">
<div class="post-meta">{{ post.categories | join: " / " }}</div>
<h3><a href="{{ post.url | relative_url }}">{{ post.title }}</a></h3>
<p>{{ post.excerpt | strip_html | strip_newlines }}</p>
{% include tag-list.html tags=post.tags limit=6 compact=true %}
</article>
{% endfor %}
</div>
</section>

<section class="daily-section daily-section--other" id="science-culture-city">
<div class="daily-section__header">
<p class="section-kicker">Elsewhere · {{ other_posts | size }} reports</p>
<h2>科学、文化、城市与其他</h2>
<p>篇幅更紧凑，但仍按独立新闻完成核验、背景和意义说明，记录同一天日本社会的其他现场。</p>
</div>
<div class="brief-grid">
{% for post in other_posts %}
<article class="brief-card">
<div class="post-meta">{{ post.categories | join: " / " }}</div>
<h3><a href="{{ post.url | relative_url }}">{{ post.title }}</a></h3>
<p>{{ post.excerpt | strip_html | strip_newlines }}</p>
{% include tag-list.html tags=post.tags limit=4 compact=true %}
</article>
{% endfor %}
</div>
</section>

## 编辑说明

本期没有为了“覆盖分类”删除任何一篇已有的重要新闻。日本银行利率、日元干预和美国潜在介入仍分别成稿，因为它们对应央行、财政当局和国际协调三个不同动作；日报通过分层与专题化解决重复感，而不是通过删稿制造多样性。

社会观察的入选条件是出现了可核验的新事实，并且该事实能够说明公共服务、家庭分工、劳动技能、文化可进入性或治理方式。活动类新闻只有在能解释更大的社会变化时才进入这一层。

“科学、文化、城市与其他”并非轻新闻摘录。每篇都保留独立来源、标签、SEO与WordPress元数据，只根据事件性质采用更短、更直接的写法。所有文章仍可单独阅读和后续更新。
''', encoding="utf-8")

(ROOT / "index.md").write_text('''---
layout: default
title: 首页
permalink: /
---

<section class="hero">
  <div class="hero-kicker">Japan Daily News · Re-reported in Chinese</div>
  <h1>重要的事，也包括一个社会如何生活。</h1>
  <p>dnews 每天先识别全国性大事，再补充能够呈现公共服务、地方生活、科学文化与城市变化的独立报道。所有文章都重新查找资料、核验并写作。</p>
  <a class="daily-link" href="{{ '/daily/2026-07-31/' | relative_url }}">阅读 2026年7月31日完整日报：26篇报道 →</a>
</section>

{% assign core_posts = site.posts | where: "daily_section", "core" | sort: "importance" %}
{% assign social_posts = site.posts | where: "daily_section", "social" | sort: "importance" %}
{% assign other_posts = site.posts | where: "daily_section", "other" | sort: "importance" %}

<p class="section-kicker">Political & economic agenda</p>
<h2 class="home-section-title">政治经济大事</h2>
<div class="news-grid">
{% for post in core_posts limit: 8 %}
  <article class="news-card">
    <div class="post-meta">{{ post.news_date | date: "%Y年%-m月%-d日" }} · {{ post.categories | join: " / " }}</div>
    <h2><a href="{{ post.url | relative_url }}">{{ post.title }}</a></h2>
    <p>{{ post.excerpt | strip_html | strip_newlines }}</p>
    {% include tag-list.html tags=post.tags limit=6 compact=true %}
  </article>
{% endfor %}
</div>

<div class="home-section-heading">
  <div>
    <p class="section-kicker">Society</p>
    <h2 class="home-section-title">社会观察</h2>
  </div>
  <a href="{{ '/daily/2026-07-31/#social-observation' | relative_url }}">查看全部8篇 →</a>
</div>
<div class="social-grid social-grid--home">
{% for post in social_posts limit: 4 %}
  <article class="social-card">
    <div class="post-meta">{{ post.categories | join: " / " }}</div>
    <h3><a href="{{ post.url | relative_url }}">{{ post.title }}</a></h3>
    <p>{{ post.excerpt | strip_html | strip_newlines }}</p>
    {% include tag-list.html tags=post.tags limit=4 compact=true %}
  </article>
{% endfor %}
</div>

<div class="home-section-heading">
  <div>
    <p class="section-kicker">Science · Culture · City</p>
    <h2 class="home-section-title">日本的其他现场</h2>
  </div>
  <a href="{{ '/daily/2026-07-31/#science-culture-city' | relative_url }}">查看全部10篇 →</a>
</div>
<div class="brief-grid brief-grid--home">
{% for post in other_posts limit: 6 %}
  <article class="brief-card">
    <div class="post-meta">{{ post.categories | join: " / " }}</div>
    <h3><a href="{{ post.url | relative_url }}">{{ post.title }}</a></h3>
    <p>{{ post.excerpt | strip_html | strip_newlines }}</p>
  </article>
{% endfor %}
</div>
''', encoding="utf-8")

(ROOT / "tests/test_tags.sh").write_text(r'''#!/usr/bin/env bash
set -euo pipefail

if [[ "${SKIP_BUILD:-0}" != "1" ]]; then
  bundle exec jekyll build
fi

homepage="_site/index.html"
daily_page="_site/daily/2026-07-31/index.html"
tag_page="_site/tags/index.html"
core_page="_site/news/2026/07/31/kumamoto-earthquake-supply-chain/index.html"
social_page="_site/news/2026/07/31/kumamoto-water-heat-evacuation/index.html"
other_page="_site/news/2026/07/31/kahaku-human-earth-exhibition/index.html"

for page in "$homepage" "$daily_page" "$tag_page" "$core_page" "$social_page" "$other_page"; do
  test -f "$page" || { echo "Missing rendered page: $page" >&2; exit 1; }
done

grep -q '政治经济大事' "$homepage"
grep -q '社会观察' "$homepage"
grep -q '日本的其他现场' "$homepage"
grep -q '政治经济大事' "$daily_page"
grep -q '社会观察' "$daily_page"
grep -q '科学、文化、城市与其他' "$daily_page"
grep -q 'class="social-grid"' "$daily_page"
grep -q 'class="brief-grid"' "$daily_page"
grep -q '相关标签' "$core_page"
grep -q '相关标签' "$social_page"
grep -q '相关标签' "$other_page"
grep -q 'kumamoto-water-heat-evacuation' "$tag_page"
grep -q 'kahaku-human-earth-exhibition' "$tag_page"

ruby <<'RUBY'
require 'yaml'
counts = Hash.new(0)
allowed = %w[core social other]
Dir['_posts/*.md'].sort.each do |path|
  text = File.read(path, encoding: 'UTF-8')
  parts = text.split(/^---\s*$\n?/, 3)
  abort "#{path}: invalid front matter" unless parts.length == 3
  data = YAML.safe_load(parts[1], aliases: true)
  tags = Array(data['tags'])
  body = parts[2]
  section = data['daily_section'].to_s
  abort "#{path}: invalid daily_section #{section.inspect}" unless allowed.include?(section)
  abort "#{path}: expected 12-25 tags, got #{tags.length}" unless (12..25).cover?(tags.length)
  missing = tags.reject { |tag| body.include?(tag.to_s) }
  abort "#{path}: tags absent from body: #{missing.join(', ')}" unless missing.empty?
  wordpress_tags = Array(data.dig('wordpress', 'tags'))
  abort "#{path}: wordpress.tags does not match tags" unless wordpress_tags == tags
  counts[section] += 1 if data['news_date'].to_s == '2026-07-31'
end
expected = {'core' => 8, 'social' => 8, 'other' => 10}
abort "section counts mismatch: #{counts.inspect}" unless counts == expected
RUBY

echo "Expanded daily edition acceptance checks passed."
''', encoding="utf-8")

scss_path = ROOT / "assets/main.scss"
scss = scss_path.read_text(encoding="utf-8")
marker = "/* Expanded daily edition */"
if marker not in scss:
    scss += '''

/* Expanded daily edition */
.daily-section { margin: 3.4rem 0 4rem; }
.daily-section__header { max-width: 800px; margin-bottom: 1.5rem; }
.daily-section__header h2, .home-section-title { margin: 0.2rem 0 0.55rem; font-size: clamp(1.65rem, 3vw, 2.35rem); line-height: 1.22; }
.daily-section__header > p:last-child { color: var(--muted); }
.social-grid, .brief-grid { display: grid; gap: 1rem; grid-template-columns: repeat(2, minmax(0, 1fr)); }
.social-card, .brief-card { border: 1px solid var(--rule); background: var(--card); }
.social-card { padding: 1.35rem 1.45rem; }
.brief-card { padding: 1.1rem 1.2rem; }
.social-card h3, .brief-card h3 { margin: 0.3rem 0 0.55rem; line-height: 1.38; }
.social-card h3 { font-size: 1.25rem; }
.brief-card h3 { font-size: 1.08rem; }
.social-card p, .brief-card p { color: var(--muted); margin-bottom: 0; }
.home-section-heading { display: flex; align-items: end; justify-content: space-between; gap: 1rem; margin: 3.4rem 0 1.2rem; border-top: 1px solid var(--rule); padding-top: 1.5rem; }
.home-section-heading .section-kicker { margin-bottom: 0; }
.home-section-heading a { flex: 0 0 auto; color: var(--accent); font-size: 0.92rem; }
.social-grid--home, .brief-grid--home { margin-bottom: 3.4rem; }
@media (max-width: 720px) {
  .social-grid, .brief-grid { grid-template-columns: 1fr; }
  .home-section-heading { display: block; }
  .home-section-heading a { display: inline-block; margin-top: 0.5rem; }
}
'''
    scss_path.write_text(scss, encoding="utf-8")

# Restore a permanent, read-only PR test workflow.
(ROOT / ".github/workflows/tags-ci.yml").write_text('''name: Test expanded daily edition

on:
  pull_request:
    paths:
      - '_posts/**'
      - '_includes/**'
      - '_layouts/**'
      - 'daily/**'
      - 'tests/test_tags.sh'
      - 'tags.md'
      - 'index.md'
      - 'assets/main.scss'
      - '_config.yml'
      - '.github/workflows/tags-ci.yml'

permissions:
  contents: read
  pages: read

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - name: Check out repository
        uses: actions/checkout@v4
      - name: Read GitHub Pages configuration
        uses: actions/configure-pages@v5
      - name: Build with GitHub Pages Jekyll
        uses: actions/jekyll-build-pages@v1
        with:
          source: ./
          destination: ./_site
      - name: Run expanded-edition acceptance checks
        run: SKIP_BUILD=1 bash tests/test_tags.sh
''', encoding="utf-8")

for relative in [
    "tools/generate_expanded_daily.py",
    "tools/run_expanded_generator.py",
    ".github/workflows/generate-expanded-daily.yml",
    "tools/finalize_expanded_daily.py",
]:
    path = ROOT / relative
    if path.exists():
        path.unlink()
