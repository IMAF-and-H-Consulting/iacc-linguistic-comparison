# Agency, visibility, and patiency: federal agencies vs autistic people

Three measures applied to each IACC strategic plan, contrasting how the text
positions federal agencies versus autistic people.

## Method

Informed by Hoefer & Martin (SCiL 2026), 'Measuring Perceptions of Personhood
with Semantic Proto-role Properties.' The full SPRL neural parser (Spaulding
et al. 2023) was not available in this environment; the proxy described below
was used instead.

**1. Visibility** — how often each entity class is named, per 10,000 words.
Uses the existing reference taxonomies already coded in the repository:
agency acronyms (NIH, CDC, HRSA, CMS, FDA, HHS, IACC, etc.) and autism
person-references (autistic people/individuals, people with autism, etc.).
Source: `autism_reference_by_plan.csv`.

**2. Relative agency** — of all agent-role mentions (agency + person), what
share belongs to each class? This measures who the document treats as the
primary actor when it does assign an actor.

**3. Proto-role agency share** — for each entity class independently, the
share of its predicate-argument mentions in which it occupies the agent role
(grammatical subject of active-voice verb) rather than the patient role
(direct object or passive subject). This is a dependency-parse proxy for
Dowty's (1991) proto-agent properties: +instigation, +volition, +awareness,
+sentience, as operationalised by Hoefer & Martin's SPRL cluster (Table 1).

spaCy (en_core_web_sm) dependency parsing classifies each mention as:
- AGENT: grammatical subject of active-voice verb (nsubj, no auxpass)
- PATIENT: direct object, or passive subject (dobj, nsubjpass, by-agent)
- OTHER: prepositional complement, possessive, appositive, etc.

Agency share = agent / (agent + patient), excluding OTHER.

## Results

| Plan | Agency vis /10k | Person vis /10k | Agency share of agents | Person share of agents | Agency proto-agency | Person proto-agency |
|---|---|---|---|---|---|---|
| SP-2009 | 8.6 | 313.7 | 38.9% | 61.1% | 0.538 | 0.688 |
| SP-2010 | 15.3 | 286.3 | 63.2% | 36.8% | 0.750 | 0.368 |
| SP-2011 | 32.0 | 261.1 | 57.6% | 42.4% | 0.494 | 0.636 |
| SP-2012 | 22.3 | 256.3 | 66.7% | 33.3% | 0.737 | 0.700 |
| SP-2013 | 20.3 | 199.2 | 86.4% | 13.6% | 0.760 | 0.450 |
| SP-2017 | 8.1 | 263.6 | 50.6% | 49.4% | 0.707 | 0.597 |
| SP-2019 | 30.3 | 285.2 | 79.1% | 20.9% | 0.723 | 0.450 |
| SP-2023 | 12.2 | 277.5 | 42.2% | 57.8% | 0.679 | 0.534 |
| SP-2026-DRAFT | 166.9 | 108.2 | 80.2% | 19.8% | 0.822 | 0.574 |

## Interpretation

The draft inverts the visibility relationship (agencies 166.9/10k vs persons
108.2/10k) and concentrates agent-role assignment on agencies (80.2% of actor
mentions vs 19.8% for autistic people). When agencies do appear in predicate-
argument structures, they occupy the agent role 82.2% of the time — the
highest in the series. Autistic people's proto-agency share (57.4%) is mid-
range, but their relative share of who-acts-in-this-document collapses because
agency mentions overwhelm person mentions in agent positions.

In SP-2023, by contrast, person agent mentions (78) exceeded agency agent
mentions (57), giving autistic people a 57.8% share of actor roles. The draft
reverses this: agencies hold 80.2% vs persons 19.8%.

Citation: Hoefer, E. S. & Martin, J. (2026). Measuring Perceptions of
Personhood with Semantic Proto-role Properties. Proceedings of the Society
for Computation in Linguistics (SCiL) 2026, 1–14.
