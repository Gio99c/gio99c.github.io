---
layout: page
title: Writing
permalink: /writing/
---

# Writing

I write about Large Language Models, Generative AI, and the practical challenges of building production ML systems. Here you'll find deep dives into model architectures, training techniques, and lessons learned from deploying AI at scale.

---

{% if site.posts.size > 0 %}
<div class="post-list">
  {% for post in site.posts %}
  <div class="post-list-item">
    <h2 class="post-title">
      <a href="{{ post.url | relative_url }}">{{ post.title }}</a>
    </h2>
    <div class="post-date">{{ post.date | date: "%B %d, %Y" }}</div>
    {% if post.excerpt %}
    <div class="post-excerpt">{{ post.excerpt | strip_html | truncate: 200 }}</div>
    {% endif %}
  </div>
  {% endfor %}
</div>
{% else %}
<div style="text-align: center; padding: 3rem 0; color: #737373;">
  <p><em>Coming soon - I'm working on some articles about transformers, LLM training, and generative AI applications.</em></p>
  
  <p style="margin-top: 2rem; font-size: 0.9rem;">
    In the meantime, feel free to <a href="/about/">learn more about me</a> or <a href="mailto:giuseppe.concialdi@example.com">get in touch</a>.
  </p>
</div>
{% endif %} 