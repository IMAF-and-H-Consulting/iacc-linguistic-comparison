# How It Was Done Page — Design

## Purpose

Add a source-grounded “How it was done” page to the IACC linguistic comparison explorer. The page will explain the real analysis and publication pipeline, let visitors click any DAG stage for more detail, and connect result-producing stages to the relevant explorer sections.

## Approach

Use a standalone `how-it-was-done.html` page with lightweight, responsive SVG and ordinary HTML links. Reuse the explorer’s ivory, plum, rose, and powder-blue visual language. Do not add a graph library, external runtime dependency, build framework, or changes to the research results.

## Navigation and preservation

- Add a “how it was done” link to the top navigation in `explorer_template.html`.
- Regenerate `index.html` with `build_explorer.py` so the navigation change survives future builds.
- Preserve all existing report content, section IDs, chart behavior, annotation loader, and source anchors.
- Give the new page clear navigation back to the explorer and its major sections.

## Source-grounded workflow

The primary path is:

1. IACC publication archive and July 2026 working draft.
2. Corpus inventory: 61 documents inventoried.
3. Inclusion and exclusion: 46 documents enter comparisons; short documents and easy-read/at-a-glance editions are excluded.
4. PDF extraction with fallback extractors, or reuse of the content-addressed cleaned-text cache.
5. Cleaning: remove running headers/footers, tables of contents, and reference lists.
6. Shared cleaned corpus.
7. Analysis branches.
8. CSV and figure outputs.
9. Curated payload selection in `build_explorer.py`.
10. Self-contained interactive explorer.

The analysis branches are:

- Style and readability measurements.
- Domain lexicon, naming conventions, and subject references.
- Agency, autistic-person, and community-role analysis from `agency_analysis.py`.
- Z-scores against earlier strategic plans and the broader record.
- Keyness and vocabulary turnover.
- TF-IDF similarity, Burrows’ Delta, and text reuse.
- Longitudinal trends, plan-to-plan change, and walk-forward reversal controls.
- Draft-section profiling.

Smoke tests are a validation branch, not a substantive linguistic measurement. The DAG and prose will distinguish notebook stages, the supplementary agency/community script, and the explorer build step.

## DAG behavior and destinations

- Every DAG node is clickable and keyboard-focusable.
- Every node has a visible text label and an accessible description of its destination.
- Result-producing nodes link to their corresponding explorer section: style, trends, subject, reversals, keyness, vocabulary, memory, or draft sections.
- Infrastructure and validation nodes link to their detailed section on the new page and, where useful, to the notebook, script, archive index, or outputs on GitHub.
- Directional connectors show actual dependencies, including parallel analysis branches and reconvergence at exported outputs.
- The graph does not imply that every analysis feeds every displayed panel; payload selection is represented as its own stage.

## Explanatory sections

Below the DAG, provide concise sections for the major stages. Each section states the inputs, transformation, outputs, and relevant caveats in plain language. Include stable anchors so every node has a meaningful destination even when no corresponding explorer panel exists.

Explain the important limits already documented by the project: heuristic sentence/syllable/passive measurements, consistent application across documents, the small eight-plan z-score baseline, SP-2023 as the primary comparator, the working-draft status of the 2026 document, and the inability of linguistic measurements to establish intent.

## Responsive and resilient behavior

- Use responsive SVG for the graph on larger screens.
- On narrow screens, provide a readable vertical or text-based equivalent that preserves sequence, branches, and links.
- Keep all explanations and links usable without JavaScript.
- Do not make graph rendering a prerequisite for reading the methodology.
- Retain visible keyboard focus, sufficient contrast, semantic headings, and descriptive link text.

## Verification

- Regenerate `index.html` and confirm only the intended navigation/generated differences occur.
- Check every new internal anchor and external/source destination.
- Test desktop and narrow-screen layouts, keyboard navigation, and no-JavaScript readability.
- Confirm existing explorer section IDs and interactions remain unchanged.
- Confirm DAG claims against `README.md`, the notebook, `agency_analysis.py`, `build_explorer.py`, and generated outputs.
