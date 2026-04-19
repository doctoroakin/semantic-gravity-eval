# Benchmark Methodology

The Semantic Gravity Benchmark measures how frontier vision-language models (VLMs) read adversarial URLs in phishing lookalike screenshots. This document specifies how runs are conducted, how the corpus is constructed, and what controls are in place to produce reproducible, unbiased results.

Related docs:
- [`EVAL_PROMPT.md`](./EVAL_PROMPT.md) — the prompt sent to every model
- [`SCORING.md`](./SCORING.md) — formal metric definitions and scoring rules
- [`ANSWER_KEY.md`](./ANSWER_KEY.md) — per-image ground truth

---

## Corpus provenance

The 41 images are researcher-constructed phishing lookalike pages. Adversarial URL modifications are drawn from attack patterns observed across 15+ years of professional threat-intelligence work tracking criminal-organization TTPs — homoglyph substitutions, compound modifications, TLD spoofing structures that mirror how real adversaries craft these attacks. The construction is **adversarial-realistic, not adversarial-optimal**: the corpus mirrors techniques observed in the wild, not images specifically engineered to trip any particular model.

**The 41-image corpus was finalized before any model was tested and was not modified during benchmarking.** These same images are in active use as part of the internal test suite for a production image-security detection pipeline, independently validating their utility as stimuli.

### What "adversarial-realistic" means in practice

Each image exhibits a single adversarial URL modification selected from a documented attack taxonomy:

- **Character homoglyph** — substitution of a visually similar character (`1↔l`, `0↔o`, `a↔e`, `vv↔w`, `rn↔m`). The adversarial characters used in the corpus match patterns observed in production phishing campaigns.
- **Compound attack** — two structurally independent modifications on a single URL (homoglyph + appended digit: `harb0rfreight8.com`).
- **TLD homoglyph** — homoglyph substitution in the top-level domain (`.0rg` for `.org` — observed as an attack pattern with tracked adversarial registration history).
- **TLD spoof** — registration of a lookalike TLD-like domain (`com.com`) producing URLs like `app1e.com.com/uk/iphone`.
- **Path-embedded homoglyph** — the domain is canonical; the adversarial character appears in the URL path (`nsbank.com/pers0nal/sign-in`).

### Selection bias control

The most common concern raised about researcher-constructed corpora is **selection bias** — the worry that images were chosen *after* seeing model failures to maximize the gap between model performance and benchmark score. The corpus was explicitly constructed to rule this out:

- The image set was finalized before the first model was tested.
- Image selection was based on pair-class coverage and brand diversity, not on observed model behavior.
- No images were added after seeing any model's failures.
- Two images (`Harb0rFr8.png` and `HarborFr8.png`) were re-captured during the April 17 Muse Spark session for methodology reasons (original submissions had operator or prompt issues); the images themselves were not modified and no adversarial content was changed.

The distribution of failure modes observed across Muse Spark, Gemini Pro 3.1, and Claude Opus 4.7 (three models, three different failure surfaces, one cross-model-replicated failure mode) is inconsistent with a corpus engineered to trip specific models — a cherry-picked corpus would show correlated failures across models on the same images.

### What the corpus is NOT

- **Not a prevalence sample.** The corpus does not claim to represent the statistical distribution of phishing attacks in the wild. Real-world phishing is dominated by typosquatting and credential-capture via non-homoglyph domains; the benchmark deliberately over-samples homoglyph attacks because the homoglyph attack class is where the measurement problem is sharpest.
- **Not an attack campaign dataset.** The images do not correspond to specific real phishing campaigns. Any resemblance to real live-pages is incidental to the adversarial-realistic construction pattern.
- **Not a threat-intelligence feed.** The benchmark measures VLM capability, not ground-truth malicious infrastructure.

---

## Clean-room execution

Each benchmark run follows a clean-room protocol. The goal is to isolate model behavior from operator, surface, and context effects.

### Per-image protocol

For each of the 41 images:

1. **Fresh session.** Every image is submitted in a new session — new browser tab for consumer surfaces, fresh API call with no conversation history for API surfaces.
2. **No system prompt.** No security framing, no "analyze this for threats," no "watch for homoglyphs." The only instruction is the evaluation prompt text.
3. **No prior context.** The model has no knowledge of prior images in the run, no awareness that a benchmark is in progress, no information about TryClear or the benchmark authors.
4. **Image before prompt.** The image is submitted first; the evaluation prompt text is submitted second, as part of the same user message.
5. **First response captured.** The first complete response is captured verbatim. No re-prompts, no clarification requests, no "can you format that as a form?" If the first response is malformed, it is captured and scored as-is.
6. **Verbatim preservation.** The raw response text is preserved exactly as returned — no whitespace normalization, no markdown stripping, no truncation.

### Between images

- **No discussion.** The operator does not engage in conversation with the model between images. Each image is a fresh session.
- **No learning propagation.** If the model responds unexpectedly on image N, this is not used to adjust the submission of image N+1.
- **No retrospective changes.** If the operator realizes mid-run that an earlier image was submitted with an error (wrong prompt, wrong image), the earlier image is re-captured in a fresh session after the rest of the run completes, with the re-capture documented in the results file.

### Rate-limit handling

For consumer surfaces, rate limits may force account rotation or pacing. When rotation occurs:
- The rotation is documented with a timestamp and account indicator (e.g., "Account A submitted images 1-10; Account B submitted images 11-20").
- Each account is itself a fresh session from the model's perspective (no conversation history).
- Rate-limit-driven delays are recorded but do not affect scoring.

For API surfaces, a 1–2 second sleep between calls is used as rate-limit courtesy, not as a statistical pacing control.

---

## Surface-specific conventions

The benchmark is surface-agnostic — any VLM can be tested — but different surfaces introduce different constraints and confounds.

### Consumer web surfaces

**Examples:** meta.ai (Muse Spark), gemini.google.com (Gemini), claude.ai (Claude), chatgpt.com (GPT).

**Strengths:** test the exact model/configuration that a consumer user receives.

**Known confounds:**
- **URL auto-rewriting** — some surfaces wrap URLs in click-through redirectors (observed with the Gemini App wrapping URLs in `google.com/search?q=` patterns). This corrupts the URL-field output. Results writeups must disclose any URL-rewriting observed.
- **Conversation state leakage** — free-tier sessions may carry context between messages. Fresh-session-per-image is essential.
- **Rate limits** — free-tier rate limits may force account rotation, adding operator overhead.
- **Reasoning-mode toggling** — some surfaces default to Instant/Fast mode. The reasoning tier intended for the benchmark must be explicitly selected per-image.
- **Markdown formatting** — meta.ai wraps URLs in `__...__` emphasis; the scorer strips this.

**Documentation required:** every consumer-surface results writeup must document the surface, tier (Fast/Instant/Thinking/Pro), and any surface-specific artifacts observed.

### API surfaces

**Examples:** AWS Bedrock, Anthropic API, Google Vertex, OpenAI API.

**Strengths:** clean-room configuration control. No URL rewriting, no conversation state leakage, explicit parameter control.

**Documentation required:** model ID, region or inference profile, temperature, max_tokens, thinking mode configuration (`enabled` / `adaptive` / `off`), thinking budget, sampling parameters.

**Stochasticity:** API calls at `temperature > 0` are nondeterministic. Single-shot SGR should be treated as a point estimate on a distribution; best-of-3 or majority-of-3 is recommended for publication-grade claims.

### Reasoning-mode asymmetries

Different models expose different reasoning controls. The benchmark documents the mode used per model rather than forcing a common mode. Observed modes across the three-model run:

| Model | Reasoning mode | Behavior |
|---|---|---|
| Muse Spark | Thinking (meta.ai) | Engaged deliberation before filling the form |
| Gemini Pro 3.1 | Thinking (Gemini App) | Engaged deliberation; reasoning traces visible |
| Claude Opus 4.7 | Adaptive (Bedrock) | Model-selected per image; chose not to engage on this corpus |
| Claude Opus 4.6 | Enabled, budget=10000 (Bedrock) | Always-on deliberation; trace visible per call |

Cross-model comparisons must acknowledge the reasoning-mode differences. The benchmark's position is that **each model is tested in its native shipping configuration** — forcing a common mode would benchmark an artificial configuration that no production user receives.

---

## Answer key and scoring protocol

### Ground truth

The answer key records, per image:
- Brand (canonical brand name)
- URL (the adversarial URL as rendered, character-exact)
- Confusable pair class
- Page type (login / email_first / landing / homepage / signup)
- Field 7 (login form present) — per-image
- Field 8 (password field present) — per-image
- Field 9 (QR code present) — per-image (the single override is BoC.png = yes)

Ground truth is established by **PM eyeball review of the actual image pixels**. When filename inference disagrees with what the bar shows, the bar wins. The answer key has evolved through v0.1 → v0.1.3 precisely because initial filename-inferred ground truths were corrected against image review.

### Run-time adjudication

During scoring, edge cases arise that the answer key may not have anticipated. When this happens:
- The scorer documents the decision and rationale in writing.
- The raw outputs are preserved so any reader can apply an alternate interpretation.
- When an adjudication pattern emerges across multiple images or models, the answer key is bumped to a new version and the decision is formalized.

Adjudication does not silently rewrite prior results. A v0.1 result stands as a v0.1 result. If re-scoring under a newer key is desired, the re-score is documented with the new version number.

### Mechanical re-scoring

The repository ships with `scripts/scorer.py` — a single-file Python tool that mechanically scores raw model outputs against any answer key version. This enables:

- Re-scoring any prior run against a new answer key version
- Independent verification of any published scoring number
- Running alternative rubrics (strict vs. v0.2 charitable) without re-parsing outputs

---

## What the benchmark can and cannot claim

### Can claim

- **Existence of Semantic Gravity failures.** If a frontier VLM returns `amazon.com` as the URL for an image that clearly shows `amaz0n.com`, the benchmark has measured a character-level auto-correction event — a classical Semantic Gravity failure. Multiple such events across multiple models is evidence that the failure mode is real and reproducible.
- **Per-model SGR on this corpus.** The benchmark produces a headline SGR number for each tested model. That number is a measurement, bounded by the corpus size and confidence interval.
- **Per-pair SGR patterns.** If a model has SGR = 1.000 on `1↔l` and 0.500 on `rn↔m`, that pattern is informative about pair-class sensitivity.
- **Failure-mode taxonomy.** Classical SG, Pattern-Consistency Gravity, and Structural Normalization Gravity have been observed as distinct phenomena with different mechanisms. The benchmark has surfaced three failure modes in three frontier models.

### Cannot claim

- **Population-level prevalence of model failure.** N = 41 is not large enough to claim "Model X fails on Y% of real-world phishing URLs." The corpus samples the model's behavior space; extrapolating to all possible adversarial URLs requires a much larger corpus.
- **Causal mechanism.** The benchmark observes *that* models auto-correct adversarial characters under brand pressure; it does not prove *why*. The academic literature (Vo et al. 2025, Li et al. 2025) proposes mechanisms; the benchmark neither confirms nor refutes them at the architectural level.
- **Real-world attack success rates.** A phishing URL's ability to deceive a VLM is necessary but not sufficient for real-world attack success. Attack success depends on email deliverability, user click-through, landing-page behavior, and credential-form submission — the benchmark tests only the VLM-reading step.
- **Universal model ranking.** Two models with the same SGR on this corpus may have very different behavior on other tasks. SGR is a narrow measurement; it is not a general model capability score.

---

## Reproducibility

The benchmark provides the materials for independent replication:

- The corpus images are published in `/corpus/homoglyph/`
- The evaluation prompt is specified byte-exact in `EVAL_PROMPT.md`
- The answer key is versioned and published in `ANSWER_KEY.md`
- Raw model outputs for every published run are preserved in `/results/{model}/raw-outputs.{json|md}`
- The mechanical scorer is published in `/scripts/scorer.py`

To replicate any run:

1. Obtain the same corpus (`/corpus/homoglyph/` — 41 PNGs)
2. Send each image + the eval prompt to the target model using the clean-room protocol
3. Capture raw outputs
4. Run the outputs through `scripts/scorer.py` against the desired answer key version
5. Compare published results

Discrepancies between a replication run and the published numbers indicate either model-update drift (the model version differs), surface-effect drift (the surface configuration differs), or run-time stochasticity (single-shot variance). All three are legitimate sources of disagreement; the benchmark does not claim deterministic reproducibility.

---

## Intended use

The benchmark is intended as:

- **A diagnostic tool for VLM developers.** Model labs can use the benchmark to measure Semantic Gravity resistance across model releases and identify specific failure modes to target.
- **An independent evaluation artifact.** Third parties can use the benchmark to measure any VLM they have access to, producing comparable results to the published runs.
- **A starting point for expansion.** v0.2 will expand corpus size, add structural-attack variants, and add multi-operator scoring. External contributions to the corpus expansion are welcome.

The benchmark is NOT intended as:

- **A ranking of "safe" vs. "unsafe" models.** SGR is one measurement among many; model choice should not be driven by SGR alone.
- **A product recommendation.** The benchmark does not endorse or discourage use of any specific model for any specific workflow.
- **A security guarantee.** A model scoring high on this benchmark may still be vulnerable to attacks not covered by the corpus. Security decisions require full threat modeling, not a single benchmark number.

---

## License

- **Methodology, corpus, and answer key:** CC BY 4.0 — free reuse with attribution.
- **Scorer code:** Apache 2.0 — free reuse with attribution; no warranty.

See `LICENSE` and `LICENSE-CORPUS` for the full terms.
