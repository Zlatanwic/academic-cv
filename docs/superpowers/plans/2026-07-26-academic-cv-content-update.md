# Academic CV Website Content Update Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace every public HugoBlox demonstration identity and content item with an accurate, privacy-safe academic research profile for Kuo Li.

**Architecture:** Keep HugoBlox as the rendering system and treat `data/authors/me.yaml` as the canonical structured profile. Use landing-page blocks for the homepage and Research Experience page, content bundles for three projects, and an explicit Publications empty state until official bibliography data exists. Add Python standard-library contract tests before each content change, then verify the generated site with Hugo 0.162.1.

**Tech Stack:** Hugo 0.162.1 Extended, HugoBlox Kit, YAML/Markdown, Python 3 `unittest`, pnpm 10.14.0, Pagefind

## Global Constraints

- Publish the Tongji University email address and GitHub profile only; do not publish a phone number.
- Do not publish GPA values.
- Do not copy `E:\大三下\cvv5-en.pdf` into the repository.
- Keep the CV menu item and download button absent until a sanitized PDF is provided.
- Remove the demonstration portrait and operate without a portrait.
- Do not invent dates, role titles, publication titles, author lists, links, DOI values, or abstracts.
- Omit ACM MM review scores and target-venue details for work under review or in preparation.
- Keep Publications as an honest empty state until complete official bibliographic metadata is available.
- Remove all HugoBlox demonstration publications, projects, posts, courses, talks, slides, assets, and CTA content.
- Preserve build/deploy workflows, HugoBlox modules, publication-import workflow, and upgrade workflow.
- Keep Hugo pinned to `0.162.1` in `hugoblox.yaml`.
- Do not add skill proficiency levels absent from the source CV.
- Use English for all public website copy.

---

## File Structure

### Create

- `tests/test_site_content.py` — source-content contracts for identity, navigation, homepage, experience, projects, publications, privacy, and demo cleanup.
- `tests/test_rendered_site.py` — integration checks against Hugo-generated HTML.
- `content/projects/semserve/index.md` — SemServe research project.
- `content/projects/skvm/index.md` — SkVM systems project.
- `content/projects/systems-projects/index.md` — consolidated systems projects.

### Modify

- `data/authors/me.yaml` — canonical identity, interests, education, skills, and honors.
- `config/_default/params.yaml` — site branding, SEO description, and public contact metadata.
- `config/_default/hugo.yaml` — site title and canonical GitHub Pages URL.
- `config/_default/menus.yaml` — Home, Publications, Research Experience, and Projects only.
- `content/_index.md` — public profile, research overview, selected projects, and Publications empty state.
- `content/experience.md` — undated research experience plus structured education, skills, and honors.
- `content/projects/_index.md` — research-project collection introduction.
- `content/publications/_index.md` — dedicated Publications empty state.

### Delete

- `assets/media/authors/me.png`
- `assets/media/slides-logo.svg`
- `static/uploads/resume.pdf`
- `content/blog/`
- `content/courses/`
- `content/events/`
- `content/slides/`
- `content/projects/pandas/`
- `content/projects/pytorch/`
- `content/projects/scikit/`
- `content/publications/conference-paper/`
- `content/publications/journal-article/`
- `content/publications/preprint/`
- `layouts/_partials/hooks/head-end/github-button.html`

---

### Task 1: Replace the public identity, branding, and navigation

**Files:**
- Create: `tests/test_site_content.py`
- Modify: `data/authors/me.yaml`
- Modify: `config/_default/params.yaml:13-28`
- Modify: `config/_default/params.yaml:128-149`
- Modify: `config/_default/hugo.yaml:5-8`
- Modify: `config/_default/menus.yaml`
- Delete: `assets/media/authors/me.png`
- Delete: `static/uploads/resume.pdf`

**Interfaces:**
- Consumes: Approved identity and privacy decisions from `docs/superpowers/specs/2026-07-26-cv-content-update-design.md`.
- Produces: Canonical author slug `me`, public site identity, and stable routes `/`, `/publications/`, `/experience/`, and `/projects/`.

- [ ] **Step 1: Write failing identity and navigation contract tests**

Create `tests/test_site_content.py`:

```python
from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read_text(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8")


def read_optional_text(relative_path: str) -> str:
    path = ROOT / relative_path
    return path.read_text(encoding="utf-8") if path.is_file() else ""


class SiteContentContractTests(unittest.TestCase):
    def test_profile_and_site_identity(self) -> None:
        profile = read_text("data/authors/me.yaml")
        params = read_text("config/_default/params.yaml")
        hugo = read_text("config/_default/hugo.yaml")

        for expected in (
            "display: Kuo Li",
            "given: Kuo",
            "family: Li",
            "B.Eng. Candidate in Data Science and Big Data Technology",
            "Department of Computer Science and Technology, Tongji University",
            "mailto:2353113@tongji.edu.cn",
            "https://github.com/Zlatanwic",
            "System optimization for LLM inference, training, and serving",
            "DL compilers, operator optimization, megakernel design, and high-performance operator generation",
            "Efficient AI, including sparse attention",
            "Agent-system infrastructure, including multi-agent orchestration and agent harnesses",
        ):
            self.assertIn(expected, profile)

        for forbidden in (
            "Alex Johnson",
            "Meta AI",
            "OpenAI",
            "Stanford University",
            "pronouns:",
            "postnominals:",
        ):
            self.assertNotIn(forbidden, profile)

        self.assertIn('name: "Kuo Li"', params)
        self.assertIn("Full-stack ML systems", params)
        self.assertNotIn("GoOwnable", params)
        self.assertIn("title: 'Kuo Li'", hugo)
        self.assertIn("baseURL: 'https://zlatanwic.github.io/academic-cv/'", hugo)
        self.assertFalse((ROOT / "assets/media/authors/me.png").exists())
        self.assertFalse((ROOT / "static/uploads/resume.pdf").exists())

    def test_navigation_has_only_approved_destinations(self) -> None:
        menu = read_text("config/_default/menus.yaml")
        expected_pairs = {
            "Home": "/",
            "Publications": "/publications/",
            "Research Experience": "/experience/",
            "Projects": "/projects/",
        }

        for name, url in expected_pairs.items():
            self.assertRegex(
                menu,
                rf"(?ms)- name: {re.escape(name)}\s+url: {re.escape(url)}\s+weight: \d+",
            )

        for forbidden in ("Talks", "News", "Courses", "Download CV", "resume.pdf"):
            self.assertNotIn(forbidden, menu)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the tests and confirm they fail for the template identity**

Run:

```bash
python -m unittest tests.test_site_content.SiteContentContractTests.test_profile_and_site_identity \
  tests.test_site_content.SiteContentContractTests.test_navigation_has_only_approved_destinations -v
```

Expected: both tests fail because the repository still contains Alex Johnson, the demo portrait/résumé, and demo navigation.

- [ ] **Step 3: Replace `data/authors/me.yaml` with the approved identity and interests**

Use this complete content:

```yaml
schema: hugoblox/author/v1
slug: me
is_owner: true
name:
  display: Kuo Li
  given: Kuo
  family: Li
role: B.Eng. Candidate in Data Science and Big Data Technology
bio: |
  Kuo Li is an undergraduate researcher at Tongji University working on
  full-stack machine learning systems. His research spans efficient LLM
  inference and serving, deep learning compilers and operator optimization,
  efficient AI, and infrastructure for agent systems.

affiliations:
  - name: Department of Computer Science and Technology, Tongji University

links:
  - icon: at-symbol
    url: mailto:2353113@tongji.edu.cn
    label: Email
  - icon: brands/github
    url: https://github.com/Zlatanwic
    label: GitHub

interests:
  - System optimization for LLM inference, training, and serving
  - DL compilers, operator optimization, megakernel design, and high-performance operator generation
  - Efficient AI, including sparse attention
  - Agent-system infrastructure, including multi-agent orchestration and agent harnesses
```

- [ ] **Step 4: Update site branding and SEO metadata**

In `config/_default/params.yaml`, replace the `identity` block with:

```yaml
  identity:
    name: "Kuo Li"
    organization: "Tongji University"
    type: person
    tagline: "Full-stack ML systems researcher"
    description: >-
      Academic profile of Kuo Li, an undergraduate researcher at Tongji
      University working on full-stack ML systems, efficient LLM inference,
      deep learning compilers, and agent infrastructure.
    social: {}
```

In the `seo.ai` block, set:

```yaml
      note: "Public academic profile and research project information."
      contact: "mailto:2353113@tongji.edu.cn"
```

Do not change unrelated theme, layout, analytics, or security settings.

- [ ] **Step 5: Set the site title and canonical URL**

In `config/_default/hugo.yaml`, replace the existing `title` and `baseURL` values with:

```yaml
title: 'Kuo Li'
baseURL: 'https://zlatanwic.github.io/academic-cv/'
```

- [ ] **Step 6: Replace navigation with approved routes**

Replace `config/_default/menus.yaml` with:

```yaml
main:
  - name: Home
    url: /
    weight: 10
  - name: Publications
    url: /publications/
    weight: 20
  - name: Research Experience
    url: /experience/
    weight: 30
  - name: Projects
    url: /projects/
    weight: 40
```

- [ ] **Step 7: Remove the demonstration portrait and résumé**

Run:

```bash
git rm -- assets/media/authors/me.png static/uploads/resume.pdf
```

Do not copy `E:\大三下\cvv5-en.pdf` into `static/uploads/`.

- [ ] **Step 8: Run the identity and navigation tests**

Run:

```bash
python -m unittest tests.test_site_content.SiteContentContractTests.test_profile_and_site_identity \
  tests.test_site_content.SiteContentContractTests.test_navigation_has_only_approved_destinations -v
```

Expected: `Ran 2 tests ... OK`.

- [ ] **Step 9: Commit the identity update**

```bash
git add tests/test_site_content.py data/authors/me.yaml \
  config/_default/params.yaml config/_default/hugo.yaml config/_default/menus.yaml
git commit -m "feat(profile): replace template identity with Kuo Li" \
  -m "Publish the approved academic identity and navigation while removing the demonstration portrait and résumé." \
  -m "Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

### Task 2: Build the research-oriented homepage

**Files:**
- Modify: `tests/test_site_content.py`
- Modify: `content/_index.md`

**Interfaces:**
- Consumes: Author slug `me` and routes created in Task 1.
- Produces: Homepage section IDs `projects` and `papers`, used by generated navigation and integration checks.

- [ ] **Step 1: Add a failing homepage contract test**

Insert this method into `SiteContentContractTests` before the `if __name__` block:

```python
    def test_homepage_is_research_focused_and_privacy_safe(self) -> None:
        homepage = read_text("content/_index.md")

        for expected in (
            "username: me",
            "Research Overview",
            "full-stack machine learning systems",
            "LLM inference, training, and serving",
            "deep learning compilers",
            "sparse attention",
            "agent-system infrastructure",
            "id: projects",
            "Selected Projects",
            "id: papers",
            "Publication details will be added as official bibliographic records become available.",
        ):
            self.assertIn(expected, homepage)

        for forbidden in (
            "Download CV",
            "resume.pdf",
            "DeepMind",
            "Featured Publications",
            "Recent Publications",
            "Recent & Upcoming Talks",
            "Recent News",
            "Build your own academic website",
            "demo: true",
        ):
            self.assertNotIn(forbidden, homepage)
```

- [ ] **Step 2: Run the homepage test and confirm it fails**

Run:

```bash
python -m unittest \
  tests.test_site_content.SiteContentContractTests.test_homepage_is_research_focused_and_privacy_safe -v
```

Expected: FAIL because the homepage still contains the demo CV button, DeepMind text, demo collections, and CTA.

- [ ] **Step 3: Replace `content/_index.md` with the approved homepage**

Use this complete content:

```yaml
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

        My current interests include system optimization for LLM inference,
        training, and serving; deep learning compilers, operator optimization,
        megakernel design, and high-performance operator generation; efficient
        AI techniques such as sparse attention; and agent-system infrastructure,
        including multi-agent orchestration and agent harnesses.
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
        Publication details will be added as official bibliographic records
        become available.
    design:
      columns: '1'
---
```

- [ ] **Step 4: Run the homepage contract test**

Run:

```bash
python -m unittest \
  tests.test_site_content.SiteContentContractTests.test_homepage_is_research_focused_and_privacy_safe -v
```

Expected: `Ran 1 test ... OK`.

- [ ] **Step 5: Commit the homepage**

```bash
git add tests/test_site_content.py content/_index.md
git commit -m "feat(home): present Kuo Li research profile" \
  -m "Replace demonstration collections and promotional content with a research overview, selected projects, and an honest Publications state." \
  -m "Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

### Task 3: Add education, research experience, skills, and honors

**Files:**
- Modify: `tests/test_site_content.py`
- Modify: `data/authors/me.yaml`
- Modify: `content/experience.md`

**Interfaces:**
- Consumes: Canonical profile and public disclosure policy from Task 1.
- Produces: Structured `education`, `skills`, and `awards` arrays consumed by the biography, skills, and awards blocks; undated research and education prose consumed by `markdown` blocks.

- [ ] **Step 1: Add a failing experience-page contract test**

Insert this method into `SiteContentContractTests`:

```python
    def test_experience_education_skills_and_honors_are_accurate(self) -> None:
        profile = read_text("data/authors/me.yaml")
        experience = read_text("content/experience.md")

        for expected in (
            "B.Eng. in Data Science and Big Data Technology",
            "Tongji University",
            "Department of Computer Science and Technology",
            "year: 2023–2027 (Expected)",
            "IELTS 7.0",
            "CET-6 571",
            "Programming Languages",
            "Rust",
            "Systems and Architecture",
            "AI Systems and Performance",
            "Engineering and Research Tools",
            "National First Prize",
            "International Silver Medal",
            'date: "December 2025"',
            'date: "October 2025"',
        ):
            self.assertIn(expected, profile)

        self.assertNotRegex(profile, r"(?m)^\s*(start|end|date_start|date_end):")
        self.assertNotRegex(profile, r"(?m)^\s*level:")
        self.assertNotRegex(profile, r"(?i)\bGPA\b")

        for expected in (
            "Image Fusion Laboratory, Tongji University",
            "Prof. Wei Tang",
            "Independent Research",
            "KV-cache management",
            "accepted for an oral presentation",
            "IPADS Laboratory, Shanghai Jiao Tong University",
            "Prof. Erhu Feng",
            "LANDS Laboratory, Nanjing University",
            "Prof. Chengying Huan",
            "RISC-V edge-inference",
            "manuscript is in preparation",
            "title: Education",
            "2023–2027 (Expected)",
            "title: Skills",
            "title: Honors",
        ):
            self.assertIn(expected, experience)

        for forbidden in ("ACM MM", "HPCA", "4/4/3/2/2", "Research Assistant"):
            self.assertNotIn(forbidden, experience)
```

- [ ] **Step 2: Run the test and confirm it fails**

Run:

```bash
python -m unittest \
  tests.test_site_content.SiteContentContractTests.test_experience_education_skills_and_honors_are_accurate -v
```

Expected: FAIL because no approved education, research experience, skills, or honors have been added.

- [ ] **Step 3: Append approved education, skills, and honors to `data/authors/me.yaml`**

Append exactly:

```yaml

education:
  - degree: B.Eng. in Data Science and Big Data Technology
    institution: Tongji University
    year: 2023–2027 (Expected)
    summary: |-
      Department of Computer Science and Technology

      English proficiency: IELTS 7.0; CET-6 571.

skills:
  - name: Programming Languages
    items:
      - label: Rust
      - label: C/C++
      - label: Python
      - label: Go
  - name: Systems and Architecture
    items:
      - label: Linux
      - label: Distributed systems
      - label: Concurrency
      - label: RISC-V
      - label: Process and memory management
      - label: Page-table mechanisms
      - label: System calls
      - label: ELF
      - label: File systems
  - name: AI Systems and Performance
    items:
      - label: CUDA C++
      - label: Operator optimization
      - label: PyTorch
      - label: Transformers
      - label: vLLM
      - label: KV Cache
      - label: Paged Attention
      - label: Nsight Compute
  - name: Engineering and Research Tools
    items:
      - label: Git
      - label: CMake
      - label: C++/CUDA extension development
      - label: Vite/Vue
      - label: Modern coding agents
      - label: AI-assisted problem solving

awards:
  - title: National First Prize
    awarder: Global Campus Artificial Intelligence Algorithm Competition, Algorithm Challenge Track
    date: "December 2025"
    summary: First-ranked team member.
    icon: hero/trophy
  - title: International Silver Medal
    awarder: International Genetically Engineered Machine Competition (iGEM)
    date: "October 2025"
    icon: hero/trophy
```

Do not add an `experience:` array because the approved design requires undated prose rather than a timeline.

- [ ] **Step 4: Replace `content/experience.md` with the approved page**

Use this complete content:

```yaml
---
title: Research Experience
type: landing

sections:
  - block: markdown
    content:
      title: Research Experience
      text: |-
        ### Image Fusion Laboratory, Tongji University
        **Advised by Prof. Wei Tang**

        Contributed to image-processing research and prepared a first-author
        manuscript. Details that could identify work under anonymous review are
        intentionally omitted.

        ### Independent Research

        Developed solo-authored research on KV-cache management. The work has
        been accepted for an oral presentation and is being extended through
        faculty collaboration.

        ### IPADS Laboratory, Shanghai Jiao Tong University
        **Advised by Prof. Erhu Feng**

        Extended and optimized SkVM, a compilation and runtime system for
        heterogeneous LLM and agent harnesses. This work contributes to a
        broader system associated with a paper accepted to SOSP 2026.

        ### LANDS Laboratory, Nanjing University
        **Advised by Prof. Chengying Huan**

        Optimized a RISC-V edge-inference pipeline based on MNN. A manuscript
        describing this work is in preparation.
    design:
      columns: '1'

  - block: markdown
    content:
      title: Education
      text: |-
        **B.Eng. in Data Science and Big Data Technology**  
        Tongji University, Department of Computer Science and Technology  
        2023–2027 (Expected)  
        English proficiency: IELTS 7.0; CET-6 571.
    design:
      columns: '1'

  - block: resume-skills
    content:
      title: Skills
      username: me

  - block: resume-awards
    content:
      title: Honors
      username: me
    design:
      date_format: 'January 2006'
---
```

The profile retains `education` so the homepage biography can show it using the exact free-form `year`. The Research Experience page uses a Markdown Education block instead of `resume-experience`, preventing the block from parsing a non-date graduation label or rendering an undated record as “Present.” The undated research entries come from the first Markdown block. Month-only honors use raw `Month YYYY` strings, which the awards block safely displays unchanged when Hugo does not parse them as complete dates.

- [ ] **Step 5: Run the experience contract test**

Run:

```bash
python -m unittest \
  tests.test_site_content.SiteContentContractTests.test_experience_education_skills_and_honors_are_accurate -v
```

Expected: `Ran 1 test ... OK`.

- [ ] **Step 6: Commit the experience page and structured credentials**

```bash
git add tests/test_site_content.py data/authors/me.yaml content/experience.md
git commit -m "feat(experience): add research background and skills" \
  -m "Present verified undated research experience with structured education, skill categories, and honors while omitting private and speculative details." \
  -m "Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

### Task 4: Replace demonstration projects with real research projects

**Files:**
- Modify: `tests/test_site_content.py`
- Modify: `content/projects/_index.md`
- Create: `content/projects/semserve/index.md`
- Create: `content/projects/skvm/index.md`
- Create: `content/projects/systems-projects/index.md`

**Interfaces:**
- Consumes: Homepage `projects` collection from Task 2.
- Produces: Three content bundles discovered automatically under the `projects` section.

- [ ] **Step 1: Add a failing project-content contract test**

Insert this method into `SiteContentContractTests`:

```python
    def test_projects_match_approved_public_descriptions(self) -> None:
        index = read_text("content/projects/_index.md")
        semserve = read_optional_text("content/projects/semserve/index.md")
        skvm = read_optional_text("content/projects/skvm/index.md")
        systems = read_optional_text("content/projects/systems-projects/index.md")

        self.assertIn("Research and Systems Projects", index)
        self.assertNotIn("I enjoy making things", index)

        for expected in (
            "SemServe: Co-designing Semantic Priority and KV-Cache Storage Precision",
            "automatic semantic scoring",
            "offline search and online computation",
            "MLFQ",
            "FP16",
            "INT8",
            "CPU memory",
            "Qwen2.5-3B",
            "Llama-3.2-3B",
            "Manuscript in preparation",
        ):
            self.assertIn(expected, semserve)
        for forbidden in ("CCF-A", "ACM MM", "review score"):
            self.assertNotIn(forbidden, semserve)

        for expected in (
            "SkVM: A Skill Compilation and Runtime System for Heterogeneous LLM and Agent Harnesses",
            "pi, claude-code, opencode, and hermes",
            "DLP, ILP, and TLP",
            "AOT compiler",
            "parallel dispatch",
            "JIT optimization",
            "SOSP 2026",
        ):
            self.assertIn(expected, skvm)

        for expected in (
            "Rust-based operating-system kernel",
            "MCP server",
            "Paged Attention",
            "Chord",
            "Mini-GFS",
            "Go",
        ):
            self.assertIn(expected, systems)
```

- [ ] **Step 2: Run the project test and confirm missing-bundle failure**

Run:

```bash
python -m unittest \
  tests.test_site_content.SiteContentContractTests.test_projects_match_approved_public_descriptions -v
```

Expected: FAIL with an assertion that the first required SemServe phrase is missing. The optional reader keeps the RED phase focused on missing content rather than a file-open error.

- [ ] **Step 3: Replace `content/projects/_index.md`**

Use:

```yaml
---
title: Projects
type: landing

sections:
  - block: collection
    content:
      title: Research and Systems Projects
      text: >-
        Selected work on efficient machine learning systems, compilation and
        runtime infrastructure, and systems engineering.
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
---
```

- [ ] **Step 4: Create the SemServe bundle**

Create `content/projects/semserve/index.md`:

```markdown
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

- Designed an automatic semantic scoring method that combines offline search
  and online computation to fit scoring under SLO-oriented objectives.
- Mapped semantic priorities directly to MLFQ scheduling.
- Assigned FP16 KV cache to the highest-priority queue, INT8 to the
  second-priority queue, and CPU memory offload to the third-priority queue.
```

- [ ] **Step 5: Create the SkVM bundle**

Create `content/projects/skvm/index.md`:

```markdown
---
title: "SkVM: A Skill Compilation and Runtime System for Heterogeneous LLM and Agent Harnesses"
summary: Compilation and runtime techniques for portable, parallel agent-harness execution.
tags:
  - LLM Agents
  - TypeScript
  - Bun
  - Docker
  - Compilers
---

SkVM is an SJTU-IPADS project exploring compilation and runtime support for
heterogeneous LLM and agent harnesses. The broader system is associated with
work accepted to SOSP 2026; this page describes my implementation
contributions rather than asserting a publication authorship record.

- Implemented containerized execution modes for four agent adapters: pi,
  claude-code, opencode, and hermes.
- Introduced three levels of parallelism—DLP, ILP, and TLP—into pass 3 of the
  AOT compiler and enabled parallel dispatch for ILP tool calls.
- Added multi-role agent optimization to the JIT optimization stage and
  compared it with multi-turn agent optimization.
```

- [ ] **Step 6: Create the consolidated systems-project bundle**

Create `content/projects/systems-projects/index.md`:

```markdown
---
title: Systems Projects
summary: Selected operating-systems, distributed-systems, and AI-systems implementations.
tags:
  - Rust
  - Go
  - Distributed Systems
  - Operating Systems
  - AI Systems
---

A selection of systems projects developed across coursework and independent
engineering work:

- A Rust-based operating-system kernel covering core process, memory, and
  file-system mechanisms.
- An MCP server for structured tool and resource access.
- Operator-fusion optimization for Paged Attention workloads.
- A distributed hash ring based on the Chord algorithm.
- A Mini-GFS implementation in Go.
```

- [ ] **Step 7: Run the project contract test**

Run:

```bash
python -m unittest \
  tests.test_site_content.SiteContentContractTests.test_projects_match_approved_public_descriptions -v
```

Expected: `Ran 1 test ... OK`.

- [ ] **Step 8: Commit the real project content**

```bash
git add tests/test_site_content.py content/projects/_index.md \
  content/projects/semserve/index.md content/projects/skvm/index.md \
  content/projects/systems-projects/index.md
git commit -m "feat(projects): add ML systems research projects" \
  -m "Document SemServe, SkVM, and selected systems implementations using the approved public-safe descriptions." \
  -m "Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

### Task 5: Replace fake publications with an explicit empty state

**Files:**
- Modify: `tests/test_site_content.py`
- Modify: `content/publications/_index.md`

**Interfaces:**
- Consumes: `/publications/` navigation route from Task 1 and empty-state wording from Task 2.
- Produces: A renderable Publications landing page with no fabricated publication bundles.

- [ ] **Step 1: Add a failing Publications contract test**

Insert this method into `SiteContentContractTests`:

```python
    def test_publications_page_is_an_honest_empty_state(self) -> None:
        publications_dir = ROOT / "content/publications"
        index = read_text("content/publications/_index.md")
        child_bundles = sorted(path.name for path in publications_dir.iterdir() if path.is_dir())

        self.assertIn("title: Publications", index)
        self.assertEqual([], child_bundles)
        self.assertIn(
            "Publication details will be added as official bibliographic records become available.",
            index,
        )
```

- [ ] **Step 2: Run the Publications test and confirm it fails**

Run:

```bash
python -m unittest \
  tests.test_site_content.SiteContentContractTests.test_publications_page_is_an_honest_empty_state -v
```

Expected: FAIL because `child_bundles` contains `conference-paper`, `journal-article`, and `preprint`. This proves the test detects fabricated publication records before checking the new empty-state wording.

- [ ] **Step 3: Replace `content/publications/_index.md`**

Use:

```yaml
---
title: Publications
type: landing
cms_exclude: true

sections:
  - block: markdown
    content:
      title: Publications
      text: >-
        Publication details will be added as official bibliographic records
        become available.
    design:
      columns: '1'
---
```

Do not create individual paper pages.

- [ ] **Step 4: Remove fake publication bundles**

Run:

```bash
git rm -r -- \
  content/publications/conference-paper \
  content/publications/journal-article \
  content/publications/preprint
```

This removes their fabricated metadata, PDFs, BibTeX files, and images together.

- [ ] **Step 5: Run the Publications contract test**

Run:

```bash
python -m unittest \
  tests.test_site_content.SiteContentContractTests.test_publications_page_is_an_honest_empty_state -v
```

Expected: `Ran 1 test ... OK`.

- [ ] **Step 6: Commit the Publications empty state**

```bash
git add tests/test_site_content.py content/publications/_index.md
git add -u content/publications
git commit -m "feat(publications): add verified empty state" \
  -m "Remove fabricated publication records and retain the Publications route until official bibliographic metadata is available." \
  -m "Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

### Task 6: Remove all remaining demonstration content and enforce privacy

**Files:**
- Modify: `tests/test_site_content.py`
- Delete: `assets/media/slides-logo.svg`
- Delete: `content/blog/`
- Delete: `content/courses/`
- Delete: `content/events/`
- Delete: `content/slides/`
- Delete: `content/projects/pandas/`
- Delete: `content/projects/pytorch/`
- Delete: `content/projects/scikit/`
- Delete: `layouts/_partials/hooks/head-end/github-button.html`

**Interfaces:**
- Consumes: Real pages created in Tasks 1–5.
- Produces: A published-content tree containing no demo identity, fake authored work, private phone number, GPA, or stale routes.

- [ ] **Step 1: Add failing cleanup and privacy tests**

Insert these helpers below `read_text`:

```python
PUBLISHED_ROOTS = (
    "content",
    "data/authors",
    "config/_default",
    "layouts",
    "static",
)
TEXT_SUFFIXES = {".html", ".md", ".txt", ".yaml", ".yml"}


def published_text() -> str:
    chunks: list[str] = []
    for relative_root in PUBLISHED_ROOTS:
        root = ROOT / relative_root
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if path.is_file() and path.suffix.lower() in TEXT_SUFFIXES:
                chunks.append(path.read_text(encoding="utf-8"))
    return "\n".join(chunks)
```

Insert these methods into `SiteContentContractTests`:

```python
    def test_demonstration_content_is_removed(self) -> None:
        removed_paths = (
            "content/blog",
            "content/courses",
            "content/events",
            "content/slides",
            "content/projects/pandas",
            "content/projects/pytorch",
            "content/projects/scikit",
            "assets/media/slides-logo.svg",
            "layouts/_partials/hooks/head-end/github-button.html",
            "static/uploads/resume.pdf",
        )
        for relative_path in removed_paths:
            self.assertFalse((ROOT / relative_path).exists(), relative_path)

        text = published_text()
        for forbidden in (
            "Alex Johnson",
            "Meta AI",
            "OpenAI",
            "Stanford University",
            "Lorem ipsum",
            "Build your own academic website",
            "alex.johnson@example.com",
        ):
            self.assertNotIn(forbidden, text)

    def test_sensitive_and_anonymous_review_data_is_not_published(self) -> None:
        text = published_text()

        self.assertNotRegex(text, r"(?i)\bGPA\b")
        self.assertNotRegex(text, r"(?<!\d)1\d{10}(?!\d)")
        self.assertNotIn("4/4/3/2/2", text)
        self.assertNotIn("pre-rebuttal review", text.lower())
        self.assertNotIn("targeting HPCA", text)
        self.assertFalse((ROOT / "static/uploads/resume.pdf").exists())
```

- [ ] **Step 2: Run the cleanup tests and confirm they fail**

Run:

```bash
python -m unittest \
  tests.test_site_content.SiteContentContractTests.test_demonstration_content_is_removed \
  tests.test_site_content.SiteContentContractTests.test_sensitive_and_anonymous_review_data_is_not_published -v
```

Expected: the demo-removal test fails because blog, course, event, slide, demo projects, and the GitHub CTA hook still exist.

- [ ] **Step 3: Remove remaining demonstration sections and assets**

Run:

```bash
git rm -r -- \
  content/blog \
  content/courses \
  content/events \
  content/slides \
  content/projects/pandas \
  content/projects/pytorch \
  content/projects/scikit
git rm -- \
  assets/media/slides-logo.svg \
  layouts/_partials/hooks/head-end/github-button.html
```

Do not remove `.github/workflows/build.yml`, `.github/workflows/deploy.yml`, `.github/workflows/import-publications.yml`, or `.github/workflows/upgrade.yml`.

- [ ] **Step 4: Run all source-content contract tests**

Run:

```bash
python -m unittest tests.test_site_content -v
```

Expected: all source-content tests pass with `OK`.

- [ ] **Step 5: Run a direct stale-reference search**

Run:

```bash
rg -n -i \
  'Alex Johnson|Meta AI|OpenAI|Stanford University|Lorem ipsum|resume\.pdf|/#talks|/#news|courses/' \
  content data/authors config/_default layouts static || true
```

Expected: no output. Review any match manually before proceeding; do not remove operational files based solely on a broad text match.

- [ ] **Step 6: Commit the demo cleanup**

```bash
git add tests/test_site_content.py
git add -u content assets/media layouts static
git commit -m "chore(content): remove HugoBlox demonstration material" \
  -m "Delete fake authored content, tutorial sections, demo projects, and promotional assets so only verified profile material remains public." \
  -m "Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

### Task 7: Verify the generated production site

**Files:**
- Create: `tests/test_rendered_site.py`
- Verify: `hugoblox.yaml`
- Verify: `.github/workflows/build.yml`
- Temporary only: `temp/hugo/`
- Generated only: `public/`, `resources/`

**Interfaces:**
- Consumes: Complete source-content tree from Tasks 1–6 and Hugo version `0.162.1`.
- Produces: Fresh evidence that the home, experience, project, and Publications routes render correctly without private or demo content.

- [ ] **Step 1: Write the rendered-site integration test**

Create `tests/test_rendered_site.py`:

```python
from __future__ import annotations

import html
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"


def rendered_text(relative_path: str) -> str:
    source = (PUBLIC / relative_path).read_text(encoding="utf-8")
    without_markup = re.sub(r"<[^>]+>", " ", source)
    return " ".join(html.unescape(without_markup).split())


class RenderedSiteTests(unittest.TestCase):
    def test_expected_routes_and_content_render(self) -> None:
        expected = {
            "index.html": ("Kuo Li", "Research Overview", "Selected Projects"),
            "experience/index.html": (
                "Image Fusion Laboratory, Tongji University",
                "IPADS Laboratory, Shanghai Jiao Tong University",
                "Programming Languages",
                "National First Prize",
            ),
            "projects/semserve/index.html": ("SemServe", "MLFQ", "FP16", "INT8"),
            "projects/skvm/index.html": ("SkVM", "DLP, ILP, and TLP", "SOSP 2026"),
            "projects/systems-projects/index.html": ("Rust-based operating-system kernel", "Mini-GFS"),
            "publications/index.html": (
                "Publication details will be added as official bibliographic records become available.",
            ),
        }

        for relative_path, phrases in expected.items():
            path = PUBLIC / relative_path
            self.assertTrue(path.is_file(), relative_path)
            text = rendered_text(relative_path)
            for phrase in phrases:
                self.assertIn(phrase, text, f"{phrase!r} missing from {relative_path}")

    def test_rendered_site_contains_no_private_or_demo_content(self) -> None:
        html_text = "\n".join(
            path.read_text(encoding="utf-8")
            for path in PUBLIC.rglob("*.html")
        )

        self.assertNotRegex(html_text, r"(?i)\bGPA\b")
        self.assertNotRegex(html_text, r"(?<!\d)1\d{10}(?!\d)")
        for forbidden in (
            "Alex Johnson",
            "Meta AI",
            "OpenAI",
            "Stanford University",
            "Lorem ipsum",
            "4/4/3/2/2",
            "Download CV",
        ):
            self.assertNotIn(forbidden, html_text)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Clean generated output and confirm the integration test fails before building**

Run:

```bash
python -c "import shutil; shutil.rmtree('public', ignore_errors=True)"
python -m unittest tests.test_rendered_site -v
```

Expected: ERROR because `public/index.html` and other generated pages do not exist. This confirms the integration test depends on a fresh build.

- [ ] **Step 3: Verify the pinned Hugo version and workflow propagation**

Run:

```bash
python - <<'PY'
from pathlib import Path

config = Path('hugoblox.yaml').read_text(encoding='utf-8')
workflow = Path('.github/workflows/build.yml').read_text(encoding='utf-8')
assert "hugo_version: '0.162.1'" in config
assert "yq '.build.hugo_version // \"\"' hugoblox.yaml" in workflow
assert 'hugo-version: ${{ env.HUGO_VERSION }}' in workflow
print('PASS: workflow installs Hugo 0.162.1 from hugoblox.yaml')
PY
```

Expected: `PASS: workflow installs Hugo 0.162.1 from hugoblox.yaml`.

- [ ] **Step 4: Install Node dependencies reproducibly**

Run:

```bash
pnpm install --frozen-lockfile
```

Expected: exit code 0 with the existing `pnpm-lock.yaml` unchanged.

- [ ] **Step 5: Download the exact Hugo Extended release into the temporary workspace**

Run from Git Bash on Windows:

```bash
python - <<'PY'
from pathlib import Path
import shutil

shutil.rmtree('temp/hugo', ignore_errors=True)
Path('temp/hugo').mkdir(parents=True, exist_ok=True)
PY
gh release download v0.162.1 \
  --repo gohugoio/hugo \
  --pattern 'hugo_extended_0.162.1_windows-amd64.zip' \
  --dir temp/hugo \
  --clobber
python -m zipfile -e \
  temp/hugo/hugo_extended_0.162.1_windows-amd64.zip \
  temp/hugo
./temp/hugo/hugo.exe version
```

Expected: version output begins with `hugo v0.162.1` and includes `extended windows/amd64`.

- [ ] **Step 6: Run the production Hugo and Pagefind builds**

Run:

```bash
./temp/hugo/hugo.exe --minify \
  --baseURL 'https://zlatanwic.github.io/academic-cv/'
pnpm run pagefind
```

Expected: both commands exit 0; Hugo writes `public/`, and Pagefind reports indexing the generated site.

- [ ] **Step 7: Run rendered-site and source-content verification**

Run:

```bash
python -m unittest tests.test_site_content tests.test_rendered_site -v
```

Expected: all tests pass with `OK`.

- [ ] **Step 8: Inspect the complete diff and repository hygiene**

Run:

```bash
git diff --check
git status --short
git diff --stat HEAD~6..HEAD
git diff HEAD~6..HEAD -- \
  data/authors/me.yaml \
  config/_default \
  content \
  layouts \
  tests
```

Expected:

- `git diff --check` exits 0.
- No tracked `public/`, `resources/`, `node_modules/`, or `temp/hugo/` files appear.
- No unrelated workflow or dependency changes appear.

- [ ] **Step 9: Remove disposable local build artifacts**

Run:

```bash
python - <<'PY'
import shutil

for path in ('public', 'resources', 'temp/hugo'):
    shutil.rmtree(path, ignore_errors=True)
PY
```

Keep the `temp/` directory only if it contains another durable artifact; otherwise remove the now-empty directory.

- [ ] **Step 10: Commit integration verification**

```bash
git add tests/test_rendered_site.py
git commit -m "test(site): verify rendered academic profile" \
  -m "Check all public routes and reject private, fabricated, or demonstration content in generated HTML." \
  -m "Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

- [ ] **Step 11: Run final verification after the last commit**

Run:

```bash
python -m unittest tests.test_site_content -v
git diff --check
git status --short
git log -7 --oneline
```

Expected:

- All source-content tests pass.
- `git diff --check` exits 0.
- The working tree is clean.
- The log shows the focused identity, homepage, experience, projects, Publications, cleanup, and rendered-site verification commits.

---

## Final Review Checklist

- [ ] The site identifies Kuo Li and no longer attributes template work to him.
- [ ] Phone number, GPA, review scores, and the unsanitized PDF are absent from published sources and rendered HTML.
- [ ] Email and GitHub are the only public contact links.
- [ ] No CV button or menu entry is present.
- [ ] Homepage includes the approved research overview, project collection, and Publications empty state.
- [ ] Research Experience has four undated entries and no invented role title.
- [ ] Education includes Tongji University, degree, expected years, IELTS, and CET-6 only.
- [ ] Skills contain no fabricated numeric levels.
- [ ] Honors use month precision without fabricated days.
- [ ] SemServe omits review scores and target venues.
- [ ] SkVM distinguishes project contribution from publication authorship.
- [ ] Publications contains no fake bundles.
- [ ] Blog, course, event, slides, demo projects, portrait, résumé, and CTA hook are removed.
- [ ] Hugo 0.162.1 production build and Pagefind indexing succeed.
- [ ] All Python contract and rendered-site tests pass.
- [ ] No unrelated workflows or dependencies are modified.
