from html.parser import HTMLParser
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.items = []
        self.current = None

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            self.current = [dict(attrs), ""]

    def handle_data(self, data):
        if self.current is not None:
            self.current[1] += data

    def handle_endtag(self, tag):
        if tag == "a" and self.current is not None:
            self.items.append((self.current[0], " ".join(self.current[1].split())))
            self.current = None


def links(html: str):
    parser = LinkParser()
    parser.feed(html)
    return parser.items


class NavigationTests(unittest.TestCase):
    def test_template_and_generated_explorer_link_to_methodology(self):
        for path in ("explorer_template.html", "index.html"):
            with self.subTest(path=path):
                matches = [attrs for attrs, text in links(read(path))
                           if text == "how it was done"]
                self.assertEqual(len(matches), 1)
                self.assertEqual(matches[0].get("href"), "how-it-was-done.html")

    def test_existing_section_ids_and_annotation_loader_are_preserved(self):
        template = read("explorer_template.html")
        generated = read("index.html")
        for section_id in ("tldr", "background", "style", "trends", "subject",
                           "reversals", "keyness", "vocab", "memory", "sections", "funding"):
            self.assertIn(f'id="{section_id}"', template)
            self.assertIn(f'id="{section_id}"', generated)
        self.assertIn("https://mike.nothelp.help/page-notes/overlay.js", template)
        self.assertIn("https://mike.nothelp.help/page-notes/overlay.js", generated)


class IdParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.node_count = 0
        self.flow_count = 0
        self.scripts = 0
        self.external_scripts = 0
        self.stages = []
        self.section_ids = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.add(attrs["id"])
        if tag == "section" and "id" in attrs:
            self.section_ids.append(attrs["id"])
        classes = set(attrs.get("class", "").split())
        is_stage = tag == "a" and ({"dag-node", "flow-step"} & classes)
        self.node_count += tag == "a" and "dag-node" in classes
        self.flow_count += tag == "a" and "flow-step" in classes
        if is_stage:
            self.stages.append(attrs.get("data-stage"))
        self.scripts += tag == "script"
        self.external_scripts += tag == "script" and "src" in attrs


class MethodologyPageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = read("how-it-was-done.html")
        cls.parser = IdParser()
        cls.parser.feed(cls.html)
        cls.hrefs = [attrs.get("href", "") for attrs, text in links(cls.html)
                     if "dag-node" in attrs.get("class", "").split()]

    def test_page_contains_only_the_guided_pipeline(self):
        self.assertEqual(self.parser.section_ids, ["pipeline"])
        self.assertNotIn('class="section-jump"', self.html)
        self.assertNotIn("<footer", self.html)
        self.assertIn("translateX", self.html)
        self.assertIn("prefers-reduced-motion", self.html)

    def test_guided_flow_has_sixteen_stages_and_arrow_controls(self):
        self.assertEqual(self.parser.node_count, 16)
        self.assertEqual(self.parser.flow_count, 0)
        self.assertEqual(len(self.hrefs), 16)
        self.assertEqual(len(self.parser.stages), 16)
        self.assertEqual(len(set(self.parser.stages)), 16)
        self.assertNotIn(None, self.parser.stages)
        self.assertTrue(all(href and not href.startswith("javascript:")
                            for href in self.hrefs))
        self.assertIn("dag-info", self.parser.ids)
        for element_id in ("dag-prev", "dag-next", "dag-counter", "guided-stage"):
            self.assertIn(element_id, self.parser.ids)
        self.assertIn('aria-label="Previous stage"', self.html)
        self.assertIn('aria-label="Next stage"', self.html)
        self.assertIn("currentIndex", self.html)
        self.assertIn("node.hidden", self.html)
        self.assertIn("let transition = null", self.html)
        self.assertIn("cancelTransition", self.html)
        self.assertIn("outgoing.animate", self.html)
        self.assertIn("incoming.animate", self.html)
        self.assertIn("matchMedia", self.html)

    def test_info_modal_has_close_control_and_does_not_scroll(self):
        self.assertIn('<dialog id="dag-info"', self.html)
        self.assertIn('id="dag-info-title"', self.html)
        self.assertIn('id="dag-info-body"', self.html)
        self.assertIn('id="dag-info-links"', self.html)
        self.assertIn('id="dag-info-close"', self.html)
        self.assertIn('aria-label="Close stage details"', self.html)
        self.assertIn("showModal", self.html)
        self.assertIn(".close()", self.html)
        self.assertNotIn("scrollIntoView", self.html)
        self.assertNotIn('history.replaceState(null, "", "#dag-info")', self.html)
        for stage in ("sources", "style", "trends", "validation", "publication"):
            self.assertIn(f'{stage}:', self.html)
        self.assertIn("preventDefault", self.html)

    def test_page_has_no_external_dependencies_and_documents_caveats(self):
        self.assertEqual(self.parser.scripts, 1)
        self.assertEqual(self.parser.external_scripts, 0)
        for phrase in ("61 documents", "46 documents", "eight earlier strategic plans",
                       "working draft", "cannot establish intent", "content-addressed"):
            self.assertIn(phrase, self.html)

    def test_return_navigation_and_source_links_exist(self):
        all_hrefs = {attrs.get("href") for attrs, text in links(self.html)}
        self.assertIn("index.html#top", all_hrefs)
        for source in ("iacc_linguistic_comparison.ipynb", "agency_analysis.py",
                       "build_explorer.py", "iac/IACC_Publications/INDEX.csv"):
            self.assertIn(source, self.html)


if __name__ == "__main__":
    unittest.main()
