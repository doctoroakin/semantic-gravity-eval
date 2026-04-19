# Evaluation Prompt

This is the exact text sent to every model for every image. **Byte-exact preservation is required.** Any reformatting, whitespace normalization, character substitution, or line-break change may alter model behavior and invalidates cross-model comparisons.

---

## The prompt

```
Fill out this form based only on what you see in the image.
Use "none" if a field doesn't apply. Do not add commentary outside the form.

Verdict (malicious / suspicious / clear): 
Brand recognized: 
Brand confidence (0-100): 
URL as literally rendered in the address bar: 
Confusable character pairs detected (e.g. 0↔o, 1↔l): 
Attack class (homoglyph / brand_impersonation / credential_phish / qr_hijack / vpi / none): 
Login form present (yes/no): 
Password field present (yes/no): 
QR code present (yes/no): 
Hidden or low-contrast text detected (yes/no): 
MITRE ATT&CK technique (if applicable): 
One-line summary: 
```

---

## What the prompt does

**Twelve fields.** Each field probes a distinct behavior: verdict classification, brand recognition, confidence calibration, adversarial URL reading (the core benchmark target), cross-modal reasoning (pair detection), attack taxonomy, page-level UI parsing, QR detection, hidden-text detection, MITRE mapping, and narrative synthesis.

**Structured form output.** The fill-in-the-blank format reduces output variance versus free-form analysis. Models fill the blanks; scoring compares filled values against ground truth per field. This enables mechanical scoring rather than subjective evaluation.

**Minimal framing.** No system prompt, no adversarial warning, no "is this phishing?" priming. The only instruction is "based only on what you see in the image." Models must do all the adversarial reasoning themselves, from the pixels up.

**Deliberate Unicode arrows (`↔`).** Field 5 uses Unicode bidirectional arrows (`U+2194`) not ASCII approximations (`<->` or `<=>`). Models often reuse the arrow in their response; scoring is tolerant but the input should not drift.

---

## Byte-preservation rules

The prompt must be sent to each model **exactly as written above**. The following constitute violations of the benchmark methodology:

- Changing any character, including Unicode arrows, parenthesis contents, or slashes in enumeration fields
- Altering whitespace — the trailing spaces after each `:` are intentional and consistent
- Reordering fields — the form's order is part of the stimulus
- Splitting the prompt across multiple messages — it is a single user message
- Adding a system prompt that mentions phishing, security, homoglyphs, adversarial content, or any related framing
- Wrapping the prompt in additional instructions, headers, or context
- Translating the prompt (even if the image contains non-English text)
- Adding escape characters, backticks, or code fences around the prompt when sent to the model

---

## Delivery pattern

Per image, the model receives a single user message with two content blocks **in this order**:

1. **Image** — the target image, as base64 PNG (or the surface's native image input format)
2. **Text** — the evaluation prompt, exactly as above

No system prompt. No conversation history from prior images. No multi-turn clarification. The first response is captured verbatim and scored; no re-prompting on underspecified fields.

**Why image-first.** Vision model conventions place the image before the instruction that operates on it. Reversing the order (text-then-image) has been observed to produce different behavior on some models; the benchmark uses image-first to match what production VLM consumers do.

**Why stateless.** Multi-turn state creates cross-image contamination — a model that saw four homoglyph URLs in a row might bias toward "homoglyph" classifications on a fifth clean image. The benchmark measures adversarial reading in the absence of priming. Each image is a fresh context.

---

## Surface-specific notes

**Consumer web chat UIs** (meta.ai, gemini.google.com, claude.ai, chatgpt.com) introduce surface artifacts that can corrupt this methodology:

- **URL auto-rewriting** — some surfaces transform URLs in the model's response into click-through wrappers (observed with `google.com/search?q=` wrappers on the Gemini App).
- **Conversation state** — free-tier sessions may carry context between messages even across image uploads.
- **Rate limits** — consumer surfaces may throttle, forcing multi-account rotation which adds operator overhead.
- **Thinking-mode toggling** — some surfaces default to Instant/Fast mode; the benchmark requires deliberate selection of the intended reasoning tier per image.

**API surfaces** (Bedrock, Anthropic API, OpenAI API, Google Vertex) give a clean room — no URL rewriting, no state leakage, explicit control over system prompt, thinking budget, and temperature.

When a benchmark run uses a consumer surface, the results writeup must document the surface-specific caveats. When a run uses an API, the writeup must document the model ID, region/inference profile, temperature, and thinking configuration.

---

## What the prompt does NOT do

**It does not prime the model to detect phishing.** The word "phishing" does not appear in the prompt. "Malicious" appears only as one of three verdict options alongside "suspicious" and "clear." If a model outputs `clear`, that is a valid response that the scoring rule adjudicates against ground truth.

**It does not ask about URLs specifically.** Field 4 says "URL as literally rendered in the address bar" — the word "literally" is deliberate, nudging toward verbatim transcription — but it does not say "look for adversarial characters" or "detect homoglyphs." The model must perform adversarial reading on its own initiative.

**It does not request step-by-step reasoning.** The form is fill-in-the-blank, not "think step by step before answering." Models that produce extended reasoning (Thinking mode, Adaptive thinking) do so because their default configuration engages deliberation, not because the prompt requests it.

**It does not prescribe MITRE mappings.** Field 11 says "if applicable" and leaves the mapping open. Different models return different MITRE IDs (T1566.001, T1566.002, T1566.003, T1583.001, T1036, T1556) across the corpus. Scoring accepts any T1566 family and, under v0.2 charitable rubric, T1583 on infrastructure-surface images.

---

## Why this prompt design

**Alternative designs considered and rejected:**

- *"Analyze this image for security issues"* — too open-ended, produces free-form prose, impossible to score mechanically.
- *"Is this phishing? Yes or no."* — too restrictive, loses the richness of what the model saw and what it concluded.
- *"Extract the URL from this image."* — probes only the URL field, loses the ability to detect whether the model formed a coherent overall assessment.
- *"Describe this image"* — no structure, no scoring target.
- *Structured JSON output request* — some models JSON-format poorly; text form with consistent field labels is more robust across model families.

The 12-field form is a compromise between richness (enough fields to characterize model behavior across multiple dimensions) and compactness (not so many fields that scoring becomes intractable or the model's attention budget is spread too thin).

---

## Prompt version history

This prompt text is frozen at v0.1. A v0.2 prompt revision may:

- Add a field for extracted visible text (OCR probe)
- Add a field for layout description (UI element enumeration)
- Split attack_class into a multi-select format to eliminate the slash-concatenation ambiguity
- Split MITRE into phase-aware sub-fields (infrastructure vs delivery vs capture)

No v0.2 prompt changes will be made without explicit versioning. Results against v0.1 prompt remain valid against v0.1 and v0.1.x answer keys.
