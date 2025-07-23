---
layout: home
---

<div class="home">
  <div class="home-intro">
    <h1>Hi, I'm Giuseppe Concialdi</h1>
    <p class="subtitle">Machine Learning Engineer focused on LLMs and Generative AI</p>
    
    <div class="home-about">
      <p>I'm passionate about building intelligent systems that can understand and generate human-like text. My work focuses on large language models, generative AI, and their practical applications.</p>
      
      <p>Currently, I'm exploring ways to make LLMs more efficient, controllable, and aligned with human values.</p>
      
      <div class="home-links">
        <a href="/about" class="btn">More about me</a>
        <a href="/blog" class="btn btn-outline">Read my blog</a>
      </div>
    </div>
  </div>

  <div class="recent-posts">
    <h2>Latest Articles</h2>
    
    <div class="post-list">
      {% assign recent_posts = site.posts | slice: 0, 3 %}
      {% for post in recent_posts %}
        <div class="post-preview">
          <h3>
            <a href="{{ post.url | relative_url }}">{{ post.title | escape }}</a>
          </h3>
          <div class="post-meta">
            <time datetime="{{ post.date | date_to_xmlschema }}" itemprop="datePublished">
              {{ post.date | date: "%b %-d, %Y" }}
            </time>
            {% if post.read_time %}
              • {% include read-time.html item=post %}
            {% endif %}
          </div>
          {% if post.excerpt %}
            <div class="post-excerpt">
              {{ post.excerpt | strip_html | truncatewords: 30 }}
            </div>
          {% endif %}
          <a href="{{ post.url | relative_url }}" class="read-more">Read more →</a>
        </div>
      {% else %}
        <p>No posts yet. Check back soon for updates!</p>
      {% endfor %}
    </div>
    
    <div class="view-all">
      <a href="{{ "/blog" | relative_url }}" class="btn">View all articles</a>
    </div>
  </div>
</div>
