# Academic CV Content Update Design

**Date:** 2026-07-26
**Source:** `E:\大三下\cvv5-en.pdf`
**Target:** HugoBlox Academic CV site in `D:\academic-cv`

## 1. Goal

Replace the HugoBlox demonstration content with an accurate, research-oriented academic profile for Kuo Li. The website will support academic research applications and faculty outreach while avoiding fabricated metadata, accidental attribution of template content, and disclosure of sensitive or double-blind research information.

## 2. Confirmed Decisions

- Use a structured academic profile rather than mirroring the PDF section by section.
- Target an academic research audience.
- Publish the Tongji University email address and GitHub profile on the website.
- Do not publish the phone number.
- Do not publish GPA values.
- Do not copy the current source PDF into the repository because it contains the phone number and GPA.
- Hide the CV navigation item and download button until a sanitized PDF is provided.
- Remove all HugoBlox demonstration content rather than merely hiding it.
- Do not use the demonstration portrait. The site will operate without a portrait until an authorized image is provided.
- Present research experiences without dates or invented role titles because the source PDF does not contain those facts.
- Handle unpublished research conservatively: omit review scores, target venues, and information that may undermine anonymous review.
- Keep a Publications page and navigation entry with an honest empty state until complete official bibliographic metadata is available.

## 3. Information Architecture

### 3.1 Navigation

The initial navigation will be:

```text
Home · Publications · Research Experience · Projects
```

A CV item will be added only after a sanitized public PDF is supplied.

Remove Talks, News, and Courses navigation items and any navigation links targeting deleted demonstration content.

### 3.2 Home

The homepage will contain the following sections.

#### Profile

- Name: Kuo Li
- Role: B.Eng. Candidate in Data Science and Big Data Technology
- Affiliation: Department of Computer Science and Technology, Tongji University
- Public links:
  - `2353113@tongji.edu.cn`
  - `https://github.com/Zlatanwic`
- No phone number
- No GPA
- No portrait until one is supplied
- No CV button until a sanitized PDF is supplied

#### Research Overview

Introduce Kuo Li as an undergraduate researcher focused on full-stack ML systems. Present these research interests:

1. System optimization for LLM inference, training, and serving
2. DL compilers, operator optimization, megakernel design, and high-performance operator generation
3. Efficient AI techniques, including sparse attention
4. Agent-system infrastructure, including multi-agent orchestration and agent harnesses

The prose should be concise and should not repeat complete project or experience descriptions.

#### Selected Projects

Show cards or links for:

- SemServe
- SkVM
- Systems Projects

#### Publications

Retain a Publications section and dedicated page. Until official records are available, show a concise empty state such as:

> Publication details will be added as official bibliographic records become available.

Do not create incomplete publication bundles or infer titles, authors, dates, DOI values, abstracts, or links.

### 3.3 Research Experience

Use a dedicated page with ordinary Markdown entries rather than a dated HugoBlox timeline. Each entry will contain the verified laboratory or context, advisor when stated, research topic, contribution, and public-safe outcome.

Entries:

1. **Image Fusion Laboratory, Tongji University**
   - Advised by Prof. Wei Tang
   - Describe image-processing research and a first-author manuscript
   - Do not publish ACM MM as the target venue
   - Do not publish pre-rebuttal review scores

2. **Independent Research**
   - Describe solo-authored work on KV-cache management
   - It is acceptable to state that the work was accepted for an oral presentation
   - Do not invent the paper title, citation, or other missing bibliographic facts

3. **IPADS Laboratory, Shanghai Jiao Tong University**
   - Advised by Prof. Erhu Feng
   - Describe work extending and optimizing SkVM
   - State technical contributions without making unsupported authorship claims about the accepted paper

4. **LANDS Laboratory, Nanjing University**
   - Advised by Prof. Chengying Huan
   - Describe RISC-V edge-inference optimization based on MNN
   - State that the manuscript is in preparation
   - Do not publish HPCA as the target venue

The page will also present Education, Skills, and Honors after the research-experience entries.

### 3.4 Education

Publish:

- Tongji University
- Department of Computer Science and Technology
- B.Eng. in Data Science and Big Data Technology
- 2023–2027 (Expected)
- IELTS 7.0
- CET-6 571

Do not publish GPA values. Do not invent exact start or graduation dates.

### 3.5 Projects

Replace the three demonstration project bundles with the following real project pages.

#### SemServe

**Title:** SemServe: Co-designing Semantic Priority and KV-Cache Storage Precision

Public-safe content:

- Extension of prior KV-cache management research
- Automatic semantic scoring method
- Offline search and online computation
- Semantic-priority mapping to MLFQ scheduling
- Storage precision strategy: FP16 for the highest-priority queue, INT8 for the second, and CPU offload for the third
- Technology tags: Python, PyTorch, Transformers, Qwen2.5-3B, Llama-3.2-3B
- Status: ongoing research or manuscript in preparation

Do not state the target conference.

#### SkVM

**Title:** SkVM: A Skill Compilation and Runtime System for Heterogeneous LLM and Agent Harnesses

Public-safe content:

- SJTU-IPADS project context
- Containerized execution modes for pi, claude-code, opencode, and hermes adapters
- Three-level parallelism classification: DLP, ILP, and TLP
- AOT compiler integration and parallel dispatch for ILP tool calls
- Multi-role agent optimization in the JIT optimization stage
- Technology tags: TypeScript, Bun, Docker, LLM Agents

The page may state that the underlying system work is associated with a paper accepted to SOSP 2026 only if phrased without making unsupported authorship claims. It will remain a project rather than a publication until official citation metadata and Kuo Li's authorship are confirmed.

#### Systems Projects

Create one consolidated page covering:

- Rust-based operating-system kernel
- MCP server
- Paged Attention operator-fusion optimization
- Chord-based distributed hash ring
- Mini-GFS in Go

Do not split these into separate pages until substantial descriptions, dates, or public links are available.

### 3.6 Skills

Present skill labels without invented numeric ratings.

- **Programming Languages:** Rust, C/C++, Python, Go
- **Systems and Architecture:** Linux, distributed systems, concurrency, RISC-V, process and memory management, page-table mechanisms, system calls, ELF, file systems
- **AI Systems and Performance:** CUDA C++, operator optimization, PyTorch, Transformers, vLLM, KV Cache, Paged Attention, Nsight Compute
- **Engineering and Research Tools:** Git, CMake, C++/CUDA extension development, Vite/Vue, modern coding agents, AI-assisted problem solving

Change any template heading such as “Skills & Hobbies” to “Skills.”

### 3.7 Honors

Publish:

1. **National First Prize**
   - Global Campus Artificial Intelligence Algorithm Competition, Algorithm Challenge Track
   - First-ranked team member
   - December 2025

2. **International Silver Medal**
   - International Genetically Engineered Machine Competition (iGEM)
   - October 2025

Use month precision where supported. Do not fabricate a day value merely to satisfy a date field; use plain Markdown if the structured award block requires a full date.

## 4. Canonical Data and File Mapping

### 4.1 Structured profile source

Use `data/authors/me.yaml` for:

- Name
- Role
- Affiliation
- Biography
- Email and GitHub
- Research interests
- Education
- Skills
- Honors where the schema can represent month precision without invented dates

Remove all template values for Alex Johnson, including pronouns, postnominals, Meta/OpenAI roles, Stanford/CMU/MIT education, fake metrics, fake social profiles, fake awards, and fictitious biography text.

### 4.2 Site identity

Update:

- `config/_default/params.yaml`
- `config/_default/hugo.yaml`

Use Kuo Li's name and a concise full-stack ML systems description. Remove template social handles and generic marketing metadata. Retain the Pages deployment behavior that overrides the build base URL.

### 4.3 Content pages

Update or create:

- `content/_index.md`
- `content/experience.md`
- `content/projects/_index.md`
- `content/projects/semserve/index.md`
- `content/projects/skvm/index.md`
- `content/projects/systems-projects/index.md`
- `content/publications/_index.md`
- `config/_default/menus.yaml`

Do not create individual publication bundles until complete records are supplied.

## 5. Demonstration Content Cleanup

Remove all content that would be false, misleading, or incorrectly attributed after changing the owner profile:

- Demonstration portrait under `assets/media/authors/`
- Demonstration publication bundles, including their PDFs, BibTeX files, and images
- Demonstration event and slides
- HugoBlox tutorial blog posts
- HugoBlox tutorial course
- Pandas, PyTorch, and scikit-learn demonstration projects and images
- Homepage demonstration CTA
- Demonstration `static/uploads/resume.pdf`
- Homepage sections and menu entries for Talks, News, and Courses

Retain operational infrastructure:

- Build and deployment workflows
- HugoBlox module configuration
- Publication-import workflow
- Upgrade workflow
- Required theme layouts and configuration

Remove any layout hook that exists solely for the deleted demonstration CTA if it has no remaining functional purpose.

## 6. Privacy and Disclosure Policy

### 6.1 Never publish in the initial update

- Phone number
- GPA values
- ACM MM pre-rebuttal review scores
- Target venue for any work under anonymous review
- Target venue for manuscripts in preparation
- Unverified authorship claims
- Invented publication metadata
- The current unsanitized source PDF

### 6.2 Public contact details

Publish only:

- Tongji University email
- GitHub profile

### 6.3 CV download

The current `E:\大三下\cvv5-en.pdf` is an information source only. It must not be copied into the repository because it contains fields the user decided not to publish.

The CV menu entry and homepage download button remain hidden until the user provides a sanitized PDF without the phone number and GPA.

## 7. Verification Strategy

### 7.1 Content integrity

Search the repository after implementation and confirm that user-facing content no longer contains:

- Alex Johnson
- Meta AI
- OpenAI
- Stanford University
- Demonstration paper titles
- Lorem ipsum
- Template email addresses or social profiles
- The private phone number
- GPA values
- ACM MM review scores

Any matches retained in dependency metadata or non-rendered historical documentation must be reviewed individually rather than blindly deleted.

### 7.2 Attribution integrity

- Every rendered use of author slug `me` must refer to Kuo Li and real content.
- No deleted blog, event, course, or publication may remain in homepage collections.
- No real project may imply an unsupported publication authorship claim.

### 7.3 Navigation and asset integrity

- All navigation targets must exist.
- No homepage block may reference a deleted content collection.
- The CV button and CV navigation item must be absent while no sanitized PDF exists.
- No demonstration image, paper PDF, BibTeX file, or résumé remains reachable.

### 7.4 Build verification

- Validate YAML and front matter syntax.
- Validate internal links and collection filters.
- Run the production Hugo build with the pinned fixed Hugo version (`0.162.1`) when Hugo is available.
- If Hugo cannot be installed locally, run repository-level configuration and link checks and use GitHub Actions as the final production-build evidence.
- Run `git diff --check` and review the complete change set before completion.

## 8. Missing Information Policy

- Do not infer dates, roles, titles, author lists, links, DOI values, or abstracts.
- Omit fields that cannot be represented accurately.
- Use undated prose rather than fabricating timeline data.
- Use project pages for technical contributions and publication pages only for official bibliographic records.
- Hide unavailable assets such as the portrait and public CV rather than retaining demonstration placeholders.

## 9. Acceptance Criteria

The update is complete when:

1. The website identifies Kuo Li accurately and contains no remaining false personal claims.
2. The homepage communicates the four approved research-interest areas and links to real project content.
3. Research Experience presents the four approved entries without invented dates or roles.
4. Education excludes GPA and contains only approved facts.
5. The three project pages accurately reflect the source CV under the conservative disclosure policy.
6. Skills and honors are represented without invented ratings or dates.
7. Publications remains an honest empty state without fabricated bibliographic records.
8. All demonstration content and its navigation/collection references are removed.
9. The phone number, GPA, review scores, and unsanitized source PDF do not appear in the repository's published content.
10. No CV download link appears until a sanitized PDF is supplied.
11. Configuration and link checks pass, and the production build succeeds in an environment with Hugo 0.162.1.
