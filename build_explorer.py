#!/usr/bin/env python3
"""Build index.html (the interactive explorer) from the analysis CSVs.

Reads outputs/iacc_linguistic/*.csv, embeds a curated JSON payload into
explorer_template.html (token /*__PAYLOAD__*/), writes index.html.
Self-contained: no CDN, works from file:// and GitHub Pages alike.
"""
import json
import math
from pathlib import Path

import pandas as pd

HERE = Path(__file__).parent
OUT = HERE / "outputs" / "iacc_linguistic"


def f2(v, nd=3):
    if v is None or (isinstance(v, float) and (math.isnan(v) or math.isinf(v))):
        return None
    return round(float(v), nd)


payload = {}

# Headline tiles are anchored on SP-2023, the plan this draft replaces. Comparing
# against the mean of eight plans 2009-2023 inflates several of these figures,
# because SP-2023 had already made part of the move (notably on "ASD" and
# person-first naming) -- see the comparator note in the methods section.
payload["headline"] = [
    {"v": '108<small> /10k</small>', "l": 'references to autism or autistic people — SP-2023: 278'},
    {"v": '10.5<small> /1k</small>', "l": '"should" — SP-2023: 1.4 (7.8x)'},
    {"v": "1.5<small>:1</small>", "l": "federal agencies named per autism reference — SP-2023: 0.04:1"},
    {"v": "0", "l": '"on the spectrum" — SP-2023: 32 per 10k'},
    {"v": "0.02<small>%</small>", "l": "text inherited from SP-2023 — SP-2023 inherited 0.94% from SP-2019"},
]

# --- z-scores ---
z = pd.read_csv(OUT / "draft_zscores.csv", index_col=0)
# SP-2023 values for the pairwise "vs the plan this replaces" view. A z-score is
# undefined against a single document, so that mode shows the ratio instead.
_sf_all = pd.read_csv(OUT / "style_features.csv").set_index("doc_id")
_sp23 = _sf_all.loc["SP-2023"]
payload["zscores"] = [
    {
        "feature": idx,
        "group": r["group"],
        "draft": f2(r["draft"]),
        "spMean": f2(r["prior SP mean"]),
        "spSd": f2(r["prior SP sd"]),
        "zSP": f2(r["z vs prior SP"], 2),
        "zAll": f2(r["z vs all prior"], 2),
        "sp23": f2(_sp23[idx]) if idx in _sp23.index else None,
        "flag": r["flag"] if isinstance(r["flag"], str) else "",
    }
    for idx, r in z.iterrows()
]

# --- trend chart data: strategic plans + draft ---
sf = pd.read_csv(OUT / "style_features.csv")
sp = sf[(sf["series"] == "strategic-plan")].sort_values("year")
docs = [{"id": r.doc_id, "year": int(r.year), "draft": bool(r.is_draft)} for r in sp.itertuples()]
doc_ids = [d["id"] for d in docs]

STYLE_PICK = {
    "should_per_1k": "'should' per 1k words",
    "will_per_1k": "'will' per 1k words",
    "deontic_index": "deontic index (obligation share of modals)",
    "hedges_per_1k": "hedges per 1k words",
    "boosters_per_1k": "boosters per 1k words",
    "passive_per_100_sent": "passives per 100 sentences",
    "first_plural_per_1k": "'we/our/us' per 1k words",
    "nominalisation_pct": "nominalisation %",
    "flesch_kincaid_grade": "Flesch-Kincaid grade",
    "flesch_reading_ease": "Flesch Reading Ease",
    "words_per_sentence": "words per sentence",
    "letters_per_word": "letters per word",
    "polysyllable_pct": "polysyllable (3+ syllables) %",
    "long_words_pct": "long words (7+ letters) %",
    "mattr": "lexical diversity (MATTR-500)",
    "acronyms_per_1k": "acronyms per 1k words",
}
sfi = sp.set_index("doc_id")
style_series = [
    {"feature": col, "label": label, "vals": [f2(sfi.loc[d, col], 3) for d in doc_ids]}
    for col, label in STYLE_PICK.items()
]

lex = pd.read_csv(OUT / "lexicon_per10k.csv")
lexicon_series = [
    {
        "group": r["group"],
        "term": r["term"],
        "label": f"{r['term']}  ·  {r['group']}",
        "vals": [f2(r[d], 2) for d in doc_ids],
    }
    for _, r in lex.iterrows()
]
# --- how often the document names its own subject ---
# Counts every explicit reference to autism or to autistic people in one
# non-overlapping pass (person-first phrases, identity-first phrases, "on the
# spectrum", self-advocate/autistic-community, then bare autism / ASD), so the
# total does not depend on which naming convention is in fashion.
ref = pd.read_csv(OUT / "autism_reference_by_plan.csv").set_index("doc_id")
REF_PICK = {
    "total_p10k": "references to autism or autistic people, per 10k words",
    "person_p10k": "references to autistic *people*, per 10k words",
    "abstract_p10k": "autism/ASD as a topic (not person-referring), per 10k",
    "agency_p10k": "federal agency acronyms, per 10k words",
    "agency_autism_ratio": "agency names per autism reference",
}
style_series += [
    {"feature": col, "label": label, "kind": "ref",
     "vals": [f2(ref.loc[d, col], 3) if d in ref.index else None for d in doc_ids]}
    for col, label in REF_PICK.items()
]
payload["reference"] = [
    {"id": d, "year": int(ref.loc[d, "year"]), "total": f2(ref.loc[d, "total_p10k"], 1),
     "person": f2(ref.loc[d, "person_p10k"], 1), "agency": f2(ref.loc[d, "agency_p10k"], 1),
     "ratio": f2(ref.loc[d, "agency_autism_ratio"], 2)}
    for d in doc_ids if d in ref.index
]

payload["trends"] = {"docs": docs, "lexicon": lexicon_series, "style": style_series}

# --- leave-one-out control for the trend-reversal count ---
ctl = pd.read_csv(OUT / "trend_reversal_control.csv")
payload["control"] = [
    {"id": r.held_out_document.replace("SP-2026-DRAFT", "2026 draft"),
     "n": int(r.trends_reversed), "tot": int(r.n_trend_terms),
     "draft": r.held_out_document == "SP-2026-DRAFT"}
    for r in ctl.sort_values("trends_reversed", ascending=False).itertuples()
]

# --- keyness (all rows embedded; display is capped/filtered in the page) ---
def keyness_slice(fname, n_each=None):
    df = pd.read_csv(OUT / fname)
    out = []
    for r in df.itertuples():
        out.append([r.term, f2(r.z, 2), f2(r.target_per10k, 2), f2(r.reference_per10k, 2), int(r.target_count), int(r.reference_count)])
    return out

payload["keyness"] = {
    "words": keyness_slice("keyness_words_vs_prior_plans.csv"),
    "bigrams": keyness_slice("keyness_bigrams_vs_prior_plans.csv"),
    "vs2023": keyness_slice("keyness_words_vs_SP-2023.csv"),
}

# --- vocabulary turnover ---
nv = pd.read_csv(OUT / "new_vocabulary.csv")
payload.setdefault("vocab", {})["new"] = [
    {"term": r.term, "count": int(r.draft_count), "kind": r.kind} for r in nv.itertuples()
]
dv = pd.read_csv(OUT / "dropped_vocabulary.csv")
payload["vocab"]["dropped"] = [
    {"term": r.term, "plans": int(r.prior_plans_using_it), "prior": f2(r.prior_SP_mean_per10k, 1), "kind": r.kind}
    for r in dv.itertuples()
]

# --- term trend reversals ---
tt = pd.read_csv(OUT / "term_trends.csv")
tt = tt[tt["spearman_rho"].abs() >= 0.5]
# "strong" = a reversal that also clears a magnitude floor: the term was used at
# least 5 times per 10k in the 2018+ documents and the draft at most halves it.
# Without a floor the verdict fires on terms used once or twice per document.
payload["termTrends"] = [
    {"term": r.term, "rho": f2(r.spearman_rho, 2), "early": f2(r.mean_per10k_before_2013, 2),
     "late": f2(r.mean_per10k_2018_on, 2), "draft": f2(r.draft_per10k, 2), "verdict": r.draft_verdict,
     "strong": bool("revers" in str(r.draft_verdict) and r.mean_per10k_2018_on >= 5
                    and (r.draft_per10k + 0.1) / (r.mean_per10k_2018_on + 0.1) <= 0.5)}
    for r in tt.itertuples()
]

# --- text reuse carryover ---
co = pd.read_csv(OUT / "reuse_carryover_by_plan.csv")
payload["carryover"] = [
    {"id": r.doc_id, "year": int(r.year),
     "prev": f2(r.from_previous_plan, 4) or 0.0,
     "any": f2(r.from_any_earlier_publication, 4) or 0.0}
    for r in co.itertuples()
]

# --- draft sections ---
sec = pd.read_csv(OUT / "draft_sections.csv")
payload["sections"] = [
    {"section": r.section, "pages": r.pages, "words": int(r.n_words), "fk": f2(r.fk_grade, 1),
     "should": f2(r.should_per_1k, 1), "idf": f2(r.identity_first_share, 3),
     "novel": f2(r.novel_text_share, 3), "nearest": r.nearest_prior_doc}
    for r in sec.itertuples()
]

template = (HERE / "explorer_template.html").read_text(encoding="utf-8")
token = "/*__PAYLOAD__*/null"
assert token in template, "payload token missing from template"
html = template.replace(token, json.dumps(payload, ensure_ascii=False, separators=(",", ":")))
out = HERE / "index.html"
out.write_text(html, encoding="utf-8")
print(f"wrote {out} ({out.stat().st_size:,} bytes)")
print(f"payload: {len(json.dumps(payload)):,} bytes JSON | "
      f"zscores={len(payload['zscores'])} keyness={sum(len(v) for v in payload['keyness'].values())} "
      f"trendSeries={len(lexicon_series) + len(style_series)} termTrends={len(payload['termTrends'])} "
      f"sections={len(payload['sections'])}")
