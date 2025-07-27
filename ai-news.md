---
layout: page
title: AI News
permalink: /ai-news/
---

# AI News

Daily digest of what's happening in AI and tech.

> **How this works**: OpenAI searches the web each morning and curates stories that matter to practitioners. Real sources, real URLs, no hallucinations.


## Latest

{% assign recent_news = site.ai_news | sort: 'date' | reverse %}
{% assign latest_news = recent_news | slice: 0, 1 %}

{% for news in latest_news %}
<div style="margin-bottom: 3rem;">
  <a href="{{ news.url | relative_url }}" style="text-decoration: none; display: block;">
    <div class="latest-news-highlight" style="background: linear-gradient(135deg, #fafafa 0%, white 100%); border: 1px solid #e5e5e5; border-radius: 12px; padding: 2rem; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05); transition: all 0.2s ease; cursor: pointer;" onmouseover="this.style.boxShadow='0 4px 12px rgba(0,0,0,0.1)'; this.style.transform='translateY(-2px)'" onmouseout="this.style.boxShadow='0 2px 8px rgba(0, 0, 0, 0.05)'; this.style.transform='translateY(0)'">
      <h2 style="margin-top: 0; margin-bottom: 1rem; font-size: 1.8rem; color: #1a1a1a;">{{ news.date | date: "%B %d, %Y" }}</h2>
      <div class="news-summary" style="color: #4a4a4a; margin-bottom: 1rem; font-size: 1.05rem; line-height: 1.5;">{{ news.summary }}</div>
      <div class="news-count" style="color: #a3a3a3; font-size: 0.9rem; font-style: italic;">{{ news.stories | size }} stories</div>
    </div>
  </a>
</div>
{% endfor %}


## Recent Articles

{% assign recent_articles = recent_news | slice: 1, 5 %}
{% for news in recent_articles %}
<div style="margin-bottom: 1.5rem;">
  <a href="{{ news.url | relative_url }}" style="text-decoration: none; display: block;">
    <div class="article-card" style="padding: 1.5rem; border: 1px solid #e5e5e5; border-radius: 8px; background: white; transition: all 0.2s ease; cursor: pointer;" onmouseover="this.style.boxShadow='0 4px 12px rgba(0,0,0,0.1)'; this.style.transform='translateY(-2px)'" onmouseout="this.style.boxShadow='none'; this.style.transform='translateY(0)'">
      <div class="article-meta" style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; color: #a3a3a3; font-size: 0.85rem;">
        <span class="article-date" style="font-weight: 500;">{{ news.date | date: "%B %d, %Y" }}</span>
        <span class="article-separator" style="color: #e5e5e5; margin: 0 1rem; font-weight: 300; font-size: 0.8rem;">•</span>
        <span class="article-count" style="font-style: italic; background: #fafafa; padding: 0.25rem 0.5rem; border-radius: 4px; border: 1px solid #e5e5e5;">{{ news.stories | size }} stories</span>
      </div>
      <h3 style="margin: 0; font-size: 1.1rem; line-height: 1.4; color: #1a1a1a;">{{ news.summary | truncate: 80 }}</h3>
    </div>
  </a>
</div>
{% endfor %}

{% if site.ai_news.size > 6 %}
<div class="view-all-archive">
  <a href="/ai-news/archive/" class="archive-link">View all {{ site.ai_news.size }} articles →</a>
</div>
{% endif %}

{% if site.ai_news.size == 0 %}
<div class="no-news">
  <p>Daily digests start tomorrow. System fetches news at 9 AM UTC.</p>
</div>
{% endif %}

---

## About

OpenAI searches the web daily for what actually matters to AI practitioners:

- Research breakthroughs with real impact
- Product launches people will use
- Industry changes that affect how we work  
- Technical advances with practical applications