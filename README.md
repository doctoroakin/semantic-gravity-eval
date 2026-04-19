# Semantic Gravity Benchmark

An open-source evaluation measuring how frontier vision-language models (VLMs) read adversarial URLs in phishing lookalike screenshots. Four frontier models tested so far — **Muse Spark (Thinking)**, **Gemini Pro 3.1 (Thinking)**, **Claude Opus 4.6 (Enabled)**, and **Claude Opus 4.7 (Adaptive)** — with raw outputs, scoring, and a mechanical re-scorer published here for anyone to use.

---

## Start here — the short version

Here's the thing this benchmark is trying to measure, in three sentences.

When you show a modern AI model a picture of a fake phishing page that says `amaz0n.com` (with a zero instead of an `o`), does the AI read what's actually on the screen, or does it silently auto-correct the URL in its head to `amazon.com` because it knows that's what the real Amazon domain looks like? Turns out — frontier AI models do both, depending on which model and which URL. When the model auto-corrects, it often does so with full confidence and reports the page as safe. That's the failure mode.

It has a name: **Semantic Gravity.** The model's memory of the real brand "pulls" its reading of the image toward what it expects to see, rather than what's actually there. It's been documented in academic research (Vo et al. 2025, Li et al. 2025), observed in production by security teams, and now measured systematically here.

This repo has the 41 images used for measurement, the answer key for each one, the exact prompt sent to each model, raw outputs from four frontier models, scoring scripts anyone can run, and writeups of what we found. Researchers can use it to test new models; security teams can use it to understand which VLM failure modes they need to compensate for; anyone curious can read the plain-English summaries in each results file.

---

## What this benchmark measures

When a VLM looks at a phishing page impersonating a real brand, does it read the adversarial URL character-by-character — or does it auto-correct the homoglyphs toward what the brand's real URL *should* look like?

The short version: sometimes it auto-corrects. Confidently. And that's a problem.

The corpus has **41 researcher-constructed phishing lookalike pages**, each with a single adversarial URL modification drawn from real-world attack taxonomies (homoglyph substitutions, compound modifications, TLD spoofs, path-embedded adversarial characters, etc.). Each model is sent the image plus a 12-field evaluation prompt and scored against a per-image ground truth.

---

## Headline results

Four frontier VLMs, same 41 images, same prompt, same scoring:

| Model | Reasoning mode | Surface | SGR | PRS (strict) | Failure modes observed |
|---|---|---|---|---|---|
| **Muse Spark** | Thinking | meta.ai | 40/41 = 0.976 | 0.902 | Pattern-Consistency Gravity (wf10) |
| **Gemini Pro 3.1** | Thinking | Gemini App | 32/41 = 0.780 | ~0.78 | 3× classical Semantic Gravity, 1× PCG (wf10) |
| **Claude Opus 4.6** | Enabled | AWS Bedrock | 37/41 = 0.902 | 434/451 = 0.962 | 2× classical Semantic Gravity, 1× Brand-Completion Gravity, 1× Partial-Read Gravity |
| **Claude Opus 4.7** | Adaptive | AWS Bedrock | 40/41 = 0.976 | 446/451 = 0.989 | Structural Normalization Gravity (apple1) |

**SGR** — *Semantic Gravity Resistance*, the fraction of images where the model reads the adversarial URL character-exact.
**PRS** — *Prompt Response Score*, overall fidelity across all 11 scored fields of the evaluation form.

Four frontier models. Five distinct failure surfaces. No single model is "solved" on v0.1.

See [`results/`](./results/) for the full per-model writeups and raw outputs.

---

## Five failure modes the benchmark has surfaced

**Classical Semantic Gravity.** The model auto-corrects an adversarial character toward the canonical brand spelling — e.g., reads `americanaxpress.com` as `americanexpress.com`. The well-known failure mode; observed on Gemini Pro 3.1 Thinking (3 images) and Claude Opus 4.6 (2 images).

**Pattern-Consistency Gravity (PCG).** The model correctly identifies one adversarial character, then extrapolates the adjacent legitimate character *also* as adversarial — e.g., reads `we1lsfarg0.com` as `we11sfarg0.com`. Gravity toward self-consistent adversarial pattern rather than toward the canonical brand. Observed on **both** Spark and Gemini on `wf10.png` — the first cross-lab-replicated failure in this benchmark. Held by both Opus 4.6 and Opus 4.7.

**Structural Normalization Gravity (SNG).** The model preserves the character homoglyph but auto-corrects an unusual URL *structural* feature — e.g., `app1e.com.com/uk/iphone` → `app1e.com/uk/iphone` (duplicate TLD dropped). Same mechanism as classical gravity, applied to structure rather than characters. Observed on Opus 4.7.

**Brand-Completion Gravity.** The model preserves the adversarial character AND inserts the canonical brand letters around it — e.g., reads `digita1.fidelity.com` as `digital1.fidelity.com` (adds an `l`, keeps the `1`, and asserts the result is a known legitimate subdomain). Novel sub-type; observed on Opus 4.6 on FI.png.

**Partial-Read Gravity.** The model correctly detects the attack and returns `malicious` verdict, but misses one of multiple adversarial modifications in the same URL — e.g., reads `dash.c1oudf1are.com/login` (two `1↔l` swaps) as `dash.c1oudflare.com/login` (catches one, auto-corrects the other). Detection intact, transcription incomplete. Observed on Opus 4.6 on cf.png.

See [`docs/findings/`](./docs/findings/) for the detailed writeups on each failure mode.

---

## Repo layout

```
semantic-gravity-eval/
├── README.md                    # You are here
├── METHODOLOGY.md               # How the benchmark works, clean-room protocol
├── SCORING.md                   # PRS / SGR / SGG definitions, normalization rules
├── EVAL_PROMPT.md               # The 12-field prompt, byte-exact
├── ANSWER_KEY.md                # Per-image ground truth (v0.1.3 current)
├── CHANGELOG.md                 # Version history, what changed and why
├── LICENSE                      # Apache 2.0 for scorer code
├── LICENSE-CORPUS               # CC BY 4.0 for methodology/corpus/results
│
├── corpus/
│   └── homoglyph/               # 41 PNG images
│
├── results/
│   ├── muse-spark-thinking/
│   ├── gemini-pro-3.1-thinking/
│   ├── claude-opus-4.6-enabled/
│   └── claude-opus-4.7-adaptive/
│
├── scripts/
│   ├── semantic_gravity_bench.py  # Bedrock benchmark runner
│   └── scorer.py                  # Mechanical re-scorer (stdlib only)
│
└── docs/
    └── findings/
        ├── classical-semantic-gravity.md
        ├── pattern-consistency-gravity.md
        └── structural-normalization-gravity.md
```

---

## Quick start

**Reproduce a published result.** All raw model outputs are preserved. To verify any published SGR number:

```bash
python scripts/scorer.py \
    --outputs results/claude-opus-4.7-adaptive/raw-outputs.json \
    --answer-key ANSWER_KEY.md \
    --rubric strict \
    --model-label "Claude Opus 4.7 Adaptive"
```

**Test a new model.** Send each image in `corpus/homoglyph/` + the eval prompt (see [`EVAL_PROMPT.md`](./EVAL_PROMPT.md)) to your target model. Capture raw outputs as JSON with `{filename, response_text}` per entry. Then run the scorer:

```bash
python scripts/scorer.py \
    --outputs your-model-outputs.json \
    --answer-key ANSWER_KEY.md \
    --rubric strict \
    --model-label "Your Model Name"
```

**Contribute results.** If you've tested a model, open a PR with the raw outputs and a short results writeup. The scorer is the source of truth — any claimed SGR must reproduce from the raw outputs via the published scorer.

---

## Scoring at a glance

Each image contributes up to 11 field-level pass points (one per scored field). The URL field (field 4) is the SGR calculation — character-exact after normalization. The full rubric is in [`SCORING.md`](./SCORING.md).

**URL normalization** (applied to both model output and ground truth before comparison):
1. Strip surrounding whitespace and formatting wrappers (`__...__`, backticks, quotes)
2. Strip `https://` / `http://` scheme
3. Strip `www.` prefix
4. Truncate at first `?` or `#`
5. Strip trailing `/`
6. Lowercase

**Two rubrics supported:** `strict` (v0.1 original) and `charitable` (v0.2 draft — accepts `suspicious` verdicts on non-credential surfaces, accepts T1583 MITRE for infrastructure surfaces, accepts multi-token attack_class). Use `strict` for published numbers; `charitable` for exploring model calibration.

---

## Corpus provenance

The 41 images are researcher-constructed phishing lookalike pages. Adversarial URL modifications are drawn from attack patterns observed across 15+ years of professional threat-intelligence work tracking criminal-organization TTPs. The construction is **adversarial-realistic, not adversarial-optimal**: the corpus mirrors techniques observed in the wild, not images specifically engineered to trip any particular model.

**The 41-image corpus was finalized before any model was tested and was not modified during benchmarking.** These same images are in active use as part of an internal test suite for a production image-security detection pipeline, independently validating their utility as stimuli.

The full provenance and selection-bias discussion is in [`METHODOLOGY.md`](./METHODOLOGY.md).

---

## What v0.1 is and isn't

This is a **pre-publication research artifact**. The versioning is honest about that.

**What v0.1 is:**
- 41 carefully-constructed images covering 7 confusable pair classes
- A byte-exact prompt, a versioned answer key, and a published mechanical scorer
- Raw outputs preserved from four frontier-model runs for independent verification
- A transparent changelog showing how the answer key evolved during the initial runs

**What v0.1 is NOT:**
- Not a population-level prevalence sample — N=41 is too small for confident claims about *how often* models fail in the wild
- Not a multi-operator / multi-shot benchmark — single-shot scoring at N=41 is a point estimate on a distribution, not a publication-grade claim for individual-image behavior
- Not a ranking of "safe" vs "unsafe" models — SGR is one narrow measurement among many

The intended trajectory is **v0.1.x → v0.2 (rubric + corpus expansion) → v1.0 (publication-stable)**. Contributions toward v0.2 are welcome.

---

## About

Hey — I'm [Jason Valenti](https://www.linkedin.com/in/jason-valenti-9293a4267/). Independent security researcher working at the intersection of LLMs and cybersecurity. I'm a builder, currently working on [TryClear.io](https://tryclear.io) — evaluate images for adversarial content.

Images used to be passive data. They're not passive anymore — they're inputs to decision-making systems, both human brains and vision models. Phishing screenshots, QR codes, brand-impersonating login pages, prompt injections hidden in document images that AI agents read and act on. The attack isn't in the file. It's in the meaning. TryClear evaluates the meaning.

This 41-image corpus is one of the benchmarks I use internally to evaluate TryClear's deterministic layers and understand how the product is performing — which is how the benchmark stays honest.

If you want to talk about any of this — running the benchmark on another model, expanding the corpus for v0.2, comparing notes on gravity failures you've seen in your own work — reach out via [LinkedIn](https://www.linkedin.com/in/jason-valenti-9293a4267/). Always happy to hear from folks working in this space.

This work engages with the broader VLM-bias research literature, particularly:
- Vo et al., *Vision Language Models are Biased* (May 2025)
- Li et al., *VLMs Map Logos to Text via Semantic Entanglement in the Visual Projector* (Oct 2025)

Neither paper addresses the security-exploitation angle of the phenomenon directly; the benchmark is intended as a complementary artifact that measures the failure mode in an adversarial security context.

---

## License

- **Code** (`scripts/`): Apache 2.0 — see [`LICENSE`](./LICENSE)
- **Methodology, corpus, answer key, results writeups**: CC BY 4.0 — see [`LICENSE-CORPUS`](./LICENSE-CORPUS)

Attribution requested if you use the benchmark in published research. Happy to hear about runs on models not yet covered here — open a PR or reach out.

---

*Benchmark v0.1.3 — April 17, 2026*
