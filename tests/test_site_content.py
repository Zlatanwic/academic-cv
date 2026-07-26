from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read_text(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8")


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
        homepage = read_text("content/_index.md")
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

        for forbidden in ("Download CV", "resume.pdf"):
            self.assertNotIn(forbidden, homepage)

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


if __name__ == "__main__":
    unittest.main()
