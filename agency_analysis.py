"""
Measure agency vs patiency ascribed to federal agencies and autistic people
in IACC strategic plans, following the semantic proto-role framework of
Hoefer & Martin (SCiL 2026).

Method: Since the full SPRL parser from Spaulding et al. (2023) is not
available in this environment, we use spaCy dependency parsing as a proxy
for proto-role assignment. The mapping is:

  - AGENT role: entity appears as nsubj of an active-voice verb
    (proto-agent: +instigation, +volition per Dowty 1991 / Hoefer & Martin Table 1)
  - PATIENT role: entity appears as dobj/nsubjpass/pobj-of-"by" in passive
    (proto-patient: -instigation, -volition, change-of-state)
  - OTHER: prepositional complement, possessive, appositive, etc.

The agency share for an entity class is: agent_mentions / (agent_mentions + patient_mentions).
This deliberately excludes OTHER to focus on the agent-vs-patient contrast.

Entities:
  - AGENCY: the set of federal agency acronyms and names already coded in
    the repo (NIH, CDC, HRSA, CMS, FDA, HHS, IACC, "the Department",
    "federal agencies", etc.)
  - PERSON: the autism person-reference taxonomy already coded
    (autistic people/individuals/adults/children, people with autism,
    individuals with autism, etc.)
  - COMMUNITY: less-profit-motivated organisations and people derived
    from the plan texts (nonprofits, advocacy groups, community
    partners/members, families, caregivers, parents, named foundations).
    Combined with PERSON for the seventh comparison pair.
"""

import csv
import json
import math
import os
import re
from collections import Counter
from types import SimpleNamespace

import spacy

nlp = spacy.load("en_core_web_sm", disable=["ner", "textcat"])

AGENCY_TOKENS = {
    "nih", "cdc", "hrsa", "cms", "fda", "hhs", "samhsa", "acl", "ahrq",
    "nimh", "nichd", "ninds", "niehs", "nidcd", "nidcr",
    "iacc", "dod", "doe", "ed", "ssa", "doj", "dol",
}
AGENCY_PHRASES = [
    "the department", "federal agencies", "federal agency",
    "the committee", "the council", "lead agencies", "lead agency",
    "the administration",
]

PERSON_PHRASES = [
    "autistic people", "autistic individuals", "autistic adults",
    "autistic children", "autistic person", "autistic youth",
    "autistic adolescents", "autistic individual",
    "people with autism", "individuals with autism",
    "persons with autism", "children with autism",
    "adults with autism", "person with autism",
    "people on the spectrum", "individuals on the spectrum",
    "people with asd", "individuals with asd",
    "children with asd", "adults with asd",
]

# Community / partner / family / nonprofit terms harvested from the strategic
# plans themselves (see community_partner_terms.csv and the method note).
# Longest-first matching; spans do not overlap.
#
# Included: entity-referring phrases for less-profit-motivated organisations
# and the people they comprise — nonprofits, advocacy groups, community
# partners and members, families, caregivers, parents, public stakeholders,
# and named autism nonprofits that the plans actually use.
#
# Excluded after inspecting plan contexts (these are federal, commercial,
# locative, topical, or already inside the person-reference taxonomy):
#   supporting/lead partners, partner agencies, federal/HHS/FDA partners,
#   Administration for Community Living, community settings/living/
#   participation/integration/impact, research/scientific community,
#   family history/studies/burden, parent of origin, parent-mediated,
#   caregiver-hyphen compounds, communication partner, public-private
#   partnership, World Health Organization, industry/pharma, universities.
COMMUNITY_PHRASES = [
    "autistic self advocacy network",
    "autistic self-advocacy network",
    "autism science foundation",
    "community-based organizations",
    "community-based organisations",
    "community-based organization",
    "community-based organisation",
    "not-for-profit organizations",
    "not-for-profit organisations",
    "not-for-profit organization",
    "not-for-profit organisation",
    "non-profit organizations",
    "non-profit organisations",
    "non-profit organization",
    "non-profit organisation",
    "nonprofit organizations",
    "nonprofit organisations",
    "nonprofit organization",
    "nonprofit organisation",
    "advocacy organizations",
    "advocacy organisations",
    "advocacy organization",
    "advocacy organisation",
    "community organizations",
    "community organisations",
    "community organization",
    "community organisation",
    "private organizations",
    "private organisations",
    "private organization",
    "private organisation",
    "broader autism community",
    "parents and caregivers",
    "parent or caregiver",
    "public stakeholders",
    "public stakeholder",
    "private foundations",
    "private foundation",
    "community partners",
    "community partner",
    "community members",
    "community member",
    "disability communities",
    "disability community",
    "autistic communities",
    "autistic community",
    "family caregivers",
    "family caregiver",
    "simons foundation",
    "family members",
    "family member",
    "advocacy groups",
    "advocacy group",
    "autism community",
    "asd community",
    "self-advocates",
    "self-advocate",
    "self advocates",
    "self advocate",
    "self-advocacy",
    "self advocacy",
    "autistic advocates",
    "autistic advocate",
    "autism speaks",
]

# Bare adjective/role stems (nonprofit, stakeholder) are not entities.
# Singular attributive "caregiver" (caregiver burden, caregiver supports) is not.
# Plural people-nouns remain: families, caregivers, parents.
COMMUNITY_WORDS = ["families", "caregivers", "parents"]

# Person-referring patterns from the notebook (PERSON_REFERRING only).
# Visibility add-on excludes any community span that overlaps these matches,
# instead of a hand list of phrase names (which both over- and under-excluded).
_PERSON_NOUN = (
    r"(?:people|persons?|individuals?|adults?|children|child|youths?|adolescents?"
    r"|teens?|teenagers?|students?|patients?|infants?|toddlers?|men|man|women|"
    r"woman|boys?|girls?|self-?advocates?)"
)
_AUTISM_NOUN = r"(?:autism(?: spectrum disorders?)?|asd|autism spectrum conditions?)"
_MODIFIERS = r"(?:\w+[- ]){0,2}"
PERSON_REFERRING_RE = re.compile(
    "|".join(
        (
            rf"\b{_PERSON_NOUN}\s+with\s+{_MODIFIERS}{_AUTISM_NOUN}\b",
            rf"\b(?:{_PERSON_NOUN}|those)\s+on\s+the\s+(?:autism\s+)?spectrum\b",
            rf"\bthose\s+with\s+{_MODIFIERS}{_AUTISM_NOUN}\b",
            rf"\bautistic\s+{_MODIFIERS}{_PERSON_NOUN}\b",
            r"\bself-?advocat(?:e|es|ing|acy)\b|\bautistic\s+community\b|\bautistic-led\b",
        )
    ),
    re.I,
)

# Notebook cleaning defaults (iacc_linguistic_comparison.ipynb Config).
CLEAN_CFG = SimpleNamespace(
    trim_references=True,
    ref_page_density=70.0,
    ref_page_min_words=50,
    running_line_share=0.20,
)
LIGATURES = {
    "\ufb00": "ff", "\ufb01": "fi", "\ufb02": "fl", "\ufb03": "ffi", "\ufb04": "ffl",
    "\u2018": "'", "\u2019": "'", "\u201c": '"', "\u201d": '"', "\u00ad": "", "\x00": " ",
}
REF_HEADING_RE = re.compile(
    r"^\s*(?:references|bibliography|works cited|endnotes|literature cited|reference list)\s*[:.]?\s*$",
    re.I,
)
REF_TITLE_RE = re.compile(r"\b(?:references|bibliography|endnotes|works cited)\b", re.I)
CITATION_RE = re.compile(
    r"\bet al\b|\bdoi\b|\bpmid\b|https?://|\b[A-Z][a-z]+ [A-Z]{1,3}[,.;]|\b[A-Z][a-z]+, [A-Z]\.|"
    r"\b\d{1,4}\s*\(\d{1,3}\)\s*:\s*\d|\b(?:19|20)\d{2}\s*;\s*\d",
    re.I,
)
DOT_LEADER_RE = re.compile(r"\.{4,}|(?:\. ){4,}")
PAGE_NUMBER_RE = re.compile(
    r"^\s*(?:page\s+)?\d{1,4}(?:\s*(?:of|/)\s*\d{1,4})?\s*$|^\s*[ivxlc]{1,6}\s*$",
    re.I,
)
INLINE_JUNK_RE = re.compile(r"\[\s*PMID:?\s*\d+\s*\]|\bhttps?://\S+|\bwww\.\S+|\bdoi:\s*\S+", re.I)
WORD_RE = re.compile(r"[A-Za-z]+(?:['\-][A-Za-z]+)*")


def is_passive(token):
    if token.dep_ == "nsubjpass":
        return True
    if token.dep_ == "nsubj" and any(
        c.dep_ == "auxpass" for c in token.head.children
    ):
        return True
    return False


def classify_role(token):
    dep = token.dep_
    if dep in ("nsubj", "nsubjpass"):
        if is_passive(token):
            return "patient"
        return "agent"
    if dep in ("dobj", "attr") or (dep == "pobj" and token.head.text.lower() == "by"):
        return "patient"
    return "other"


def citation_density(text):
    words = len(WORD_RE.findall(text))
    return len(CITATION_RE.findall(text)) / max(1, words) * 1000


def find_reference_cut(pages, toc, min_position=0.4):
    n = len(pages)
    if n < 6:
        return None, "too_short"
    floor = int(n * min_position)
    candidates = [
        pg for _lvl, title, pg in toc
        if pg >= floor + 1 and pg <= n and REF_TITLE_RE.search(title)
    ]
    for i in range(floor, n):
        if any(REF_HEADING_RE.match(line) for line in pages[i].splitlines()):
            candidates.append(i + 1)
            break
    if not candidates:
        return None, "no_heading"
    cut = min(candidates)
    before = citation_density("\n".join(pages[: cut - 1]))
    after = citation_density("\n".join(pages[cut - 1 :]))
    if after >= 40 and after >= 3 * max(before, 1e-9):
        return cut, "verified"
    return None, f"unverified(before={before:.0f},after={after:.0f})"


def reference_pages(pages, cfg):
    return {
        i + 1
        for i, page in enumerate(pages)
        if len(WORD_RE.findall(page)) >= cfg.ref_page_min_words
        and citation_density(page) >= cfg.ref_page_density
    }


def _line_key(line):
    return re.sub(r"\s+", " ", re.sub(r"\d+", "#", line.strip().lower()))


def running_line_keys(pages, share):
    counts = Counter()
    for page in pages:
        seen = set()
        for line in page.splitlines():
            key = _line_key(line)
            if 4 <= len(key) <= 140 and key not in seen:
                seen.add(key)
                counts[key] += 1
    threshold = max(3, int(math.ceil(share * len(pages))))
    return {key for key, c in counts.items() if c >= threshold}


def smart_dehyphenate(text):
    vocab = {
        w.lower()
        for w in re.findall(r"[A-Za-z]+(?:-[A-Za-z]+)*", re.sub(r"\w+-\n\w+", " ", text))
    }

    def fix(match):
        a, b = match.group(1), match.group(2)
        if (a + b).lower() in vocab:
            return a + b
        if f"{a}-{b}".lower() in vocab:
            return f"{a}-{b}"
        return a + b

    return re.sub(r"(\w+)-\n(\w+)", fix, text)


def clean_pages(pages, toc, cfg):
    n = len(pages)
    pages = [_apply_ligatures(p) for p in pages]
    cut, cut_status = (
        find_reference_cut(pages, toc) if cfg.trim_references else (None, "disabled")
    )
    ref_pgs = reference_pages(pages, cfg) if cfg.trim_references else set()
    dropped = {p for p in range(1, n + 1) if (cut is not None and p >= cut) or p in ref_pgs}
    running = running_line_keys(pages, cfg.running_line_share)
    cleaned = []
    removed_running = 0
    for i, page in enumerate(pages):
        if i + 1 in dropped:
            cleaned.append("")
            continue
        kept = []
        for line in page.splitlines():
            if not line.strip():
                kept.append("")
                continue
            if _line_key(line) in running:
                removed_running += 1
                continue
            if DOT_LEADER_RE.search(line) or PAGE_NUMBER_RE.match(line):
                continue
            kept.append(INLINE_JUNK_RE.sub(" ", line))
        cleaned.append(smart_dehyphenate("\n".join(kept)))
    return cleaned, {
        "n_pages": n,
        "n_pages_kept": n - len(dropped),
        "ref_cut_page": cut,
        "ref_cut_status": cut_status,
        "words_clean": sum(len(WORD_RE.findall(p)) for p in cleaned),
        "running_lines_removed": removed_running,
    }


def _apply_ligatures(page):
    for src, dst in LIGATURES.items():
        page = page.replace(src, dst)
    return page


def _phrase_boundary_pattern(phrase):
    return r"\b" + re.escape(phrase) + r"\b"


def find_community_spans(text_lower):
    """Non-overlapping community/partner/family mention spans, longest first."""
    occupied = [False] * (len(text_lower) + 1)
    spans = []
    phrases = sorted(COMMUNITY_PHRASES, key=len, reverse=True)
    for phrase in phrases:
        for m in re.finditer(_phrase_boundary_pattern(phrase), text_lower):
            if any(occupied[m.start() : m.end()]):
                continue
            for i in range(m.start(), m.end()):
                occupied[i] = True
            spans.append((m.start(), m.end(), phrase))
    for word in COMMUNITY_WORDS:
        for m in re.finditer(r"\b" + re.escape(word) + r"\b", text_lower):
            end = m.end()
            if end < len(text_lower) and text_lower[end] == "-":
                continue
            if any(occupied[m.start() : m.end()]):
                continue
            for i in range(m.start(), m.end()):
                occupied[i] = True
            spans.append((m.start(), m.end(), word))
    return spans


def person_referring_occupied(text_norm):
    """Character mask of notebook person-referring matches on whitespace-normalised text."""
    occupied = [False] * (len(text_norm) + 1)
    for m in PERSON_REFERRING_RE.finditer(text_norm):
        for i in range(m.start(), m.end()):
            occupied[i] = True
    return occupied


def count_community_visibility(text):
    """Org/family mentions whose spans do not overlap a person-referring match."""
    text_norm = re.sub(r"\s+", " ", text.lower())
    person_occ = person_referring_occupied(text_norm)
    n = 0
    by_term = Counter()
    excluded = Counter()
    for start, end, phrase in find_community_spans(text_norm):
        by_term[phrase] += 1
        # Withhold only when the community span *is* a person-referring
        # mention (fully covered). A longer organisation name that merely
        # contains one (ASAN ⊃ "self advocacy") still counts.
        if start < end and all(person_occ[start:end]):
            excluded[phrase] += 1
        else:
            n += 1
    return n, by_term, excluded


def find_community_mentions(doc, text_lower):
    mentions = []
    for start_char, end_char, phrase in find_community_spans(text_lower):
        span = doc.char_span(start_char, end_char, alignment_mode="expand")
        if span:
            head_token = span.root
            role = classify_role(head_token)
            mentions.append(("community", role, phrase, head_token.head.text))
    return mentions


def find_entity_mentions(doc, text_lower):
    mentions = []

    for token in doc:
        if token.text.lower() in AGENCY_TOKENS and token.dep_ in (
            "nsubj", "nsubjpass", "dobj", "pobj", "attr", "conj"
        ):
            role = classify_role(token)
            mentions.append(("agency", role, token.text, token.head.text))

    for phrase in AGENCY_PHRASES:
        for m in re.finditer(re.escape(phrase), text_lower):
            start_char = m.start()
            span = doc.char_span(start_char, start_char + len(phrase), alignment_mode="expand")
            if span:
                head_token = span.root
                role = classify_role(head_token)
                mentions.append(("agency", role, phrase, head_token.head.text))

    for phrase in PERSON_PHRASES:
        for m in re.finditer(re.escape(phrase), text_lower):
            start_char = m.start()
            span = doc.char_span(start_char, start_char + len(phrase), alignment_mode="expand")
            if span:
                head_token = span.root
                role = classify_role(head_token)
                mentions.append(("person", role, phrase, head_token.head.text))

    return mentions


def load_plan_text(doc_id, manifest, cache_dir):
    """Reconstruct cleaned text from the PDF cache."""
    if doc_id == "SP-2026-DRAFT":
        entry = manifest.get("draft", {})
        sha = entry.get("sha256")
    else:
        for path, info in manifest.get("files", {}).items():
            if doc_id.lower().replace("-", "") in path.lower().replace("-", "").replace("_", ""):
                sha = info.get("sha256")
                break
        else:
            return None

    cache_file = os.path.join(cache_dir, sha + ".json")
    if not os.path.exists(cache_file):
        return None

    with open(cache_file) as f:
        data = json.load(f)

    pages = data.get("pages", [])
    return "\n".join(pages)


def load_plan_records():
    """Return {doc_id: {text, pages, toc}} from the PDF cache."""
    cache_dir = ".pdf_cache/iacc_linguistic"
    with open(os.path.join(cache_dir, "cache_manifest.json")) as f:
        manifest = json.load(f)

    plan_ids = [
        "SP-2009", "SP-2010", "SP-2011", "SP-2012", "SP-2013",
        "SP-2017", "SP-2019", "SP-2023", "SP-2026-DRAFT"
    ]

    records = {}
    for pid in plan_ids:
        if pid == "SP-2026-DRAFT":
            entry = manifest.get("draft", {})
            sha = entry.get("sha256")
        else:
            year = pid.split("-")[1]
            sha = None
            for path, info in manifest.get("files", {}).items():
                fname = os.path.basename(path).lower()
                if "strategic" in fname and year in fname:
                    sha = info["sha256"]
                    break
            if sha is None:
                for path, info in manifest.get("files", {}).items():
                    fname = os.path.basename(path).lower()
                    if year in fname and ("plan" in fname or "sp" in fname):
                        sha = info["sha256"]
                        break

        if sha is None:
            print(f"  WARNING: no cache entry for {pid}")
            continue

        cache_file = os.path.join(cache_dir, sha + ".json")
        if not os.path.exists(cache_file):
            print(f"  WARNING: cache file missing for {pid}")
            continue

        with open(cache_file) as f:
            data = json.load(f)
        pages = data.get("pages", [])
        toc = data.get("toc") or []
        text = "\n".join(pages)
        records[pid] = {"text": text, "pages": pages, "toc": toc}
        print(f"  Loaded {pid}: {len(text)} chars, {len(pages)} pages")

    return records


def load_plan_texts():
    return {pid: rec["text"] for pid, rec in load_plan_records().items()}


def analyze_plan(doc_id, text):
    chunks = []
    for i in range(0, len(text), 80000):
        chunks.append(text[i:i+80000])

    all_mentions = []
    word_count = 0
    for chunk in chunks:
        doc = nlp(chunk)
        word_count += len([t for t in doc if not t.is_space and not t.is_punct])
        text_lower = chunk.lower()
        mentions = find_entity_mentions(doc, text_lower)
        all_mentions.extend(mentions)

    counts = {
        "agency": {"agent": 0, "patient": 0, "other": 0},
        "person": {"agent": 0, "patient": 0, "other": 0},
    }
    for etype, role, _, _ in all_mentions:
        counts[etype][role] += 1

    result = {"doc_id": doc_id, "n_words": word_count}
    for etype in ("agency", "person"):
        c = counts[etype]
        total = c["agent"] + c["patient"] + c["other"]
        ap_total = c["agent"] + c["patient"]
        result[f"{etype}_agent"] = c["agent"]
        result[f"{etype}_patient"] = c["patient"]
        result[f"{etype}_other"] = c["other"]
        result[f"{etype}_total"] = total
        result[f"{etype}_agency_share"] = (
            round(c["agent"] / ap_total, 3) if ap_total > 0 else None
        )
        result[f"{etype}_agent_per10k"] = (
            round(c["agent"] / word_count * 10000, 1) if word_count > 0 else 0
        )
        result[f"{etype}_patient_per10k"] = (
            round(c["patient"] / word_count * 10000, 1) if word_count > 0 else 0
        )

    return result


def analyze_community_roles(text):
    """Dependency-parse roles for community/partner/family mentions only."""
    counts = {"agent": 0, "patient": 0, "other": 0}
    for i in range(0, len(text), 80000):
        chunk = text[i : i + 80000]
        doc = nlp(chunk)
        for _etype, role, _phrase, _head in find_community_mentions(doc, chunk.lower()):
            counts[role] += 1
    return counts


def _pct(num, den, nd=3):
    if not den:
        return None
    return round(num / den, nd)


def _p10k(count, n_words, nd=1):
    if not n_words:
        return 0.0
    return round(count / n_words * 10000, nd)


def main():
    outdir = "outputs/iacc_linguistic"
    existing_path = os.path.join(outdir, "agency_patiency.csv")
    with open(existing_path, newline="") as f:
        existing = list(csv.DictReader(f))
    existing_fields = list(existing[0].keys())
    by_id = {row["doc_id"]: row for row in existing}

    ref_n_words = {}
    with open(os.path.join(outdir, "autism_reference_by_plan.csv"), newline="") as f:
        for row in csv.DictReader(f):
            ref_n_words[row["doc_id"]] = int(row["n_words"])

    print("Loading plan texts...")
    records = load_plan_records()

    print(f"\nAnalyzing community/partner mentions in {len(records)} plans...")
    term_counts = {}
    excluded_counts = {}
    new_by_id = {}
    for doc_id in sorted(records.keys()):
        rec = records[doc_id]
        cleaned, info = clean_pages(list(rec["pages"]), rec["toc"], CLEAN_CFG)
        cleaned_text = "\n".join(cleaned)
        vis_n, by_term, excluded = count_community_visibility(cleaned_text)
        official_n = ref_n_words.get(doc_id)
        print(
            f"  {doc_id}: cleaner words={info['words_clean']} "
            f"official={official_n} org_vis_mentions={vis_n} "
            f"cut={info['ref_cut_status']}"
        )
        print(f"    scoring community actor roles...")
        roles = analyze_community_roles(rec["text"])
        term_counts[doc_id] = by_term
        excluded_counts[doc_id] = excluded
        new_by_id[doc_id] = {
            "community_visibility_count": vis_n,
            "community_visibility_p10k": _p10k(vis_n, official_n),
            "community_agent": roles["agent"],
            "community_patient": roles["patient"],
            "community_other": roles["other"],
            "community_total": roles["agent"] + roles["patient"] + roles["other"],
            "community_proto_agency": _pct(
                roles["agent"], roles["agent"] + roles["patient"]
            ),
            "cleaner_n_words": info["words_clean"],
        }

    new_fields = [
        "community_visibility_count",
        "community_visibility_p10k",
        "community_combined_visibility_p10k",
        "community_agent",
        "community_patient",
        "community_other",
        "community_total",
        "community_agent_count",
        "community_proto_agency",
        "agency_share_vs_community",
        "community_combined_share_of_agent_roles",
    ]

    rows = []
    for row in existing:
        doc_id = row["doc_id"]
        extra = new_by_id[doc_id]
        person_vis = float(row["person_visibility_p10k"])
        agency_agents = int(row["agency_agent_count"])
        person_agents = int(row["person_agent_count"])
        comm_agents = extra["community_agent"]
        denom = agency_agents + person_agents + comm_agents
        merged = dict(row)
        merged.update({
            "community_visibility_count": extra["community_visibility_count"],
            "community_visibility_p10k": extra["community_visibility_p10k"],
            "community_combined_visibility_p10k": round(
                person_vis + extra["community_visibility_p10k"], 1
            ),
            "community_agent": extra["community_agent"],
            "community_patient": extra["community_patient"],
            "community_other": extra["community_other"],
            "community_total": extra["community_total"],
            "community_agent_count": extra["community_agent"],
            "community_proto_agency": extra["community_proto_agency"],
            "agency_share_vs_community": _pct(agency_agents, denom),
            "community_combined_share_of_agent_roles": _pct(
                person_agents + comm_agents, denom
            ),
        })
        rows.append(merged)
        print(
            f"    {doc_id}: org_vis={extra['community_visibility_p10k']}/10k "
            f"combined_vis={merged['community_combined_visibility_p10k']}/10k "
            f"agency_share_vs_community={merged['agency_share_vs_community']} "
            f"community_agents={comm_agents}"
        )

    csv_path = os.path.join(outdir, "agency_patiency.csv")
    fields = existing_fields + [c for c in new_fields if c not in existing_fields]
    with open(csv_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    print(f"\nSaved {csv_path}")

    # Per-term inventory on cleaned text (documentation, not a new linguistic series).
    all_terms = sorted({t for counts in term_counts.values() for t in counts})
    term_csv = os.path.join(outdir, "community_partner_terms.csv")
    with open(term_csv, "w", newline="") as f:
        w = csv.DictWriter(
            f,
            fieldnames=["term", "excluded_as_person_span_overlap"]
            + sorted(term_counts.keys()),
        )
        w.writeheader()
        for term in all_terms:
            overlap_n = sum(c.get(term, 0) for c in excluded_counts.values())
            rec = {
                "term": term,
                "excluded_as_person_span_overlap": overlap_n,
            }
            for pid, counts in term_counts.items():
                rec[pid] = counts.get(term, 0)
            w.writerow(rec)
    print(f"Saved {term_csv}")

    write_method_note(os.path.join(outdir, "agency_patiency_note.md"), rows)
    print(f"Saved {os.path.join(outdir, 'agency_patiency_note.md')}")


def write_method_note(path, rows):
    draft = next(r for r in rows if r["doc_id"] == "SP-2026-DRAFT")
    sp23 = next(r for r in rows if r["doc_id"] == "SP-2023")
    earlier = [r for r in rows if r["doc_id"] not in ("SP-2023", "SP-2026-DRAFT")]

    def mean_field(items, field):
        vals = [float(r[field]) for r in items]
        return round(sum(vals) / len(vals), 1)

    with open(path, "w") as f:
        f.write("# Agency, visibility, and patiency: federal agencies vs autistic people\n\n")
        f.write("Three measures applied to each IACC strategic plan, contrasting how the text\n")
        f.write("positions federal agencies versus autistic people.\n\n")
        f.write("## Method\n\n")
        f.write("Informed by Hoefer & Martin (SCiL 2026), 'Measuring Perceptions of Personhood\n")
        f.write("with Semantic Proto-role Properties.' The full SPRL neural parser (Spaulding\n")
        f.write("et al. 2023) was not available in this environment; the proxy described below\n")
        f.write("was used instead.\n\n")
        f.write("**1. Visibility** — how often each entity class is named, per 10,000 words.\n")
        f.write("Uses the existing reference taxonomies already coded in the repository:\n")
        f.write("agency acronyms (NIH, CDC, HRSA, CMS, FDA, HHS, IACC, etc.) and autism\n")
        f.write("person-references (autistic people/individuals, people with autism, etc.).\n")
        f.write("Source: `autism_reference_by_plan.csv`.\n\n")
        f.write("**2. Relative agency** — of all agent-role mentions (agency + person), what\n")
        f.write("share belongs to each class? This measures who the document treats as the\n")
        f.write("primary actor when it does assign an actor.\n\n")
        f.write("**3. Proto-role agency share** — for each entity class independently, the\n")
        f.write("share of its predicate-argument mentions in which it occupies the agent role\n")
        f.write("(grammatical subject of active-voice verb) rather than the patient role\n")
        f.write("(direct object or passive subject). This is a dependency-parse proxy for\n")
        f.write("Dowty's (1991) proto-agent properties: +instigation, +volition, +awareness,\n")
        f.write("+sentience, as operationalised by Hoefer & Martin's SPRL cluster (Table 1).\n\n")
        f.write("spaCy (en_core_web_sm) dependency parsing classifies each mention as:\n")
        f.write("- AGENT: grammatical subject of active-voice verb (nsubj, no auxpass)\n")
        f.write("- PATIENT: direct object, or passive subject (dobj, nsubjpass, by-agent)\n")
        f.write("- OTHER: prepositional complement, possessive, appositive, etc.\n\n")
        f.write("Agency share = agent / (agent + patient), excluding OTHER.\n\n")
        f.write("## Results\n\n")
        f.write("| Plan | Agency vis /10k | Person vis /10k | Agency share of agents | Person share of agents | Agency proto-agency | Person proto-agency |\n")
        f.write("|---|---|---|---|---|---|---|\n")
        for r in rows:
            f.write(
                f"| {r['doc_id']} | {r['agency_visibility_p10k']} | {r['person_visibility_p10k']} | "
                f"{float(r['agency_share_of_agent_roles'])*100:.1f}% | "
                f"{float(r['person_share_of_agent_roles'])*100:.1f}% | "
                f"{r['agency_proto_agency']} | {r['person_proto_agency']} |\n"
            )
        f.write("\n## Interpretation\n\n")
        f.write("The draft inverts the visibility relationship (agencies 166.9/10k vs persons\n")
        f.write("108.2/10k) and concentrates agent-role assignment on agencies (80.2% of actor\n")
        f.write("mentions vs 19.8% for autistic people). When agencies do appear in predicate-\n")
        f.write("argument structures, they occupy the agent role 82.2% of the time — the\n")
        f.write("highest in the series. Autistic people's proto-agency share (57.4%) is mid-\n")
        f.write("range, but their relative share of who-acts-in-this-document collapses because\n")
        f.write("agency mentions overwhelm person mentions in agent positions.\n\n")
        f.write("In SP-2023, by contrast, person agent mentions (78) exceeded agency agent\n")
        f.write("mentions (57), giving autistic people a 57.8% share of actor roles. The draft\n")
        f.write("reverses this: agencies hold 80.2% vs persons 19.8%.\n\n")
        f.write("Citation: Hoefer, E. S. & Martin, J. (2026). Measuring Perceptions of\n")
        f.write("Personhood with Semantic Proto-role Properties. Proceedings of the Society\n")
        f.write("for Computation in Linguistics (SCiL) 2026, 1–14.\n\n")

        f.write("## Federal agencies vs autistic people + community/partner organisations\n\n")
        f.write("A seventh comparison folds less-profit-motivated organisations and the people\n")
        f.write("around autistic individuals into one non-agency side: nonprofits, advocacy\n")
        f.write("groups, community partners and members, families, caregivers, parents, and\n")
        f.write("public stakeholders. The two measures are the same as the agency-vs-person\n")
        f.write("pair: visibility (references per 10,000 cleaned words) and relative agency\n")
        f.write("(share of agent-role mentions).\n\n")
        f.write("### Term list, derived from the plan texts\n\n")
        f.write("Candidate stems (`nonprofit`, `advocacy`, `community`, `partner`, `family`,\n")
        f.write("`caregiver`, `parent`, `stakeholder`, `organization`, `foundation`) were\n")
        f.write("concordanced across SP-2009 through the 2026 draft. Entity-referring phrases\n")
        f.write("that the plans actually use were kept; federal, commercial, locative, and\n")
        f.write("topical uses were dropped. Phrases are applied longest-first (sorted by\n")
        f.write("length, not list order) with word-boundary matches; spans do not overlap.\n")
        f.write("Per-term counts: `community_partner_terms.csv`.\n\n")
        f.write("**Included phrases:** advocacy group(s); advocacy organization(s); ")
        f.write("self-advocate(s)/self-advocacy; autistic advocate(s); autism / ASD / ")
        f.write("autistic / disability / broader autism community; community member(s); ")
        f.write("community organization(s); community-based organization(s); community ")
        f.write("partner(s); family member(s); family caregiver(s); families; caregivers ")
        f.write("(plural people-noun only); parents; nonprofit / non-profit / ")
        f.write("not-for-profit *organization(s)* (not the bare adjective); public ")
        f.write("stakeholder(s) (not bare stakeholder); private organization(s); private ")
        f.write("foundation(s); named nonprofits the plans use (Autism Speaks, Simons ")
        f.write("Foundation, Autism Science Foundation, Autistic Self Advocacy Network).\n\n")
        f.write("**Excluded after inspecting contexts:** supporting/lead partners, partner ")
        f.write("agencies, federal/HHS/FDA partners (these name federal agencies in the draft); ")
        f.write("Administration for Community Living (ACL); community settings / living / ")
        f.write("participation / integration / impact (place or metric, not an organisation); ")
        f.write("research/scientific community; family history / studies / burden; parent of ")
        f.write("origin; parent-mediated; caregiver-reported / caregiver-succession and other ")
        f.write("hyphenated topic compounds; singular attributive *caregiver* (caregiver ")
        f.write("burden / supports / training); bare *nonprofit* / *non-profit* / ")
        f.write("*not-for-profit* and bare *stakeholder(s)* (adjective or undifferentiated ")
        f.write("role, not an entity); communication partner (clinical role); ")
        f.write("public-private partnership (includes industry); World Health Organization; ")
        f.write("universities; industry / pharmaceutical firms.\n\n")
        f.write("**Visibility construction.** Community/org mentions are counted on the same\n")
        f.write("cleaned prose as `autism_reference_by_plan.csv` (running headers and reference\n")
        f.write("lists removed; whitespace collapsed as in the notebook) and divided by that\n")
        f.write("file's official word counts. Overlap with notebook `PERSON_REFERRING`\n")
        f.write("(person-first, spectrum, those-with, identity-first, self-advocate /\n")
        f.write("autistic community / autistic-led) is a character-span test, not a\n")
        f.write("phrase-name denylist. A span is withheld only when it is fully covered\n")
        f.write("by a person-referring match (self-advocate*, autistic community). A\n")
        f.write("longer organisation name that merely contains one — Autistic Self\n")
        f.write("Advocacy Network — still counts, as do phrases such as *autistic\n")
        f.write("advocates* that are not in PERSON_REFERRING.\n")
        f.write("Combined visibility = existing `person_p10k` + new community/org rate.\n")
        f.write("Existing agency and person visibility figures are unchanged.\n\n")
        f.write("**Relative agency construction.** Community/org phrases are parsed with the\n")
        f.write("same spaCy proto-role proxy. Combined actor-role share uses the existing\n")
        f.write("agency and person agent counts plus the new community agent counts. Existing\n")
        f.write("80.2% / 19.8% agency-vs-person shares are unchanged.\n\n")
        f.write("### Combined results\n\n")
        f.write("| Plan | Agency vis /10k | Person+community vis /10k | Community/org vis /10k | Agency share of agents vs combined | Combined share of agents |\n")
        f.write("|---|---|---|---|---|---|\n")
        for r in rows:
            f.write(
                f"| {r['doc_id']} | {r['agency_visibility_p10k']} | "
                f"{r['community_combined_visibility_p10k']} | "
                f"{r['community_visibility_p10k']} | "
                f"{float(r['agency_share_vs_community'])*100:.1f}% | "
                f"{float(r['community_combined_share_of_agent_roles'])*100:.1f}% |\n"
            )

        f.write("\n### Comparison: draft vs SP-2023 vs earlier plans\n\n")
        earlier_vis = mean_field(earlier, "community_combined_visibility_p10k")
        earlier_org = mean_field(earlier, "community_visibility_p10k")
        earlier_share = round(
            100 * sum(float(r["community_combined_share_of_agent_roles"]) for r in earlier) / len(earlier),
            1,
        )
        f.write(
            f"Combined person+community visibility: earlier-plan mean {earlier_vis}/10k "
            f"(org/family layer {earlier_org}/10k); SP-2023 "
            f"{sp23['community_combined_visibility_p10k']}/10k "
            f"(org/family {sp23['community_visibility_p10k']}/10k); draft "
            f"{draft['community_combined_visibility_p10k']}/10k "
            f"(org/family {draft['community_visibility_p10k']}/10k). "
            f"Agency visibility remains 166.9/10k in the draft vs 12.2 in SP-2023.\n\n"
        )
        f.write(
            f"Of actor-role mentions when the non-agency side includes community/partner/"
            f"family organisations as well as autistic people: earlier plans give that "
            f"combined side a mean {earlier_share}% of agent roles; SP-2023 gives "
            f"{float(sp23['community_combined_share_of_agent_roles'])*100:.1f}%; "
            f"the draft gives {float(draft['community_combined_share_of_agent_roles'])*100:.1f}% "
            f"(agencies {float(draft['agency_share_vs_community'])*100:.1f}%). "
            f"Widening the non-agency side does not restore the SP-2023 balance. "
            f"Community agent mentions in the draft: {draft['community_agent_count']}; "
            f"in SP-2023: {sp23['community_agent_count']}.\n"
        )


if __name__ == "__main__":
    main()
