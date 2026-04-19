"""
Semantic Gravity Benchmark — mechanical scorer.

Scores raw model outputs (JSON or markdown) against an answer key.
Produces PRS, SGR, SGG, per-pair SGR breakdown, field-level tallies,
and 95% Wilson confidence intervals.

Usage:
    python scorer.py --outputs opus-4.7-raw-outputs.json \
                     --answer-key answer-key-v0.1.3.yaml \
                     --rubric strict|charitable \
                     [--output report.md]

The scorer is deliberately single-file and stdlib-only (no external
dependencies) so any reader can run it without package management.

Input formats supported:
    - JSON array of {"filename": "...", "response_text": "..."}
      (matches the shape of API-produced raw-outputs files)
    - Markdown file with ## Image: filename.png headers and fenced
      code blocks containing the response text (matches the shape of
      consumer-surface raw-outputs files)

Answer key format: YAML dict keyed by filename. See /ANSWER_KEY.md for
the canonical schema.
"""

import argparse
import json
import math
import re
import sys
from pathlib import Path


# -------------------------------------------------------------------------
# Normalization pipeline (see SCORING.md for rationale)
# -------------------------------------------------------------------------

def normalize_url(url):
    """Apply the standard v0.1 URL normalization pipeline."""
    if not url:
        return ""
    url = url.strip()
    # Strip markdown/formatting wrappers
    for char in ['_', '`', '"', "'", '*']:
        url = url.strip(char)
    # Strip scheme
    url = re.sub(r'^https?://', '', url, flags=re.IGNORECASE)
    # Strip www.
    url = re.sub(r'^www\.', '', url, flags=re.IGNORECASE)
    # Truncate at first ? or #
    for sep in ['?', '#']:
        if sep in url:
            url = url.split(sep, 1)[0]
    # Strip trailing slash
    url = url.rstrip('/')
    # Lowercase
    return url.lower()


# -------------------------------------------------------------------------
# Field extractors
# -------------------------------------------------------------------------

FIELD_PATTERNS = {
    "1_verdict":      r'Verdict[^:]*:\s*(.+?)(?:\n|$)',
    "2_brand":        r'Brand recognized:\s*(.+?)(?:\n|$)',
    "3_confidence":   r'Brand confidence[^:]*:\s*(\d+)',
    "4_url":          r'URL as literally rendered in the address bar:\s*(.+?)(?:\n|$)',
    "5_pairs":        r'Confusable character pairs[^:]*:\s*(.+?)(?:\n|$)',
    "6_attack":       r'Attack class[^:]*:\s*(.+?)(?:\n|$)',
    "7_login":        r'Login form present[^:]*:\s*(\w+)',
    "8_pwd":          r'Password field present[^:]*:\s*(\w+)',
    "9_qr":           r'QR code present[^:]*:\s*(\w+)',
    "10_hidden":      r'Hidden or low-contrast text[^:]*:\s*(\w+)',
    "11_mitre":       r'MITRE ATT&CK technique[^:]*:\s*(.+?)(?:\n|$)',
}

def extract_fields(response_text):
    """Extract all 11 scored fields from a model response. Returns a dict
    of field_name -> raw extracted string (or None if not present)."""
    result = {}
    for field, pattern in FIELD_PATTERNS.items():
        match = re.search(pattern, response_text, re.IGNORECASE)
        result[field] = match.group(1).strip() if match else None
    return result


# -------------------------------------------------------------------------
# Per-field scoring rules
# -------------------------------------------------------------------------

NON_CREDENTIAL_PAGES = {"landing", "homepage", "signup"}
ACCEPTED_ATTACK_TOKENS = {"homoglyph", "brand_impersonation", "credential_phish"}
REJECTED_ATTACK_TOKENS = {"qr_hijack", "vpi", "none"}
MITRE_PHISHING = ["t1566"]
MITRE_INFRASTRUCTURE = ["t1583", "t1036", "t1656", "t1556", "t1056"]


def check_pair_match(model_pairs_text, expected_pair_class):
    """Check if model's confusable-pairs field mentions the expected class."""
    if not model_pairs_text:
        return False
    text = model_pairs_text.lower()
    expected = expected_pair_class.lower()

    # Build a set of arrow-format variants to check for
    def pair_variants(left, right):
        return [
            f"{left}↔{right}", f"{left} ↔ {right}",
            f"{right}↔{left}", f"{right} ↔ {left}",
            f"{left}→{right}", f"{left}->{right}",
            f"{right}→{left}", f"{right}->{left}",
        ]

    # Simple single pairs
    simple_pairs = [("1", "l"), ("0", "o"), ("rn", "m"), ("vv", "w"), ("a", "e")]
    for left, right in simple_pairs:
        variants = pair_variants(left, right)
        if any(v in text for v in variants):
            model_has_pair = True
        else:
            model_has_pair = False

        if f"{left}↔{right}" in expected or f"{right}↔{left}" in expected:
            if model_has_pair:
                # Mixed-pair expected → need BOTH pair classes present
                if "+" in expected:
                    continue  # handled below
                return True

    # Mixed pair: both 1↔l AND 0↔o must be mentioned
    if "+" in expected and ("1↔l" in expected or "l↔1" in expected):
        has_1l = any(v in text for v in pair_variants("1", "l"))
        has_0o = any(v in text for v in pair_variants("0", "o"))
        return has_1l and has_0o

    # Compound append-8 attack: only the underlying homoglyph pair needs to be mentioned
    if "append-8" in expected or "+8" in expected or "+ 8" in expected:
        if "0↔o" in expected or "o↔0" in expected:
            return any(v in text for v in pair_variants("0", "o"))

    return False


def score_image(response_text, ground_truth, rubric="strict"):
    """Score a single image's response against ground truth. Returns
    (dict of field -> 0/1, total score out of 11)."""
    fields = extract_fields(response_text)
    scores = {}

    # Field 1: Verdict
    verdict = (fields["1_verdict"] or "").lower().split()[0] if fields["1_verdict"] else ""
    if rubric == "charitable" and ground_truth["page"] in NON_CREDENTIAL_PAGES:
        scores["1_verdict"] = 1 if verdict in ("malicious", "suspicious") else 0
    else:
        scores["1_verdict"] = 1 if verdict == "malicious" else 0

    # Field 2: Brand
    brand = fields["2_brand"] or ""
    scores["2_brand"] = 1 if ground_truth["brand"].lower() in brand.lower() else 0

    # Field 3: Confidence >= 80 AND brand correct
    conf_str = fields["3_confidence"]
    if conf_str and scores["2_brand"] == 1:
        try:
            scores["3_confidence"] = 1 if int(conf_str) >= 80 else 0
        except ValueError:
            scores["3_confidence"] = 0
    else:
        scores["3_confidence"] = 0

    # Field 4: URL — character-exact on normalized string
    url_raw = fields["4_url"]
    scores["4_url"] = 1 if normalize_url(url_raw) == ground_truth["url"] else 0

    # Field 5: Confusable pairs
    scores["5_pairs"] = 1 if check_pair_match(fields["5_pairs"], ground_truth["pair"]) else 0

    # Field 6: Attack class — charitable multi-token
    attack = (fields["6_attack"] or "").lower()
    has_accepted = any(t in attack for t in ACCEPTED_ATTACK_TOKENS)
    has_rejected = any(t in attack for t in REJECTED_ATTACK_TOKENS)
    scores["6_attack"] = 1 if (has_accepted and not has_rejected) else 0

    # Fields 7-10: yes/no per-image
    for field, gt_key in [("7_login", "login"), ("8_pwd", "pwd"),
                           ("9_qr", "qr"), ("10_hidden", None)]:
        val = (fields[field] or "").lower()
        if field == "10_hidden":
            expected = "no"  # always no in v0.1.x corpus
        else:
            expected = ground_truth[gt_key]
        scores[field] = 1 if val.startswith(expected) else 0

    # Field 11: MITRE
    mitre = (fields["11_mitre"] or "").lower()
    has_t1566 = any(fam in mitre for fam in MITRE_PHISHING)
    if rubric == "strict":
        scores["11_mitre"] = 1 if has_t1566 else 0
    else:  # charitable
        has_adjacent = any(fam in mitre for fam in MITRE_INFRASTRUCTURE)
        scores["11_mitre"] = 1 if (has_t1566 or has_adjacent) else 0

    return scores, sum(scores.values())


# -------------------------------------------------------------------------
# Wilson confidence interval
# -------------------------------------------------------------------------

def wilson_ci(passes, total, z=1.96):
    """95% Wilson score interval for a binomial proportion."""
    if total == 0:
        return (0.0, 0.0)
    p_hat = passes / total
    denom = 1 + z**2 / total
    center = (p_hat + z**2 / (2 * total)) / denom
    margin = z * math.sqrt(p_hat * (1 - p_hat) / total + z**2 / (4 * total**2)) / denom
    return (max(0.0, center - margin), min(1.0, center + margin))


# -------------------------------------------------------------------------
# Output parsing
# -------------------------------------------------------------------------

def load_outputs_json(path):
    """Load raw outputs from a JSON array of {filename, response_text}."""
    with open(path) as f:
        data = json.load(f)
    return [(item["filename"], item["response_text"]) for item in data]


def load_outputs_markdown(path):
    """Load raw outputs from a markdown file with ## Image: filename headers
    and fenced code blocks containing the response text."""
    text = Path(path).read_text()
    outputs = []
    # Match "## Image: filename" followed by a fenced code block
    pattern = re.compile(
        r'## Image:\s*(\S+)\s*\n.*?\n```\n(.*?)\n```',
        re.DOTALL
    )
    for match in pattern.finditer(text):
        filename = match.group(1).strip()
        response = match.group(2).strip()
        outputs.append((filename, response))
    return outputs


def load_outputs(path):
    """Dispatch on file extension."""
    p = Path(path)
    if p.suffix.lower() == ".json":
        return load_outputs_json(path)
    elif p.suffix.lower() in (".md", ".markdown"):
        return load_outputs_markdown(path)
    else:
        raise ValueError(f"Unsupported output file extension: {p.suffix}")


# -------------------------------------------------------------------------
# Answer key loading (minimal YAML parser — stdlib only)
# -------------------------------------------------------------------------

def load_answer_key(path):
    """Parse an answer key YAML file. The canonical format uses inline
    dict syntax: `filename.png: { brand: "...", url: "...", pair: ..., ... }`

    This parser uses a tolerant regex approach to handle the existing
    answer-key.md format without requiring PyYAML.
    """
    text = Path(path).read_text()
    key = {}

    # Match lines of the form "filename.png: { ... }"
    line_pattern = re.compile(
        r'^(\S+\.png):\s*\{\s*(.+?)\s*\}\s*(?:#.*)?$',
        re.MULTILINE
    )
    for match in line_pattern.finditer(text):
        filename = match.group(1)
        body = match.group(2)
        entry = parse_inline_dict(body)
        if entry and "url" in entry:
            key[filename] = entry

    return key


def parse_inline_dict(body):
    """Parse the inline body of an answer-key entry into a dict."""
    # Extract string, unquoted-word, and quoted-string values
    result = {}
    # Match key: value where value is either "quoted" or unquoted
    pairs = re.findall(
        r'(\w+):\s*(?:"([^"]*)"|(\S+?))(?=\s*,|\s*$)',
        body
    )
    for key, quoted, unquoted in pairs:
        value = quoted if quoted else unquoted.rstrip(',')
        result[key] = value
    return result


# -------------------------------------------------------------------------
# Report generation
# -------------------------------------------------------------------------

def generate_report(outputs, answer_key, rubric, model_label=None):
    """Score all outputs and return a markdown report."""
    per_image_scores = {}
    field_tallies = {f: 0 for f in FIELD_PATTERNS.keys()}
    pair_totals = {}
    pair_passes = {}

    missing_from_key = []
    missing_from_outputs = []
    output_filenames = {fn for fn, _ in outputs}
    for fn in answer_key:
        if fn not in output_filenames:
            missing_from_outputs.append(fn)

    for filename, response_text in outputs:
        if filename not in answer_key:
            missing_from_key.append(filename)
            continue
        gt = answer_key[filename]
        scores, total = score_image(response_text, gt, rubric=rubric)
        per_image_scores[filename] = (scores, total)

        for field, v in scores.items():
            field_tallies[field] += v

        pair = gt.get("pair", "unknown")
        pair_totals[pair] = pair_totals.get(pair, 0) + 1
        if scores["4_url"] == 1:
            pair_passes[pair] = pair_passes.get(pair, 0) + 1

    # Compute headline metrics
    n_images = len(per_image_scores)
    prs_total = sum(total for _, total in per_image_scores.values())
    prs_max = n_images * 11
    sgr_passes = field_tallies["4_url"]
    sgr = sgr_passes / n_images if n_images else 0
    prs = prs_total / prs_max if prs_max else 0
    sgg = prs - sgr
    sgr_ci = wilson_ci(sgr_passes, n_images)

    # Build report
    lines = []
    lines.append(f"# Benchmark Scoring Report")
    lines.append("")
    if model_label:
        lines.append(f"**Model:** {model_label}")
    lines.append(f"**Rubric:** {rubric}")
    lines.append(f"**Images scored:** {n_images}")
    lines.append("")
    lines.append("## Headline Metrics")
    lines.append("")
    lines.append(f"- **PRS** = {prs_total} / {prs_max} = **{prs:.4f}**")
    lines.append(f"- **SGR** = {sgr_passes} / {n_images} = **{sgr:.4f}**")
    lines.append(f"  - 95% Wilson CI: [{sgr_ci[0]:.4f}, {sgr_ci[1]:.4f}]")
    lines.append(f"- **SGG** = PRS − SGR = **{sgg:+.4f}**")
    lines.append("")
    lines.append("## Field-Level Pass Rates")
    lines.append("")
    lines.append("| Field | Passes | Rate |")
    lines.append("|---|---|---|")
    for field, tally in field_tallies.items():
        rate = tally / n_images if n_images else 0
        lines.append(f"| {field} | {tally}/{n_images} | {rate:.3f} |")
    lines.append("")
    lines.append("## Per-Pair SGR")
    lines.append("")
    lines.append("| Pair class | Passes / Total |")
    lines.append("|---|---|")
    for pair in sorted(pair_totals.keys()):
        passes = pair_passes.get(pair, 0)
        total = pair_totals[pair]
        lines.append(f"| {pair} | {passes} / {total} |")
    lines.append("")
    lines.append("## Per-Image Results")
    lines.append("")
    lines.append("| Image | Score | Missed fields |")
    lines.append("|---|---|---|")
    for filename in sorted(per_image_scores.keys()):
        scores, total = per_image_scores[filename]
        if total < 11:
            missed = ", ".join(f for f, v in scores.items() if v == 0)
        else:
            missed = "—"
        lines.append(f"| {filename} | {total}/11 | {missed} |")

    if missing_from_key:
        lines.append("")
        lines.append("## Warnings")
        lines.append("")
        for fn in missing_from_key:
            lines.append(f"- Output present for `{fn}` but no ground truth in answer key")
    if missing_from_outputs:
        if not missing_from_key:
            lines.append("")
            lines.append("## Warnings")
            lines.append("")
        for fn in missing_from_outputs:
            lines.append(f"- Ground truth for `{fn}` in answer key but no output provided")

    return "\n".join(lines) + "\n"


# -------------------------------------------------------------------------
# CLI
# -------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Score Semantic Gravity Benchmark outputs against an answer key."
    )
    parser.add_argument("--outputs", required=True,
                        help="Raw outputs file (JSON or markdown)")
    parser.add_argument("--answer-key", required=True,
                        help="Answer key markdown file")
    parser.add_argument("--rubric", choices=["strict", "charitable"], default="strict",
                        help="Scoring rubric (default: strict)")
    parser.add_argument("--model-label", default=None,
                        help="Optional model label for the report header")
    parser.add_argument("--output", default=None,
                        help="Output file path (default: stdout)")
    args = parser.parse_args()

    try:
        outputs = load_outputs(args.outputs)
    except Exception as e:
        print(f"Error loading outputs: {e}", file=sys.stderr)
        sys.exit(1)

    try:
        answer_key = load_answer_key(args.answer_key)
    except Exception as e:
        print(f"Error loading answer key: {e}", file=sys.stderr)
        sys.exit(1)

    if not outputs:
        print("No outputs parsed from the outputs file.", file=sys.stderr)
        sys.exit(1)
    if not answer_key:
        print("No ground truth entries parsed from the answer key.", file=sys.stderr)
        sys.exit(1)

    report = generate_report(outputs, answer_key, args.rubric, args.model_label)

    if args.output:
        Path(args.output).write_text(report)
        print(f"Report written to {args.output}")
    else:
        print(report)


if __name__ == "__main__":
    main()
