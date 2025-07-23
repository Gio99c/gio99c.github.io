---
layout: post
title:  "Understanding Transformer Architectures"
date:   2025-07-23 10:00:00 -0400
categories: blog
---

## The Core Idea

The Transformer architecture, introduced in the paper "Attention Is All You Need," revolutionized how we approach sequence-to-sequence tasks in NLP. Unlike RNNs or LSTMs, it processes tokens in parallel, relying entirely on self-attention mechanisms to capture dependencies.

```python
import torch
import torch.nn as nn

class SelfAttention(nn.Module):
    def __init__(self, embed_size, heads):
        super(SelfAttention, self).__init__()
        self.embed_size = embed_size
        self.heads = heads
        self.head_dim = embed_size // heads

        assert (
            self.head_dim * heads == embed_size
        ), "Embedding size needs to be divisible by heads"

        self.values = nn.Linear(self.head_dim, self.head_dim, bias=False)
        self.keys = nn.Linear(self.head_dim, self.head_dim, bias=False)
        self.queries = nn.Linear(self.head_dim, self.head_dim, bias=False)
        self.fc_out = nn.Linear(heads * self.head_dim, embed_size)
```

This parallelization allows for significantly faster training on large datasets, paving the way for models like BERT and GPT.
