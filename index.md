---
layout: default
title: 首页
permalink: /
---

<section class="hero">
  <div class="hero-kicker">Japan Daily News · Re-reported in Chinese</div>
  <h1>从日本的信息洪流中，找出真正重要的事。</h1>
  <p>dnews 每天先进行跨媒体发现和事件聚类，再为入选事件重新查找原始资料与独立报道，写成一篇可以单独读懂的中文新闻。</p>
  <a class="daily-link" href="{{ '/daily/2026-07-31/' | relative_url }}">阅读 2026年7月31日日本重要新闻日报 →</a>
</section>

<p class="section-kicker">Latest reports</p>

<div class="news-grid">
{% assign ordered_posts = site.posts | sort: "importance" %}
{% for post in ordered_posts limit: 8 %}
  <article class="news-card">
    <div class="post-meta">{{ post.news_date | date: "%Y年%-m月%-d日" }} · {{ post.categories | join: " / " }}</div>
    <h2><a href="{{ post.url | relative_url }}">{{ post.title }}</a></h2>
    <p>{{ post.excerpt | strip_html | strip_newlines }}</p>
    {% include tag-list.html tags=post.tags limit=6 compact=true %}
  </article>
{% endfor %}
</div>
