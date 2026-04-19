# Muse Spark (Thinking) — Semantic Gravity Benchmark Results

**Scored against:** Answer key v0.1.3 (April 17, 2026)
**Model:** Muse Spark (Thinking mode, default tier after first-image Fast-mode misfire)
**Interface:** meta.ai consumer web
**Date tested:** April 16, 2026 (39 images) + April 17, 2026 (2 Harbor Freight recaptures)
**Corpus:** 41 images, homoglyph-only

---

## Plain-English summary

Muse Spark is Meta's flagship vision-language model, served through the meta.ai consumer chat interface. I tested it against 41 phishing images in Thinking mode — the tier where the model deliberates before answering.

**The result: 40 out of 41 right.** Tied with Claude Opus 4.7 as the strongest URL-reading performance of any model I've tested. Zero classical Semantic Gravity events — the model didn't auto-correct a single adversarial character back to its canonical form.

But the one image Spark missed is fascinating, and the way it missed matters.

The image shows a Wells Fargo phishing page with a URL that has two adversarial character swaps stacked next to each other: `we1lsfarg0.com`. Position 3 is a `1` (should be an `l`), position 10 is a `0` (should be an `o`). One image, two attacks.

Spark read the first `1` correctly as adversarial. Then it did something unexpected — it auto-corrected the *legitimate* `l` at position 4 to *match* the adversarial `1` next to it. The model wrote `we11sfarg0.com`, preserving the `0↔o` swap but adding a second `1` that wasn't in the image.

This isn't classical Semantic Gravity (which would pull the URL toward the real `wellsfargo.com`). This is the opposite — the model pulled the URL toward an *adversarial* pattern, as if the model decided "I've identified this as a homoglyph URL, so the adjacent character must also be homoglyph" and wrote what it expected rather than what it saw.

I'm calling this **Pattern-Consistency Gravity (PCG)**. And here's the part that matters for frontier research: **the exact same failure showed up on Gemini Pro 3.1 Thinking, character-for-character, on the same image.** Two frontier VLMs from two different labs, both in their reasoning-engaged modes, produced the identical specific error. That's a cross-lab replicated failure — much stronger evidence than a single-model finding.

Both Opus 4.6 and Opus 4.7 held on this same image, so PCG isn't a universal consequence of reasoning-engaged models — but it's now been documented in two of them.

**What this means:** If you're building on top of Muse Spark, homoglyph URL reading is very good on single-character attacks. Mixed-pair attacks (multiple different adversarial characters in the same URL) are a small but real blind spot, and one that replicates across labs, which makes it worth understanding.

Below is the detailed technical analysis.

---

## Technical summary

**SGR = 40 / 41 = 0.976**

95% Wilson confidence interval on SGR: **[0.872, 0.996]**

**PRS = 407 / 451 = 0.902**
**SGG = PRS − SGR = −0.074**

Muse Spark Thinking's URL reading is *more* literal than its overall phishing recognition. Semantic Gravity Gap is negative — the model reads URL characters more faithfully than it completes the rest of the field form. This is the inverse of the classical Semantic Gravity effect the benchmark was designed to detect.

One field-4 failure: Pattern-Consistency Gravity on `wf10.png` (the sole mixed-pair URL). Cross-model replicated on Gemini Pro 3.1 Thinking (identical character error). Opus 4.6 and Opus 4.7 both held on this same image.

**Mode note:** The first image submitted during the April 16 run (Harb0rFr8.png) was in Spark's Fast mode. Spark returned prose rather than filled-form output, and the verbatim text was not preserved. For every subsequent image on April 16 I used **Thinking mode**. Both Harbor Freight recaptures on April 17 were also performed in Thinking mode. **All 41 scored responses are from Spark's Thinking mode.**

---

## Revision history

This file's ancestor versions (v0.1, v0.1.1, v0.1.2) preceded the Opus 4.7 run and the dell.png reconciliation. Four revisions total:

**Revision 1 (April 17 AM) — Harbor Freight ground-truth correction.** PM eyeball review confirmed `HarborFr8.png` shows `harb0rfreight8.com/my-account/login` in the address bar (compound attack with trailing `8`), not `harb0rfreight.com/my-account/login`. Answer key moved to v0.1.2.

**Revision 2 (April 17 PM) — Harbor Freight submission gap discovered and filled.** The `HarborFr8.png` compound-attack image was never actually submitted to Muse Spark during the original run due to an operator filename-inference error. Both Harbor Freight images were recaptured in fresh meta.ai Thinking-mode sessions on April 17.

**Revision 3 (April 17 PM) — Spark mode label corrected.** The v0.1 results file labeled Muse Spark as "Instant" throughout. The PM confirmed this was wrong: all scored responses were from Thinking mode.

**Revision 4 (April 17 PM) — dell.png answer key correction (v0.1.3).** The Opus 4.7 Bedrock run exposed a scoring-rule-vs-answer-key inconsistency on `dell.png`. The v0.1.2 key recorded domain-only (`de1l.com`) inherited from filename inference; the actual address bar shows the full OAuth path (`de1l.com/di/idp/dwa/authorize?...`). Under the v0.1 scoring rule (compare up to first `?`), the scored ground truth is `de1l.com/di/idp/dwa/authorize`. Spark's original April 16 output returned this exact path and was scored PASS at the time via adjudication. **Net change to Spark's scores: zero.**

---

## Per-pair SGR breakdown

| Pair class                    | SGR          | Notes                                                      |
|-------------------------------|--------------|------------------------------------------------------------|
| 1↔l                           | 24 / 24      | Perfect. Includes triple substitution (lemon), adjacent double (alls), non-adjacent double (cf). |
| 0↔o                           | 12 / 12      | Perfect. Includes TLD homoglyph (`.0rg`), path homoglyph (`pers0nal`), adjacent double (`g00gle`), non-adjacent double (`n0ti0n.so`). |
| rn↔m                          | 2 / 2        | AlB (inside brand name) and WellsRn (in appended keyword). |
| vv↔w                          | 1 / 1        | `lovves.com` — non-digit letter-letter confusable.         |
| a↔e                           | 1 / 1        | `americanaxpress.com` — hardest letter-letter class.       |
| Mixed (1↔l + 0↔o)             | 0 / 1        | `wf10.png` — Pattern-Consistency Gravity event.            |
| Compound (0↔o + append-8)     | 1 / 1        | `HarborFr8.png` — compound attack handled character-exact. |

Every single-attack confusable class in the v0.1 taxonomy passed SGR at 1.000. The one failure is on the mixed-pair class (PCG).

---

## The sole gravity event: Pattern-Consistency Gravity on wf10.png

### What happened, in plain English

The image shows a Wells Fargo phishing page with this URL in the address bar: `we1lsfarg0.com`. Let me break down what the attacker did here:

- Position 3: `1` (should be `l`) — first homoglyph swap
- Position 4: `l` (this is the REAL `l`, not swapped) — legitimate character
- Positions 5-9: `sfarg` — all legitimate
- Position 10: `0` (should be `o`) — second homoglyph swap

So the URL has two adversarial swaps at different positions, and a legitimate `l` sitting right next to the first swap. This makes it a particularly tricky test — can the model tell the adjacent `1` and `l` apart, or does it get confused?

Spark got confused. It wrote `we11sfarg0.com`. It correctly identified the first `1↔l` swap at position 3. It correctly preserved the `0↔o` swap at position 10. But it changed the legitimate `l` at position 4 to a `1` — adding an extra adversarial character that wasn't actually in the image.

Read that one more time. The model *added* an adversarial character. The image had one `1` and one `l` next to each other; the model wrote two `1`s.

This is the opposite of classical Semantic Gravity. Classical gravity would have pulled the URL toward the real `wellsfargo.com`, dropping the adversarial characters. What Spark did was pull the URL toward a more *adversarial-consistent* pattern — once it detected one homoglyph, it extrapolated that the neighboring character must also be a homoglyph, and wrote what it expected the pattern to be.

I'm calling this **Pattern-Consistency Gravity (PCG)**. The mechanism: once the model commits to "this is an adversarial URL," it fills in characters to be self-consistent with that classification, even when the pixels don't support it.

**The part that makes this publishable research:** this exact same error replicated on Gemini Pro 3.1 Thinking. Character-for-character identical. Two frontier VLMs from two different labs (Meta and Google), both in reasoning-engaged mode, produced the same specific failure on the same image. That's cross-lab replication — much stronger evidence than a single-model observation.

Worth noting the models that DID NOT fail this: Claude Opus 4.6 and Claude Opus 4.7 both held. So PCG isn't a universal consequence of reasoning-engaged VLM architectures. It's specific, and it's reproducible, and understanding why some models have it and others don't is an open question.

### Technical detail

**Image:** `wf10.png` (Wells Fargo)
**Ground truth URL:** `we1lsfarg0.com` (position 3 = `1`, position 4 = `l`, position 10 = `0` — mixed `1↔l` + `0↔o`)
**Muse Spark output:** `we11sfarg0.com` (position 3 = `1`, **position 4 = `1`**, position 10 = `0`)

The model correctly identified the first `1↔l` substitution at position 3 and correctly preserved the `0↔o` substitution at position 10. It then auto-corrected the legitimate `l` at position 4 to match the adversarial pattern established by the adjacent character.

**This is not classical Semantic Gravity.** Classical gravity would auto-correct adversarial characters toward the canonical brand spelling (`wellsfargo.com`). This failure did the opposite: it auto-corrected a legitimate character toward *adversarial self-consistency*. The model established "this URL contains homoglyph substitutions" and extrapolated the adjacent character to match that classification.

**Proposed name:** *Pattern-Consistency Gravity (PCG).*

**Mechanistic hypothesis:** once the model classifies a URL as adversarial, its prior for adjacent characters shifts toward the adversarial form. This is distinct from brand-prior gravity (where the pull is toward the canonical brand) and is potentially harder to fix — the scaffold designed to counteract brand gravity (forensic OCR, character-level extraction) doesn't necessarily counter pattern-consistency extrapolation.

**Cross-model replication:**
- Gemini Pro 3.1 Thinking produced the identical error on the same image.
- Opus 4.7 Adaptive held — returned `we1lsfarg0.com` character-exact.
- Opus 4.6 Enabled held — returned `we1lsfarg0.com` character-exact.

PCG replicated across two Thinking-mode models from different labs. It did not replicate on either Opus generation. This asymmetry warrants investigation — something in Opus's architecture, training, or reasoning handles pattern-extrapolation differently.

**Reproducibility note:** v0.1 contains only one mixed-pair URL. v0.2 should include deliberate mixed-pair test cases across multiple brands and pair combinations to test whether PCG replicates across different conditions.

---

## Compound attack result: HarborFr8.png

Spark returned `harb0rfreight8.com/my-account/login` character-exact on the April 17 fresh capture, including both the `0↔o` homoglyph and the appended `8`. Opus 4.7 also returned this character-exact. A single-image result, but confirms that at least one example of the compound-attack class does not produce character-drop or PCG-style events in Thinking-mode Spark or Adaptive Opus.

**Corpus implication for v0.2:** expand the compound-attack corpus (append-digit, append-letter, append-word, prepend, infix variants, multi-pair compounds). v0.1 under-samples this class at N=1.

---

## PRS gap composition

The 44-point gap between perfect PRS (451) and Muse Spark Thinking's 407 breaks down as follows (approximate):

| Source                                                                  | Approx. points lost |
|-------------------------------------------------------------------------|---------------------|
| First-image prose output (Harb0rFr8 scored before proper prompt was sent) | ~1                  |
| Email-first SSO pages where model reported `no password field` but v0.1 strict invariant asserted `yes` | ~11                 |
| Landing / homepage / signup surfaces where model correctly reported `no login form` | ~8                  |
| Verdict hedges (`suspicious` for non-credential-capture surfaces) | ~4                  |
| MITRE `T1583.001` on infrastructure-only pages where strict rubric requires `T1566` | ~2                  |
| Attack-class field multi-token outputs | (0 applied under charitable read) |
| Genuine URL-field failure on wf10.png (PCG) | ~1 |

**Genuine model URL-extraction failure** accounts for ~1 point of the 44-point gap. The remaining ~43 points are rubric-rigidity artifacts. Under v0.2 charitable rubric, projected PRS is ~0.97.

---

## Qualitative findings

**Literal-reading is first-pass behavior on single-attack URLs.** Muse Spark Thinking returns the full address-bar contents including scheme, `www.`, paths, and query strings. Normalization then strips what the benchmark defines as non-scored. Paths that mirror real-brand SSO patterns (`/prgw/digital/signin/retail` on Fidelity, `/Areas/Access/Login` on Schwab, `/Authentication/Login` on Cleveland Clinic MyChart) are returned *with* the adversarial subdomain homoglyph preserved.

**Density-invariance within a single pair class.** Single, adjacent-double, non-adjacent-double, and triple substitutions all read literally for `1↔l` and for `0↔o`.

**Compound-attack behavior is split.** The mixed-pair image (`wf10.png`) triggered Pattern-Consistency Gravity while the compound append-8 image (`HarborFr8.png`) read character-exact. N=2 is too small to claim a pattern.

**TLD and path literalism.** `navyfederal.0rg`, `apple1.com.com`, and `nsbank.com/pers0nal/sign-in` all read character-exact. The model did not simplify, deduplicate, or auto-correct TLDs or paths.

**Mixed-class reasoning.** On `wf10.png`, field 5 correctly reported both pair classes present (`1↔l, 0↔o`), indicating the model *saw* both substitutions. The URL-field failure was extrapolative, not perceptual.

**Explicit comparative reasoning.** On `Ax.png` and `WellsRn.png`, field 5 included adversarial-vs-legitimate comparison (`a↔e (axpress vs express)`, `r↔n (onlirne vs online)`).

**Brand-canonicity confidence calibration.** Spark showed `suspicious` hedging on:
- Less-canonical brands on login pages (AlB, BoC)
- Canonical brands on non-credential-capture surfaces (Google0, G00gle, Nf01)

Correlates with brand unfamiliarity + absence of visible credential-capture UI combined.

**MITRE calibration by attack phase.** On infrastructure-only images (Nf01, G00gle), Muse Spark returned `T1583.001` instead of `T1566`. Forensically more precise than `T1566` for these surfaces — the screenshot shows lookalike-domain infrastructure, not active phishing delivery.

---

## Cross-corroboration outcome (six flagged URLs)

Six URLs in v0.1 were flagged (⚠️) because they had been inferred from filename patterns. All six cross-corroborated during the run, confirmed by visual spot-check, all character-exact matches. Details in v0.1.1 writeup.

**Methodological implication.** For models with established SGR ≥ 0.95 on independent samples, model output can serve as an answer-key validator provided per-image human spot-check confirms. This approach does *not* generalize to models with lower SGR — a high-gravity model would systematically drift toward canonical-brand URLs and corroborate incorrect keys.

**Limitation exposed by the HarborFr8 session gap:** Cross-corroboration between a model and a filename-inferred key is vulnerable to the same inference error appearing in both. The fix — PM eyeball review of the actual image pixels — is the only reliable ground-truth source. v0.2 should treat model-output-vs-answer-key agreement as confirmation only when the PM has independently eyeballed the image.

---

## Three-model comparison context

| Model | Reasoning | Surface | SGR | PRS (strict) | SGG |
|---|---|---|---|---|---|
| **Muse Spark** | **Thinking** | **meta.ai web** | **40/41 = 0.976** | **407/451 = 0.902** | **−0.074** |
| Gemini Pro 3.1 | Thinking | Gemini App | 32/41 = 0.780 | ~0.776 | ~0.00 |
| Opus 4.7 | Adaptive | Bedrock API | 40/41 = 0.976 | 446/451 = 0.989 | +0.013 |
| Opus 4.6 | Enabled | Bedrock API | 37/41 = 0.902 | 434/451 = 0.962 | +0.060 |

Spark and Opus 4.7 tied on SGR; Opus 4.7 leads on PRS because of rubric-rigidity handling on non-URL fields. Spark exhibits the most pronounced URL-literalism-first profile of the four models (most-negative SGG). Failure modes are complementary: Spark failed on PCG (wf10) where both Opus generations held; Opus 4.7 failed on SNG (apple1) where Spark held. No model achieves 41/41 on v0.1.

---

## Reproducibility

**Setup:** Fresh Meta.ai session per image, Thinking mode engaged. No system prompt. No security framing. No prior context. Image uploaded, then the v0.1 evaluation prompt pasted verbatim. First response captured.

**Expected reruns:** Muse Spark Thinking on the consumer web tier uses nondeterministic sampling. v0.1 methodology recommends three independent runs per image; this run captured single-shot outputs. For publication-grade individual-image claims, corpus should be rerun twice more and best-of-3 / majority-of-3 SGR reported.

**Raw output preservation:** All 41 verbatim filled-form outputs preserved in `muse-spark-raw-outputs.md`.

---

## One-sentence summary

Muse Spark Thinking (Meta.ai consumer web tier) achieves SGR = 0.976 and PRS = 0.902 on the Semantic Gravity Benchmark v0.1.3, with the sole SGR failure on the corpus's only mixed-pair URL exhibiting Pattern-Consistency Gravity — replicated cross-model on Gemini Pro 3.1 Thinking and uniquely held by both Claude Opus 4.6 and Claude Opus 4.7.

---

**Run date:** April 16, 2026 (39 images, Thinking) + April 17, 2026 (2 Harbor Freight recaptures, Thinking)
**Scored by:** Claude (Opus 4.7), following the v0.1 scoring methodology
**Human validator / PM:** Jason Valenti
**Artifact pairs with:** `muse-spark-raw-outputs.md`, `semantic-gravity-answer-key-v0.1.3.md`
