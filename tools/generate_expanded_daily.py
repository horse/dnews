#!/usr/bin/env python3
from pathlib import Path
import base64
import io
import tarfile

ROOT = Path(__file__).resolve().parents[1]
PAYLOAD = """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"""

with tarfile.open(fileobj=io.BytesIO(base64.b64decode(PAYLOAD)), mode="r:gz") as archive:
    archive.extractall(ROOT)

core_files = ['_posts/2026-08-01-kumamoto-quake-supply-chain.md', '_posts/2026-08-01-boj-holds-rate-inflation-risk.md', '_posts/2026-08-01-japan-yen-intervention-estimate.md', '_posts/2026-08-01-us-treasury-yen-readiness.md', '_posts/2026-08-01-japan-national-intelligence-bureau.md', '_posts/2026-08-01-tokyo-cpi-july.md', '_posts/2026-08-01-japan-labor-june.md', '_posts/2026-08-01-japan-industrial-output-june.md']
for relative in core_files:
    path = ROOT / relative
    text = path.read_text(encoding="utf-8")
    if "daily_section: core" not in text:
        marker = "news_date: '2026-07-31'\n"
        if marker not in text:
            raise RuntimeError(f"news_date marker missing in {relative}")
        text = text.replace(marker, marker + "daily_section: core\n", 1)
        path.write_text(text, encoding="utf-8")

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

<section class="daily-section daily-section--core">
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

<section class="daily-section daily-section--social">
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

<section class="daily-section daily-section--other">
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
  <a href="{{ '/daily/2026-07-31/#社会观察' | relative_url }}">查看全部8篇 →</a>
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
  <a href="{{ '/daily/2026-07-31/#科学-文化-城市与其他' | relative_url }}">查看全部10篇 →</a>
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
(ROOT / "tests/test_tags.sh").write_text('''#!/usr/bin/env bash
set -euo pipefail

if [[ "${SKIP_BUILD:-0}" != "1" ]]; then
  bundle exec jekyll build
fi

homepage="_site/index.html"
daily_page="_site/daily/2026-07-31/index.html"
tag_page="_site/tags/index.html"
article_page="_site/news/2026/07/31/kumamoto-earthquake-supply-chain/index.html"
social_page="_site/news/2026/07/31/kumamoto-water-heat-evacuation/index.html"
other_page="_site/news/2026/07/31/kahaku-human-earth-exhibition/index.html"

for page in "$homepage" "$daily_page" "$tag_page" "$article_page" "$social_page" "$other_page"; do
  test -f "$page" || {
    echo "Missing rendered page: $page" >&2
    exit 1
  }
done

grep -q 'href="/dnews/tags/"' "$homepage"
grep -q 'class="tag-pill"' "$homepage"
grep -q '政治经济大事' "$homepage"
grep -q '社会观察' "$homepage"
grep -q '日本的其他现场' "$homepage"
grep -q '政治经济大事' "$daily_page"
grep -q '社会观察' "$daily_page"
grep -q '科学、文化、城市与其他' "$daily_page"
grep -q 'class="social-grid"' "$daily_page"
grep -q 'class="brief-grid"' "$daily_page"
grep -q '相关标签' "$article_page"
grep -q '相关标签' "$social_page"
grep -q '相关标签' "$other_page"
grep -q '日本气象厅' "$article_page"
grep -q '标签收录新闻正文中出现的' "$tag_page"
grep -q '熊本县' "$tag_page"
grep -q 'kumamoto-earthquake-supply-chain' "$tag_page"
grep -q 'kumamoto-water-heat-evacuation' "$tag_page"
grep -q 'kahaku-human-earth-exhibition' "$tag_page"

ruby <<'RUBY'
require 'yaml'

edition_counts = Hash.new(0)
allowed_sections = %w[core social other]

Dir['_posts/*.md'].sort.each do |path|
  text = File.read(path, encoding: 'UTF-8')
  parts = text.split(/^---\s*$\n?/, 3)
  abort "#{path}: invalid front matter" unless parts.length == 3

  data = YAML.safe_load(parts[1], aliases: true)
  tags = Array(data['tags'])
  body = parts[2]
  section = data['daily_section'].to_s

  unless allowed_sections.include?(section)
    abort "#{path}: invalid or missing daily_section #{section.inspect}"
  end

  unless (12..25).cover?(tags.length)
    abort "#{path}: expected 12-25 tags, got #{tags.length}"
  end

  missing = tags.reject { |tag| body.include?(tag.to_s) }
  unless missing.empty?
    abort "#{path}: tags absent from body: #{missing.join(', ')}"
  end

  wordpress_tags = Array(data.dig('wordpress', 'tags'))
  unless wordpress_tags == tags
    abort "#{path}: wordpress.tags does not match tags"
  end

  if data['news_date'].to_s == '2026-07-31'
    edition_counts[section] += 1
  end
end

expected = {'core' => 8, 'social' => 8, 'other' => 10}
unless edition_counts == expected
  abort "2026-07-31 section counts mismatch: expected #{expected.inspect}, got #{edition_counts.inspect}"
end
RUBY

echo "Expanded daily edition acceptance checks passed."
''', encoding="utf-8")

scss_path = ROOT / "assets/main.scss"
scss = scss_path.read_text(encoding="utf-8")
css = '''/* Expanded daily edition */
.daily-section {
  margin: 3.4rem 0 4rem;
}

.daily-section__header {
  max-width: 800px;
  margin-bottom: 1.5rem;
}

.daily-section__header h2,
.home-section-title {
  margin: 0.2rem 0 0.55rem;
  font-size: clamp(1.65rem, 3vw, 2.35rem);
  line-height: 1.22;
}

.daily-section__header > p:last-child {
  color: var(--muted);
}

.social-grid,
.brief-grid {
  display: grid;
  gap: 1rem;
}

.social-grid {
  grid-template-columns: repeat(2, minmax(0, 1fr));
}

.brief-grid {
  grid-template-columns: repeat(2, minmax(0, 1fr));
}

.social-card,
.brief-card {
  border: 1px solid var(--rule);
  background: var(--card);
}

.social-card {
  padding: 1.35rem 1.45rem;
}

.brief-card {
  padding: 1.1rem 1.2rem;
}

.social-card h3,
.brief-card h3 {
  margin: 0.3rem 0 0.55rem;
  line-height: 1.38;
}

.social-card h3 {
  font-size: 1.25rem;
}

.brief-card h3 {
  font-size: 1.08rem;
}

.social-card p,
.brief-card p {
  color: var(--muted);
  margin-bottom: 0;
}

.home-section-heading {
  display: flex;
  align-items: end;
  justify-content: space-between;
  gap: 1rem;
  margin: 3.4rem 0 1.2rem;
  border-top: 1px solid var(--rule);
  padding-top: 1.5rem;
}

.home-section-heading .section-kicker {
  margin-bottom: 0;
}

.home-section-heading a {
  flex: 0 0 auto;
  color: var(--accent);
  font-size: 0.92rem;
}

.social-grid--home,
.brief-grid--home {
  margin-bottom: 3.4rem;
}

@media (max-width: 720px) {
  .social-grid,
  .brief-grid {
    grid-template-columns: 1fr;
  }

  .home-section-heading {
    display: block;
  }

  .home-section-heading a {
    display: inline-block;
    margin-top: 0.5rem;
  }
}
'''
if "/* Expanded daily edition */" not in scss:
    scss_path.write_text(scss.rstrip() + "\n\n" + css.lstrip(), encoding="utf-8")

# Remove the one-time generator from the resulting commit.
for relative in [
    "tools/generate_expanded_daily.py",
    ".github/workflows/generate-expanded-daily.yml",
]:
    path = ROOT / relative
    if path.exists():
        path.unlink()
