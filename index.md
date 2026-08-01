---
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
