---
layout: page
title: AI News
permalink: /ai-news/
---

# AI News

Daily digest of what's happening in AI and tech.

> **How this works**: GPT-4.1 searches the web each morning and picks the stories that matter to practitioners. All summaries link to original sources.

---

## Latest

{% assign recent_news = site.ai_news | sort: 'date' | reverse %}
{% assign latest_news = recent_news | slice: 0, 1 %}

{% for news in latest_news %}
<div class="latest-news-highlight">
  <h2><a href="{{ news.url | relative_url }}">{{ news.date | date: "%b %d" }}</a></h2>
  <div class="news-summary">{{ news.summary }}</div>
  <div class="news-count">{{ news.stories | size }} stories</div>
</div>
{% endfor %}

---

## Archive

{% for news in recent_news %}
<div class="news-timeline-item">
  <div class="news-date">{{ news.date | date: "%b %d" }}</div>
  <div class="news-content">
    <h3><a href="{{ news.url | relative_url }}">Daily digest</a></h3>
    <p class="news-preview">{{ news.summary | truncate: 120 }}</p>
    <span class="news-count">{{ news.stories | size }} stories</span>
  </div>
</div>
{% endfor %}

{% if site.ai_news.size == 0 %}
<div class="no-news">
  <p>Daily digests start tomorrow. System fetches news at 9 AM UTC.</p>
</div>
{% endif %}

---

## About

This pulls the most important AI and tech news each day. Focus is on:

- Research breakthroughs that practitioners should know
- Product launches and company announcements  
- Industry developments and policy changes
- Technical advances with real-world impact

The AI skips fluff and focuses on what's useful. Each story includes context on why it matters.