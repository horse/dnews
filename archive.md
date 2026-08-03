---
layout: page
title: 日报归档
permalink: /archive/
---

{% assign daily_pages = site.pages | where: "edition_type", "morning" | sort: "edition_date" | reverse %}
{% assign current_year = "" %}

{% for daily in daily_pages %}
  {% assign daily_year = daily.edition_date | slice: 0, 4 %}
  {% if daily_year != current_year %}
    {% unless forloop.first %}</ul>{% endunless %}
    <h2>{{ daily_year }}年</h2>
    <ul class="daily-archive">
    {% assign current_year = daily_year %}
  {% endif %}
  <li>
    <a href="{{ daily.url | relative_url }}">{{ daily.title }}</a>
    {% if daily.description %}<br><span>{{ daily.description }}</span>{% endif %}
  </li>
  {% if forloop.last %}</ul>{% endif %}
{% endfor %}
