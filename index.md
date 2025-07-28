---
layout: default
---

# Hi, I'm Giuseppe Concialdi

I build AI systems that solve real problems. My work spans language models, computer vision, and generative AI—with a focus on making these technologies work reliably in practice.

I spend most of my time on:
* **Generative AI** - Creating AI agents that can reason and act autonomously
* **Language Models** - Designing and optimizing transformer-based models
* **Computer Vision** - Building systems that understand and process visual data
* **MLOps & Infrastructure** - Scaling ML systems for production environments

I write about what I learn along the way, from model architectures to the practical challenges of deploying AI at scale.

---

## Latest Writing

{% assign recent_posts = site.posts | slice: 0, 2 %}
{% for post in recent_posts %}
<div class="post-list-item">
  <h3 class="post-title">
    <a href="{{ post.url | relative_url }}">{{ post.title }}</a>
  </h3>
  <div class="post-date">{{ post.date | date: "%B %d, %Y" }}</div>
  {% if post.excerpt %}
  <div class="post-excerpt">{{ post.excerpt | strip_html | truncate: 160 }}</div>
  {% endif %}
</div>
{% endfor %}

{% if site.posts.size == 0 %}
<p><em>Coming soon - I'm working on some articles about transformers, LLM training, and generative AI applications.</em></p>
{% endif %}

[View all posts →](/writing/)

---

## Latest AI News

{% assign latest_news = site.ai_news | sort: 'date' | reverse | slice: 0, 1 %}
{% for news in latest_news %}
<div class="latest-news-highlight">
  <h2><a href="{{ news.url | relative_url }}">AI News Digest</a></h2>
  <div class="news-summary">{{ news.summary | strip_html | truncate: 200 }}</div>
  <div class="news-count">{{ news.stories | size }} stories • {{ news.date | date: "%B %d, %Y" }}</div>
</div>
{% endfor %}

[View all AI news →](/ai-news/)

---

## Connect

Feel free to reach out if you'd like to discuss AI research, collaborate on projects, or just chat about the latest developments in machine learning.

* [GitHub](https://github.com/gio99c) 
* [LinkedIn](https://linkedin.com/in/giuseppe-concialdi)
* [Email](mailto:giuseppe.concialdi@gmail.com)
