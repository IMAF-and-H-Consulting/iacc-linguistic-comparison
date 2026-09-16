# Critique Memo: The July 2026 IACC Strategic Plan Working Draft, Measured Against the IACC Record (2007–2023)

**Date:** 2026-09-16
**Prepared by:** Mike, with analysis verification and consolidation by Kimi
**Sources:** `iacc_linguistic_comparison.ipynb`; outputs in `outputs/iacc_linguistic/`; draft PDF `iac/IACC Strategic Plan Working Draft July 17.pdf`; IACC publications archive `iac/IACC_Publications/` (downloaded from iacc.hhs.gov 2026-09-15)

---

## 0. What this memo is

A consolidated, verified account of how the July 2026 IACC Strategic Plan working draft differs from every document the Interagency Autism Coordinating Committee published between 2007 and 2023 — linguistically, lexically, and structurally — with plain-language explanations of each measurement method, and an interpretation section that separates **measured fact** from **inference**.

**Corpus:** 46 documents in the comparison set — the draft plus 8 earlier strategic plans (2009–2023) and 37 other IACC publications (Summaries of Advances, Reports to Congress, portfolio analyses, letters). 15 inventoried documents were excluded from comparisons as too short or as easy-read/at-a-glance editions (different register, too small for stable statistics).

**Verification status:** every headline number below was cross-checked twice — (a) the report against its own CSV exports, and (b) independently, by re-extracting the draft and the 2023 plan with a different PDF tool (poppler `pdftotext` rather than the notebook's `pymupdf`) and re-counting. Raw and cleaned rates are flagged as such. Raw-text comparisons include reference lists and are used only to check direction and magnitude.

---

## 1. The methods, in plain language

Each measurement is defined here once, then used freely below.

- **Per-1k / per-10k (normalised rate).** A count divided by document length, expressed per 1,000 or 10,000 words. This is the "normalization": it makes an 80,000-word draft comparable to a 10,000-word 2009 plan. "Should: 10.5 per 1k" means the word *should* appears about 10–11 times in every 1,000 words.
- **Flesch Reading Ease (FRE).** A 0–100 readability score from average sentence length and syllables per word. Higher = easier. 60–70 is a news article; 30 is a university textbook; **below 10 is extreme** — dense legal or scientific prose. Formula: `206.835 − 1.015×(words/sentence) − 84.6×(syllables/word)`.
- **Flesch–Kincaid grade (FK).** The estimated US school grade needed to follow the text, from the same two ingredients. 12 = high-school senior; 16 = college graduate; **18+ = postgraduate**.
- **Coleman–Liau, Gunning Fog, SMOG, ARI.** Four other readability formulas using word/sentence length instead of syllables. Used here as corroboration, not headline.
- **MATTR (moving-average type–token ratio).** Lexical diversity: slide a 500-word window through the text, count how many distinct words appear in each window, average. Higher = richer, less repetitive vocabulary. Unlike raw type–token ratio it is not biased by document length.
- **Nominalisation percentage (`nominalisation_pct`).** The share of words ending in -tion/-sion/-ment/-ness/-ity/-ance/-ence/-ism — verbs and adjectives frozen into nouns ("we decide" → "a determination was made"; "analyse" → "analysis of the analysis"). Nominalisation is the classic marker of bureaucratic and scientistic register: it hides actors ("who decides?") inside abstract nouns.
- **Deontic index.** Among all modal verbs, the share expressing obligation: (must + shall + should + "required/need to") ÷ all modals (incl. will/would/may/might/can/could). High = the document *commands*; low = it *describes or predicts*.
- **Hedges / boosters.** Rates of uncertainty markers ("may, suggests, preliminary, unclear") versus certainty markers ("clearly, demonstrates, essential, definitive").
- **Passive constructions per 100 sentences.** A heuristic count of be-verb + participle ("was conducted"). Passive voice hides who acts.
- **Z-score vs earlier plans.** The draft's value minus the earlier plans' mean, divided by their standard deviation. |z| > 2 is the conventional "unusual" line. **Caveat:** there are only 8 earlier plans, and they are stylistically consistent, so their standard deviations are small and z-values are inflated. The *direction* of every z reported here is trustworthy; treat the *magnitude* as "far outside the range," not a precise distance.
- **Keyness (weighted log-odds, Monroe et al. 2008).** For each word: how much more (or less) the draft uses it than the earlier plans, as a log-odds ratio with its standard error, stabilised by a prior so rare words don't dominate. Reported as a z-score: red = distinctively draft, blue = distinctively earlier plans.
- **TF-IDF cosine (content similarity).** Each document becomes a vector of its content words/bigrams weighted by how distinctive they are; cosine (0–1) measures topical overlap. Higher = same subject matter.
- **Burrows' Delta (style distance).** Uses only the 150 most frequent words — mostly function words (the, of, should) — z-scored per document, mean absolute difference. A standard stylometric/authorship measure of *how* a text is written, regardless of topic. Higher = more different style.
- **8-word shingles (text reuse).** Slide an 8-word window through the text; the share of those windows found verbatim in earlier documents measures how much of a text is inherited boilerplate or copied passage.
- **Spearman trend (term_trends).** Rank-correlation between a word's rate and publication year across the 45 pre-draft documents. A word "rises" or "falls" across 2007–2023; the draft is then judged to **continue** or **reverse** each trend relative to the 2018-onwards average.

---

## 2. Measured findings

### 2.1 Size and shape

| Measure | Draft | Earlier plans (mean ± sd) | z |
|---|---|---|---|
| Words (cleaned prose) | 81,788 | 32,326 (max 60,494, SP-2023) | — |
| Flesch Reading Ease | **0.57** | 27.9 ± 8.2 | −3.3 |
| Flesch–Kincaid grade | **17.9** | 14.6 | elevated (within ±2 range) |
| Coleman–Liau | 21.6 | 15.9 ± 1.1 | +5.0 |
| Syllables per word | 2.21 | 1.86 ± 0.05 | +6.8 |
| Letters per word | 6.62 | 5.64 ± 0.17 | +5.9 |
| Words of 7+ letters | 49.4% | 37.9% ± 2.2 | +5.4 |
| Polysyllables (3+ syll.) | 35.4% | 24.0% ± 1.5 | +7.7 |
| Nominalisation % | 11.77 | 7.55 ± 0.77 | +5.5 |
| MATTR-500 | 0.551 | 0.490 ± 0.01 | +5.8 |

The draft is the most lexically diverse, longest-worded, most nominalised, and least readable document in the record. FRE 0.57 sits essentially at the floor of the scale; FK 17.9 requires postgraduate reading level. Independently confirmed by raw re-extraction: words of 12+ letters make up **7.9%** of the draft vs **5.0%** of SP-2023; of 10+ letter words, **38%** are nominalisations vs **31%**.

The most-used 12+ letter words, side by side:

- **Draft 2026:** implementation (348), communication (303), developmental, gastrointestinal, participation, translational, accountability (116), mitochondrial, surveillance (90), coordination, consolidated, stabilization, standardized, longitudinal, inflammatory.
- **SP-2023:** interventions (314), disabilities, communication, developmental, co-occurring, environmental, understanding (92), opportunities, participants, evidence-based, perspectives, underrepresented, autism-related.

### 2.2 Voice: from describing to directing

| Measure | Draft | Earlier plans | z |
|---|---|---|---|
| "should" per 1k | **10.53** | 1.07 ± 0.30 | **+31.1** |
| Deontic index | **0.66** | 0.21 ± 0.05 | +8.9 |
| "will" per 1k | 0.23 | 2.76 ± 0.84 | −3.0 |
| Hedges per 1k | 4.8 | 7.7 | (notable) |
| Boosters per 1k | 2.6 | 2.2 | (flat) |
| First-person plural per 1k | 0.09 | 1.19 | (notable) |
| Passives per 100 sentences | 18.4 | 25.1 | (lower in draft) |

Earlier plans *survey and predict* ("will," hedged findings, a collective "we"). The draft *instructs*: "should" is ~10× denser than the earlier-plan mean — the single most extreme measurement in the study. The draft is grammatically a directive to federal agencies, not a committee's survey of a field.

### 2.3 Naming autism (per 10k words; draft vs earlier-plan mean)

| Expression | Draft | Earlier plans |
|---|---|---|
| ASD (case-sensitive) | **1.2** | 156.9 |
| Person-first ("people with autism") | **2.6** | 54.8 |
| Identity-first ("autistic people") | 22.0 | 9.2 |
| "on the (autism) spectrum" | **0.0** | 9.9 |
| "autism spectrum disorder(s)" | 0.1 | 5.2 |
| "disorder(s)" | 4.8 | 21.3 |
| "condition(s)" | **26.9** | 15.6 |
| **"profound autism"** | **5.5** | **0.0** |
| nonspeaking / minimally verbal | 3.5 | 2.2 |
| neurodivers* | 0.0 | 0.2 |
| vaccin* | **0.0** | 4.5 |

Identity-first *share* of naming phrases: 90% in the draft vs 75% in SP-2023 — but this is a **ratio effect**: person-first collapsed while identity-first grew only modestly.

Independent raw cross-check against SP-2023 (uncleaned text; reference lists included — direction/magnitude only):

| Expression | SP-2023 /10k | Draft /10k |
|---|---|---|
| autistic individual(s) | 14.7 | **8.3** |
| autistic adults/children | 11.4 | **8.0** |
| autistic people | 4.1 | 4.3 |
| spectrum (any use) | 69.9 | **26.9** |
| on the spectrum | 17.4 | **0.9** |
| profound autism | 0.0 | **4.6** (50 occurrences) |
| nonspeaking / non-speaking | 0.5 | **2.8** |
| minimally verbal | 0.5 | 1.4 |

**The label the community prefers was adopted; the individuated person was written out.** Mentions of "autistic individuals/adults/children" *fell* versus SP-2023; "autistic people" held flat; the spectrum frame — the accepted diversity framing — was effectively deleted; and "condition" replaced "disorder" as the default noun.

### 2.4 What is to be done: treatments up, interventions down, medications up 10×

Per-10k, cleaned (draft vs earlier-plan mean): implementation 39.0 vs 4.1; service(s) 28.2 vs 62.1; support(s) 61.7 vs 33.2; intervention(s) 20.9 vs 46.9; biomarker(s) 24.8 vs 5.6.

Raw cross-check vs SP-2023 (direction/magnitude only):

| Term | SP-2023 /10k | Draft /10k |
|---|---|---|
| treatment(s) | 6.3 | **19.9** |
| intervention(s) | 45.4 | **19.6** |
| medication(s) | 2.0 | **20.0** |
| prescrib* | 0.5 | 3.2 |
| dose / dosage | 0.5 | 1.4 |
| placebo | 0.7 | 0.7 (flat) |
| behavioral | 7.6 | 9.0 |

The swap is specific: **medication vocabulary rose tenfold while interventions halved and placebo stayed flat** — this is pharmacology talk, not generic clinical-trial talk. Keyness bigrams corroborate: "medication effects," "immune metabolic," "trials design," "clinically meaningful," "biomarker-defined." **Leucovorin — 24 mentions — has never appeared in any earlier IACC publication.**

### 2.5 Causes and biology (per 10k; draft vs earlier-plan mean)

immun* 27.8 vs 5.9; regression 21.6 vs 1.4; safety/wandering/elopement 29.8 vs 7.6. New therapeutic-domain architecture: nine "Priority Therapeutic Domains" covering neurotransmission, immune/autoimmune, folate metabolism (leucovorin), GI/microbiome, neurodevelopmental regression, mitochondrial/redox, autonomic dysfunction, sleep/circadian, epilepsy — plus motor planning/praxis and adaptive trial design.

**"Profound autism" as policy instrument.** The draft proposes "adoption of a **standardized functional designation of profound autism for research and policy purposes**," and couples the category to prevalence: "the share of children with profound autism — minimal or no functional speech and who require continuous care — **has risen alongside the broader trend**." The term appears ~50 times; it never appeared in the entire 2007–2023 record. The rhetorical effect is to convert rising diagnosis counts into rising *severity* claims.

### 2.6 Governance vocabulary (per 10k; draft vs earlier-plan mean)

Agency acronyms (HHS/NIH/CDC/FDA/CMS…) 166.9 vs 18.6 (9×); federal 71.2 vs 10.0; **IACC itself 4.5 vs 38.0**. New coinages never before seen in the record (176 words, 5+ uses): dashboard (42), workplans (42), compact (39), comparative-effectiveness (38), NAPTI (38), biomarker-defined (37), implementation-ready (34), praxis (32), tier (31), prescribing (21), leucovorin (18), deterioration (18), civil-rights (17), communication-access (17), decompensation (17). The draft proposes two new federal instruments: **NAPTI** (National Autism Precision Therapeutics Initiative) for translation, and **Autism.gov** (37 mentions) for navigation and "public accountability."

Dropped words (used in 3+ earlier plans, absent from the draft): sharing, enhance, **scientists**, **evidence-based**, repository, mutations, infants, prevented, collaborative, **advocates**, explore, **vaccine**, gender, international, ABA, survey, males.

### 2.7 Similarity, style, and institutional memory

- **Content:** nearest earlier document is SP-2023 at cosine 0.29 — versus 0.41 average similarity between consecutive earlier plans. The draft is further from its own series than any plan was from its predecessor.
- **Style:** nearest by Burrows' Delta is SP-2011 (Delta 1.13); the draft clusters away from every recent plan.
- **Text reuse:** **0.03%** of the draft's 8-word shingles occur anywhere in the earlier record (68 shared shingles total; longest shared passage: 16 words). Earlier plans inherited on average **24%** of their shingles from prior publications and 11% from the immediately preceding plan (range 1–41%). The draft inherits **0.02%** from SP-2023.
- The draft's own preface states why, in part: *"Our drafting process did not have the benefit of a complete institutional record or formal handoff from the prior planning cycle."* But earlier plans were built largely from the same *published* record and still inherited a quarter of their text — the near-zero reuse indicates a deliberate clean room, not merely a missing archive.

### 2.8 Trends reversed

Of 80 terms with a strong monotonic trend (|ρ| ≥ 0.5) across 2007–2023, the draft **reverses 55**. Rising terms it reverses include: college, veterans, accessibility, **suicide**, equity, arts, demographic, leadership, inpatient, **justice**, health, living, sex. Falling terms it revives: syndrome, treatment, abnormalities.

### 2.9 Inside the draft

37 outline sections of 300+ words; every section is ~100% novel text (no inherited boilerplate anywhere). Most prescriptive sections (should per 1k): Autonomic Dysfunction (18.5), Epilepsy (17.9), Neurotransmission (17.2), Sleep (16.3), Caregiver Stabilization (16.2). Densest prose (FK grade): Appendix C (30.6), Contributing Factors and Causality (22.2), Mitochondrial/Metabolic (20.6), Implications for Federal Action (20.6), Communication Access for Nonspeaking People (20.3). The section written *about* nonspeaking people requires postgraduate reading level. No easy-read or plain-language companion exists for the draft (the 2023 plan had one).

---

## 3. Interpretation

### 3.1 What the data shows (measured)

Four mutually reinforcing shifts, each independently measurable:

1. **Genre shift: survey → directive.** The epistemic machinery of the old plans (will/may/suggests; hedges; "we") was replaced by obligation grammar ("should" ×10; deontic index 0.66 vs 0.21) and management vocabulary (dashboards, workplans, implementation, accountability). The document directs agencies; it does not deliberate.
2. **Subject shift: services → mechanism.** Services and interventions fall by half; treatments triple; medications rise tenfold; biomarkers, subgroups, and therapeutic domains organise the document. The unit of analysis is no longer a person receiving support but a biological subtype receiving a compound.
3. **Naming shift: person-reference thinning.** The community-approved *label* (identity-first) was adopted — superficially a concession to self-advocates — while individuated person references fell, the spectrum frame was deleted, and autism was recast as a "condition." Simultaneously, a severity frame was built: "profound autism" (0 → ~50), nonspeaking foregrounded, tied to an explicit claim that the severe *share* is rising.
4. **Register shift: the jargon wall.** The least readable document in the record (FRE 0.57; FK 17.9; 49% long words; nominalisation z = +5.5), with no plain-language companion, including in its sections about people who cannot read it.

Plus one meta-finding: **institutional rupture.** 0.03% inherited text against a 24% series norm; 55 of 80 long-run vocabulary trends reversed; the committee's own name nearly absent from its own plan (IACC 4.5 vs 38.0 per 10k). Seventeen years of negotiated, incremental, publicly-built language — discarded in one draft.

### 3.2 The interpretation we favour (inference, argued)

**Jargon here is not a byproduct; it is audience selection.** A document at FK 18 does three things at once:

- **Self-advocates cannot complain precisely.** You cannot object to a sentence you cannot parse. Objection costs are raised above the capacity of the constituencies most affected — including the nonspeaking people the document discusses in its densest prose.
- **Scientists cannot rebut cheaply.** Pseudo-precise framing ("biomarker-defined confirmation," "standardized functional designation," "immune-metabolic subgroups") sounds falsifiable but is asserted, not derived; a rigorous rebuttal must unpack each compound claim. Asymmetry of effort: a page to assert, a monograph to refute.
- **Laypeople hear credentials.** Long words, acronyms, and therapeutic-domain architecture read as expertise to journalists, legislators, and parents. The register manufactures authority while withholding the accessibility that would let readers check it.

This is a documented rhetorical pattern in fields whose claims weaken under scrutiny: insular jargon, scientific phrasing, and complexity signalling substitute for evidence that survives inspection. The draft's register is consistent with that pattern — and inconsistent with the record of a committee that previously published easy-read editions so affected people could answer back.

**The severity pivot deserves scrutiny, not reflexive acceptance.** "Profound autism" enters federal planning here for the first time, ~50 occurrences, explicitly coupled to a rising-share claim. That framing serves whoever benefits from a public image of autism as predominantly severe, mute, and biologically treatable: it re-anchors prevalence debates, justifies pharmacological investment, and marginalises the self-advocate framing (spectrum, neurodiversity — both deleted from the lexicon). Whether this reflects the sincerely held priorities of a new committee or a coordinated agenda cannot be decided by linguistics alone. What linguistics *can* say: the pivot was executed silently, without acknowledging the 17-year vocabulary it replaced, and in prose calibrated to be unanswerable by the people it describes.

**Deletion by silence is the document's most characteristic move.** "Vaccine" — 4.5/10k across the earlier record, mostly in debunking contexts — occurs zero times. "Neurodiversity": zero. Suicide, equity, justice, accessibility, veterans: all rising trends, all reversed. Nothing was argued against; the words simply no longer exist. A reader of the draft alone cannot detect this. Only measurement against the baseline can.

### 3.3 Honest counterweights (what the data cannot prove)

- **Intent is not measurable.** Genre change, jargon, and novelty are also consistent with an inexperienced committee, consultant-drafted text, or haste under statutory deadline. The preface's "no handoff" admission is a genuine mitigating fact for the rupture finding.
- **Some shifts are defensible on merits.** Identity-first labelling, attention to nonspeaking people, caregiver stabilisation, and life-course coverage (aging, transportation, housing sections are all present) answer real community demands. The critique is not that these appear; it is what was *removed* to make room, and the register in which it was done.
- **The Autism CARES Act of 2024** broadened the plan's remit toward services and policy, which legitimately pushes toward implementation vocabulary. It does not, however, explain the collapse of "services," "interventions," "community," or "advocates."
- **The z-scores** rest on 8 prior plans; "FRE 0.57" rests on heuristic sentence-splitting. Directions are solid; exact magnitudes are approximate.
- **Raw cross-check rates** in §2.3–2.4 include reference lists; use the notebook's cleaned rates for citation.

### 3.4 Bottom line

Within one drafting cycle, the IACC's strategic plan changed its grammar (describe → command), its subject (persons receiving services → subtypes receiving treatments), its naming (spectrum/disorder → condition/profound), its audience (families and community → agency auditors), and its memory (24% inherited → 0.03%). Any one shift could be innocent. Their convergence in a single document — in the least readable, most jargon-dense text the committee has ever produced — is the signature of a worldview being installed, not a plan being updated.

---

## Appendix: key files

- `iacc_linguistic_comparison.ipynb` — full analysis, methods, and smoke tests
- `outputs/iacc_linguistic/report.md` — auto-generated headline numbers
- `outputs/iacc_linguistic/draft_zscores.csv` — all z-scores
- `outputs/iacc_linguistic/lexicon_per10k.csv` — naming/lexicon rates, all documents
- `outputs/iacc_linguistic/keyness_words_vs_prior_plans.csv`, `keyness_bigrams_vs_prior_plans.csv` — distinctive vocabulary
- `outputs/iacc_linguistic/new_vocabulary.csv`, `dropped_vocabulary.csv` — coined and deleted words
- `outputs/iacc_linguistic/reuse_carryover_by_plan.csv` — text inheritance by plan
- `outputs/iacc_linguistic/term_trends.csv` — rising/falling terms and the draft's verdicts
- `outputs/iacc_linguistic/draft_sections.csv` — per-section style, novelty, nearest earlier document
