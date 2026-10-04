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
| SP-2010 | 15.3 | 286.3 | 63.2% | 36.8% | 0.75 | 0.368 |
| SP-2011 | 32.0 | 261.1 | 57.6% | 42.4% | 0.494 | 0.636 |
| SP-2012 | 22.3 | 256.3 | 66.7% | 33.3% | 0.737 | 0.7 |
| SP-2013 | 20.3 | 199.2 | 86.4% | 13.6% | 0.76 | 0.45 |
| SP-2017 | 8.1 | 263.6 | 50.6% | 49.4% | 0.707 | 0.597 |
| SP-2019 | 30.3 | 285.2 | 79.1% | 20.9% | 0.723 | 0.45 |
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

## Federal agencies vs autistic people + community/partner organisations

A seventh comparison folds less-profit-motivated organisations and the people
around autistic individuals into one non-agency side: nonprofits, advocacy
groups, community partners and members, families, caregivers, parents, and
public stakeholders. The two measures are the same as the agency-vs-person
pair: visibility (references per 10,000 cleaned words) and relative agency
(share of agent-role mentions).

### Term list, derived from the plan texts

Candidate stems (`nonprofit`, `advocacy`, `community`, `partner`, `family`,
`caregiver`, `parent`, `stakeholder`, `organization`, `foundation`) were
concordanced across SP-2009 through the 2026 draft. Entity-referring phrases
that the plans actually use were kept; federal, commercial, locative, and
topical uses were dropped. Longest-first, non-overlapping match. Per-term
counts: `community_partner_terms.csv`.

**Included phrases:** advocacy group(s); advocacy organization(s); self-advocate(s)/self-advocacy; autistic advocate(s); autism / ASD / autistic / disability / broader autism community; community member(s); community organization(s); community-based organization(s); community partner(s); family member(s); family caregiver(s); families; caregivers; caregiver (not hyphenated compounds); parents; nonprofit / non-profit / not-for-profit and their 'organization' variants; stakeholder(s); public stakeholder(s); private organization(s); private foundation(s); named nonprofits the plans use (Autism Speaks, Simons Foundation, Autism Science Foundation, Autistic Self Advocacy Network).

**Excluded after inspecting contexts:** supporting/lead partners, partner agencies, federal/HHS/FDA partners (these name federal agencies in the draft); Administration for Community Living (ACL); community settings / living / participation / integration / impact (place or metric, not an organisation); research/scientific community; family history / studies / burden; parent of origin; parent-mediated; caregiver-reported / caregiver-succession and other hyphenated topic compounds; communication partner (clinical role); public-private partnership (includes industry); World Health Organization; universities; industry / pharmaceutical firms.

**Visibility construction.** Community/org mentions are counted on the same
cleaned prose as `autism_reference_by_plan.csv` (running headers and reference
lists removed) and divided by that file's official word counts. Phrases already
inside the person-visibility taxonomy (self-advocate*, autistic community) are
not added again. Combined visibility = existing `person_p10k` + new community/
org rate. Existing agency and person visibility figures are unchanged.

**Relative agency construction.** Community/org phrases are parsed with the
same spaCy proto-role proxy. Combined actor-role share uses the existing
agency and person agent counts plus the new community agent counts. Existing
80.2% / 19.8% agency-vs-person shares are unchanged.

### Combined results

| Plan | Agency vis /10k | Person+community vis /10k | Community/org vis /10k | Agency share of agents vs combined | Combined share of agents |
|---|---|---|---|---|---|
| SP-2009 | 8.6 | 361.7 | 48.0 | 28.0% | 72.0% |
| SP-2010 | 15.3 | 327.3 | 41.0 | 42.9% | 57.1% |
| SP-2011 | 32.0 | 306.7 | 45.6 | 46.9% | 53.1% |
| SP-2012 | 22.3 | 289.4 | 33.1 | 48.3% | 51.7% |
| SP-2013 | 20.3 | 224.6 | 25.4 | 73.1% | 26.9% |
| SP-2017 | 8.1 | 306.6 | 43.0 | 34.2% | 65.8% |
| SP-2019 | 30.3 | 346.9 | 61.7 | 71.6% | 28.4% |
| SP-2023 | 12.2 | 337.2 | 59.7 | 31.5% | 68.5% |
| SP-2026-DRAFT | 166.9 | 137.7 | 29.5 | 74.2% | 25.8% |

### Comparison: draft vs SP-2023 vs earlier plans

Combined person+community visibility: earlier-plan mean 309.0/10k (org/family layer 42.5/10k); SP-2023 337.2/10k (org/family 59.7/10k); draft 137.7/10k (org/family 29.5/10k). Agency visibility remains 166.9/10k in the draft vs 12.2 in SP-2023.

Of actor-role mentions when the non-agency side includes community/partner/family organisations as well as autistic people: earlier plans give that combined side a mean 50.7% of agent roles; SP-2023 gives 68.5%; the draft gives 25.8% (agencies 74.2%). Widening the non-agency side does not restore the SP-2023 balance. Community agent mentions in the draft: 27; in SP-2023: 46.
