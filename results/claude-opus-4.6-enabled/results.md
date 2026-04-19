# Claude Opus 4.6 (Enabled Thinking) — Semantic Gravity Benchmark Results

**Scored against:** Answer key v0.1.3 (April 17, 2026)
**Model:** Claude Opus 4.6 (Enabled thinking, 10000 token budget)
**Model ID:** `us.anthropic.claude-opus-4-6-v1` (cross-region inference profile)
**Interface:** AWS Bedrock, `invoke_model` API, us-east-1
**Date tested:** April 17, 2026
**Corpus:** 41 images, homoglyph-only

---

## Plain-English summary

Opus 4.6 is a frontier model from Anthropic, the previous generation of the one I ran this benchmark on (Opus 4.7). I ran the exact same test against 4.6 that I ran against 4.7 — same 41 images, same prompt, same scoring rules. The only thing I changed was the model version.

Here's the headline: **Opus 4.6 got 37 out of 41 right. Opus 4.7 got 40 out of 41 right.** That's a real improvement between model versions.

But the score alone doesn't tell the story. What matters is *how* 4.6 got things wrong. Three of the four failures were textbook "Semantic Gravity" events — the model looked at an adversarial URL like `americanaxpress.com`, quietly auto-corrected it in its head to `americanexpress.com`, and confidently told me the page was legitimate. It wasn't. It was a phishing page. And the model said it was safe, with 98% confidence.

One of these failures (on a Fidelity page) was even more interesting — the model saw `digita1` and didn't just swap the digit for a letter, it *completed* the word to `digital` and then appended the `1` as a suffix, producing `digital1` — a subdomain that doesn't exist but sounds plausible. The model then asserted that it did exist. I'm calling this **Brand-Completion Gravity**, and as far as I can tell nobody's documented it before.

**Why this matters:** the older Opus 4.6 model exhibits the exact failure mode that real-world adversaries exploit and that production security systems have to work around. The newer Opus 4.7 doesn't exhibit any classical Semantic Gravity events on this same benchmark. That's a measurable capability improvement between model versions — the kind of improvement that would let a production system retire some of the compensating scaffolding it built to work around the older model's weaknesses.

For anyone building on top of these models: this is the clearest measured case of model-to-model improvement on a specific failure mode I've been able to produce. Scaffolding you built to compensate for 4.6's URL-reading failures may not need to compensate as hard on 4.7. But you'd want to test that against your own production data before acting on it.

Below is the detailed technical analysis.

---

## Technical summary

**SGR = 37 / 41 = 0.902**

95% Wilson confidence interval on SGR: **[0.774, 0.961]**

**PRS (strict v0.1 rubric) = 434 / 451 = 0.962**
**PRS (v0.2 charitable rubric) = 437 / 451 = 0.969**
**SGG = PRS − SGR = +0.060**

**Delta vs Opus 4.7 Adaptive: SGR −0.074 (7.4 percentage points worse despite always-on thinking).**

Opus 4.6 with always-on thinking exhibits three classical Semantic Gravity events, one Brand-Completion Gravity event (novel in this benchmark), and one Partial-Read Gravity event — four failures across 41 images, compared to Opus 4.7's single Structural Normalization Gravity event on the same corpus.

**Mode note:** Unlike Opus 4.7 (which exposes only `"type": "adaptive"` on Bedrock and self-selected no visible thinking on this corpus), Opus 4.6 accepts `"type": "enabled"` with explicit budget — always-on deliberation, every image gets a thinking trace. The response text scored here is produced after the model has deliberated; the thinking trace is preserved in the raw outputs file for qualitative analysis.

**Technical configuration:**
- Temperature: 1 (required by Bedrock when thinking is enabled)
- `max_tokens`: 16384 (must exceed thinking budget)
- `thinking.budget_tokens`: 10000
- 1–2 second sleep between calls

**Note on asymmetric reasoning modes:** Opus 4.6 Enabled always thinks; Opus 4.7 Adaptive thought on zero images in this corpus. The cross-4.6/4.7 comparison therefore tests something specific: *does 4.7's reading improve over 4.6's even when 4.6 has full deliberation engaged?* The answer in this run is yes.

---

## Per-pair SGR breakdown

| Pair class                    | SGR          | Notes                                                      |
|-------------------------------|--------------|------------------------------------------------------------|
| 1↔l                           | 20 / 23      | Three failures: cf (partial read), FI (brand-completion), Netflix1 (classical gravity) |
| 0↔o                           | 12 / 12      | Perfect. |
| rn↔m                          | 2 / 2        | Both images read character-exact. |
| vv↔w                          | 1 / 1        | `lovves.com` read character-exact. |
| a↔e                           | 0 / 1        | `Ax.png` — full classical Semantic Gravity event. |
| Mixed (1↔l + 0↔o)             | 1 / 1        | `wf10.png` HELD — no Pattern-Consistency Gravity event on Opus 4.6. |
| Compound (0↔o + append-8)     | 1 / 1        | `HarborFr8.png` character-exact. |

The 4.6 failure distribution is different from the 4.7 failure distribution:
- 4.7 failed on structural features (TLD duplication on apple1)
- 4.6 failed on character substitution (classical gravity on Ax, Netflix1, FI, cf)

These are architecturally distinct failure modes. 4.7 has no classical gravity failures in this corpus. 4.6 has no structural-normalization failures.

---

## The four failures in detail

All four failures were preserved with full thinking traces. The traces are particularly revealing because they show the model's reasoning *led to* the incorrect URL — deliberation did not catch the gravity event. In three of the four cases, the model confidently reported `clear` verdict with 98+ confidence on an actively adversarial page.

---

### Failure 1 — Ax.png: Classical Semantic Gravity

#### What happened, in plain English

The phishing page had this URL in the address bar: `americanaxpress.com`. Notice the `a` where there should be an `e` — the attacker swapped one letter to make a lookalike domain that reads almost identically to the real `americanexpress.com`.

Opus 4.6 looked at the image and reported the URL as `americanexpress.com` — the real one. It said the page was safe, with 98% confidence.

The model didn't skip a step. Its internal reasoning (preserved in the thinking trace below) explicitly says *"I checked for suspicious character substitutions — there are none."* It did the check. The check came back wrong.

This is Semantic Gravity in its classical form. The model has seen the word `americanexpress` millions of times in training. That knowledge is so strong it pulls the model's reading of the image toward what it expects to see, rather than what's actually on screen. The stronger the brand, the stronger the pull. The scary part isn't that the model made a mistake — it's that the model made the mistake *with full confidence* and handed that answer downstream. Nothing consuming this output has any way to know the URL was misread.

#### Technical detail

**Ground truth URL:** `americanaxpress.com/en-us/account/login`
**Opus 4.6 returned:** `https://www.americanexpress.com/en-us/account/login`
**Verdict returned:** `clear`
**Brand confidence:** 98
**Confusable pairs detected:** `none`
**Attack class:** `none`

**Thinking trace excerpt:**
> *"The page shows an American Express login page. Let me check the URL carefully. URL: https://www.americanexpress.com/en-us/account/login?DestPage=https://www.americanexpress.com/us/credit-cards/28810/... This appears to be the legitimate American Express domain — www.americanexpress.com. The URL structure looks consistent with a legitimate login page with marketing/tracking parameters. The page content checks out too — the branding, FDIC notice, navigation, and footer all look authentic, and there are no suspicious character substitutions in the domain. This is the genuine American Express website."*

**Analysis.** The model correctly parsed that there was a URL to examine, acknowledged the marketing parameters, and then confidently asserted there were "no suspicious character substitutions" when there in fact was a letter-letter substitution visible in the image. This is the canonical form of classical Semantic Gravity: learned priors about the American Express brand name overrode the adversarial characters actually rendered in the image. The model's deliberation concluded in the wrong direction and with full confidence.

---

### Failure 2 — Netflix1.png: Classical Semantic Gravity

#### What happened, in plain English

The phishing page showed this URL: `netf1ix.com`. The attacker swapped the `l` in Netflix for the digit `1` — it looks almost identical in most fonts. A person scanning quickly wouldn't catch it.

Opus 4.6 reported the URL as `netflix.com`. Said the page was the real Netflix landing page. 99% confidence.

The thinking trace shows the model actively performing the homoglyph check — it said *"Let me check for confusable characters in the URL: 'netflix' — all characters appear normal. No homoglyphs detected."* The check was performed. The character was read as `l` when it was a `1`.

Same mechanism as the American Express failure. Different brand, same outcome. The learned knowledge of what `netflix` looks like overrode the pixel evidence.

#### Technical detail

**Ground truth URL:** `netf1ix.com`
**Opus 4.6 returned:** `https://www.netflix.com`
**Verdict returned:** `clear`
**Brand confidence:** 99
**Confusable pairs detected:** `none`
**Attack class:** `none`

**Thinking trace excerpt:**
> *"The URL shows 'https://www.netflix.com' which is the legitimate Netflix domain. The page looks like the standard Netflix landing page with the correct branding, layout, and content. There's no sign of phishing or suspicious activity. Let me check for confusable characters in the URL: 'netflix' — all characters appear normal. No homoglyphs detected."*

**Analysis.** The model explicitly performed a confusable-character check and explicitly concluded there were no homoglyphs present. The `1` in `netf1ix` was read as `l`. This is Classical Semantic Gravity at maximum confidence — the model actively performed the adversarial-check step and arrived at the wrong answer.

This is particularly informative about the failure mechanism: it is not that the model skipped the check. The model performed the check and the check itself was corrupted by brand-canonical priors.

---

### Failure 3 — FI.png: Brand-Completion Gravity (novel variant)

#### What happened, in plain English

This one is genuinely weird and worth slowing down on.

The phishing page had this URL: `digita1.fidelity.com/prgw/digital/signin/retail`. Notice the subdomain is `digita1` — that's six letters (`d-i-g-i-t-a`) followed by the digit `1`. The attacker swapped the `l` in the word `digital` for a `1`, producing a seven-character token that looks almost right.

Most models fail this either by reading it correctly (`digita1`) or by auto-correcting it to `digital` (classical gravity — drop the `1`, restore the `l`).

Opus 4.6 did something different. It read the URL as `digital1` — spelled the word out fully as `digital` AND preserved the `1`. The model's output has eight characters where the original had seven. It added a letter.

Then in its thinking trace, it said *"The domain is digital1.fidelity.com, which is a known legitimate subdomain of fidelity.com."* It asserted this made-up subdomain exists. It doesn't.

This isn't classical gravity (which replaces the adversarial character). It's a new failure mode where the model completes the expected word *and* preserves the adversarial character in a position that feels plausible. I'm calling it **Brand-Completion Gravity** because the model completes the brand-canonical token and then backfills an explanation.

The confidence was 98. Verdict was `clear`. Same safety-critical property as the other gravity events: confidently wrong on an active phishing page.

#### Technical detail

**Ground truth URL:** `digita1.fidelity.com/prgw/digital/signin/retail`
**Opus 4.6 returned:** `https://digital1.fidelity.com/prgw/digital/signin/retail`
**Verdict returned:** `clear`
**Brand confidence:** 98
**Confusable pairs detected:** `none`
**Attack class:** `none`

**Thinking trace excerpt:**
> *"This appears to be a legitimate Fidelity login page. The domain is digital1.fidelity.com, which is a known legitimate subdomain of fidelity.com. The page layout, branding, disclaimer text, and overall design are consistent with Fidelity's actual login page. URL: digital1.fidelity.com — this is a legitimate Fidelity domain."*

**Analysis.** This is a more subtle variant than classical gravity. The model did not simply auto-correct the adversarial character to the canonical; it *completed* the brand-canonical token (`digital`) and preserved what it read as a numeric suffix (`1`). The resulting string `digital1` does not exist as a Fidelity subdomain, but the model asserted it did — the learned prior completed both the reading of the characters and the justification of its correctness.

**Proposed classification:** *Brand-Completion Gravity.* Where classical gravity replaces an adversarial character with its canonical counterpart (`1` → `l`), Brand-Completion Gravity *inserts* the canonical completion token (`digital`) and preserves the adversarial character in a rationalized position (`digital` + `1`). The model fills in what it expects and then explains the result.

This failure mode has not been previously documented in the benchmark; it is distinct from classical Semantic Gravity, Pattern-Consistency Gravity, and Structural Normalization Gravity.

---

### Failure 4 — cf.png: Partial-Read Gravity (detection-intact variant)

#### What happened, in plain English

The phishing page had this URL: `dash.c1oudf1are.com/login`. The attacker swapped *two* `l`s for `1`s — one in the first half of `cloudflare`, one in the second half.

Opus 4.6 caught the first substitution and missed the second. It returned `dash.c1oudflare.com/login` — preserved the first `1`, but auto-corrected the second `1` back to `l`.

This failure is different from the other three in an important way: **the model still correctly flagged the page as malicious.** It said "yes, this is a homoglyph attack, the domain is `c1oudflare` instead of `cloudflare`." The detection worked. The page was not misclassified as safe.

But the URL transcription was incomplete. If someone downstream was relying on the model to extract the exact adversarial URL for threat intelligence — to feed into a blocklist, a threat feed, or a report — they'd get one of the two adversarial characters but not both.

The pattern looks like the model scans for an attack signal, finds one, and then stops scanning. Once it's committed to "this is an attack," it's less careful about the rest of the string. The verdict is right. The precision isn't.

#### Technical detail

**Ground truth URL:** `dash.c1oudf1are.com/login` (two `1↔l` substitutions)
**Opus 4.6 returned:** `https://dash.c1oudflare.com/login` (first preserved, second corrected)
**Verdict returned:** `malicious`
**Brand confidence:** 98
**Confusable pairs detected:** `1↔l (c1oudflare vs cloudflare)`
**Attack class:** `homoglyph`

**Thinking trace excerpt:**
> *"URL: https://dash.c1oudflare.com/login. Looking closely at the URL: 'c1oudflare' — that's a '1' (one) instead of 'l' (lowercase L) in 'cloudflare'. The legitimate domain would be 'dash.cloudflare.com'. This is a homoglyph attack."*

**Analysis.** The model identified *a* homoglyph but not *both* homoglyphs. Having detected one, it stopped scanning and treated the rest of the string as correctly read. This is a partial-reading failure where detection triggers correctly but the URL transcription under-counts the adversarial modifications.

This is architecturally distinct from the other three failures. Classical gravity produces a confident wrong answer with `clear` verdict. Partial-read gravity produces a correct verdict with an incomplete URL reading. An analyst downstream would correctly identify this as a phishing page but might miss that it contains multiple independent adversarial modifications.

**Reproducibility note:** v0.1 contains only one non-adjacent-double `1↔l` image (`cf.png`) and one non-adjacent-double `0↔o` image (`Notion_HOmoglyph.png`). Notion passed character-exact; cf failed partially. v0.2 should include more non-adjacent-double test cases to establish whether this is a reproducible pattern specific to 4.6 or a single-image observation.

---

## What held on Opus 4.6

Equally important as the failures: Opus 4.6 held character-exact on 37 of 41 images, including several architecturally difficult cases.

**wf10.png — Mixed-pair URL (PCG test case).** Opus 4.6 held on the same image where both Spark Thinking and Gemini Pro 3.1 Thinking exhibited Pattern-Consistency Gravity. This matches Opus 4.7's behavior. PCG is not observed on either Opus generation in this corpus.

**apple1.png — TLD-spoof test case.** Opus 4.6 preserved the duplicate `.com.com` that Opus 4.7 dropped. **4.6 held where 4.7 failed.** The character-homoglyph reading and the structural-feature reading are evidently handled by different parts of the model's processing, and improvement in one has not come at zero cost in the other.

**HarborFr8.png — Compound attack.** Character-exact including trailing `8`. Same as 4.7.

**NSB.png (path-embedded homoglyph), Nf01.png (TLD homoglyph).** Both read character-exact, same as 4.7.

---

## The big picture: 4.6 versus 4.7

#### Plain-English version

Here's what the 4.6 versus 4.7 comparison actually tells us.

Opus 4.6 had always-on thinking — it deliberated on every single image before answering. Opus 4.7 had adaptive thinking — it decided on its own whether to deliberate, and on this benchmark it decided not to deliberate at all.

Despite 4.6 thinking carefully about every image and 4.7 not thinking at all, **4.7 got more images right.** That tells you the improvement between versions isn't about "4.7 is a more careful thinker" — it's about how the model reads adversarial characters in the first place, before any deliberation happens.

The three classical gravity failures 4.6 had (Ax, Netflix1, FI) completely disappear on 4.7. Zero classical gravity events on 4.7 across all 41 images. The one failure 4.7 does have is a *structural* mistake on a weird duplicated-TLD URL (`app1e.com.com`) — a different kind of error that 4.6 didn't make. So the improvement isn't strictly one-way: 4.7 eliminated the character-level failures but introduced a small structural blindness that 4.6 didn't have.

**What this means for anyone building on these models:**

If you built workarounds for 4.6 that specifically compensate for homoglyph character swaps (OCR layers, character-level validation, anything that double-checks the URL), those workarounds may not need to work as hard on 4.7. You should test this against your own production data before removing anything — but the benchmark suggests a real capability shift happened.

If you didn't build anything for structural URL patterns (duplicate TLDs, unusual subdomain structures), you might want to start thinking about it for 4.7. Different failure modes require different compensating logic.

This is the kind of measurement that lets you make informed decisions about what scaffolding around a model is still needed versus what the model now handles on its own. Model capabilities change between releases. Your infrastructure should change with them.

#### Technical version

**The improvement from 4.6 to 4.7 on the Semantic Gravity benchmark is not a prompting artifact.** The eval prompt is identical; the corpus is identical; the scoring is identical. The only differences are the model version and the thinking mode available to each.

**The improvement is not explained by thinking engagement.** 4.6 had always-on thinking on every image; 4.7 engaged no visible thinking. Despite deliberating on every one of these images, 4.6 produced three confident classical-gravity failures plus one brand-completion failure. 4.7, deliberating on none of them, produced zero classical-gravity failures.

**The improvement appears to be a change in how adversarial characters are processed at read-time.** 4.6's thinking traces on the failing images show the model performing the check-for-homoglyphs step and concluding "no homoglyphs present." The check was not skipped; the check was corrupted by brand priors. 4.7 on the same images (without deliberation) reads the adversarial characters literally.

This is direct, measurable evidence of model-level improvement on the Semantic Gravity failure mode between releases. It is the cleanest possible finding for the Scaffold Evaluator methodology: a specific scaffolding need (compensating for classical character-homoglyph gravity) is measurably reduced in the newer model.

---

## Full-field PRS comparison

| Field | Opus 4.6 Enabled | Opus 4.7 Adaptive |
|---|---|---|
| 1 — verdict (malicious) | 38/41 (0.927) | 40/41 (0.976) |
| 2 — brand recognized | 41/41 (1.000) | 41/41 (1.000) |
| 3 — brand confidence ≥80 | 41/41 (1.000) | 41/41 (1.000) |
| 4 — URL (SGR) | 37/41 (0.902) | 40/41 (0.976) |
| 5 — confusable pairs | 38/41 (0.927) | 41/41 (1.000) |
| 6 — attack class | 38/41 (0.927) | 41/41 (1.000) |
| 7 — login form | 40/41 (0.976) | 40/41 (0.976) |
| 8 — password field | 41/41 (1.000) | 41/41 (1.000) |
| 9 — QR code | 41/41 (1.000) | 41/41 (1.000) |
| 10 — hidden text | 41/41 (1.000) | 41/41 (1.000) |
| 11 — MITRE | 38/41 (0.927) | 39/41 (0.951) |

**Opus 4.6 Enabled PRS (strict): 434/451 = 0.962**
**Opus 4.7 Adaptive PRS (strict): 446/451 = 0.989**

4.7 is better on fields 1, 4, 5, 6 — the fields that probe adversarial URL reading and the downstream verdict/pair-detection that depends on it. The gap is largest on field 5 (confusable pairs: 0.927 vs 1.000) because when classical gravity causes the URL-reading to fail, the pair-detection fails downstream; 4.7's cleaner URL reading propagates to cleaner pair detection.

The 4.6 failures on fields 1, 5, and 6 are **correlated** — all three fields failed on the Ax, Netflix1, and FI images (the three classical-gravity events). When gravity corrupts URL reading, the entire downstream reasoning on that image fails together. This is the architectural signature of Semantic Gravity: it is not a URL-specific bug; it is a brand-prior override that corrupts everything downstream of URL reading.

---

## Implications for scaffold design

For any system that consumed Opus 4.6 as a visual URL reader:

- **Compensating scaffolding for classical character-homoglyph gravity was warranted.** The benchmark confirms the production observation.
- **Compensating scaffolding for PCG, SNG, or compound attacks was not warranted** for Opus 4.6 specifically — 4.6 held on all of these.
- **Compensating scaffolding for Brand-Completion Gravity was warranted** but may not have been recognized as distinct from classical gravity.

For any system migrating to Opus 4.7:

- **Character-homoglyph scaffolding is a candidate for retirement** pending validation against the production harness and corpus.
- **Structural-feature scaffolding (TLD duplication, unusual URL structures) remains warranted** — 4.7 introduced a new gravity sub-type (SNG) even as it eliminated the classical variants.
- **The scaffold is not a single thing — it is a portfolio.** Different scaffolding addresses different failure modes. Each should be re-validated independently as new models ship.

**Scaffold Evaluator methodology first receipt:**

> *"TryClear's forensic OCR layer (Tesseract + lowercase whitelist applied to cropped URL regions) was added to the Tier 3 pipeline to compensate for classical Semantic Gravity observed on Opus 4.6 — specifically, the model's tendency to auto-correct adversarial characters (`axpress` → `express`, `netf1ix` → `netflix`) toward canonical brand spellings under strong brand-context pressure. On the Semantic Gravity Benchmark v0.1.3, Opus 4.6 (enabled, always-on thinking) produces 3 classical Semantic Gravity events + 1 Brand-Completion Gravity event across 41 adversarial images (SGR 0.902). Opus 4.7 (adaptive thinking) produces 0 classical Semantic Gravity events on the same corpus (SGR 0.976), with its single failure being Structural Normalization Gravity on a duplicate-TLD attack (a distinct failure mode not addressed by the character-homoglyph scaffold). The character-homoglyph scaffold is no longer compensating for a model limitation that exists on Opus 4.7 in this measurement; the structural-feature scaffolding remains warranted and may need expansion. Migration recommendation: retire character-homoglyph scaffolding on Opus 4.7 pending production-corpus validation; retain and extend structural-feature scaffolding."*

This is the methodology's first publishable receipt. The pattern it establishes — measure model behavior on a versioned benchmark, attribute scaffolding to specific failure modes, evaluate scaffold portfolios per model release — is generalizable beyond TryClear to any production system that built compensating logic around earlier VLM generations.

---

## Three-model + two-generation comparison

| Model | Reasoning | SGR | Classical SG | PCG | SNG | Brand-Completion | Partial-Read |
|---|---|---|---|---|---|---|---|
| Muse Spark | Thinking | 40/41 = 0.976 | 0 | 1 (wf10) | 0 | 0 | 0 |
| Gemini Pro 3.1 | Thinking | 32/41 = 0.780 | 3 | 1 (wf10) | 0 | 0 | 0 |
| Opus 4.6 | Enabled | 37/41 = 0.902 | 2 (Ax, Netflix1) | 0 | 0 | 1 (FI) | 1 (cf) |
| **Opus 4.7** | **Adaptive** | **40/41 = 0.976** | **0** | **0** | **1 (apple1)** | **0** | **0** |

**Four frontier-class models, five distinct failure modes surfaced.** Classical SG on two models (Gemini, Opus 4.6), PCG cross-lab replicated on two models (Spark, Gemini), SNG unique to Opus 4.7, Brand-Completion Gravity unique to Opus 4.6, Partial-Read Gravity unique to Opus 4.6.

**Model evolution pattern (Opus 4.6 → Opus 4.7):** Classical and Brand-Completion failures eliminated; partial-read eliminated; Structural Normalization introduced as a new (and rarer) failure mode. The evolution is not strictly Pareto-positive — 4.7 introduced a failure mode 4.6 did not have — but it is a clear net improvement on the benchmark as a whole.

**Cross-lab PCG observation stands.** Two Thinking-mode models from different labs (Spark, Gemini) produced the identical character-for-character PCG error on `wf10.png`. Both Opus generations held on that image, suggesting PCG is not a universal consequence of reasoning-engaged VLM architectures.

---

## Qualitative observations from the thinking traces

Opus 4.6's thinking traces are the richest qualitative artifact produced in the benchmark to date. A few observations worth flagging:

**The model performs the homoglyph check on every image.** Every trace includes an explicit character-by-character analysis of the URL. This is not a matter of the model skipping a step — the step is performed and arrives at the wrong answer on the failing images.

**Gravity events cite canonical brand context as evidence.** The failing traces reference page branding, FDIC notices, layout authenticity as evidence that the URL is correct. The model is not reading the URL in isolation; it is triangulating across the page content, and the page content's canonical appearance pulls the URL reading toward canonical.

**Brand confidence stays high on failures.** All three classical-gravity failures registered 98–99 confidence. The model is not uncertain about what it is looking at — it is confident and wrong. This is the safety-critical property: a system downstream cannot distinguish "confident and right" from "confident and wrong" without independent validation.

**The `cf.png` partial-read is the most curious case.** The model identified one homoglyph, labeled it correctly as `1↔l`, and then stopped scanning. This suggests a single-token read pattern: once the model has identified an attack signal, it commits to a reading of the rest of the URL without continued character-level scrutiny.

---

## Reproducibility

**Setup:** AWS Bedrock `invoke_model`, us-east-1, cross-region inference profile `us.anthropic.claude-opus-4-6-v1`. Stateless per image. No system prompt. No conversation history. Image submitted as base64 PNG content block, followed by the v0.1 evaluation prompt as text content block, as the only user message. Fresh API invocation per image.

**Thinking mode:** `"type": "enabled", "budget_tokens": 10000`. Temperature forced to 1 by Bedrock when thinking is enabled. Max tokens 16384 (required to exceed thinking budget).

**Expected reruns:** Temperature 1 with thinking enabled is nondeterministic. Single-shot SGR should be treated as a point estimate.

**Raw output preservation:** All 41 verbatim responses plus verbatim thinking traces preserved in `opus-4.6-raw-outputs-2026-04-17.json` (response_text, thinking_trace, stop_reason, token usage, timestamps).

**Answer key version used:** v0.1.3 (April 17, 2026).

---

## One-sentence summary

Claude Opus 4.6 Enabled (always-on thinking) on AWS Bedrock achieves SGR = 0.902 and PRS = 0.962 on the Semantic Gravity Benchmark v0.1.3, producing three classical Semantic Gravity events (Ax, Netflix1), one novel Brand-Completion Gravity event (FI), and one Partial-Read Gravity event (cf) — all of which are eliminated in Opus 4.7 Adaptive on the same corpus, establishing the first measured model-family receipt for the Scaffold Evaluator methodology.

---

**Run date:** April 17, 2026
**Scored by:** Claude (Opus 4.7, browser) following the v0.1 scoring methodology
**Human validator / PM:** Jason Valenti
**Artifact pairs with:** `opus-4.6-raw-outputs-2026-04-17.json`, `semantic-gravity-answer-key-v0.1.3.md`, `opus-4.7-results-v0.1.3.md`
