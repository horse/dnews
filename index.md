---
layout: default
title: 首页
permalink: /
---

{% assign latest_post = site.posts | first %}
{% assign latest_news_date = latest_post.news_date %}
{% assign latest_news_date_path = latest_news_date | date: "%Y-%m-%d" %}
{% assign latest_news_date_label = latest_news_date | date: "%Y年%-m月%-d日" %}
{% assign latest_posts = site.posts | where: "news_date", latest_news_date %}
{% assign core_posts = latest_posts | where: "daily_section", "core" | sort: "importance" %}
{% assign social_posts = latest_posts | where: "daily_section", "social" | sort: "importance" %}
{% assign other_posts = latest_posts | where: "daily_section", "other" | sort: "importance" %}
{% assign latest_report_count = latest_posts | size %}
{% assign social_report_count = social_posts | size %}
{% assign other_report_count = other_posts | size %}

<section class="hero">
  <div class="hero-kicker">Japan Morning News · Re-reported in Chinese</div>
  <h1>重要的事，也包括一个社会如何生活。</h1>
  <p>dnews 每天从可信新闻媒体和权威机构发布中筛选事件，重新检索、核验并写成可独立阅读的中文新闻；社交媒体热度和搜索趋势不作为选题依据。</p>
  <a class="daily-link" href="{{ '/daily/' | append: latest_news_date_path | append: '/' | relative_url }}">阅读 {{ latest_news_date_label }} 日本新闻早报：{{ latest_report_count }}篇报道 →</a>
</section>

<p class="section-kicker">Political, economic & major events</p>
<h2 class="home-section-title">政治经济与重大事件</h2>
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
  <a href="{{ '/daily/' | append: latest_news_date_path | append: '/#social-observation' | relative_url }}">查看全部{{ social_report_count }}篇 →</a>
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
  <a href="{{ '/daily/' | append: latest_news_date_path | append: '/#science-culture-city' | relative_url }}">查看全部{{ other_report_count }}篇 →</a>
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
