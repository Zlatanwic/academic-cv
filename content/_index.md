---
title: ''
summary: >-
  Kuo Li is an undergraduate researcher at Tongji University working on
  full-stack machine learning systems.
type: landing

sections:
  - block: resume-biography-3
    content:
      username: me
      text: ''
      headings:
        about: Research Profile
        education: Education
        interests: Research Interests
    design:
      background:
        gradient_mesh:
          enable: true
      name:
        size: md
      avatar:
        size: medium
        shape: circle

  - block: markdown
    content:
      title: Research Overview
      subtitle: Full-stack machine learning systems
      text: |-
        I work on full-stack machine learning systems, from efficient model
        execution and deep learning compiler techniques to the infrastructure
        needed by modern agent systems.

        My current interests include system optimization for LLM inference, training, and serving;
        deep learning compilers, operator optimization, megakernel design, and
        high-performance operator generation; efficient AI techniques such as
        sparse attention; and agent-system infrastructure, including multi-agent
        orchestration and agent harnesses.
    design:
      columns: '1'

  - block: collection
    id: projects
    content:
      title: Selected Projects
      text: Research and systems projects in efficient AI and agent infrastructure.
      filters:
        folders:
          - projects
    design:
      view: article-grid
      fill_image: false
      columns: 3
      show_date: false
      show_read_time: false
      show_read_more: true

  - block: markdown
    id: papers
    content:
      title: Publications
      text: >-
        Publication details will be added as official bibliographic records become available.
    design:
      columns: '1'
---
