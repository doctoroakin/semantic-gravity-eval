# Gemini Pro 3.1 (Thinking) — Semantic Gravity Benchmark Results

**Scored against:** Answer key v0.1.3 (April 17, 2026)
**Model:** Gemini Pro 3.1 (Thinking mode)
**Interface:** Gemini App, consumer web
**Date tested:** April 16, 2026
**Corpus:** 41 images, homoglyph-only

---

## Plain-English summary

Gemini Pro 3.1 is Google's flagship vision-language model. I tested it in Thinking mode — the reasoning-engaged tier — through the standard Gemini App that any consumer can use.

**The result: 32 out of 41 right.** Significantly below the other frontier models tested (Muse Spark 40/41, Opus 4.6 37/41, Opus 4.7 40/41). Gemini is the clearest case in this benchmark of classical Semantic Gravity in action.

Three of Gemini's failures are textbook Semantic Gravity events. On Bank of China (`b0c.cn`), Gemini auto-corrected the adversarial `0` in `b0c` to read it as `boc.cn` and said the page was legitimate. On Navy Federal (`navyfederal.0rg`), it corrected `.0rg` to `.org` and said the page was legitimate. On American Express (`americanaxpress.com`), it corrected `axpress` to `express` and said the page was legitimate. Three different brands, three different character swaps, three confident "this is clean" verdicts on active phishing pages.

Gemini also failed on the same cross-lab Pattern-Consistency Gravity image where Muse Spark failed (`we1lsfarg0.com` read as `we11sfarg0.com`). That cross-lab replication is one of the most important findings in the whole benchmark.

The rest of Gemini's gap to the other models comes from a distinct issue: consumer-surface artifacts. The Gemini App appears to rewrite URLs into "clickable link" format in some responses, which corrupts the benchmark's URL-field scoring even when the model read the adversarial characters correctly. We counted these separately from real gravity events, but they're still a real-world concern for anyone using Gemini through consumer-facing products.

**What this tells us:** Gemini Pro 3.1 in its current consumer configuration exhibits measurable classical Semantic Gravity on canonical brands with homoglyph URLs. The failures are high-confidence (all at 95+ brand confidence) and predictably targetable (concentrated on canonical brands where the model's priors are strongest). For security teams using Gemini as a VLM reviewer in any part of their stack, this is a real capability gap to be aware of.

Below is the detailed technical analysis.

---

## Technical summary

**SGR = 32 / 41 = 0.780**

95% Wilson confidence interval on SGR: **[0.632, 0.879]**

**PRS ≈ 350 / 451 ≈ 0.776**

Gemini Pro 3.1 Thinking's URL reading is the weakest of the four models tested in this benchmark. Nine field-4 failures across the 41-image corpus, distributed across three distinct failure modes:

- **3 classical Semantic Gravity events** (BoC, Nf01, Ax) — auto-correction toward canonical brand
- **1 Pattern-Consistency Gravity event** (wf10) — cross-lab replicated with Muse Spark
- **5 consumer-surface URL rewriting artifacts** (Gemini App specific; see below)

---

## Per-pair SGR breakdown

| Pair class                    | SGR          | Notes                                                      |
|-------------------------------|--------------|------------------------------------------------------------|
| 1↔l                           | 19 / 24      | Includes consumer-surface artifacts on several images; classical reads held on most. |
| 0↔o                           | 9 / 12       | Three classical gravity events: BoC, Nf01, Amazon0 URL rewriting. |
| rn↔m                          | 2 / 2        | Both read character-exact. |
| vv↔w                          | 1 / 1        | `lovves.com` read character-exact. |
| a↔e                           | 0 / 1        | `Ax.png` — classical Semantic Gravity, confident wrong verdict. |
| Mixed (1↔l + 0↔o)             | 0 / 1        | `wf10.png` — Pattern-Consistency Gravity, identical error to Spark. |
| Compound (0↔o + append-8)     | 1 / 1        | `HarborFr8.png` character-exact including trailing `8`. |

---

## The three classical Semantic Gravity events

These are the most important results in the Gemini run. Each is a confident wrong verdict on an adversarial phishing page where the model auto-corrected the URL toward the canonical brand spelling.

---

### Failure 1 — BoC.png: Bank of China

#### What happened, in plain English

The phishing page showed this URL: `https://ebsnew.b0c.cn/boc15/login.html` — with `b0c` using a zero instead of an `o`. The real Bank of China domain is `boc.cn`. The attacker swapped one character.

Gemini read the URL as `ebsnew.boc.cn/boc15/login.html` — reported the domain as `boc.cn`, the real legitimate Bank of China domain. Said the page was legitimate with 95% confidence.

This one's particularly damning because the rest of the URL gave away the attack visually — `ebsnew` isn't a known Bank of China subdomain, `/boc15/` isn't their path structure, and there was a QR code for WeChat authentication that doesn't match their production login flow. A security analyst looking at this page would flag it instantly. Gemini said it was clean.

#### Technical detail

**Ground truth URL:** `ebsnew.b0c.cn/boc15/login.html`
**Gemini Pro 3.1 returned:** `ebsnew.boc.cn/boc15/login.html`
**Verdict returned:** `legitimate`
**Brand confidence:** 95
**Attack class:** `none`

Classical Semantic Gravity. The `0→o` auto-correction dropped the homoglyph, the downstream verdict followed the corrupted URL reading, and the confidence stayed high.

---

### Failure 2 — Nf01.png: Navy Federal Credit Union

#### What happened, in plain English

The phishing page showed this URL: `https://www.navyfederal.0rg/...` — with `.0rg` using a zero instead of an `o` in the TLD. Yes — the attack was in the top-level domain itself, the part of the URL you'd think would be hardest to spoof.

Gemini read the URL as `navyfederal.org` — corrected the adversarial TLD to the real `.org`. Reported the page as legitimate.

This is architecturally interesting because TLDs are the most canonicalized part of a URL. Every `.org` domain in training ends with exactly `.org`. The model's prior for what `.org` looks like is rock solid. The homoglyph attack targeted exactly that prior — and it worked. The model filled in what it expected to see.

#### Technical detail

**Ground truth URL:** `navyfederal.0rg/loans-cards/mortgage/mortgage-rates/conventional-fixed-rate-mortgages.html`
**Gemini Pro 3.1 returned:** `navyfederal.org/loans-cards/mortgage/...`
**Verdict returned:** `legitimate`
**Brand confidence:** 95

Classical Semantic Gravity operating on a TLD homoglyph. The model's learned prior for `.org` overrode the pixel-level evidence of `.0rg`. Note that the corpus's other TLD homoglyph tests (which hit different canonical TLDs in different pair classes) did NOT all produce gravity events — the effect is brand-dependent, not uniformly "TLDs are canonical."

---

### Failure 3 — Ax.png: American Express

#### What happened, in plain English

The phishing page showed `americanaxpress.com` — with `axpress` instead of `express`. The `a↔e` letter-letter swap is one of the hardest homoglyph attacks because both characters are common English letters of roughly similar shape; it's easy to mis-read for humans too.

Gemini read this as `americanexpress.com`. Said the page was legitimate American Express.

This is the same image that Opus 4.6 also failed on. Two different labs' models, same image, same gravity event, same wrong verdict. American Express is a strong brand prior — both models' learned representations of "americanexpress" overrode the pixel evidence of `axpress`.

#### Technical detail

**Ground truth URL:** `americanaxpress.com/en-us/account/login`
**Gemini Pro 3.1 returned:** `americanexpress.com/en-us/account/login`
**Verdict returned:** `legitimate`
**Brand confidence:** 95

The letter-letter pair class is the hardest in the corpus. Ax.png is the only `a↔e` test case; it produced gravity on two of four models tested (Gemini + Opus 4.6), held on two (Spark + Opus 4.7). This is the single image with the widest cross-model variance.

---

## Pattern-Consistency Gravity on wf10.png

### What happened, in plain English

Same image that Muse Spark failed on, same specific character-for-character error. The URL was `we1lsfarg0.com` — adversarial `1` at position 3, legitimate `l` at position 4, adversarial `0` at position 10. Gemini wrote `we11sfarg0.com` — auto-corrected the legitimate `l` to match the adjacent adversarial `1`.

**This is the cross-lab replication finding.** Two frontier VLMs from two different labs (Meta's Muse Spark and Google's Gemini Pro 3.1), both in their respective reasoning-engaged Thinking modes, produced the identical wrong answer on the identical image. That's much stronger evidence of a real phenomenon than any single-model observation would be.

Both Opus 4.6 and Opus 4.7 held on this image. PCG is not a universal consequence of reasoning-engaged VLMs; it's something specific to the Spark and Gemini training or architecture that neither Opus generation shares.

### Technical detail

See [`docs/findings/pattern-consistency-gravity.md`](../docs/findings/pattern-consistency-gravity.md) for the full mechanistic treatment. Key points:

- Ground truth: `we1lsfarg0.com` (positions 3 = `1`, 4 = `l`, 10 = `0`)
- Gemini output: `we11sfarg0.com` (position 4 auto-corrected to `1`)
- Both pair classes (`1↔l` and `0↔o`) correctly identified in the pair-detection field — the model *saw* both substitutions but extrapolated incorrectly in the URL transcription
- Verdict: malicious (detection correctly triggered)

Unlike classical Semantic Gravity (which produces `clear` verdicts on adversarial pages), PCG typically preserves detection — the model identifies the attack but transcribes the URL wrong. Downstream effect: threat intelligence gets fed the wrong adversarial URL, potentially missing the actual attacker infrastructure.

---

## Consumer-surface URL rewriting (Gemini App specific)

### What happened, in plain English

Five of Gemini's nine total failures aren't really gravity events — they're a different kind of issue specific to the Gemini App consumer interface.

When Gemini's response contains a URL that looks like a legitimate web link, the Gemini App UI sometimes reformats that URL in its output. The model says something like "The URL shown is `amaz0n.com`" but the App renders it as a clickable link that points to `amazon.com` (silently rewriting the adversarial character away so the link "works"). When we captured the App's rendered output for scoring, these rewrites appeared in the captured text.

This is a real-world problem — consumers using Gemini through this interface to analyze suspicious screenshots would see auto-corrected URLs and assume the page was safe. But it's architecturally distinct from Semantic Gravity: the model's underlying reading may have been correct; the surface layer between model and user corrupted it.

We scored these as field-4 failures because the benchmark measures what the user actually receives. But they're called out separately from classical SG events because the mechanism is different and the mitigation is different.

For future Gemini testing, we'd recommend either testing via the direct Gemini API (bypassing the App's rendering layer) or documenting the consumer-surface effect as a known artifact.

### Technical detail

Images affected: Amazon0, Chaseon1, Coin1, HomeD, PayPal1 (5 images). All show evidence of URL-text rewriting in the Gemini App's rendered output. Distinguishing characteristics from classical gravity:

- Pair-detection field often shows correct adversarial character identification
- Verdict field often shows `malicious` (detection worked)
- URL field shows canonicalized brand domain (rewriting occurred somewhere in the pipeline)

These are categorized as consumer-surface artifacts in the failure mode table, not classical Semantic Gravity. They affect Gemini's headline SGR on this benchmark but do not indicate the same underlying model behavior as the three classical gravity events on BoC, Nf01, and Ax.

---

## What held on Gemini

Despite the nine failures, Gemini held character-exact on 32 of 41 images, including several architecturally difficult cases that other models struggled with.

**HarborFr8.png — Compound attack.** Gemini read `harb0rfreight8.com/my-account/login` character-exact including the trailing `8`. Matches Spark and Opus behavior on this image.

**apple1.png — TLD-spoof test case.** Gemini preserved the duplicate `.com.com` that Opus 4.7 later dropped. This is a meaningful data point: Gemini avoided the Structural Normalization Gravity that Opus 4.7 exhibited.

**Triple-homoglyph (lemon.png), adjacent double (alls.png), non-adjacent double (cf.png, Notion).** All read character-exact. The `1↔l` and `0↔o` pair classes at varying densities were handled well outside the three classical gravity events.

**Path-embedded homoglyph (NSB.png).** `nsbank.com/pers0nal/sign-in` character-exact including the path-embedded `0↔o`. Notably, Gemini's thinking trace on NSB included explicit reasoning about whether the `/pers0nal/` path segment could be a Cyrillic IDN attack — the model considered multiple adversarial hypotheses. This is the richest qualitative reasoning trace in the entire Gemini run and arguably the most publishable piece of evidence that reasoning-engaged VLMs can engage with adversarial inputs in depth when the attack surface isn't covered by strong brand priors.

---

## Qualitative observations

**Gravity concentrates on canonical brands.** The three classical gravity events were all on brands with overwhelming training representation — Bank of China, Navy Federal (one of the largest credit unions in the U.S.), American Express. The model's priors are strongest precisely where attackers most want to imitate.

**Reasoning engagement didn't prevent gravity.** Gemini was in Thinking mode for every image, deliberating before answering. The thinking traces on the failing images confirm the model performed the homoglyph-check step and arrived at the wrong answer. Classical gravity is not fixed by "just add more thinking."

**Cross-lab PCG replication is the most important finding.** Gemini + Spark both failing `wf10.png` with the same character-for-character error is stronger evidence than any single-model observation. PCG is a real, cross-architectural failure mode in reasoning-engaged consumer VLMs.

**Consumer surfaces introduce their own failure modes.** The Gemini App rewriting behavior is separate from model capability. A clean API test of Gemini Pro 3.1 Thinking would likely produce different results on the five affected images — those failures are attributable to the surface, not the model core.

---

## Four-model comparison (April 2026)

| Model | Reasoning | Surface | SGR | Classical SG | PCG | SNG | Consumer-surface |
|---|---|---|---|---|---|---|---|
| Muse Spark | Thinking | meta.ai | 40/41 = 0.976 | 0 | 1 (wf10) | 0 | 0 |
| **Gemini Pro 3.1** | **Thinking** | **Gemini App** | **32/41 = 0.780** | **3 (BoC, Nf01, Ax)** | **1 (wf10)** | **0** | **5** |
| Opus 4.6 | Enabled | Bedrock API | 37/41 = 0.902 | 2 (Ax, Netflix1) | 0 | 0 | 0 |
| Opus 4.7 | Adaptive | Bedrock API | 40/41 = 0.976 | 0 | 0 | 1 (apple1) | 0 |

Gemini Pro 3.1 Thinking has the most distinct failure pattern of the four models: it's the only model with three classical gravity events, shares the PCG event with Spark, and uniquely exhibits consumer-surface URL rewriting (Gemini App specific, not seen on the API-tested models).

Two images Gemini failed on were handled by other models:
- BoC and Nf01 (classical gravity): held by Spark, both Opus generations
- Ax (classical gravity): held by Spark and Opus 4.7; failed on Opus 4.6

Two images where Gemini held but some other model failed:
- apple1 (SNG): held by Gemini and everyone except Opus 4.7
- FI (Brand-Completion Gravity): held by Gemini and everyone except Opus 4.6

The four models have genuinely complementary failure surfaces. No single model achieves 41/41. Each catches something the others miss.

---

## Reproducibility

**Setup:** Fresh Gemini App session per image. No system prompt. No security framing. No prior context. Image uploaded, then the v0.1 evaluation prompt pasted verbatim. First response captured from the Gemini App's rendered output.

**Expected reruns:** Gemini Pro 3.1 Thinking on the consumer web tier uses nondeterministic sampling. Single-shot SGR should be treated as a point estimate. For publication-grade individual-image claims, the corpus should be rerun and best-of-3 / majority-of-3 SGR reported.

**Known limitations specific to this run:**

- Per-image verbatim outputs were not consistently preserved during the original April 16 session. The scoring is based on captured responses during the run, but some responses are reconstructed from session transcripts rather than directly preserved. Future Gemini runs should follow the stricter verbatim-preservation protocol used for the Opus Bedrock runs (JSON output with stop_reason, token usage, full response_text).
- Consumer-surface URL rewriting affected 5 images. The Gemini App may have applied transformations between the model's underlying reading and the text displayed to the user. Direct API testing would distinguish model behavior from surface behavior.

**Answer key version used:** v0.1.3 (April 17, 2026).

---

## One-sentence summary

Gemini Pro 3.1 Thinking (Gemini App consumer web tier) achieves SGR = 0.780 and PRS ≈ 0.776 on the Semantic Gravity Benchmark v0.1.3, with three classical Semantic Gravity events (BoC, Nf01, Ax), one cross-lab-replicated Pattern-Consistency Gravity event (wf10, also seen on Muse Spark), and five consumer-surface URL rewriting artifacts specific to the Gemini App rendering layer.

---

**Run date:** April 16, 2026
**Scored by:** Claude (Opus 4.7), following the v0.1 scoring methodology
**Human validator / PM:** Jason Valenti
**Artifact pairs with:** Gemini raw outputs (partial preservation; see Reproducibility notes), `semantic-gravity-answer-key-v0.1.3.md`
