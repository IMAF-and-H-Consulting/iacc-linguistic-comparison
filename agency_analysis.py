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
"""

import json
import os
import re
import csv
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


def load_plan_texts():
    cache_dir = ".pdf_cache/iacc_linguistic"
    with open(os.path.join(cache_dir, "cache_manifest.json")) as f:
        manifest = json.load(f)

    plan_ids = [
        "SP-2009", "SP-2010", "SP-2011", "SP-2012", "SP-2013",
        "SP-2017", "SP-2019", "SP-2023", "SP-2026-DRAFT"
    ]

    file_map = {}
    for path, info in manifest.get("files", {}).items():
        file_map[info["sha256"]] = os.path.join(cache_dir, info["sha256"] + ".json")

    texts = {}
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
        texts[pid] = "\n".join(pages)
        print(f"  Loaded {pid}: {len(texts[pid])} chars")

    return texts


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


def main():
    print("Loading plan texts...")
    texts = load_plan_texts()

    print(f"\nAnalyzing {len(texts)} plans...")
    results = []
    for doc_id in sorted(texts.keys()):
        print(f"  Processing {doc_id}...")
        r = analyze_plan(doc_id, texts[doc_id])
        results.append(r)
        ag = r["agency_agency_share"]
        pg = r["person_agency_share"]
        print(f"    agency→agency_share={ag}, person→agency_share={pg}")
        print(f"    agency mentions: agent={r['agency_agent']}, patient={r['agency_patient']}, other={r['agency_other']}")
        print(f"    person mentions: agent={r['person_agent']}, patient={r['person_patient']}, other={r['person_other']}")

    outdir = "outputs/iacc_linguistic"
    csv_path = os.path.join(outdir, "agency_patiency.csv")
    fields = list(results[0].keys())
    with open(csv_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(results)
    print(f"\nSaved {csv_path}")

    md_path = os.path.join(outdir, "agency_patiency_note.md")
    with open(md_path, "w") as f:
        f.write("# Agency and patiency ascribed to federal agencies vs autistic people\n\n")
        f.write("Method: dependency-parse proxy for semantic proto-role labeling\n")
        f.write("(Hoefer & Martin, SCiL 2026, 'Measuring Perceptions of Personhood\n")
        f.write("with Semantic Proto-role Properties').\n\n")
        f.write("The full SPRL parser (Spaulding et al. 2023) was not available;\n")
        f.write("instead, spaCy dependency parsing classifies each entity mention as:\n")
        f.write("- AGENT: grammatical subject of active-voice verb (proto-agent: +instigation, +volition)\n")
        f.write("- PATIENT: direct object, or passive subject (proto-patient: -instigation, -volition)\n")
        f.write("- OTHER: prepositional, possessive, appositive, etc.\n\n")
        f.write("Agency share = agent / (agent + patient), excluding OTHER.\n\n")
        f.write("| Plan | Agency→agent share | Person→agent share | Gap | Agency mentions | Person mentions |\n")
        f.write("|---|---|---|---|---|---|\n")
        for r in results:
            ag = r["agency_agency_share"]
            pg = r["person_agency_share"]
            gap = round(ag - pg, 3) if ag is not None and pg is not None else None
            f.write(f"| {r['doc_id']} | {ag} | {pg} | {gap} | {r['agency_total']} | {r['person_total']} |\n")
        f.write("\nAgency share >0.5 means the entity class is more often the agent (actor)\n")
        f.write("than the patient (acted-upon) in the sentences where it appears.\n")
    print(f"Saved {md_path}")


if __name__ == "__main__":
    main()
