# Semantic Gravity Benchmark — Answer Key v0.1.3

**Supersedes:** v0.1.2
**Date regenerated:** April 17, 2026
**Corpus size:** 41 images
**Location:** `~/Desktop/TestPics/homoglyph/`
**Skip:** `harb_zoomed.png` (cropped zoom, not a full screenshot)
**Exclude from scoring:** `clean/` subfolder (reserved for v0.2 false-positive testing)

---

## What changed from v0.1.2

One correction, prompted by the April 17 Opus 4.7 Bedrock run.

`dell.png` address bar displays the full OAuth authorization URL: `https://www.de1l.com/di/idp/dwa/authorize?response_type=id_token&client_id=...`. Under the v0.1 scoring rule (compare up to the first `?`), the scored ground truth is `de1l.com/di/idp/dwa/authorize`.

The v0.1.2 answer key recorded this URL as domain-only (`de1l.com`), inherited from v0.1's filename-inferred ground truth. Both Muse Spark Thinking (April 16) and Claude Opus 4.7 (April 17) returned the full OAuth path with the homoglyph `1` at position 3 preserved. During the Spark scoring session, this was adjudicated PASS (the homoglyph character was the canonical test of the image and was preserved). The answer key needs to reflect what the scoring rule actually compares.

This is not a change in scoring outcome — it is a change in the recorded key to match the scoring behavior that has been applied consistently across both models. Spark's SGR is unchanged; Opus's SGR moves to 40/41 (from 39/41 under the stricter v0.1.2 interpretation).

---

## What changed from v0.1.1 → v0.1.2 (carried forward)

`HarborFr8.png` address bar shows `harb0rfreight8.com/my-account/login` — a **compound attack** combining the `0↔o` homoglyph with an appended `8` producing a fully distinct lookalike domain. The v0.1.1 key incorrectly recorded this as the same domain as `Harb0rFr8.png` with a deeper path. Confirmed by PM eyeball review of the actual image pixels on April 17, 2026.

This makes the Harbor Freight pair a **simple-vs-compound attack test** rather than a URL-length test:

- `Harb0rFr8.png` — simple `0↔o` on canonical brand domain
- `HarborFr8.png` — compound `0↔o` + appended `8` producing a fully distinct lookalike domain

The confusable-pair label for `HarborFr8.png` is `0↔o + append-8` to reflect the compound structure.

---

## What changed from v0.1 → v0.1.1 (carried forward)

Corrections from the Muse Spark Thinking benchmark run on April 16, 2026. Six flagged (⚠️) entries cross-corroborated against model outputs and confirmed by visual spot-check; one entry (`clevland.png`) added. Several URLs had been inferred from filenames and were incomplete once the actual address bars were read.

Principle: **the address bar itself is the ground truth.** Wherever filename inference disagreed with what the bar shows, the bar wins. This includes paths, query-string positions, subdomain structure, and TLD characters.

**Fields 7 (login_form_present) and 8 (password_field_present) are no longer treated as universal invariants.** The v0.1 key asserted `yes/yes` for every image. The corpus actually contains three page types — single-step login pages, email-first SSO pages (email visible, password on second screen), and landing / marketing / homepage surfaces (no credential form visible at all). Each image carries per-image values for these fields based on what's actually rendered.

`apple1.png` is not a URL-homoglyph variant. It uses a TLD-spoof structure (`app1e.com.com/uk/iphone`) — the attacker registered `com.com` as a domain.

---

## Invariants (unchanged from v0.1)

Every image is a browser screenshot of a real brand's web page with an adversarial character substitution in the URL bar. For every image:

```yaml
verdict: malicious              # see v0.2 note below on suspicious for non-credential surfaces
attack_class: homoglyph         # brand_impersonation and credential_phish also accepted
qr_code_present: no             # except BoC.png (per-image override: yes)
hidden_or_low_contrast_text: no
mitre_attack: T1566             # T1566.001 and T1566.002 also accepted
                                # see v0.2 note below on T1583 for infrastructure surfaces
```

Fields 7 and 8 are specified per-image.

---

## Per-image answer key

Brand confidence: pass if model outputs any number ≥80 AND brand is correct.
URL: scored character-exact on the full URL up to query parameters (domain + path). See scoring doc.
`page_type` is informational — it drives the `login_form_present` and `password_field_present` values.

```yaml
# ───────────────────────────────────────────────────────────────────────────────
# Filename                  Brand                                Adversarial URL (character-exact)                                Confusable              Page type          Login  Pwd
# ───────────────────────────────────────────────────────────────────────────────
AlB.png:                  { brand: "Alabama Credit Union",       url: "alabarnacu.com",                                            pair: rn↔m,             page: login,        login: yes, pwd: yes }
alls.png:                 { brand: "Allstate",                   url: "a11state.com",                                              pair: 1↔l,              page: login,        login: yes, pwd: yes }  # adjacent double
Amazon0.png:              { brand: "Amazon",                     url: "amaz0n.com",                                                pair: 0↔o,              page: homepage,     login: no,  pwd: no  }
apple1.png:               { brand: "Apple",                      url: "app1e.com.com/uk/iphone",                                   pair: 1↔l,              page: landing,      login: no,  pwd: no  }  # TLD-spoof via com.com
AutoZ.png:                { brand: "AutoZone",                   url: "aut0zone.com/signin",                                       pair: 0↔o,              page: email_first,  login: yes, pwd: no  }
Ax.png:                   { brand: "American Express",           url: "americanaxpress.com/en-us/account/login",                   pair: a↔e,              page: login,        login: yes, pwd: yes }
bcbs.png:                 { brand: "Highmark Blue Cross Blue Shield", url: "b1uecross-highmark.com/member/member-guide",           pair: 1↔l,              page: landing,      login: no,  pwd: no  }
BoA0.png:                 { brand: "Bank of America",            url: "bankofamerica-0nline.com",                                  pair: 0↔o,              page: login,        login: yes, pwd: yes }
Br.png:                   { brand: "Banana Republic",            url: "secure-bananarepub1ic.gap.com/my-account/sign-in",          pair: 1↔l,              page: email_first,  login: yes, pwd: no  }
BoC.png:                  { brand: "Bank of China",              url: "ebsnew.b0c.cn/boc15/login.html",                            pair: 0↔o,              page: login,        login: yes, pwd: yes, qr: yes }  # WeChat QR override
CapOne.png:               { brand: "Capital One",                url: "verified.capita1one.com/auth/signin",                       pair: 1↔l,              page: login,        login: yes, pwd: yes }
cf.png:                   { brand: "Cloudflare",                 url: "dash.c1oudf1are.com/login",                                 pair: 1↔l,              page: login,        login: yes, pwd: yes }  # non-adjacent double
Chaseon1.png:             { brand: "Chase",                      url: "chase-on1ine.com",                                          pair: 1↔l,              page: login,        login: yes, pwd: yes }
clevland.png:             { brand: "Cleveland Clinic",           url: "mychart.cleve1andclinic.org/authentication/login",          pair: 1↔l,              page: email_first,  login: yes, pwd: no  }
Coin1.png:                { brand: "Coinbase",                   url: "coinbase-1ogin.com",                                        pair: 1↔l,              page: landing,      login: no,  pwd: no  }
CS.png:                   { brand: "Charles Schwab",             url: "c1ient.schwab.com/areas/access/login",                      pair: 1↔l,              page: login,        login: yes, pwd: yes }
dell.png:                 { brand: "Dell",                       url: "de1l.com/di/idp/dwa/authorize",                             pair: 1↔l,              page: email_first,  login: yes, pwd: no  }  # v0.1.3: full OAuth path
FI.png:                   { brand: "Fidelity",                   url: "digita1.fidelity.com/prgw/digital/signin/retail",           pair: 1↔l,              page: login,        login: yes, pwd: yes }
G00gle.png:               { brand: "Google",                     url: "g00gle.com",                                                pair: 0↔o,              page: homepage,     login: no,  pwd: no  }  # adjacent double
Google0.png:              { brand: "Google",                     url: "g0ogle.com",                                                pair: 0↔o,              page: homepage,     login: no,  pwd: no  }  # single
Gs.png:                   { brand: "Goldman Sachs",              url: "go1dman.com",                                               pair: 1↔l,              page: login,        login: yes, pwd: yes }
Harb0rFr8.png:            { brand: "Harbor Freight",             url: "harb0rfreight.com/my-account/login",                        pair: 0↔o,              page: login,        login: yes, pwd: yes }  # simple 0↔o
HarborFr8.png:            { brand: "Harbor Freight",             url: "harb0rfreight8.com/my-account/login",                      pair: "0↔o + append-8", page: login,        login: yes, pwd: yes }  # compound attack
HomeD.png:                { brand: "Home Depot",                 url: "homedep0t.com/auth/view/signin",                            pair: 0↔o,              page: email_first,  login: yes, pwd: no  }
lemon.png:                { brand: "Lululemon",                  url: "shop.1u1u1emon.com/account/login",                          pair: 1↔l,              page: email_first,  login: yes, pwd: no  }  # triple
los.png:                  { brand: "Lowes",                      url: "lovves.com",                                                pair: vv↔w,             page: homepage,     login: no,  pwd: no  }
Marb.png:                 { brand: "Marlboro",                   url: "gtc.mar1boro.com/marlboro/security/login",                  pair: 1↔l,              page: login,        login: yes, pwd: yes }  # long URL (JWT stripped by normalization)
Micro0.png:               { brand: "Microsoft",                  url: "account.micr0soft.com/account",                             pair: 0↔o,              page: email_first,  login: yes, pwd: no  }
Netflix1.png:             { brand: "Netflix",                    url: "netf1ix.com",                                               pair: 1↔l,              page: landing,      login: no,  pwd: no  }
Nf01.png:                 { brand: "Navy Federal Credit Union",  url: "navyfederal.0rg/loans-cards/mortgage/mortgage-rates/conventional-fixed-rate-mortgages.html", pair: 0↔o, page: landing, login: no, pwd: no }  # TLD homoglyph
Notion_HOmoglyph.png:     { brand: "Notion",                     url: "n0ti0n.so/login",                                           pair: 0↔o,              page: email_first,  login: yes, pwd: no  }  # non-adjacent double, .so TLD
NSB.png:                  { brand: "Nevada State Bank",          url: "nsbank.com/pers0nal/sign-in",                               pair: 0↔o,              page: login,        login: yes, pwd: yes }  # path homoglyph
or.png:                   { brand: "Oracle",                     url: "signon.orac1e.com/signin",                                  pair: 1↔l,              page: email_first,  login: yes, pwd: no  }
PayPal1.png:              { brand: "PayPal",                     url: "paypa1.com/signin",                                         pair: 1↔l,              page: email_first,  login: yes, pwd: no  }
SimpMarb.png:             { brand: "Marlboro",                   url: "gtc.mar1boro.com",                                          pair: 1↔l,              page: login,        login: yes, pwd: yes }  # short URL (paired with Marb.png)
sl.png:                   { brand: "Slack",                      url: "s1ack.com/get-started",                                     pair: 1↔l,              page: signup,       login: yes, pwd: no  }
slsf.png:                 { brand: "Salesforce",                 url: "login.sa1esforce.com",                                      pair: 1↔l,              page: login,        login: yes, pwd: yes }
WellsRn.png:              { brand: "Wells Fargo",                url: "wellsfargo-onlirne.com",                                    pair: rn↔m,             page: login,        login: yes, pwd: yes }
wf10.png:                 { brand: "Wells Fargo",                url: "we1lsfarg0.com",                                            pair: "1↔l + 0↔o",      page: login,        login: yes, pwd: yes }  # mixed-pair
wgreen.png:               { brand: "Walgreens",                  url: "wa1greens.com/login.jsp",                                   pair: 1↔l,              page: login,        login: yes, pwd: yes }
wmrt.png:                 { brand: "Walmart",                    url: "identity.wa1mart.com/account/login",                        pair: 1↔l,              page: email_first,  login: yes, pwd: no  }
```

---

## Confusable pair distribution

| Pair class                  | Image count | Notable images                                                              |
|-----------------------------|-------------|-----------------------------------------------------------------------------|
| 1↔l                         | 24          | FI, sl, CS, slsf, CapOne, cf (non-adjacent double), alls (adjacent double), lemon (triple) |
| 0↔o                         | 12          | Amazon0, Harb0rFr8, HomeD, BoC, Micro0, Nf01 (TLD), NSB (path), G00gle (adjacent double), Google0, Notion_HOmoglyph (non-adjacent double) |
| rn↔m                        | 2           | AlB (inside brand name), WellsRn (in appended keyword)                      |
| vv↔w                        | 1           | los (Lowe's)                                                                |
| a↔e                         | 1           | Ax (American Express)                                                       |
| Mixed (1↔l + 0↔o)           | 1           | wf10                                                                        |
| Compound (0↔o + append-8)   | 1           | HarborFr8                                                                   |

---

## v0.2 scoring clarifications

Three rubric issues v0.2 should formalize:

**Attack class field (field 6).** Models frequently return slash-concatenated multi-class outputs (e.g., `homoglyph / brand_impersonation / credential_phish`). v0.2 should accept: *passes if the stripped output contains at least one accepted token AND does not contain any rejected token (`qr_hijack`, `vpi`, `none`).*

**MITRE ATT&CK field (field 11).** For images showing infrastructure surfaces (landing / homepage / signup), models may correctly map to `T1583.001` (Acquire Infrastructure: Domains) rather than `T1566.x` (Phishing). Both are defensible readings of the underlying attack, distinguished by phase. v0.2 should accept either family for images where `page_type` is `landing` / `homepage` / `signup`.

**Verdict field (field 1).** Some models hedge from `malicious` to `suspicious` on non-credential-capture surfaces. v0.2 should consider accepting `suspicious` as a pass when `page_type` is `landing` / `homepage` / `signup`. The strict `malicious`-only rule is retained for `login` and `email_first` pages.

These changes do not affect SGR — SGR is computed only on field 4 and is insulated from rubric tensions on adjacent fields.

---

## Pattern-Consistency Gravity (carried from v0.1.1)

On `wf10.png` (`we1lsfarg0.com`), the April 16 Muse Spark Thinking run and the April 16 Gemini Pro 3.1 Thinking run both produced the same character-for-character error: `we11sfarg0.com`, auto-correcting the legitimate `l` at position 4 to match the adversarial `1` at position 3. This is gravity toward self-consistent adversarial pattern rather than toward the canonical brand. Two frontier VLMs from different labs, both in reasoning-engaged modes, same image, same specific failure.

Opus 4.7 Adaptive (April 17) **held on this image** — returned `we1lsfarg0.com` character-exact. First model in the benchmark to read the mixed-pair URL correctly.

---

## Structural Normalization Gravity (new in v0.1.3)

The April 17 Opus 4.7 Bedrock run introduced a new gravity sub-category.

On `apple1.png`, ground truth URL is `app1e.com.com/uk/iphone` — the attacker registered `com.com` as a domain, producing what reads as a duplicate TLD. Opus 4.7 returned `app1e.com/uk/iphone` — **dropped the duplicate `.com`**. The `1↔l` homoglyph was correctly preserved.

This is not classical character-homoglyph Semantic Gravity (the homoglyph was held). It is auto-correction of an unusual URL structural feature toward the canonical form. The model "corrected" what it perceived as an erroneous duplicate TLD.

**Proposed classification:** *Structural Normalization Gravity* — a subclass of classical Semantic Gravity where the adversarial feature is an unusual URL structure (duplicate TLDs, unusual subdomain patterns, atypical path structures) rather than a character-level substitution, and the model normalizes toward the canonical structural form.

Spark Thinking and Gemini Pro 3.1 Thinking both preserved the duplicate `.com.com` on this image. This is the first known Structural Normalization Gravity event in the benchmark, specific to Opus 4.7 in this corpus.

**Corpus implication for v0.2:** expand structural-feature test cases deliberately. Candidates: duplicate TLDs, subdomain depth anomalies, unusual path structures, punycode domains, double-hyphen patterns, protocol obfuscation.

---

## Compound-attack test case (HarborFr8.png)

The `HarborFr8.png` image is the single compound-attack test case in the v0.1 corpus. Domain `harb0rfreight8.com` carries two structurally independent modifications: the `0↔o` homoglyph and an appended `8`.

Tested against three models on the April 17 fresh captures:
- Muse Spark Thinking: character-exact ✓
- Claude Opus 4.7 Adaptive: character-exact ✓

Single-image result on a single pair class. Not a generalizable finding. Indicates frontier VLMs can handle at least one example of the compound-attack class without degradation. v0.2 should expand this coverage with append-digit, append-letter, append-word, prepend, infix variants.

---

## Three-model result summary (April 2026)

| Model | Reasoning mode | SGR | Classical SG | PCG | Structural Normalization | Compound |
|---|---|---|---|---|---|---|
| Muse Spark | Thinking | 40/41 = 0.976 | none | 1 (wf10) | pass | pass |
| Gemini Pro 3.1 | Thinking | 32/41 = 0.780 | 3 (BoC, Nf01, Ax) | 1 (wf10) | pass (apple1) | pass |
| Opus 4.7 | Adaptive | 40/41 = 0.976 | none | pass (wf10) | **1 (apple1)** | pass |

**Three frontier models, three distinct failure surfaces.** No model achieves 41/41 on v0.1. The benchmark surfaces three architecturally distinct gravity failure modes (classical, pattern-consistency, structural-normalization). Cross-model replication of the wf10 PCG event on two Thinking-mode models is particularly noteworthy.

---

## Version history

| Version | Date | Changes |
|---------|------|---------|
| v0.1 | April 2026 | Initial public release. 40 images. Universal invariants. Filename-inferred URLs. |
| v0.1.1 | April 16, 2026 | 41 images (added clevland.png). All URLs transcribed from actual address bars. Six ⚠️ entries cross-corroborated. Per-image page_type, login, pwd. Pair-class distribution corrected. v0.2 rubric clarifications captured. Pattern-Consistency Gravity documented. |
| v0.1.2 | April 17, 2026 | Corrected `HarborFr8.png` ground truth to `harb0rfreight8.com/my-account/login` (compound attack). Harbor Freight pair relabeled to simple-vs-compound. |
| v0.1.3 | April 17, 2026 | Corrected `dell.png` ground truth to `de1l.com/di/idp/dwa/authorize` (full OAuth path under the v0.1 scoring rule). Structural Normalization Gravity documented following Opus 4.7 Bedrock run. Three-model result summary added. |

---

**Authored:** April 17, 2026
**Corpus:** `~/Desktop/TestPics/homoglyph/` — 41 images
