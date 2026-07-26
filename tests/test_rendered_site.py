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
