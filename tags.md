---
layout: page
title: 标签
permalink: /tags/
---

<p class="tag-index-intro">标签收录新闻正文中出现的人名、地名、组织名、制度名、事件名、行业与关键概念。分类用于区分大领域，标签用于连接具体对象。</p>

{% assign sorted_tags = site.tags | sort %}

<div class="tag-cloud" aria-label="全部标签">
{% for tag_entry in sorted_tags %}
  {% assign tag_name = tag_entry[0] %}
  {% assign tag_posts = tag_entry[1] %}
  <a class="tag-pill tag-pill--count" href="#{{ tag_name | url_encode }}">{{ tag_name }} <span>{{ tag_posts | size }}</span></a>
{% endfor %}
</div>

<div class="tag-groups">
{% for tag_entry in sorted_tags %}
  {% assign tag_name = tag_entry[0] %}
  {% assign tag_posts = tag_entry[1] | sort: "importance" %}
  <section class="tag-group" id="{{ tag_name | escape }}">
    <h2>{{ tag_name }} <span class="tag-count">{{ tag_posts | size }}</span></h2>
    <ul>
    {% for post in tag_posts %}
      <li>
        <a href="{{ post.url | relative_url }}">{{ post.title }}</a>
        {% if post.news_date %}<span>{{ post.news_date | date: "%Y年%-m月%-d日" }}</span>{% endif %}
      </li>
    {% endfor %}
    </ul>
  </section>
{% endfor %}
</div>
