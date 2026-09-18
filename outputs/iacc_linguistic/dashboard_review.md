# Review of the IACC Linguistic Comparison dashboard and critique memo

**Reviewer's remit:** read the dashboard (`index.html`), `report.md` and `critique_memo.md` as a hostile
but fair reader would, before the package goes to the advocacy committee. Every number below was
recomputed independently from the shipped text cache (`.pdf_cache/iacc_linguistic/`) with my own
tokenizer, not read off the existing CSVs. Supporting tables: `dashboard_review_checks.csv`.

**Verdict:** the analysis is real, the engineering is clean, and after this pass the package is
defensible. The original deck's problem was the comparator: four of five headline tiles measured the
draft against the *mean of eight plans 2009–2023* instead of against **SP-2023, the plan it actually
replaces**, and on three of them the shift being attributed to the 2026 draft had largely already
happened in 2023. One tile ("55 of 80 trends reversed") failed a control outright. Both are now fixed,
and the naming finding has been replaced by a stronger aggregate measure that does not depend on the
comparator at all.

**Changes made in this pass** (`index.html` rebuilt; `build_explorer.py`, `explorer_template.html`,
`critique_memo.md` edited):

1. Headline tiles re-anchored to SP-2023; the "ASD 1.2 vs 157" and "55 of 80" tiles retired.
2. New section 03, *the document's own subject* — the aggregate autism-reference measure described in §2 below, with the agency-acronym counterpart.
3. Third comparator added to the style panel, "vs SP-2023", shown as a ratio (a z-score is undefined against one document) and made the default view.
4. Trend-reversal section now carries its leave-one-out control and a magnitude-floored default view of 13 substantial reversals instead of 55 weak ones.
5. Text-reuse section corrected: the like-for-like comparison is SP-2023's 0.94% carry-forward from SP-2019, not the 24% annual-update-era average.
6. Readability claim narrowed to the word-length statistic, which is the one that is actually extreme.
7. Methods panel rewritten with a comparator note, the readability correction, and a "what this cannot show" paragraph covering intent, the draft-versus-publication asymmetry, and the draft's own plain-language mandates.
8. Provenance line now gives the document's real title, its "subject to errors and revision" marking, and the 31 July 2026 public-review date.
9. The notebook now computes both new measures itself (§4b subject reference, §9b reversal control), exports `autism_reference_by_plan.csv`, `trend_reversal_control.csv` and `substantial_reversals.csv`, and `report.md` regenerates with the SP-2023 anchoring, the readability correction, the reuse reframing and the control. Every number in this review, in the memo and on the dashboard now comes from one run of the notebook — nothing is computed outside it.

---

## 1. What survives independent recomputation — lead with these

| Claim | Independent check | Status |
|---|---|---|
| Obligation grammar: "should" ×8–10 | 865 occurrences, 80/10k raw vs 8.2/10k in SP-2023; cleaned 105 vs 13.6 | **Holds.** Strongest finding in the study; robust to baseline choice, cleaning, and tokenizer |
| "will" collapses | 1.8/10k vs 18.3 (raw) | **Holds** |
| Longest, most polysyllabic words in the record | letters/word 6.45 vs 5.61; syllables/word 2.20 vs 1.93; 7+ letter words 46.6% vs 37.3% (raw, my tokenizer) | **Holds** |
| Spectrum frame deleted | "on the spectrum" 7 uses vs 149 in SP-2023 | **Holds and strengthens** — SP-2023 used it *more* than the plan average, so this is a genuine deletion, not a continuation |
| "profound autism" is new | 45 raw / ~50 cleaned occurrences; 0 anywhere 2007–2023 | **Holds** |
| Pharmacology vocabulary | medication(s) 219 vs 20; leucovorin 24 vs 0; intervention(s) 211 vs 446 | **Holds** |
| New federal instruments | NAPTI 38, autism.gov 37, dashboard(s) 5.1/10k, accountab* 19.4/10k vs 0.5 | **Holds** |
| vaccin* = 0, neurodivers* = 0 | confirmed, 0 occurrences each; SP-2023 had 31 and 5 | **Holds** |
| Near-zero verbatim text reuse | 0.03% of shingles | **Holds as a number**, but see §2.3 for the framing |

## 1a. The finding this package should lead with

Which label a document prefers changes with the field, and person-first usage has been falling across
autism writing for a decade by deliberate community preference — so the draft's person-first collapse
is partly a trend it inherits, and the "90% identity-first share" is a share of a shrinking
denominator (identity-first is itself 2.7× *below* SP-2023). Counting every convention together
removes the problem entirely. Measured in one non-overlapping pass over cleaned text — person-first
phrases, identity-first phrases, "on the spectrum", self-advocate/autistic-community, then bare
*autism* and *ASD*:

| | 2009 | 2010 | 2011 | 2012 | 2013 | 2017 | 2019 | 2023 | **2026 draft** |
|---|---|---|---|---|---|---|---|---|---|
| all autism references /10k | 314 | 286 | 261 | 256 | 199 | 264 | 285 | 278 | **108** |
| of those, to autistic *people* /10k | 79 | 86 | 72 | 56 | 39 | 78 | 99 | 113 | **28** |
| federal agency acronyms /10k | 9 | 15 | 32 | 22 | 20 | 8 | 30 | 12 | **167** |
| agency names per autism reference | 0.03 | 0.05 | 0.12 | 0.09 | 0.10 | 0.03 | 0.11 | 0.04 | **1.54** |

Eight plans across seventeen years sit in a band of 199–314 references per 10,000 words (mean 268,
sd 33). The draft sits at **108 — 4.8 standard deviations below the mean, 2.6× below SP-2023, and
1.8× below even the lowest earlier plan (SP-2013, 199 per 10k).** Both components fall:
person-referring mentions 113 → 28, autism-as-topic 164 → 81. Collective referents (population,
cohort, subgroup, subtype) now outnumber references to autistic people, inverting SP-2023's roughly
4:1 the other way. And every plan from 2009 to 2023 named autism 8–36× more often than it named a
federal agency; the draft names agencies **1.5× more often than it refers to autism at all**.

This is the result to lead with. It is robust to the naming debate, to the choice of baseline, to
cleaning decisions, and to the tokenizer — I get the same picture from raw text, from
header-stripped text, from the notebook's own cleaned text, and with the person-reference patterns
tightened to allow no intervening modifiers (24.2 vs 110.5 per 10k). It is also the finding an advocacy committee can act on without a
methods argument: a federal autism plan that refers to autistic people a quarter as often as its
predecessor, and to federal agencies more often than to autism, is a document whose subject has
changed.


## 1b. The reversal control, corrected

**My first control was wrong, and wrong in the direction that understated your finding.** I held each
document out, refit the trends on the other 44 — *including documents published after it* — and scored
it against the fixed 2018-onwards average. For a 2011 plan that asks whether 2011 looks like 2018–2023.
For any term with a time trend the answer is no by construction, so the five annual-update plans
returned 75–79 of 80 and I reported "hold out any document and it reverses 41–99%" as though the
draft's 55 were unremarkable. The six documents that scored highest are exactly the six that predate the
window they were scored against. Your own design did not have this defect: the draft is a 2026 document
judged against 2018–2023, which is genuinely its own past.

**The time-symmetric control.** Each document is scored by the draft's rule against *its own* past:
trends refitted on the documents published before it, compared with the mean of its own trailing
eight-year window. Documents with fewer than 15 prior documents or 3 in the window are skipped, leaving
29. Percentages are the comparable unit because the trend set grows with the corpus (34 terms for a 2017
document, 80 for the draft).

| | SP-2013 | SP-2019 | SP-2023 | SP-2017 | **2026 draft** |
|---|---|---|---|---|---|
| strong trends reversed | 25.0% | 42.1% | 48.2% | 60.6% | **68.8%** (55 of 80) |

The 28 earlier documents span **25.0–75.9%**, median **48.2%**. So two things are true at once, and the
package should say both: a reversal share near half is the corpus norm and this measure has no magnitude
floor — but **the draft ranks 2 of 29 documents and is the highest of every strategic plan in the
series**, above SP-2017's 60.6%. Only USPSTF-2016 (75.9%) is higher, and that is an external clinical
review rather than an IACC plan.

**The metric is still too loose to quote on its own.** From the retrospective diagnostic, which remains
useful as a floor-check: 61 of the 80 terms are "reversed" by 8 or more of the 11 documents tested, the
minimum for any term is 4, and no term is reversed by the draft alone. Re-scoring the draft against a
recent-*plans*-only baseline gives 53 rather than 55, so what the measure lacks is a minimum size of
change, not a cleaner comparison set. That is why the thirteen magnitude-floored reversals — used at
least 5 per 10k recently and at least halved by the draft, including health, disparities, adulthood,
racial, suicide, sex and justice — are the ones to put in front of a committee.

**Worked example — "health" (rising, ρ = 0.61).** The draft uses it 47.0 times per 10,000 words against
a 2018+ mean of 111.1, so the rule fires. SP-2009 through SP-2017 sit at 34–59 per 10k, also below that
mean: the plans have always used "health" less than the reports-to-Congress and summaries-of-advances
that make up 13 of the 15 documents in that window. "Justice" behaves the same way — draft 0.0, window
mean 5.1, earlier plans 0.8–3.8.

**A reproducibility bug surfaced while building this, and is fixed.** The control originally joined
held-out scores to the canonical term list by *display label*. A label is a stem's most common spelling,
taken from a map that keeps accumulating on every tokenisation call, so once the section analysis had
run "caregivers" became "caregiver" and the join silently dropped a row: re-running the control cell
after the rest of the notebook gave 78/79 where the first pass gave 79/80. The surface-form and
Title-Case maps are now frozen once the corpus pass finishes, the control joins on stems, and the
notebook asserts that the per-term detail reconciles with its own totals.

## 1c. Plan against plan, with no window and no baseline choice

Every trend measure so far compares one document against an average of several others, which needs a
window, a trend fit and a decision about which documents belong in the baseline. The pairwise question
avoids all three: **how far does each plan move from the plan immediately before it?**

One fixed vocabulary for all eight steps — 386 terms averaging at least 5 uses per 10,000 words across
the nine plans. Fixing it matters: selecting terms on the *earlier* plan of each pair biases every
comparison toward decreases, and that is what produced the suspiciously uniform 79–90% decrease shares
in my first cut. On the fixed set the median term ratio across the seven published-plan steps is 0.99,
so the measure carries no built-in direction.

| Plan vs its predecessor | years apart | changed ≥2× | at least halved | at least doubled | median ratio | trend terms | reversed |
|---|---|---|---|---|---|---|---|
| 2010 vs 2009 | 1 | 15.3% | 2.3% | 13.0% | 0.95 | — | — |
| 2011 vs 2010 | 1 | 13.0% | 3.9% | 9.1% | 0.88 | — | — |
| 2012 vs 2011 | 1 | 34.7% | 21.8% | 13.0% | 0.93 | — | — |
| 2013 vs 2012 | 1 | 32.1% | 11.9% | 20.2% | 1.04 | 213 | 29.1% |
| 2017 vs 2013 | 4 | 26.2% | 11.1% | 15.0% | 1.10 | 196 | 21.4% |
| 2019 vs 2017 | 2 | 50.5% | 33.4% | 17.1% | 0.72 | 188 | 20.2% |
| 2023 vs 2019 | 4 | 49.0% | 16.8% | 32.1% | 1.30 | 187 | **42.8%** |
| **2026 draft vs 2023** | 3 | **62.2%** | **45.1%** | 17.1% | **0.60** | 173 | 32.4% |

**Two findings, and they point different ways.**

*Divergence.* The draft is the largest plan-to-plan step in the series on every magnitude column: it
changes 62.2% of the shared vocabulary by a factor of two or more, against 50.5% for the next largest
step (2019 vs 2017) and 13–35% for the annual-update era. 45.1% of the vocabulary is at least halved,
where no earlier step exceeds 33.4%. The median term ends at 0.60× its SP-2023 rate. Note the
escalation: churn has been above 49% for the last three steps, so the draft extends a pattern that began
with SP-2019 rather than breaking from a stable series.

*Reversal.* On the strict pairwise rule — trend fitted on the plan series only, judged against the
predecessor's own level, with a 2× magnitude floor so a trivial change cannot register — the draft
reverses **32.4%** of its trend terms and **SP-2023 reverses 42.8%**. SP-2023 is the bigger reverser,
and the reason is visible in the direction columns: SP-2023 was an expansionary rewrite (median ratio
1.30, 32.1% of terms at least doubled), and raising a falling term counts as a reversal. The draft
mostly pushes already-falling terms further down, which the rule scores as *continuing* the trend.

**So the honest summary of this metric family:** the draft is the most divergent plan-to-plan step in
the record, and its divergence is near-uniform contraction rather than a change of subject. It is not
the biggest trend-reverser once a magnitude floor is imposed and the comparison is kept inside the plan
series. My claim in the previous pass — "the highest share of any strategic plan" — is true only of the
corpus-wide walk-forward version, which has no magnitude floor and mixes document types; it does not
survive this stricter test, and the package should not lean on it.


## 2. What was wrong, and what was changed

### 2.1 The baseline is wrong on the headline tiles (highest priority)

The draft replaces **SP-2023**. Three of the five headline tiles compare it to the eight-plan mean,
which hides that SP-2023 had already made most of the move:

| Tile / claim | 8-plan mean | **SP-2023** | Draft | Share of the shift already in SP-2023 |
|---|---|---|---|---|
| "ASD" per 10k — the tile reads *1.2 vs 157* | 156.9 | **21.2** | 1.2 | **87%** |
| person-first collapse | 54.8 | **19.2** | 2.6 | **68%** |
| "IACC" nearly absent from its own plan | 38.0 | **15.7** | 4.5 | **67%** |

The "ASD → 1.2 from 157" tile is the most exposed: SP-2023 had already dropped the acronym by 8.5×.
The draft's additional move is real (21.2 → 1.2) but it is a 17× change, not a 130× change, and the
credit for abandoning "ASD" belongs substantially to the 2023 committee. Same for "IACC": my
symmetric re-check on raw text with running headers removed gives 3.9/10k for the draft vs 10.5/10k
for SP-2023 — a 2.7× decline, against a series in which SP-2019 (70.5) → SP-2023 (15.7) was itself a
4.5× decline. The trend predates the draft.

Note also that the identity-first finding *inverts* under the correct baseline: the dashboard reports
identity-first rising (22.0 vs a 9.2 mean), but SP-2023 was at **58.7** — the draft uses identity-first
language **2.7× less** than the plan it replaces. The memo's §2.3 raw cross-check already says this;
the dashboard tile and `report.md` still say the opposite. That is an internal contradiction inside
one package, and it is on the single topic the advocacy committee cares most about.

**Fix:** make SP-2023 the primary comparator everywhere (tiles, `report.md`, the z-score panel's
default view), with the eight-plan mean as a secondary column. This costs you almost nothing
rhetorically — "should" is still 7.8× SP-2023, "will" still collapses 13×, the spectrum frame is
still deleted — and it removes the deck's main attack surface.

### 2.2 "55 of 80 long-run trends, reversed" has no control, and fails one

I replicated the verdict rule on the shipped cache and reproduced your 55/80 for the draft exactly.
Then I held out other documents and re-ran the same rule against the same 80 terms:

| Held out | SP-2013 | SP-2017 | **2026 draft** | SP-2019 | SP-2023 | SOA-2023 | RTC-2023 |
|---|---|---|---|---|---|---|---|
| "trends reversed" of 80 (retrospective diagnostic) | 79 | 59 | **55** | 50 | 38 | 36 | 33 |

Scored against its own past instead, each earlier document reverses 25–76% (median 48%) of its own
trend set, and **the draft's 69% is the highest of any strategic plan** — see §1b. The measure is a near-tautology: a trend fitted across 45 documents and then scored
against the 2018+ mean with no magnitude threshold will flag almost any single document. Eleven of
your 55 reversals are terms the draft simply never uses, and 13 have a 2018+ base rate under 2 per
10,000 words ("spark", "in-person", "receipt", "welfare").

**Fix:** either drop this tile, or replace it with the controlled version — "the draft reverses 55 of 80 —
69% of its trend set, the highest share of any plan, where the corpus median is 48%" — which is honest and
still informative. Adding a magnitude floor (say, reversals where the 2018+ rate exceeds 5 per 10k
and the draft moves by ≥2×) would give you a defensible short list instead of a large weak one.

### 2.3 "Least readable document in the record" is true on 2 of your own 6 formulas

From your own `style_features.csv`, the draft's rank among the 46 analysis documents (1 = hardest):

| Formula | Draft | Hardest document | Draft's rank |
|---|---|---|---|
| Flesch Reading Ease | 0.57 | draft | **1** |
| Coleman–Liau | 21.6 | draft | **1** |
| Flesch–Kincaid grade | 17.95 | **SP-2023 (18.47)** | 3 |
| Gunning Fog | 21.84 | **SP-2023 (21.95)** | 2 |
| SMOG | 18.02 | **SP-2023 (18.79)** | 3 |
| ARI | 19.35 | **SP-2023 (20.57)** | 3 |

The draft's sentences are *shorter* than SP-2023's (19.2 vs 28.4 words). FRE and Coleman–Liau weight
word length heavily, so they single out the draft; the four grade-level formulas put it in the same
postgraduate band as SP-2017 and SP-2023, slightly below both. The memo calls the other four
formulas "corroboration, not headline" — but they do not corroborate, they contradict, and the memo's
own table quietly concedes FK is "within ±2 range" while §2.1 and §3.1 still say "least readable in
the record". A reviewer who opens your CSV finds this in two minutes.

Also: FRE 0.57 is an extrapolation past the bottom of a scale calibrated on schoolbook prose. Quoting
it as a headline tile ("0.6") invites the objection that you are reporting a formula artifact.

**Fix:** change the claim to what the data actually supports — *"the draft uses the longest and most
polysyllabic words of any document in the 17-year record (46.6% of words are 7+ letters vs 37.3% in
SP-2023); on grade-level measures it is as dense as the 2017 and 2023 plans, not denser."* Report the
word-length statistics as the headline, since those are the ones that are unambiguously extreme, and
keep FRE in the table with a note that it is out of calibrated range.

### 2.4 The reuse framing (24% → 0.03%) overstates by ~40×

From your own `reuse_carryover_by_plan.csv`, the 24% series norm is carried by the annual-update era:
SP-2010 inherited 52.8%, SP-2011 31.1%, SP-2013 40.1% — those documents were literally republished
updates of their predecessors. The three most recent plans inherited **4.4% (SP-2017), 19.4%
(SP-2019), 14.7% (SP-2023)** from any earlier publication, and from their *immediate predecessor*:
1.1%, 5.9%, and **0.9%**. SP-2023 inherited under one percent of its text from SP-2019.

So the defensible statement is "the draft inherits 0.02% from SP-2023, where SP-2023 inherited 0.94%
from SP-2019 — roughly 50× less" — not "24% norm versus 0.03%", which compares against a drafting
practice the committee abandoned a decade ago.

### 2.5 The "jargon wall as audience selection" argument is contradicted by the draft itself

§3.2 of the memo argues that the register is chosen to make objection costly, and cites the absence of
a plain-language companion. The draft mandates plain-language and AAC-accessible standards for the
products it proposes — I count 10 passages requiring "federal plain-language, accessibility,
multilingual, and AAC-accessible standards" for autism.gov, family-facing tools, benefits guidance,
and screening materials. It also carries **65 pages of references with 55+ DOIs**, which cuts against
"asserted, not derived". And its title page reads "WORKING DRAFT — SUBJECT TO ERRORS AND REVISION",
issued for public review on 31 July 2026; the 2023 easy-read edition accompanied a *final* plan, so
"no plain-language companion exists" is comparing a draft to a publication.

The register finding is solid. The *motive* inference built on it is the weakest paragraph in the
package and the one most likely to be quoted back at the committee as evidence of bias. It is also
unnecessary: "this document is written at a level most of the people it governs cannot read, and no
plain-language version has been circulated for the comment period" is both true and sufficient.
Recommend cutting the "audience selection", "manufactures authority", and "worldview being installed"
constructions, and cutting the unsourced sentence about "a documented rhetorical pattern in fields
whose claims weaken under scrutiny" — it insinuates without citing, and it is the one line in the memo
that could be called a smear.

---

## 3. A strong finding you have not promoted

Sex and gender language is almost completely gone, and it is a bigger deletion than most of what the
memo highlights:

| Term (raw text) | SP-2023 | 2026 draft |
|---|---|---|
| women / woman / girls / female(s) | 152 uses (15.0/10k) | **2 uses (0.19/10k)** |
| gender* | 103 uses (10.2/10k) | **1 use (0.09/10k)** |
| "sex" | 102 uses (10.1/10k) | 12 uses (1.1/10k) |
| men / boys / male(s) | 54 uses | **0 uses** |

A federal autism plan that never says "women", "girls" or "gender" — in a field where female
under-diagnosis is a live, well-documented services issue — is a concrete, checkable, advocacy-relevant
finding, and it survives the SP-2023 baseline test (the deletion is entirely the draft's, not a
continuation). It currently appears only as "sex" buried in the reversal table. Promote it to a
headline tile in place of the "55 of 80" one.

## 4. Dashboard-specific notes

- **It works.** Self-contained, no CDN, `lang` set, viewport meta, payload fully inlined, 3,579 words /
  4,939 bigrams / 80 trend terms / 37 sections all present and matching the CSVs. No build errors.
- **Hold it to your own accessibility standard.** The memo's sharpest criticism is that the draft is
  unreadable to the people it governs. The memo itself scores FK 17.7 / FRE 7.8 — statistically the same
  register as the draft (FK 18.6 / FRE −0.9). The dashboard prose is better (FK 12.8) but still above a
  plain-language target. Before this goes to an advocacy committee that includes self-advocates,
  write a one-page plain-language summary (target grade 8) and link it from the header. That single
  addition also immunises you against the obvious retort.
- **Chart encodings are colour-only.** Z-score bars and the carryover bars distinguish categories by
  red/orange/grey alone; the keyness table likewise. Add a shape, hatch, or sign prefix so the charts
  survive greyscale printing and colour-vision deficiency — again, the standard you are holding the
  draft to.
- **Provenance line needs tightening.** The eyebrow says "working draft · July 17, 2026"; the document's
  own running header says "for Public Review and Discussion on July 31, 2026" and the title page says
  "Working Draft — Subject to Errors and Revision". State the document's own title, the review date,
  and where a reader can obtain it. A committee will ask, and "July 17" with no link looks like a leak.
- ~~**Attribution.**~~ *Fixed:* the memo's second-author line is removed; it now reads "Prepared by: Mike".
- ~~**`report.md` headline is a filename.**~~ *Fixed:* the report generator now titles it "The 2026 IACC
  Strategic Plan working draft, measured against the IACC publication record" and names the source PDF,
  its draft marking and the primary comparator underneath.
- **Document the exclusions in the dashboard, not just the README.** 15 of 61 documents were excluded;
  the methods panel says "easy-read editions and documents under 2,000 words" but not which ones. One
  expandable list closes that question permanently.
- **The z-score panel should default to "vs all 45 earlier documents".** With n=8 and SP-2023 itself
  an outlier on several lexicon features, the 8-plan z magnitudes (z = +31) look unserious to anyone who
  knows the formula, and the caveat text does not undo the impression the bar makes.

## 5. Suggested follow-on work, in priority order

1. **Re-anchor everything to SP-2023** and regenerate the tiles, `report.md` and the memo's §2.
2. **Citation audit of the 65-page reference list** — are the claims behind "profound autism",
   leucovorin, and the immune/metabolic domains supported by primary trials, reviews, or preprints?
   This is the analysis that would actually test the memo's "asserted, not derived" charge, and it is
   the one a committee can act on.
3. **Section-level baseline comparison** — match the draft's sections to the comparable SP-2023
   chapters rather than to "nearest earlier document", so the reader sees like-for-like.
4. **Plain-language one-pager** at grade 8, linked from the dashboard header.

---

*Re-checks in this review were computed from the repository's own text cache with an independent
tokenizer and syllable heuristic; raw-text figures include reference lists and are used for direction
and magnitude only, matching the memo's convention. Tables: `dashboard_review_checks.csv`.*
