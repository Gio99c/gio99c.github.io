---
layout: page
title: AI News Archive
permalink: /ai-news/archive/
---

# AI News Archive

All daily AI news digests in chronological order.


{% assign all_news = site.ai_news | sort: 'date' | reverse %}

{% for news in all_news %}
<div style="margin-bottom: 1.5rem;">
  <a href="{{ news.url | relative_url }}" style="text-decoration: none; display: block;">
    <div class="article-card" style="padding: 1.5rem; border: 1px solid #e5e5e5; border-radius: 8px; background: white; transition: all 0.2s ease; cursor: pointer;" onmouseover="this.style.boxShadow='0 4px 12px rgba(0,0,0,0.1)'; this.style.transform='translateY(-2px)'" onmouseout="this.style.boxShadow='none'; this.style.transform='translateY(0)'">
      <div class="article-meta" style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; color: #a3a3a3; font-size: 0.85rem;">
        <span class="article-date" style="font-weight: 500;">{{ news.date | date: "%B %d, %Y" }}</span>
        <span class="article-separator" style="color: #e5e5e5; margin: 0 1rem; font-weight: 300; font-size: 0.8rem;">•</span>
        <span class="article-count" style="font-style: italic; background: #fafafa; padding: 0.25rem 0.5rem; border-radius: 4px; border: 1px solid #e5e5e5;">{{ news.stories | size }} stories</span>
      </div>
      <h3 style="margin: 0; font-size: 1.1rem; line-height: 1.4; color: #1a1a1a;">{{ news.summary | truncate: 100 }}</h3>
    </div>
  </a>
</div>
{% endfor %}

{% if site.ai_news.size == 0 %}
<div class="no-news">
  <p>No articles yet. Daily digests start tomorrow.</p>
</div>
{% endif %}


<div class="back-to-news">
  <a href="/ai-news/">← Back to AI News</a>
</div> 