# How It Was Done Page Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a responsive, source-grounded methodology page whose clickable DAG connects the real analysis pipeline to explorer results and source files.

**Architecture:** Keep the existing generated explorer unchanged except for one navigation link sourced from `explorer_template.html`. Add a dependency-free `how-it-was-done.html` containing an accessible SVG DAG, a narrow-screen HTML equivalent, and anchored explanatory sections. Validate static contracts with Python’s standard-library HTML parser and rebuild the explorer with the existing script.

**Tech Stack:** HTML5, inline CSS, inline SVG, Python 3 standard library (`unittest`, `html.parser`), existing `build_explorer.py` and pandas environment.

## Global Constraints

- Do not add a graph library, external runtime dependency, build framework, or changes to research results.
- Preserve every existing explorer section ID, the annotation loader, chart code, and report content.
- The page and all methodology links must work without JavaScript.
- Every DAG node must be clickable, keyboard-focusable, visibly labeled, and connected according to actual source dependencies.
- Reuse `--paper:#f7f4ec`, `--ink:#2c2639`, `--muted:#6b6570`, `--red:#bd7f76`, and `--blue:#8099b8` from the explorer.
- Do not push, merge, or publish without separate user confirmation.

---

### Task 1: Preserve the New Navigation Through Rebuilds

**Files:**
- Modify: `explorer_template.html:197-200`
- Modify: `index.html` only by running `build_explorer.py`
- Test: `tests/test_how_it_was_done.py`

**Interfaces:**
- Consumes: existing navigation markup and `build_explorer.py`.
- Produces: `how-it-was-done.html` navigation link in both template and generated explorer; test helpers `read(path: str) -> str` and `links(html: str) -> list[tuple[dict[str, str], str]]`.

- [ ] **Step 1: Write the failing navigation test**

Create `tests/test_how_it_was_done.py`:

```python
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
```

- [ ] **Step 2: Run the test and confirm the expected failure**

Run: `python -m unittest tests.test_how_it_was_done.NavigationTests -v`

Expected: FAIL because neither file contains a link whose text is `how it was done`.

- [ ] **Step 3: Add the template navigation link**

In `explorer_template.html`, append this link immediately after the existing funding link on line 199, without reformatting adjacent links:

```html
<a class="lnk" href="how-it-was-done.html">how it was done</a>
```

- [ ] **Step 4: Regenerate and test both files**

Run: `python build_explorer.py && python -m unittest tests.test_how_it_was_done.NavigationTests -v`

Expected: builder prints `wrote .../index.html`; one navigation test passes.

- [ ] **Step 5: Commit the navigation contract**

```bash
git add explorer_template.html index.html tests/test_how_it_was_done.py
git commit -m "Add methodology page to explorer navigation"
```

---

### Task 2: Build the Accessible, Source-Grounded Methodology Page

**Files:**
- Create: `how-it-was-done.html`
- Modify: `tests/test_how_it_was_done.py`

**Interfaces:**
- Consumes: navigation target from Task 1; verified source facts from `README.md`, notebook sections 1–12, `agency_analysis.py`, and `build_explorer.py`.
- Produces: page anchors `sources`, `inventory`, `extraction`, `cleaning`, `measurements`, `validation`, `outputs`, and `publication`; 16 `.dag-node` links; 16 `.flow-step` links in the mobile equivalent.

- [ ] **Step 1: Add failing page-structure and destination tests**

Append these classes before `if __name__ == "__main__":`:

```python
class IdParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.node_count = 0
        self.flow_count = 0
        self.scripts = 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.add(attrs["id"])
        classes = set(attrs.get("class", "").split())
        self.node_count += tag == "a" and "dag-node" in classes
        self.flow_count += tag == "a" and "flow-step" in classes
        self.scripts += tag == "script"


class MethodologyPageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = read("how-it-was-done.html")
        cls.parser = IdParser()
        cls.parser.feed(cls.html)
        cls.hrefs = [attrs.get("href", "") for attrs, text in links(cls.html)
                     if "dag-node" in attrs.get("class", "").split()]

    def test_page_has_stable_explanatory_anchors(self):
        expected = {"sources", "inventory", "extraction", "cleaning",
                    "measurements", "validation", "outputs", "publication"}
        self.assertTrue(expected.issubset(self.parser.ids))

    def test_all_sixteen_dag_nodes_have_real_destinations(self):
        self.assertEqual(self.parser.node_count, 16)
        self.assertEqual(self.parser.flow_count, 16)
        self.assertEqual(len(self.hrefs), 16)
        self.assertTrue(all(href and not href.startswith("javascript:")
                            for href in self.hrefs))
        local_anchors = {href[1:] for href in self.hrefs if href.startswith("#")}
        self.assertTrue(local_anchors.issubset(self.parser.ids))

    def test_analysis_nodes_link_to_matching_explorer_sections(self):
        expected = {"index.html#style", "index.html#subject",
                    "index.html#reversals", "index.html#keyness",
                    "index.html#vocab", "index.html#memory",
                    "index.html#sections", "index.html#trends"}
        self.assertTrue(expected.issubset(set(self.hrefs)))

    def test_page_is_dependency_free_and_documents_caveats(self):
        self.assertEqual(self.parser.scripts, 0)
        for phrase in ("61 documents", "46 documents", "eight earlier strategic plans",
                       "working draft", "cannot establish intent", "content-addressed"):
            self.assertIn(phrase, self.html)

    def test_return_navigation_and_source_links_exist(self):
        all_hrefs = {attrs.get("href") for attrs, text in links(self.html)}
        self.assertIn("index.html#top", all_hrefs)
        self.assertIn("iacc_linguistic_comparison.ipynb", all_hrefs)
        self.assertIn("agency_analysis.py", all_hrefs)
        self.assertIn("build_explorer.py", all_hrefs)
        self.assertIn("iac/IACC_Publications/INDEX.csv", all_hrefs)
```

- [ ] **Step 2: Run the tests and confirm the page is absent**

Run: `python -m unittest tests.test_how_it_was_done.MethodologyPageTests -v`

Expected: ERROR in `setUpClass` with `FileNotFoundError: how-it-was-done.html`.

- [ ] **Step 3: Create the standalone styled page**

Create `how-it-was-done.html` with this document shell and exact core styles, then place the DAG and sections from Steps 4–6 inside `<main class="wrap">`:

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>How the IACC Linguistic Comparison Was Done</title>
<style>
:root{--paper:#f7f4ec;--ink:#2c2639;--muted:#6b6570;--line:#d9d4c9;--hair:#e7e1d2;--red:#bd7f76;--blue:#8099b8;--mono:ui-monospace,"SF Mono","Cascadia Code",Menlo,Consolas,monospace;--serif:Georgia,"Iowan Old Style","Times New Roman",serif}
*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font-family:var(--serif);line-height:1.55}a{color:#5477a0;text-decoration:none;border-bottom:1px solid #c6c2ce}a:focus-visible{outline:3px solid var(--red);outline-offset:4px}.wrap{max-width:1100px;margin:auto;padding:0 28px}nav{position:sticky;top:0;background:rgba(247,244,236,.96);border-bottom:1px solid var(--line);z-index:10}nav .wrap{display:flex;gap:22px;padding-top:11px;padding-bottom:11px;overflow-x:auto}nav a{font:12px var(--mono);white-space:nowrap;border:none}.brand{font-size:19px!important;color:var(--ink)}header{padding:64px 0 36px;border-bottom:1px solid var(--line)}.eyebrow,.kicker{font:11px var(--mono);letter-spacing:.14em;text-transform:uppercase;color:#9b6463}h1{font-size:clamp(42px,6vw,68px);font-weight:400;line-height:1.02;letter-spacing:-.035em;max-width:850px;margin:14px 0 20px}.sub{font-size:18px;color:var(--muted);max-width:780px}.dag-shell{margin:34px 0 46px;padding:20px;border:1px solid var(--line);background:#f3efe4}.dag{display:block;width:100%;height:auto}.dag-edge{stroke:#aa9fac;stroke-width:1.6;fill:none;marker-end:url(#arrow)}.dag-node rect{fill:#fbf8f0;stroke:#c9bec8;stroke-width:1.2}.dag-node:nth-of-type(3n+1) rect{fill:#e7d9df}.dag-node:nth-of-type(3n+2) rect{fill:#dde6ee}.dag-node text{fill:var(--ink);font:12px var(--mono);pointer-events:none}.dag-node:hover rect,.dag-node:focus-visible rect{stroke:var(--red);stroke-width:3}.dag-node:focus-visible{outline:none}.mobile-flow{display:none}section{padding:38px 0 24px;border-top:1px solid var(--hair);scroll-margin-top:60px}h2{font-size:30px;font-weight:400;letter-spacing:-.02em;margin:8px 0 12px}h3{font-size:19px;font-weight:400}.lede,li{color:var(--muted)}.io{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin:20px 0}.io div{padding:14px;background:rgba(255,255,255,.3);border-top:1px solid var(--line)}.io strong{display:block;font:11px var(--mono);letter-spacing:.1em;text-transform:uppercase;color:var(--red);margin-bottom:7px}.io p{margin:0;font-size:14px}.note{border-left:3px solid var(--blue);padding:8px 0 8px 16px;color:var(--muted)}.links{font:12px var(--mono);line-height:2}.links a{margin-right:18px}footer{padding:34px 0 64px;color:var(--muted)}@media(max-width:760px){.wrap{padding:0 18px}.dag-shell{display:none}.mobile-flow{display:block;margin:28px 0 42px}.flow-step{display:block;position:relative;margin:0 0 12px;padding:13px 15px;border:1px solid var(--line);background:#f3efe4;color:var(--ink);font:12px var(--mono)}.flow-step:after{content:"↓";position:absolute;left:50%;bottom:-18px;color:var(--red)}.flow-step:last-child:after{content:""}.io{grid-template-columns:1fr}h1{font-size:44px}}@media(prefers-reduced-motion:no-preference){.dag-node{transition:opacity .15s}.dag-node:hover{opacity:.82}}
</style>
</head>
<body>
<nav aria-label="Primary"><div class="wrap"><a class="brand" href="index.html#top">IACC × 2026</a><a href="index.html#tldr">explorer</a><a href="#pipeline">pipeline</a><a href="#measurements">measurements</a><a href="#caveats">caveats</a></div></nav>
<header><div class="wrap"><div class="eyebrow">Reproducible methods · source archive to interactive evidence</div><h1>How it was done.</h1><p class="sub">Follow the 61-document inventory through extraction, cleaning, parallel linguistic measurements, exported evidence, and the 46-document interactive comparison.</p><p class="links"><a href="iacc_linguistic_comparison.ipynb">analysis notebook</a><a href="https://github.com/IMAF-and-H-Consulting/iacc-linguistic-comparison">GitHub repository</a><a href="outputs/iacc_linguistic/report.md">full report</a></p></div></header>
<main class="wrap">
<!-- Steps 4–6 insert the complete pipeline and explanatory sections here. -->
</main>
<footer><div class="wrap"><a href="index.html#top">← Back to the interactive explorer</a></div></footer>
</body>
</html>
```

Remove the HTML comment after inserting the content; no placeholder comments may remain.

- [ ] **Step 4: Add the exact 16-node DAG and mobile equivalent**

At the start of `<main>`, add `<section id="pipeline">` with heading `From source documents to an interactive comparison`. Inside `.dag-shell`, use one `<svg class="dag" viewBox="0 0 1040 900" role="img" aria-labelledby="dag-title dag-desc">`; define an arrow marker and describe the branches in `dag-desc`. Use `<a class="dag-node" href="...">` with `<rect width="220" height="58" rx="3">` and centered `<text>` labels. Place the nodes and draw `.dag-edge` lines in this exact order and dependency direction:

| Node | Label | Destination | Incoming dependencies |
|---|---|---|---|
| 1 | Source archive + draft | `#sources` | none |
| 2 | Corpus inventory · 61 | `#inventory` | 1 |
| 3 | Analysis set · 46 | `#inventory` | 2 |
| 4 | Extract or reuse cache | `#extraction` | 3 |
| 5 | Clean shared corpus | `#cleaning` | 4 |
| 6 | Style + readability | `index.html#style` | 5 |
| 7 | Lexicon + subject | `index.html#subject` | 5 |
| 8 | Agency + community | `index.html#subject` | 5 |
| 9 | Z-scores + keyness | `index.html#keyness` | 6, 7 |
| 10 | Vocabulary turnover | `index.html#vocab` | 7 |
| 11 | Similarity + text reuse | `index.html#memory` | 5 |
| 12 | Trends + controls | `index.html#trends` and add a separate visible companion link to `index.html#reversals` in the measurements section | 6, 7 |
| 13 | Draft sections | `index.html#sections` | 5 |
| 14 | Smoke tests | `#validation` | 6, 7, 9, 10, 11, 12, 13 |
| 15 | CSVs + figures | `#outputs` | 6, 7, 8, 9, 10, 11, 12, 13, 14 |
| 16 | Payload → explorer | `#publication` | 15 |

Arrange nodes 1–5 vertically, nodes 6–13 in two columns of parallel branches, node 14 beneath the branches, and nodes 15–16 vertically at the bottom. Ensure connectors terminate at node boundaries rather than crossing labels. Immediately after `.dag-shell`, repeat the same 16 labels and hrefs as `<a class="flow-step">` elements inside `<div class="mobile-flow" aria-label="Analysis pipeline">`; add visible text `Parallel measurement branches follow the cleaned corpus and reconverge at exported outputs.` so the linear mobile presentation does not imply false serial dependencies.

- [ ] **Step 5: Write the anchored methodology content**

Add these sections with an `.io` grid (`Input`, `Transformation`, `Output`) and the listed source links:

1. `#sources`: archive downloaded 2026-09-15 plus `IACC Strategic Plan Working Draft July 17.pdf`; link `iac/IACC_Publications/INDEX.csv` and the notebook.
2. `#inventory`: 61 documents inventoried; 46 documents analyzed; 15 excluded as under 2,000 words or easy-read/at-a-glance editions; link `outputs/iacc_linguistic/documents.csv`.
3. `#extraction`: PyMuPDF primary extractor; pypdf/pdfplumber/pdftotext fallbacks; content-addressed cache keyed by SHA-256; unchanged documents reuse cache while changed PDFs are re-extracted.
4. `#cleaning`: remove running headers/footers, tables of contents, and reference lists; use citation density to verify reference-cut behavior; all later measurements use the cleaned prose.
5. `#measurements`: subsections for style/readability, lexicon/reference counts, agency/community proto-roles, z-scores, weighted log-odds keyness, vocabulary turnover, TF-IDF cosine, Burrows’ Delta, 8-word shingles, Spearman trends, walk-forward controls, and 37 draft sections. Link `agency_analysis.py`, the eight explorer destinations tested above, and `outputs/iacc_linguistic/critique_memo.md`.
6. `#validation`: notebook section 12 smoke tests and `outputs/iacc_linguistic/dashboard_review_checks.csv`; validation checks measurement code rather than proving substantive intent.
7. `#outputs`: notebook section 11 writes CSVs, PNG figures, and `report.md` to `outputs/iacc_linguistic/`; link that report.
8. `#publication`: `build_explorer.py` reads selected CSVs, replaces `/*__PAYLOAD__*/null` in `explorer_template.html` with JSON, and writes self-contained `index.html`; link `build_explorer.py` and `explorer_template.html`.
9. `#caveats`: sentence splitting, syllable counting, and passive detection are heuristic but consistent; z-scores use only eight earlier strategic plans and inflated magnitudes should not be read as effect sizes; SP-2023 is the primary comparator; the 2026 source is a working draft; linguistic comparison cannot establish intent.

- [ ] **Step 6: Run all static tests**

Run: `python -m unittest tests.test_how_it_was_done -v`

Expected: six tests pass (one navigation and five methodology tests).

- [ ] **Step 7: Commit the methodology page**

```bash
git add how-it-was-done.html tests/test_how_it_was_done.py
git commit -m "Add clickable analysis pipeline and methodology page"
```

---

### Task 3: Verify Rendering, Rebuild Stability, and Existing Explorer Integrity

**Files:**
- Modify only if a verified defect requires it: `how-it-was-done.html`
- Modify only if a verified defect requires it: `tests/test_how_it_was_done.py`
- Inspect: `index.html`, `explorer_template.html`

**Interfaces:**
- Consumes: completed page and generated explorer from Tasks 1–2.
- Produces: verified responsive page, valid destinations, stable regeneration, and unchanged explorer behavior/anchors.

- [ ] **Step 1: Add a rebuild-stability test**

Append this test to `NavigationTests`:

```python
    def test_existing_section_ids_and_annotation_loader_are_preserved(self):
        template = read("explorer_template.html")
        generated = read("index.html")
        for section_id in ("tldr", "background", "style", "trends", "subject",
                           "reversals", "keyness", "vocab", "memory", "sections", "funding"):
            self.assertIn(f'id="{section_id}"', template)
            self.assertIn(f'id="{section_id}"', generated)
        self.assertIn("https://mike.nothelp.help/page-notes/overlay.js", template)
        self.assertIn("https://mike.nothelp.help/page-notes/overlay.js", generated)
```

Run: `python -m unittest tests.test_how_it_was_done -v`

Expected: seven tests pass.

- [ ] **Step 2: Verify regeneration is deterministic**

Run:

```bash
shasum -a 256 index.html > /tmp/iacc-index-before.sha256
python build_explorer.py
shasum -a 256 -c /tmp/iacc-index-before.sha256
```

Expected: `index.html: OK`.

- [ ] **Step 3: Check every local destination programmatically**

Run this script from the repository root:

```bash
python - <<'PY'
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote

class Links(HTMLParser):
    def __init__(self):
        super().__init__(); self.hrefs=[]; self.ids=set()
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if 'id' in a: self.ids.add(a['id'])
        if tag == 'a' and 'href' in a: self.hrefs.append(a['href'])

root=Path.cwd(); cache={}
def parse(path):
    if path not in cache:
        p=Links(); p.feed(path.read_text(encoding='utf-8')); cache[path]=p
    return cache[path]

for name in ('index.html','how-it-was-done.html'):
    source=root/name
    for href in parse(source).hrefs:
        if href.startswith(('http://','https://','mailto:')): continue
        file_part, _, anchor=href.partition('#')
        target=(source.parent / unquote(file_part)).resolve() if file_part else source
        assert target.exists(), f'{name}: missing {href}'
        if anchor and target.suffix == '.html':
            assert unquote(anchor) in parse(target).ids, f'{name}: missing anchor {href}'
print('All local page and anchor destinations resolve.')
PY
```

Expected: `All local page and anchor destinations resolve.`

- [ ] **Step 4: Validate desktop, mobile, keyboard, and no-JavaScript rendering**

Serve locally without leaving a background process:

```bash
python -m http.server 8000
```

Open `http://localhost:8000/how-it-was-done.html` during the bounded validation session. Verify:

- Desktop DAG has no connector/label collisions and all 16 nodes activate by pointer and Tab + Enter.
- At 375 px width, `.dag-shell` is hidden, all 16 `.flow-step` links appear in reading order, and no horizontal page overflow occurs.
- With JavaScript disabled, the DAG, mobile flow, explanatory text, and links remain available.
- `index.html` still opens its chart controls, tables, search, and existing section navigation.
- Stop the temporary server with Ctrl+C before continuing.

Expected: all checks pass; no development server remains running.

- [ ] **Step 5: Review the final diff and commit verification coverage**

Run: `git diff --check && git status --short && python -m unittest tests.test_how_it_was_done -v`

Expected: no whitespace errors; seven tests pass; only intended files are modified.

```bash
git add tests/test_how_it_was_done.py how-it-was-done.html
git commit -m "Verify methodology links and explorer rebuild stability"
```

If no files changed in this task, skip the commit rather than creating an empty commit.
