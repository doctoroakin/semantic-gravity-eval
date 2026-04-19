# Changelog

All notable changes to the Semantic Gravity Benchmark are documented here. This benchmark evolves through transparent iteration — the changelog exists specifically so readers can see what was learned at each stage and verify claims against the version that was live when a given result was produced.

---

## [v0.1.3] — April 17, 2026

### Changed
- **`dell.png` ground truth corrected** to record the full OAuth authorization path: `de1l.com/di/idp/dwa/authorize`. The v0.1.2 key recorded domain-only (`de1l.com`), inherited from v0.1's filename inference. Under the benchmark's scoring rule (compare URL up to the first `?`), the scored ground truth is the full path. Both Muse Spark Thinking (April 16) and Claude Opus 4.7 Adaptive (April 17) returned this path verbatim with the `1↔l` homoglyph at position 3 preserved. The v0.1.3 key reconciles the recorded key with what the scoring rule actually compares.

### Added
- **Structural Normalization Gravity (SNG) documented** as a new gravity sub-type. Observed on Opus 4.7 Adaptive on `apple1.png`: the model preserved the `1↔l` homoglyph but dropped the duplicate TLD (`.com.com` → `.com`). This is auto-correction targeting URL structural features rather than character homoglyphs — a distinct failure mode from classical Semantic Gravity and Pattern-Consistency Gravity.
- **Three-model result summary table** added to the answer key showing SGR, classical SG count, PCG count, SNG count, and compound-attack behavior across Muse Spark Thinking, Gemini Pro 3.1 Thinking, and Opus 4.7 Adaptive.

### Rationale
The dell.png correction surfaced during Opus 4.7 scoring; both Spark and Opus were returning the full OAuth path identically, but the answer key was domain-only, causing strict-rubric scoring to mark both as fail. Under adjudication the full-path reads were always PASS — the key needed to reflect that. Zero net change to any model's headline SGR.

---

## [v0.1.2] — April 17, 2026

### Changed
- **`HarborFr8.png` ground truth corrected** to `harb0rfreight8.com/my-account/login`. PM eyeball review of actual image pixels on April 17 confirmed the domain contains both the `0↔o` homoglyph AND an appended `8` — a **compound attack** with two structurally independent adversarial modifications on a single URL. The v0.1.1 key incorrectly recorded this as the same domain as `Harb0rFr8.png` with a deeper path.
- **Harbor Freight pair relabeled** from URL-length test to simple-vs-compound attack test. The pair now tests whether models handle a compound attack (`0↔o` + appended digit) as well as they handle the simple single-character homoglyph.
- **Compound pair class added** to the distribution table (`0↔o + append-8`, count 1).

### Rationale
During transcript review, a submission gap was discovered in the original Spark run: `HarborFr8.png` was never actually sent to Spark on April 16, due to an operator filename-inference error (assumed `Fr8` was mnemonic shorthand for "Freight" rather than containing a literal `8`). The image was recaptured in a fresh Thinking-mode Spark session on April 17; Opus 4.7 then received the corrected image in its clean April 17 run.

---

## [v0.1.1] — April 16, 2026

### Changed
- **All URLs transcribed from actual address bars.** The v0.1 key had inferred URLs from filenames for several images. Six entries were flagged (⚠️) during the Spark run and cross-corroborated against model output + visual spot-check; one entry (`clevland.png`) had been missing from v0.1 and was added.
- **Fields 7 (login_form_present) and 8 (password_field_present) moved from universal invariants to per-image values.** v0.1 asserted `yes/yes` for all images; the corpus actually contains three page types (single-step login, email-first SSO, and landing/homepage/signup surfaces). Each image now carries per-image values for these fields based on what's actually rendered.
- **`apple1.png` reclassified** from "double-homoglyph" to TLD-spoof via registered lookalike domain (`app1e.com.com/uk/iphone` — the attacker registered `com.com` as the lookalike domain).

### Added
- **`clevland.png`** — previously missing from v0.1 scoring, added as the 41st image.
- **Pattern-Consistency Gravity (PCG) documented** as a gravity sub-type distinct from classical brand-canonical gravity. Observed on `wf10.png` where the model auto-corrected a legitimate character to match an adjacent adversarial character (`we1lsfarg0.com` → `we11sfarg0.com`), extrapolating toward self-consistent adversarial pattern rather than toward the canonical brand. Replicated cross-lab on both Muse Spark Thinking and Gemini Pro 3.1 Thinking.
- **v0.2 rubric clarifications** — notes on proposed charitable-rubric adjustments for fields 1, 6, and 11 based on observed model behavior (multi-token attack_class, T1583 on infrastructure surfaces, suspicious hedging on non-credential pages).

### Rationale
The Muse Spark Thinking benchmark run on April 16 surfaced the v0.1 answer key's inference errors and universal-invariant over-reach. The April 16 scoring session adjudicated these in real time; v0.1.1 formalizes those adjudications as the canonical answer key.

---

## [v0.1] — April 2026

### Initial release
- 40 images (clevland.png missing, added in v0.1.1)
- Universal invariants asserted across all images (verdict, attack_class, login_form, password_field, qr_code, hidden_text, mitre)
- URLs inferred from filename patterns (six inferences were later confirmed cross-corroboratively; several others were incomplete and corrected in v0.1.1)
- Scoring methodology: PRS (11-field total score) + SGR (URL field only, character-exact after normalization)
- Normalization: strip `https?://`, strip `www.`, strip at first `?` or `#`, strip trailing `/`, lowercase

---

## Version numbering philosophy

The benchmark uses semantic versioning adapted for a research artifact:

- **Patch (v0.1.1 → v0.1.2)** — corrections to ground truth that reflect what was already visibly true in the images. Scoring outcomes may shift on specific images but headline numbers reconcile to previous adjudications.
- **Minor (v0.1 → v0.2)** — scoring rubric changes, corpus expansion, or new pair classes. Previous version's results remain valid as historical artifacts; new runs use the new version.
- **Major (v1.0)** — reserved for a publication-stable benchmark release with validated multi-operator scoring, expanded corpus (200+ images), and cross-lab reproducibility verification.

v0.1.x versions are explicitly pre-publication. Results produced against any v0.1.x key are valid datapoints for the research community but should not be cited as representing final benchmark numbers. The intended trajectory is: v0.1.x → v0.2 (rubric + corpus expansion) → v1.0 (publication-stable).

---

## Per-model result history

| Model | Date | SGR | PRS (strict) | Against answer key |
|---|---|---|---|---|
| Muse Spark (Thinking) | April 16 + April 17 recaptures, 2026 | 40/41 = 0.976 | 407/451 = 0.902 | v0.1.3 (reconciled) |
| Gemini Pro 3.1 (Thinking) | April 16, 2026 | 32/41 = 0.780 | ~0.776 | v0.1.2 |
| Claude Opus 4.7 (Adaptive) | April 17, 2026 | 40/41 = 0.976 | 446/451 = 0.989 | v0.1.3 |

Historical note: Spark's SGR was scored as 40/41 under v0.1 strict, v0.1.1, v0.1.2 with methodology updates, and v0.1.3 with the dell.png reconciliation. The headline number has remained stable across all four versions because the Spark-specific adjudications applied during the April 16 run happened to match the formal rules adopted in v0.1.3. This is a feature of the run-time adjudication pattern, not a coincidence.
