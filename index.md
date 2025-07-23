---
layout: default
---

# Hi, I'm Giuseppe Concialdi

I'm a Machine Learning Engineer specializing in Large Language Models and Generative AI. I build systems that understand and generate natural language at scale. 

Currently, I focus on:
* **LLM Architecture & Training** - Designing and optimizing transformer-based models
* **Generative AI Applications** - Building practical AI systems for real-world problems  
* **MLOps & Infrastructure** - Scaling ML systems for production environments

Outside of work, I write about cutting-edge developments in AI, share insights from building with LLMs, and explore the latest research in generative models.

---

## Latest Writing

{% assign recent_posts = site.posts | slice: 0, 5 %}
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

## Connect

Feel free to reach out if you'd like to discuss AI research, collaborate on projects, or just chat about the latest developments in machine learning.

* [GitHub](https://github.com/gio99c) 
* [LinkedIn](https://linkedin.com/in/giuseppe-concialdi)
* [Email](mailto:giuseppe.concialdi@example.com)
