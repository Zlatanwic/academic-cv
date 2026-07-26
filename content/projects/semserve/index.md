---
title: "SemServe: Co-designing Semantic Priority and KV-Cache Storage Precision"
summary: Semantic-priority scheduling and adaptive KV-cache storage for efficient LLM serving.
tags:
  - LLM Serving
  - KV Cache
  - Python
  - PyTorch
  - Transformers
  - Qwen2.5-3B
  - Llama-3.2-3B
---

**Status:** Manuscript in preparation

SemServe extends earlier research on KV-cache management by jointly optimizing
semantic priority and cache-storage precision for LLM serving.

- Designed an automatic semantic scoring method that combines offline search and online computation
  to fit scoring under SLO-oriented objectives.
- Mapped semantic priorities directly to MLFQ scheduling.
- Assigned FP16 KV cache to the highest-priority queue, INT8 to the
  second-priority queue, and CPU memory offload to the third-priority queue.
