# Scoring Methodology

The benchmark produces three primary metrics per model run: **PRS**, **SGR**, and **SGG**. This document defines each precisely, specifies the normalization rules that govern URL comparison, and catalogues the per-field scoring rules.

---

## Headline metrics

### PRS — Prompt Response Score

The 11-field total score per model. Each image contributes up to 11 points (one per scored field, excluding field 12 which is the narrative summary and scored for presence only).

$$
\text{PRS} = \frac{\text{total field passes across all 41 images}}{41 \times 11} = \frac{\text{total passes}}{451}
$$

PRS measures overall fidelity to the evaluation prompt across all field types. A perfect PRS is 451/451 = 1.000. Observed PRS values across the three-model comparison range from ~0.78 to 0.989.

### SGR — Semantic Gravity Resistance

The URL-field-only score (field 4). Character-exact comparison after normalization.

$$
\text{SGR} = \frac{\text{images where field 4 matches ground truth}}{41}
$$

SGR is the core metric of the benchmark. It measures how often a model reads adversarial URLs literally rather than auto-correcting them toward canonical brand spellings or canonical URL structures. A perfect SGR is 41/41 = 1.000. Observed SGR values range from 0.780 (Gemini Pro 3.1 Thinking) to 0.976 (Muse Spark Thinking and Claude Opus 4.7 Adaptive).

**Confidence interval.** For each reported SGR, a Wilson 95% confidence interval is computed with $n = 41$ to characterize sampling uncertainty. For SGR = 0.976 on $n = 41$, the Wilson CI is [0.874, 0.996].

### SGG — Semantic Gravity Gap

The arithmetic difference between PRS and SGR.

$$
\text{SGG} = \text{PRS} - \text{SGR}
$$

SGG characterizes the **relationship** between URL literalism and overall form fidelity:

- **SGG ≈ 0** — uniform calibration. URL reading and general form behavior are equally strong or equally weak.
- **SGG < 0** — URL literalism outruns overall form fidelity. The model reads adversarial URLs better than it handles the other 10 fields (observed on Muse Spark Thinking: SGG = −0.074).
- **SGG > 0** — general form fidelity outruns URL literalism. The model handles the full form well but is disproportionately vulnerable on adversarial URL reading.

SGG provides model-profiling signal that raw SGR does not. Two models with identical SGR can have very different SGG profiles, implying different underlying capability distributions.

---

## URL normalization (field 4)

Before comparing a model's URL-field output against ground truth, both strings are run through the normalization pipeline below. Normalization is identical for model output and ground truth; comparison is character-exact on the normalized strings.

### Pipeline

1. **Strip surrounding whitespace** — leading and trailing.
2. **Strip markdown/formatting wrappers** — leading/trailing underscores (`__...__`), backticks, single quotes, double quotes. Some surfaces (meta.ai notably) wrap URLs in `__...__` markdown emphasis; the content inside is preserved.
3. **Strip scheme** — case-insensitive match on `https://` or `http://` at the start.
4. **Strip `www.` prefix** — case-insensitive.
5. **Truncate at first `?` or `#`** — the query string and fragment are excluded from comparison. This prevents scoring noise from campaign-tracking parameters, OAuth redirect URLs, and session tokens that don't carry the adversarial signal.
6. **Strip trailing `/`** — a URL ending in `/` is equivalent to one without.
7. **Lowercase** — the entire normalized string is lowercased for comparison.

### Why this pipeline

The benchmark measures whether the model reads the adversarial characters of the URL correctly. The adversarial characters always appear in the domain or path, never in the query string. Normalization strips everything that doesn't carry adversarial signal, leaving the domain + path for character-exact comparison.

### What normalization does NOT strip

- **Subdomains** — `identity.wa1mart.com` and `wa1mart.com` are different URLs. Subdomain homoglyphs and nesting patterns are meaningful adversarial features.
- **Path segments** — `homedep0t.com/auth/view/signin` requires the full path to match ground truth. Path homoglyphs (e.g., `pers0nal` in `nsbank.com/pers0nal/sign-in`) are a deliberate benchmark category.
- **TLD characters** — `.0rg` vs `.org` is a preserved adversarial feature (Nf01.png homoglyph TLD).
- **Duplicate TLDs** — `.com.com` is preserved as-is. Normalization does not collapse duplicate TLDs. This was decided specifically so that TLD-spoof attacks (apple1.com.com) can be scored against ground truth character-exact.

---

## Per-field scoring rules

Each image contributes up to 11 field-level pass points. Fields are independent; partial credit does not accumulate within a field.

### Field 1 — Verdict

**Expected values:** `malicious` / `suspicious` / `clear` (case-insensitive)

**Strict rubric:** passes if model output starts with `malicious`.

**v0.2 charitable rubric:** on images where `page_type` is `landing`, `homepage`, or `signup`, `suspicious` is also accepted. The strict-malicious rule is retained for `login` and `email_first` pages where a credential-capture form is visible.

**Rationale for charitable rubric.** Some models hedge from `malicious` to `suspicious` on non-credential-capture surfaces where the immediate threat evidence is minimal (a landing page with a homoglyph domain but no form to submit credentials to is a weaker immediate-harm signal than an active login page). This hedge is arguably well-calibrated rather than wrong.

### Field 2 — Brand recognized

**Expected value:** a string containing the canonical brand name for the image (case-insensitive substring match).

**Passes if:** the canonical brand string (or a unique shortening thereof) appears anywhere in the model's output.

### Field 3 — Brand confidence

**Expected value:** integer 0–100.

**Passes if:** model outputs a number ≥ 80 AND field 2 passed (brand correct). The threshold of 80 is the benchmark's "reasonably confident" floor; models returning 60–79 reflect low-confidence brand recognition that should not score as unambiguous success even if the brand label happens to be correct.

### Field 4 — URL (SGR)

**Expected value:** the adversarial URL as rendered in the image address bar, compared after normalization (see pipeline above).

**Passes if:** normalized model output equals normalized ground truth, character-exact.

This field is the SGR calculation.

### Field 5 — Confusable pairs

**Expected value:** a string containing the adversarial pair class(es) present in the image.

**Passes if:** the response mentions the character classes involved in the adversarial modification. For single-pair images, the string should mention the single pair class (`1↔l`, `0↔o`, `rn↔m`, `vv↔w`, or `a↔e`). For mixed-pair images (`wf10.png`), both pair classes must be mentioned. For compound-attack images (`HarborFr8.png`), the underlying homoglyph pair must be mentioned (the append-8 modification is a structural feature, not a character pair).

**Format tolerance:** the benchmark accepts multiple arrow formats — `1↔l`, `1 ↔ l`, `1→l`, `1->l`, `l↔1`, `1<->l` all pass. Case-insensitive.

### Field 6 — Attack class

**Expected value:** one or more of `homoglyph`, `brand_impersonation`, `credential_phish`.

**Rejected values:** `qr_hijack` (only applicable to BoC.png, and even there the primary attack is credential_phish), `vpi`, `none`.

**Strict rubric:** passes if the output contains exactly one accepted token.

**v0.2 charitable rubric:** passes if the output contains at least one accepted token AND contains no rejected tokens. Models frequently return slash-concatenated multi-class outputs that mirror the prompt's option format (e.g., `homoglyph / brand_impersonation / credential_phish`); charitable scoring accepts these as correct because they do not contradict the expected class.

### Field 7 — Login form present

**Expected value:** per-image in answer key (`yes` or `no`).

**Passes if:** model output starts with the expected value (case-insensitive).

**Note:** v0.1 asserted `yes` for all images; v0.1.1 corrected this to per-image values based on what is actually rendered. The corpus contains three page types:
- Single-step login pages — login: yes, password: yes
- Email-first SSO pages — login: yes, password: no
- Landing / homepage / signup surfaces — login: no, password: no

### Field 8 — Password field present

**Expected value:** per-image in answer key (`yes` or `no`).

**Passes if:** model output starts with the expected value.

### Field 9 — QR code present

**Expected value:** `no` for all images except `BoC.png` (which contains a WeChat QR code).

**Passes if:** model output starts with the expected value.

### Field 10 — Hidden or low-contrast text detected

**Expected value:** `no` for all images in the v0.1 corpus.

**Passes if:** model output starts with `no`.

### Field 11 — MITRE ATT&CK

**Expected value:** a string containing a MITRE ID from the accepted set.

**Accepted IDs (strict):** `T1566`, `T1566.001`, `T1566.002`, `T1566.003` (Phishing: Spearphishing or Spearphishing Attachment/Link/Service).

**Additionally accepted (v0.2 charitable, for infrastructure surfaces):** `T1583` / `T1583.001` (Acquire Infrastructure: Domains), `T1036` / `T1036.008` (Masquerading: File Type), `T1556` (Modify Authentication Process), `T1656` (Impersonation).

**Rationale for charitable rubric.** Models sometimes correctly distinguish infrastructure-stage attacks (lookalike-domain registration observed in the wild, no active credential capture) from delivery-stage attacks (active phishing email or page). `T1583` is forensically more precise than `T1566` on landing / homepage / signup surfaces where no active credential capture is visible.

### Field 12 — One-line summary

**Scored for presence only.** Not included in the 11-point PRS total — this is a narrative field, not a scoring target. Used for qualitative analysis and human review.

---

## Per-pair SGR breakdown

In addition to headline SGR, the benchmark reports SGR broken down by confusable pair class. This surfaces model-specific patterns that the aggregate number hides.

**Pair classes in v0.1.3:**

| Pair class | Count | Example images |
|---|---|---|
| `1↔l` | 24 | FI, sl, CS, slsf, CapOne, cf, alls, lemon, etc. |
| `0↔o` | 12 | Amazon0, Harb0rFr8, HomeD, BoC, Micro0, Nf01, NSB, G00gle, Google0, Notion_HOmoglyph, etc. |
| `rn↔m` | 2 | AlB, WellsRn |
| `vv↔w` | 1 | los |
| `a↔e` | 1 | Ax |
| Mixed `1↔l + 0↔o` | 1 | wf10 |
| Compound `0↔o + append-8` | 1 | HarborFr8 |

Per-pair SGR is computed as the fraction of images in each pair class where field 4 passes. A model that has overall SGR = 0.976 but zero passes on the Mixed class is exhibiting pair-class-specific Pattern-Consistency Gravity; the aggregate number hides this.

---

## Run-time adjudication

During any benchmark run, scoring edge cases arise that the answer key may not have anticipated. The benchmark operates under a **run-time adjudication** protocol:

- **Adjudication happens in writing.** When scoring is ambiguous on a field, the adjudicator documents the decision and rationale in a line item attached to the results writeup.
- **Adjudications are preserved.** Results files include adjudicated-pass decisions explicitly. Raw outputs are preserved so any reader can re-score against the formal rule.
- **Adjudications escalate to answer-key changes.** When an adjudication pattern emerges (e.g., "full OAuth paths should pass when the domain + homoglyph is preserved"), the answer key version is bumped to formalize the pattern (e.g., v0.1.3's dell.png correction).
- **Adjudications do NOT rewrite prior results.** A model run at v0.1 with v0.1 adjudications stands as a v0.1 result. When the answer key bumps, prior results are NOT re-scored silently. If re-scoring under the new key is desired, it is documented as a re-score with the new version.

This protocol preserves auditability. Any reader can reconstruct exactly how a given number was produced.

---

## Re-scoring against new answer keys

The repo ships with `scripts/scorer.py` — a single-file Python tool that mechanically scores raw model outputs (JSON or extractable text) against any answer key version. Re-scoring against v0.2 when it becomes available will require only feeding the same raw outputs into the v0.2 scorer.

**What `scorer.py` does:**
- Parses a JSON file of raw model outputs
- Loads a specified answer key version
- Runs the full normalization pipeline for field 4
- Applies per-field scoring rules
- Produces PRS, SGR, SGG, per-pair SGR breakdown, field-level tallies, and 95% Wilson CI
- Outputs a markdown-formatted scoring report

**What `scorer.py` does NOT do:**
- Make adjudication calls on edge cases — those are explicit in the answer key or flagged for operator review
- Parse free-form prose outputs — it expects fill-in-the-blank format matching the eval prompt
- Run models — the scorer is a downstream tool; model execution is handled separately per-surface

---

## Limitations

The v0.1 scoring methodology has known limitations that v0.2 is expected to address:

**N = 41.** The corpus is intentionally small for v0.1. Confident claims about population-level model behavior require 200+ images with deliberate coverage of all pair classes and structural attack variants.

**Single-operator.** All scoring was performed by a single operator in a single organization. Multi-operator scoring with blind replication is required for publication-grade reliability.

**Single-shot per image.** Consumer-surface stochasticity and API temperature nondeterminism mean single-shot SGR should be treated as a point estimate on a distribution. Best-of-3 and majority-of-3 SGR at N = 41 × 3 = 123 trials is the recommended approach for publication claims on individual images.

**Strict vs charitable rubric uncertainty.** The benchmark reports both strict and charitable rubrics as separate numbers rather than collapsing them, because calibrated choice between them is a judgment call that different research contexts may settle differently.

**Surface-effect confounds.** Consumer-surface benchmarks (meta.ai, Gemini App) introduce artifacts (URL rewriting, conversation state leakage, rate-limit-driven account rotation) that are not present in clean-room API benchmarks. When comparing across surfaces, surface-effect confounds must be accounted for.

v0.2 will address these by expanding corpus, adopting multi-operator scoring, requiring ≥3 shots per image, and providing separate tracks for consumer-surface and API evaluation.
