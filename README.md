# Giuseppe Concialdi - Personal Website

[![Build Status](https://github.com/gio99c/gio99c.github.io/actions/workflows/jekyll.yml/badge.svg)](https://github.com/gio99c/gio99c.github.io/actions/workflows/jekyll.yml)

This is the source code for my personal website and blog, built with Jekyll and hosted on GitHub Pages.

## Features

- Clean, minimal design focused on content
- Responsive layout that works on all devices
- Blog with syntax highlighting for code snippets
- Dark/light mode based on system preferences
- Fast loading and optimized for performance

## Local Development

### Prerequisites

- Ruby 2.5.0 or higher
- RubyGems
- GCC and Make
- Jekyll (see installation instructions below)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/gio99c/gio99c.github.io.git
   cd gio99c.github.io
   ```

2. Install Jekyll and bundler gems:
   ```bash
   gem install jekyll bundler
   ```

3. Install dependencies:
   ```bash
   bundle install
   ```

### Running Locally

1. Start the Jekyll server:
   ```bash
   bundle exec jekyll serve
   ```

2. Open your browser to `http://localhost:4000`

## Adding New Content

### Blog Posts

Create a new markdown file in the `_posts` directory with the following naming convention:

```
_posts/YYYY-MM-DD-title-of-post.md
```

Each post should start with front matter like this:

```yaml
---
layout: post
title: "Your Post Title"
date: YYYY-MM-DD HH:MM:SS +0000
categories: [category1, category2]
tags: [tag1, tag2, tag3]
---
```

### Pages

Create a new markdown file in the root directory with front matter like this:

```yaml
---
layout: page
title: "Page Title"
permalink: /page-url/
---
```

## Customization

### Theme Colors

Edit the color variables in `_sass/minima/_custom-styles.scss` to change the color scheme.

### Layouts

Customize layouts in the `_layouts` directory.

## Deployment

This site is automatically deployed to GitHub Pages when changes are pushed to the `main` branch.

## License

This project is open source and available under the [MIT License](LICENSE).

## Acknowledgements

- [Jekyll](https://jekyllrb.com/)
- [Minima](https://github.com/jekyll/minima)
- [Font Awesome](https://fontawesome.com/)
# gio99c.github.io
