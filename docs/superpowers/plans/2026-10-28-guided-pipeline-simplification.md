# Guided Pipeline Simplification Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reduce the methodology page to its header and guided pipeline while adding directional, reduced-motion-aware stage transitions.

**Architecture:** Keep the existing standalone HTML page and 16-anchor progressive fallback. Extend `renderStage()` / `moveStage()` with a cancellable two-card Web Animations API handoff; keep dialog content in the existing `details` object.

**Tech Stack:** HTML, CSS, vanilla JavaScript, Python `unittest`, headless Chrome CDP.

## Global Constraints

- Only the primary navigation, header, description, source links, and guided pipeline remain.
- All 16 stages, modal links, keyboard navigation, and no-JavaScript fallbacks must remain functional.
- Next moves outgoing content left and incoming content from the right; Previous reverses this.
- No scrolling, hash changes, horizontal overflow, external dependencies, or motion under reduced-motion preferences.
- Do not use subagents; implement inline in the current workspace.

---

### Task 1: Remove lower-page content and preserve explanations

**Files:**
- Modify: `tests/test_how_it_was_done.py`
- Modify: `how-it-was-done.html`

**Interfaces:**
- Consumes: existing `IdParser`, `MethodologyPageTests`, `details` object, and guided-stage anchors.
- Produces: a page whose only `<section>` is `#pipeline`, plus valid fallback URLs and caveats in `details`.

- [ ] **Step 1: Write failing structural tests**

Extend `IdParser` with `self.section_ids = []` and append `attrs["id"]` when `tag == "section" and "id" in attrs`. Replace the stable-anchor test with:

```python
def test_page_contains_only_the_guided_pipeline(self):
    self.assertEqual(self.parser.section_ids, ["pipeline"])
    for deleted_id in ("sources", "inventory", "extraction", "cleaning",
                       "measurements", "validation", "outputs", "publication", "caveats"):
        self.assertNotIn(deleted_id, self.parser.section_ids)
    self.assertNotIn('class="section-jump"', self.html)
    self.assertNotIn("<footer", self.html)
    self.assertIn("translateX", self.html)
    self.assertIn("prefers-reduced-motion", self.html)
```

Update source-link assertions to inspect `self.html` for `agency_analysis.py` and `build_explorer.py`, since those links remain in JavaScript dialog data rather than static anchors.

- [ ] **Step 2: Run the test and verify it fails**

Run: `python -m unittest tests.test_how_it_was_done.MethodologyPageTests.test_page_contains_only_the_guided_pipeline -v`
Expected: FAIL because lower sections and the footer still exist and `translateX` is not implemented.

- [ ] **Step 3: Simplify markup and CSS**

Remove the `measurements` and `caveats` nav links, `.section-jump`, `.graph-note`, every section after `#pipeline`, and `<footer>`. Remove CSS used only by `.io`, `.note`, `.method-grid`, `.method-card`, `.caveats`, `footer`, and `.graph-note`.

Change deleted local-hash fallbacks to real artifacts:

```text
sources      -> iac/IACC_Publications/INDEX.csv
inventory    -> outputs/iacc_linguistic/documents.csv
extraction   -> iacc_linguistic_comparison.ipynb
cleaning     -> outputs/iacc_linguistic/report.md
validation   -> outputs/iacc_linguistic/dashboard_review_checks.csv
outputs      -> outputs/iacc_linguistic/report.md
publication  -> index.html#top
```

Add draft status to `sources`, heuristic and small-baseline/comparator cautions to `style`, and retain the existing no-intent caution in `validation`.

- [ ] **Step 4: Run structural tests**

Run: `python -m unittest tests.test_how_it_was_done -v`
Expected: only the new animation assertion fails; deleted-content and fallback-link assertions pass.

---

### Task 2: Add cancellable directional slide-and-fade handoffs

**Files:**
- Modify: `tests/test_how_it_was_done.py`
- Modify: `how-it-was-done.html`

**Interfaces:**
- Consumes: `nodes`, `currentIndex`, `renderStage()`, and `moveStage(change)` from the guided pipeline.
- Produces: `moveStage(change)` with opposite Next/Previous transforms and one active card after every completed or cancelled handoff.

- [ ] **Step 1: Add animation-state assertions**

Add to the guided-flow test:

```python
self.assertIn("let transition = null", self.html)
self.assertIn("cancelTransition", self.html)
self.assertIn("outgoing.animate", self.html)
self.assertIn("incoming.animate", self.html)
self.assertIn("matchMedia", self.html)
```

- [ ] **Step 2: Implement the transition**

Add `.guided-stage{position:relative;overflow:hidden}` in guided mode. In `moveStage(change)`, cancel any active transition, compute the clamped destination, capture outgoing geometry, call `renderStage()`, temporarily place the outgoing card absolutely over the incoming card, and animate both for 250 ms:

```javascript
const direction = change > 0 ? 1 : -1;
outgoing.animate(
  [{transform: "translateX(0)", opacity: 1},
   {transform: `translateX(${-direction * 56}px)`, opacity: 0}],
  {duration: 250, easing: "cubic-bezier(.22,.61,.36,1)"}
);
incoming.animate(
  [{transform: `translateX(${direction * 56}px)`, opacity: 0},
   {transform: "translateX(0)", opacity: 1}],
  {duration: 250, easing: "cubic-bezier(.22,.61,.36,1)"}
);
```

Use `Promise.allSettled()` for completion so cancellation never creates an unhandled rejection. `cancelTransition()` must cancel animations, hide and clean the outgoing node, remove temporary classes/styles, and leave exactly the current node visible. Bypass animation when `matchMedia("(prefers-reduced-motion: reduce)").matches` is true.

- [ ] **Step 3: Run the regression suite**

Run: `python -m unittest tests.test_how_it_was_done -v`
Expected: 7 tests PASS.

- [ ] **Step 4: Validate in Chrome**

Use a temporary CDP script and remove it afterward. At 1280 px and 375 px verify: all 16 stages, opposite in-flight transforms, rapid clicks, one final visible card, no horizontal overflow, unchanged `scrollY`/hash, modal focus and all close routes, and immediate reduced-motion navigation. Capture and inspect desktop and mobile screenshots.

---

### Task 3: Final verification and delivery

**Files:**
- Verify: `how-it-was-done.html`
- Verify: `tests/test_how_it_was_done.py`
- Verify: `docs/superpowers/specs/2026-10-28-guided-pipeline-simplification-design.md`
- Verify: `docs/superpowers/plans/2026-10-28-guided-pipeline-simplification.md`

- [ ] **Step 1: Run fresh final checks**

Run: `python -m unittest tests.test_how_it_was_done -v && git diff --check && git status --short`
Expected: 7 tests PASS, no whitespace errors, and only intended files modified.

- [ ] **Step 2: Commit and push**

```bash
git add how-it-was-done.html tests/test_how_it_was_done.py docs/superpowers
git commit -m "Simplify guided pipeline and add directional motion"
git push
```

- [ ] **Step 3: Open a pull request**

PR #17 is merged. Open a new PR from `fix/dag-details-modal` to `main`, verify it is open and contains the new commit, and report that the live site updates after merge. Do not merge it.
