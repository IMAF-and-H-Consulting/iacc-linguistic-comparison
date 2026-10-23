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


if __name__ == "__main__":
    unittest.main()
