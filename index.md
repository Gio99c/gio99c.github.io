---
layout: home
---

# Giuseppe Concialdi

## Machine Learning Engineer

Welcome to my personal space on the web. I'm a Machine Learning Engineer with a passion for Large Language Models (LLMs) and generative models. Here, I share my thoughts, projects, and articles on the latest advancements in AI.

[About Me]({{ "/about.html" | relative_url }}) - [Blog]({{ "/blog.html" | relative_url }})

---

### Recent Posts

{% for post in site.posts limit:5 %}
- [{{ post.title }}]({{ post.url | relative_url }}) - {{ post.date | date: "%B %d, %Y" }}
{% endfor %}
