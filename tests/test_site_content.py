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
