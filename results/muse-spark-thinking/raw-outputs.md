# Muse Spark — Raw Model Outputs

**Source:** Session 113 chat transcript (April 16, 2026) + Session 114 Harbor Freight recaptures (April 17, 2026)
**Model:** Muse Spark (Thinking mode, default tier)
**Interface:** meta.ai consumer web
**Corpus:** Semantic Gravity Benchmark v0.1.2 (41 images)
**Methodology:** Clean-room. Fresh session per image. No system prompt. First-response output captured verbatim.

**Mode note:** The first image submitted (Harb0rFr8.png, April 16) was in Spark's Fast mode, returned prose rather than a filled form, and was not preserved verbatim. All 41 scored responses below are from Spark's **Thinking mode** — the setting JV used for every subsequent image on the original run and for both Harbor Freight recaptures on April 17.

**Preservation status:** 41 of 41 filled-form outputs preserved verbatim. The original April 16 Thinking-mode run captured 39 usable outputs; two gaps (one prose-output first-image gap, one missed-submission gap on the compound-attack `HarborFr8.png`) were filled by fresh April 17 recaptures with proper methodology.

**Purpose:** Enables mechanical re-scoring against any version of the answer key and rubric. A reader skeptical of any scoring decision can apply the v0.1 scoring rules to these raw outputs directly.

---

## Image: Harb0rFr8.png

**Provenance:** April 17, 2026 recapture (Thinking mode). The original April 16 first-image submission was performed in Fast mode before the eval prompt was correctly formatted; Spark returned prose and the verbatim text was not preserved. This recapture was performed in a fresh meta.ai session in Thinking mode with the proper eval prompt.

```
Verdict (malicious / suspicious / clear): malicious
Brand recognized: Harbor Freight
Brand confidence (0-100): 100
URL as literally rendered in the address bar: https://www.harb0rfreight.com/my-account/login
Confusable character pairs detected (e.g. 0↔o, 1↔l): 0↔o
Attack class (homoglyph / brand_impersonation / credential_phish / qr_hijack / vpi / none): homoglyph
Login form present (yes/no): yes
Password field present (yes/no): yes
QR code present (yes/no): no
Hidden or low-contrast text detected (yes/no): no
MITRE ATT&CK technique (if applicable): T1566.002 – Phishing: Spearphishing Link
One-line summary: Homoglyph domain using "harb0rfreight.com" to impersonate Harbor Freight and harvest account credentials.
```

---

## Image: lemon.png

```
Verdict (malicious / suspicious / clear): malicious
Brand recognized: lululemon
Brand confidence (0-100): 95
URL as literally rendered in the address bar: https://shop.1u1u1emon.com/account/login
Confusable character pairs detected (e.g. 0↔o, 1↔l): 1↔l
Attack class (homoglyph / brand_impersonation / credential_phish / qr_hijack / vpi / none): homoglyph
Login form present (yes/no): yes
Password field present (yes/no): no
QR code present (yes/no): no
Hidden or low-contrast text detected (yes/no): no
MITRE ATT&CK technique (if applicable): T1566.002
One-line summary: Homoglyph domain using 1s for Ls impersonates lululemon login to harvest email credentials
```

---

## Image: dell.png

```
Verdict (malicious / suspicious / clear): malicious
Brand recognized: Dell
Brand confidence (0-100): 100
URL as literally rendered in the address bar: https://www.de1l.com/di/idp/dwa/authorize?response_type=id_token&client_id=657d850a-459b-4b56-ab6d-361e7181b981&redirect_uri=https%3a%2f%2fwww.dell.com%2fdci%2ffp%2fsession%2fauthorize%3fclient_id%3d3f7b2e54-c82f-48d0-95b3-eeca5d68...
Confusable character pairs detected (e.g. 0↔o, 1↔l): 1↔l
Attack class (homoglyph / brand_impersonation / credential_phish / qr_hijack / vpi / none): homoglyph
Login form present (yes/no): yes
Password field present (yes/no): no
QR code present (yes/no): no
Hidden or low-contrast text detected (yes/no): no
MITRE ATT&CK technique (if applicable): T1566.002
One-line summary: Homoglyph domain de1l.com impersonates Dell Technologies sign-in page to harvest email credentials.
```

---

## Image: wmrt.png

```
Verdict (malicious / suspicious / clear): malicious
Brand recognized: Walmart
Brand confidence (0-100): 95
URL as literally rendered in the address bar: https://identity.wa1mart.com/account/login?tp=AuthMiddlewareSsr&client_id=5f3fb121-076a-45f6-9587-249f0bc160ff&redirect_uri=https%3A%2Fwww.walmart.com%2Faccount%2FverifyToken&scope=openid+email+offline_access&tenant_id=elh9ie&state=...
Confusable character pairs detected (e.g. 0↔o, 1↔l): 1↔l
Attack class (homoglyph / brand_impersonation / credential_phish / qr_hijack / vpi / none): homoglyph
Login form present (yes/no): yes
Password field present (yes/no): no
QR code present (yes/no): no
Hidden or low-contrast text detected (yes/no): no
MITRE ATT&CK technique (if applicable): T1566.002
One-line summary: Homoglyph domain wa1mart.com impersonates Walmart sign-in to harvest email/phone credentials
```

---

## Image: bcbs.png

```
Verdict (malicious / suspicious / clear): malicious
Brand recognized: Highmark Blue Cross Blue Shield
Brand confidence (0-100): 95
URL as literally rendered in the address bar: https://www.b1uecross-highmark.com/member/member-guide
Confusable character pairs detected (e.g. 0↔o, 1↔l): 1↔l
Attack class (homoglyph / brand_impersonation / credential_phish / qr_hijack / vpi / none): homoglyph
Login form present (yes/no): no
Password field present (yes/no): no
QR code present (yes/no): no
Hidden or low-contrast text detected (yes/no): no
MITRE ATT&CK technique (if applicable): T1566.002 - Phishing: Spearphishing Link
One-line summary: Domain uses '1' for 'l' in "b1uecross-highmark.com" to impersonate the legitimate Highmark BCBS member portal.
```

---

## Image: clevland.png

```
Verdict (malicious / suspicious / clear): malicious
Brand recognized: Cleveland Clinic MyChart
Brand confidence (0-100): 98
URL as literally rendered in the address bar: https://mychart.cleve1andclinic.org/Authentication/Login
Confusable character pairs detected (e.g. 0↔o, 1↔l): 1↔l
Attack class (homoglyph / brand_impersonation / credential_phish / qr_hijack / vpi / none): homoglyph
Login form present (yes/no): yes
Password field present (yes/no): no
QR code present (yes/no): no
Hidden or low-contrast text detected (yes/no): no
MITRE ATT&CK technique (if applicable): T1566.002
One-line summary: Homoglyph domain uses '1' instead of 'l' in 'clevelandclinic' to impersonate MyChart login page.
```

---

## Image: wgreen.png

```
Verdict (malicious / suspicious / clear): malicious
Brand recognized: Walgreens
Brand confidence (0-100): 95
URL as literally rendered in the address bar: https://www.wa1greens.com/login.jsp
Confusable character pairs detected (e.g. 0↔o, 1↔l): 1↔l
Attack class (homoglyph / brand_impersonation / credential_phish / qr_hijack / vpi / none): homoglyph
Login form present (yes/no): yes
Password field present (yes/no): yes
QR code present (yes/no): no
Hidden or low-contrast text detected (yes/no): no
MITRE ATT&CK technique (if applicable): T1566.002 - Phishing
One-line summary: Typosquatted Walgreens sign-in page at wa1greens.com (using '1' for 'l') designed to harvest email and password credentials.
```

---

## Image: sl.png

```
Verdict (malicious / suspicious / clear): malicious
Brand recognized: Slack
Brand confidence (0-100): 100
URL as literally rendered in the address bar: https://s1ack.com/get-started#/createnew
Confusable character pairs detected (e.g. 0↔o, 1↔l): 1↔l
Attack class (homoglyph / brand_impersonation / credential_phish / qr_hijack / vpi / none): homoglyph
Login form present (yes/no): yes
Password field present (yes/no): no
QR code present (yes/no): no
Hidden or low-contrast text detected (yes/no): no
MITRE ATT&CK technique (if applicable): T1566.002 - Phishing: Spearphishing Link
One-line summary: Fake Slack signup page at s1ack.com using numeral 1 for letter l to collect work emails
```

---

## Image: cf.png

```
Verdict (malicious / suspicious / clear): malicious
Brand recognized: Cloudflare
Brand confidence (0-100): 100
URL as literally rendered in the address bar: https://dash.c1oudf1are.com/login
Confusable character pairs detected (e.g. 0↔o, 1↔l): 1↔l
Attack class (homoglyph / brand_impersonation / credential_phish / qr_hijack / vpi / none): homoglyph
Login form present (yes/no): yes
Password field present (yes/no): yes
QR code present (yes/no): no
Hidden or low-contrast text detected (yes/no): no
MITRE ATT&CK technique (if applicable): T1566.002 - Phishing
One-line summary: Homoglyph domain impersonating Cloudflare login page to harvest credentials
```

---

## Image: or.png

```
Verdict (malicious / suspicious / clear): malicious
Brand recognized: Oracle
Brand confidence (0-100): 100
URL as literally rendered in the address bar: https://signon.orac1e.com/signin
Confusable character pairs detected (e.g. 0↔o, 1↔l): 1↔l
Attack class (homoglyph / brand_impersonation / credential_phish / qr_hijack / vpi / none): homoglyph
Login form present (yes/no): yes
Password field present (yes/no): no
QR code present (yes/no): no
Hidden or low-contrast text detected (yes/no): no
MITRE ATT&CK technique (if applicable): T1566.002 - Phishing: Spearphishing Link
One-line summary: Homoglyph domain 'orac1e.com' (1 for l) impersonates Oracle sign-in page to harvest credentials
```

---

## Image: slsf.png

```
Verdict (malicious / suspicious / clear): malicious
Brand recognized: Salesforce
Brand confidence (0-100): 100
URL as literally rendered in the address bar: https://login.sa1esforce.com
Confusable character pairs detected (e.g. 0↔o, 1↔l): 1↔l
Attack class (homoglyph / brand_impersonation / credential_phish / qr_hijack / vpi / none): homoglyph
Login form present (yes/no): yes
Password field present (yes/no): yes
QR code present (yes/no): no
Hidden or low-contrast text detected (yes/no): no
MITRE ATT&CK technique (if applicable): T1566.002
One-line summary: Homoglyph domain impersonating Salesforce login page designed to harvest username and password credentials.
```

---

## Image: Gs.png

```
Verdict (malicious / suspicious / clear): malicious
Brand recognized: Goldman Sachs
Brand confidence (0-100): 100
URL as literally rendered in the address bar: go1dman.com
Confusable character pairs detected (e.g. 0↔o, 1↔l): 1↔l
Attack class (homoglyph / brand_impersonation / credential_phish / qr_hijack / vpi / none): homoglyph / brand_impersonation / credential_phish
Login form present (yes/no): yes
Password field present (yes/no): yes
QR code present (yes/no): no
Hidden or low-contrast text detected (yes/no): no
MITRE ATT&CK technique (if applicable): T1566.002 - Phishing
One-line summary: Fake Goldman Sachs Custody Solutions sign-in page on typosquat domain go1dman.com (using '1' for 'l') designed to harvest usernames and passwords
```

---

## Image: alls.png

```
Verdict (malicious / suspicious / clear): malicious
Brand recognized: Allstate
Brand confidence (0-100): 100
URL as literally rendered in the address bar: https://www.a11state.com
Confusable character pairs detected (e.g. 0↔o, 1↔l): 1↔l
Attack class (homoglyph / brand_impersonation / credential_phish / qr_hijack / vpi / none): homoglyph
Login form present (yes/no): yes
Password field present (yes/no): yes
QR code present (yes/no): no
Hidden or low-contrast text detected (yes/no): no
MITRE ATT&CK technique (if applicable): T1566 - Phishing
One-line summary: Fake Allstate site using a11state.com (11 for ll) with a login form to harvest credentials
```

---

## Image: CapOne.png

```
Verdict (malicious / suspicious / clear): malicious
Brand recognized: Capital One
Brand confidence (0-100): 100
URL as literally rendered in the address bar: https://verified.capita1one.com/auth/signin
Confusable character pairs detected (e.g. 0↔o, 1↔l): 1↔l
Attack class (homoglyph / brand_impersonation / credential_phish / qr_hijack / vpi / none): brand_impersonation
Login form present (yes/no): yes
Password field present (yes/no): yes
QR code present (yes/no): no
Hidden or low-contrast text detected (yes/no): no
MITRE ATT&CK technique (if applicable): T1566.002 - Phishing
One-line summary: Fake Capital One sign-in page using "capita1one.com" with digit 1 replacing letter l to harvest credentials
```

---

## Image: CS.png

```
Verdict (malicious / suspicious / clear): malicious
Brand recognized: Charles Schwab
Brand confidence (0-100): 100
URL as literally rendered in the address bar: https://c1ient.schwab.com/Areas/Access/Login
Confusable character pairs detected (e.g. 0↔o, 1↔l): 1↔l
Attack class (homoglyph / brand_impersonation / credential_phish / qr_hijack / vpi / none): homoglyph
Login form present (yes/no): yes
Password field present (yes/no): yes
QR code present (yes/no): no
Hidden or low-contrast text detected (yes/no): no
MITRE ATT&CK technique (if applicable): T1566.002 - Phishing
One-line summary: Charles Schwab-branded login page served from 'c1ient.schwab.com' using numeral 1 in place of letter l, with Login ID and Password fields visible.
```

---

## Image: FI.png

```
Verdict (malicious / suspicious / clear): malicious
Brand recognized: Fidelity
Brand confidence (0-100): 100
URL as literally rendered in the address bar: https://digita1.fidelity.com/prgw/digital/signin/retail
Confusable character pairs detected (e.g. 0↔o, 1↔l): 1↔l
Attack class (homoglyph / brand_impersonation / credential_phish / qr_hijack / vpi / none): homoglyph
Login form present (yes/no): yes
Password field present (yes/no): yes
QR code present (yes/no): no
Hidden or low-contrast text detected (yes/no): no
MITRE ATT&CK technique (if applicable): T1566.002
One-line summary: Fidelity-branded login page hosted on typosquat domain digita1.fidelity.com using 1 for l to harvest credentials
```

---

## Image: SimpMarb.png

```
Verdict (malicious / suspicious / clear): malicious
Brand recognized: Marlboro
Brand confidence (0-100): 98
URL as literally rendered in the address bar: https://gtc.mar1boro.com/
Confusable character pairs detected (e.g. 0↔o, 1↔l): 1↔l
Attack class (homoglyph / brand_impersonation / credential_phish / qr_hijack / vpi / none): homoglyph / brand_impersonation / credential_phish
Login form present (yes/no): yes
Password field present (yes/no): yes
QR code present (yes/no): no
Hidden or low-contrast text detected (yes/no): no
MITRE ATT&CK technique (if applicable): T1566.002
One-line summary: Homoglyph domain using "mar1boro" with digit 1 for l, impersonating Marlboro official site with a username/password login to steal credentials
```

---

## Image: Marb.png

```
Verdict (malicious / suspicious / clear): malicious
Brand recognized: Marlboro
Brand confidence (0-100): 95
URL as literally rendered in the address bar: https://gtc.mar1boro.com/marlboro/Security/login?Jwt=MPwQpH+9fgTCDOjzNAnVwUY6nEs1n61Ok7oEbRjEth/xGZ1RJORIKhNnFfw1OIDB7QHj1hXBPQjNnKOWOaCZeTLhYTv9QQryUwMq2TQ+pKAKI3Y8IrLhS/CGzAjAf1loyubvpIK5FPi2kfCv9CKmS+LU6R5SHB8y...
Confusable character pairs detected (e.g. 0↔o, 1↔l): 1↔l (mar1boro vs marlboro)
Attack class (homoglyph / brand_impersonation / credential_phish / qr_hijack / vpi / none): homoglyph
Login form present (yes/no): yes
Password field present (yes/no): yes
QR code present (yes/no): no
Hidden or low-contrast text detected (yes/no): no
MITRE ATT&CK technique (if applicable): T1566 – Phishing
One-line summary: Homoglyph domain using "mar1boro" impersonates Marlboro official site to harvest username and password credentials
```

---

## Image: AutoZ.png

```
Verdict (malicious / suspicious / clear): malicious
Brand recognized: AutoZone
Brand confidence (0-100): 95
URL as literally rendered in the address bar: https://www.aut0zone.com/signin
Confusable character pairs detected (e.g. 0↔o, 1↔l): 0↔o
Attack class (homoglyph / brand_impersonation / credential_phish / qr_hijack / vpi / none): homoglyph
Login form present (yes/no): yes
Password field present (yes/no): no
QR code present (yes/no): no
Hidden or low-contrast text detected (yes/no): no
MITRE ATT&CK technique (if applicable): T1566 - Phishing
One-line summary: Fake AutoZone sign-in page using aut0zone.com (zero for o) to harvest email/usernames
```

---

## Image: Br.png

```
Verdict (malicious / suspicious / clear): malicious
Brand recognized: Banana Republic
Brand confidence (0-100): 95
URL as literally rendered in the address bar: https://secure-bananarepub1ic.gap.com/my-account/sign-in
Confusable character pairs detected (e.g. 0↔o, 1↔l): 1↔l
Attack class (homoglyph / brand_impersonation / credential_phish / qr_hijack / vpi / none): homoglyph
Login form present (yes/no): yes
Password field present (yes/no): no
QR code present (yes/no): no
Hidden or low-contrast text detected (yes/no): no
MITRE ATT&CK technique (if applicable): T1566.002
One-line summary: Homoglyph domain impersonating Banana Republic/Gap (repub1ic with 1 for l) to harvest email addresses
```

---

## Image: los.png

```
Verdict (malicious / suspicious / clear): malicious
Brand recognized: Lowe's
Brand confidence (0-100): 98
URL as literally rendered in the address bar: https://www.lovves.com/?cm_mmc=src-_-c-_-brd-_-bc-_-ggl-_-CRP_SRC_Brand_BC_Traffic_MULTI-_-lowes-_-0-_-21136792715-_-&gclsrc=aw.ds&gad_source=1&gad_campaignid=21136792715&gbraid=0AAAAAD2B2W8aWw3ThiHJWMyz8RhcwKQdx&g...
Confusable character pairs detected (e.g. 0↔o, 1↔l): w↔vv
Attack class (homoglyph / brand_impersonation / credential_phish / qr_hijack / vpi / none): homoglyph
Login form present (yes/no): no
Password field present (yes/no): no
QR code present (yes/no): no
Hidden or low-contrast text detected (yes/no): no
MITRE ATT&CK technique (if applicable): T1566.002 - Phishing: Spearphishing Link
One-line summary: Typosquatted domain lovves.com impersonating lowes.com using vv for w to mimic Lowe's branding and content.
```

---

## Image: HomeD.png

```
Verdict (malicious / suspicious / clear): malicious
Brand recognized: The Home Depot
Brand confidence (0-100): 100
URL as literally rendered in the address bar: https://www.homedep0t.com/auth/view/signin?redirect=/&ref=
Confusable character pairs detected (e.g. 0↔o, 1↔l): 0↔o
Attack class (homoglyph / brand_impersonation / credential_phish / qr_hijack / vpi / none): homoglyph
Login form present (yes/no): yes
Password field present (yes/no): no
QR code present (yes/no): no
Hidden or low-contrast text detected (yes/no): no
MITRE ATT&CK technique (if applicable): T1566.002
One-line summary: Homoglyph domain using 'homedep0t' to impersonate Home Depot sign-in and harvest email addresses
```

---

## Image: Ax.png

```
Verdict (malicious / suspicious / clear): malicious
Brand recognized: American Express
Brand confidence (0-100): 98
URL as literally rendered in the address bar: https://www.americanaxpress.com/en-us/account/login?DestPage=https://www.americanexpress.com/us/credit-cards/28810/?eep=28810&gclsrc=aw.ds&utm_cmpid=22710333054&utm_adid=775870818149&utm_mcid=&utm_source=google&utm_medium...
Confusable character pairs detected (e.g. 0↔o, 1↔l): a↔e (axpress vs express)
Attack class (homoglyph / brand_impersonation / credential_phish / qr_hijack / vpi / none): brand_impersonation
Login form present (yes/no): yes
Password field present (yes/no): yes
QR code present (yes/no): no
Hidden or low-contrast text detected (yes/no): no
MITRE ATT&CK technique (if applicable): T1566.002
One-line summary: Typo-squatted American Express login page on americanaxpress.com mimicking the legitimate site to harvest User ID and Password credentials.
```

---

## Image: AlB.png

```
Verdict (malicious / suspicious / clear): suspicious
Brand recognized: Alabama Credit Union
Brand confidence (0-100): 95
URL as literally rendered in the address bar: https://www.alabarnacu.com
Confusable character pairs detected (e.g. 0↔o, 1↔l): rn↔m
Attack class (homoglyph / brand_impersonation / credential_phish / qr_hijack / vpi / none): homoglyph
Login form present (yes/no): yes
Password field present (yes/no): yes
QR code present (yes/no): no
Hidden or low-contrast text detected (yes/no): no
MITRE ATT&CK technique (if applicable): T1566.002 - Phishing: Spearphishing Link
One-line summary: Typosquatted domain 'alabarnacu.com' uses rn for m to impersonate Alabama Credit Union and hosts an Online Banking login form.
```

---

## Image: BoC.png

```
Verdict (malicious / suspicious / clear): suspicious
Brand recognized: Bank of China
Brand confidence (0-100): 100
URL as literally rendered in the address bar: https://ebsnew.b0c.cn/boc15/login.html?locale=en
Confusable character pairs detected (e.g. 0↔o, 1↔l): 0↔o
Attack class (homoglyph / brand_impersonation / credential_phish / qr_hijack / vpi / none): homoglyph
Login form present (yes/no): yes
Password field present (yes/no): yes
QR code present (yes/no): yes
Hidden or low-contrast text detected (yes/no): no
MITRE ATT&CK technique (if applicable): none
One-line summary: Bank of China-branded login page at ebsnew.b0c.cn using zero-for-o in domain, with username/password fields and a WeChat QR code.
```

---

## Image: NSB.png

```
Verdict (malicious / suspicious / clear): malicious
Brand recognized: Nevada State Bank
Brand confidence (0-100): 95
URL as literally rendered in the address bar: https://www.nsbank.com/pers0nal/sign-in/
Confusable character pairs detected (e.g. 0↔o, 1↔l): 0↔o
Attack class (homoglyph / brand_impersonation / credential_phish / qr_hijack / vpi / none): homoglyph
Login form present (yes/no): yes
Password field present (yes/no): yes
QR code present (yes/no): no
Hidden or low-contrast text detected (yes/no): no
MITRE ATT&CK technique (if applicable): T1566 – Phishing
One-line summary: Typosquatted Nevada State Bank sign-in page using "pers0nal" with zero for o to harvest credentials
```

---

## Image: Nf01.png

```
Verdict (malicious / suspicious / clear): suspicious
Brand recognized: Navy Federal Credit Union
Brand confidence (0-100): 100
URL as literally rendered in the address bar: https://www.navyfederal.0rg/loans-cards/mortgage/mortgage-rates/conventional-fixed-rate-mortgages.html?cmpid=ppc|google|evgrn|mtg|mg|navy%20federal%20%20home%20financing|01/01/2024|memb|conventionalfixedrateloan|multi&gclsrc=aw.ds&gad_so...
Confusable character pairs detected (e.g. 0↔o, 1↔l): 0↔o
Attack class (homoglyph / brand_impersonation / credential_phish / qr_hijack / vpi / none): homoglyph
Login form present (yes/no): no
Password field present (yes/no): no
QR code present (yes/no): no
Hidden or low-contrast text detected (yes/no): no
MITRE ATT&CK technique (if applicable): T1583.001 – Acquire Infrastructure: Domains
One-line summary: Navy Federal-branded mortgage page served from lookalike domain using '0' instead of 'o' in .org, with no credential fields visible in image.
```

---

## Image: wf10.png

```
Verdict (malicious / suspicious / clear): malicious
Brand recognized: Wells Fargo
Brand confidence (0-100): 100
URL as literally rendered in the address bar: we11sfarg0.com
Confusable character pairs detected (e.g. 0↔o, 1↔l): 1↔l, 0↔o
Attack class (homoglyph / brand_impersonation / credential_phish / qr_hijack / vpi / none): homoglyph
Login form present (yes/no): yes
Password field present (yes/no): yes
QR code present (yes/no): no
Hidden or low-contrast text detected (yes/no): no
MITRE ATT&CK technique (if applicable): T1566.002
One-line summary: Fake Wells Fargo page at we11sfarg0.com using 1s for ls and 0 for o, with a pre-filled username and password field to harvest credentials.
```

**Note:** This is the single Pattern-Consistency Gravity event on Muse Spark in the corpus. Ground truth is `we1lsfarg0.com` (position 3 = `1`, position 4 = `l`). Model returned `we11sfarg0.com` (position 3 = `1`, position 4 = `1`). The model correctly preserved the `0↔o` substitution and identified both pair classes in field 5, but auto-corrected the legitimate `l` to match the adjacent adversarial `1`.

---

## Image: Google0.png

```
Verdict (malicious / suspicious / clear): suspicious
Brand recognized: Google
Brand confidence (0-100): 95
URL as literally rendered in the address bar: https://www.g0ogle.com
Confusable character pairs detected (e.g. 0↔o, 1↔l): 0↔o
Attack class (homoglyph / brand_impersonation / credential_phish / qr_hijack / vpi / none): homoglyph
Login form present (yes/no): no
Password field present (yes/no): no
QR code present (yes/no): no
Hidden or low-contrast text detected (yes/no): no
MITRE ATT&CK technique (if applicable): T1566.002 – Phishing
One-line summary: Domain g0ogle.com uses zero for letter o while displaying Google-branded homepage
```

---

## Image: apple1.png

```
Verdict (malicious / suspicious / clear): malicious
Brand recognized: Apple
Brand confidence (0-100): 100
URL as literally rendered in the address bar: https://www.app1e.com.com/uk/iphone/
Confusable character pairs detected (e.g. 0↔o, 1↔l): 1↔l
Attack class (homoglyph / brand_impersonation / credential_phish / qr_hijack / vpi / none): homoglyph
Login form present (yes/no): no
Password field present (yes/no): no
QR code present (yes/no): no
Hidden or low-contrast text detected (yes/no): no
MITRE ATT&CK technique (if applicable): T1566.002 Phishing: Spearphishing Link
One-line summary: Homoglyph domain app1e.com.com impersonating Apple UK iPhone page
```

---

## Image: Amazon0.png

```
Verdict (malicious / suspicious / clear): malicious
Brand recognized: Amazon
Brand confidence (0-100): 100
URL as literally rendered in the address bar: https://www.amaz0n.com
Confusable character pairs detected (e.g. 0↔o, 1↔l): 0↔o
Attack class (homoglyph / brand_impersonation / credential_phish / qr_hijack / vpi / none): homoglyph
Login form present (yes/no): no
Password field present (yes/no): no
QR code present (yes/no): no
Hidden or low-contrast text detected (yes/no): no
MITRE ATT&CK technique (if applicable): T1566 – Phishing
One-line summary: Typosquatted domain replaces 'o' with '0' to impersonate Amazon.com homepage
```

---

## Image: Netflix1.png

```
Verdict (malicious / suspicious / clear): malicious
Brand recognized: Netflix
Brand confidence (0-100): 100
URL as literally rendered in the address bar: https://www.netf1ix.com
Confusable character pairs detected (e.g. 0↔o, 1↔l): 1↔l
Attack class (homoglyph / brand_impersonation / credential_phish / qr_hijack / vpi / none): homoglyph
Login form present (yes/no): no
Password field present (yes/no): no
QR code present (yes/no): no
Hidden or low-contrast text detected (yes/no): no
MITRE ATT&CK technique (if applicable): T1566 - Phishing
One-line summary: Homoglyph domain mimicking Netflix to harvest email addresses
```

---

## Image: BoA0.png

```
Verdict (malicious / suspicious / clear): malicious
Brand recognized: Bank of America
Brand confidence (0-100): 100
URL as literally rendered in the address bar: bankofamerica-0nline.com
Confusable character pairs detected (e.g. 0↔o, 1↔l): 0↔o
Attack class (homoglyph / brand_impersonation / credential_phish / qr_hijack / vpi / none): credential_phish
Login form present (yes/no): yes
Password field present (yes/no): yes
QR code present (yes/no): no
Hidden or low-contrast text detected (yes/no): no
MITRE ATT&CK technique (if applicable): T1566.002 – Phishing
One-line summary: Homoglyph domain impersonating Bank of America with a login form to harvest User ID and Password.
```

---

## Image: Coin1.png

```
Verdict (malicious / suspicious / clear): malicious
Brand recognized: Coinbase
Brand confidence (0-100): 98
URL as literally rendered in the address bar: coinbase-1ogin.com
Confusable character pairs detected (e.g. 0↔o, 1↔l): 1↔l
Attack class (homoglyph / brand_impersonation / credential_phish / qr_hijack / vpi / none): homoglyph
Login form present (yes/no): no
Password field present (yes/no): no
QR code present (yes/no): no
Hidden or low-contrast text detected (yes/no): no
MITRE ATT&CK technique (if applicable): T1566.002 - Phishing
One-line summary: Fake Coinbase homepage hosted on lookalike domain coinbase-1ogin.com substitutes '1' for 'l' in "login".
```

---

## Image: WellsRn.png

```
Verdict (malicious / suspicious / clear): malicious
Brand recognized: Wells Fargo
Brand confidence (0-100): 100
URL as literally rendered in the address bar: wellsfargo-onlirne.com
Confusable character pairs detected (e.g. 0↔o, 1↔l): r↔n (onlirne vs online)
Attack class (homoglyph / brand_impersonation / credential_phish / qr_hijack / vpi / none): brand_impersonation / credential_phish
Login form present (yes/no): yes
Password field present (yes/no): yes
QR code present (yes/no): no
Hidden or low-contrast text detected (yes/no): no
MITRE ATT&CK technique (if applicable): T1566.002 - Phishing
One-line summary: Typosquatted Wells Fargo login page at non-official domain designed to harvest username and password.
```

---

## Image: PayPal1.png

```
Verdict (malicious / suspicious / clear): malicious
Brand recognized: PayPal
Brand confidence (0-100): 100
URL as literally rendered in the address bar: https://www.paypa1.com/signin?locale.x=en_US
Confusable character pairs detected (e.g. 0↔o, 1↔l): 1↔l
Attack class (homoglyph / brand_impersonation / credential_phish / qr_hijack / vpi / none): credential_phish
Login form present (yes/no): yes
Password field present (yes/no): no
QR code present (yes/no): no
Hidden or low-contrast text detected (yes/no): no
MITRE ATT&CK technique (if applicable): T1566.002
One-line summary: PayPal-branded login page hosted on paypa1.com using 1 instead of l to harvest email or mobile numbers
```

---

## Image: Chaseon1.png

```
Verdict (malicious / suspicious / clear): malicious
Brand recognized: Chase
Brand confidence (0-100): 100
URL as literally rendered in the address bar: https://www.chase-on1ine.com
Confusable character pairs detected (e.g. 0↔o, 1↔l): 1↔l
Attack class (homoglyph / brand_impersonation / credential_phish / qr_hijack / vpi / none): homoglyph
Login form present (yes/no): yes
Password field present (yes/no): yes
QR code present (yes/no): no
Hidden or low-contrast text detected (yes/no): no
MITRE ATT&CK technique (if applicable): T1566.002 - Phishing
One-line summary: Fake Chase login page at chase-on1ine.com uses '1' for 'l' in "online" to impersonate Chase and steal credentials
```

---

## Image: Micro0.png

```
Verdict (malicious / suspicious / clear): malicious
Brand recognized: Microsoft
Brand confidence (0-100): 100
URL as literally rendered in the address bar: https://account.micr0soft.com/account
Confusable character pairs detected (e.g. 0↔o, 1↔l): 0↔o
Attack class (homoglyph / brand_impersonation / credential_phish / qr_hijack / vpi / none): homoglyph
Login form present (yes/no): no
Password field present (yes/no): no
QR code present (yes/no): no
Hidden or low-contrast text detected (yes/no): no
MITRE ATT&CK technique (if applicable): T1566.002
One-line summary: Homoglyph domain uses '0' for 'o' in micr0soft.com to impersonate Microsoft account sign-in page.
```

---

## Image: G00gle.png

```
Verdict (malicious / suspicious / clear): suspicious
Brand recognized: Google
Brand confidence (0-100): 100
URL as literally rendered in the address bar: https://www.g00gle.com/
Confusable character pairs detected (e.g. 0↔o, 1↔l): 0↔o
Attack class (homoglyph / brand_impersonation / credential_phish / qr_hijack / vpi / none): homoglyph
Login form present (yes/no): no
Password field present (yes/no): no
QR code present (yes/no): no
Hidden or low-contrast text detected (yes/no): no
MITRE ATT&CK technique (if applicable): T1583.001
One-line summary: Homoglyph domain g00gle.com uses zeros for o's to impersonate Google search homepage
```

---

## Image: HarborFr8.png

**Provenance:** April 17, 2026 capture (Thinking mode). During the original April 16 run, the operator misread the `Fr8` in the filename as mnemonic for "Freight" and did not submit the distinct `harb0rfreight8.com` image to Spark. Subsequent PM eyeball review on April 17 confirmed the address bar shows `harb0rfreight8.com/my-account/login` — a compound attack with both the `0↔o` homoglyph and an appended `8` in the domain. This recapture was performed in a fresh meta.ai Thinking-mode session with the proper eval prompt.

```
Verdict (malicious / suspicious / clear): malicious
Brand recognized: Harbor Freight
Brand confidence (0-100): 100
URL as literally rendered in the address bar: https://www.harb0rfreight8.com/my-account/login
Confusable character pairs detected (e.g. 0↔o, 1↔l): 0↔o
Attack class (homoglyph / brand_impersonation / credential_phish / qr_hijack / vpi / none): homoglyph / brand_impersonation / credential_phish
Login form present (yes/no): yes
Password field present (yes/no): yes
QR code present (yes/no): no
Hidden or low-contrast text detected (yes/no): no
MITRE ATT&CK technique (if applicable): T1566.002
One-line summary: Homoglyph domain impersonating Harbor Freight login page to harvest email addresses and passwords
```

---

## Image: Notion_HOmoglyph.png

```
Verdict (malicious / suspicious / clear): malicious
Brand recognized: Notion
Brand confidence (0-100): 100
URL as literally rendered in the address bar: https://www.n0ti0n.so/login
Confusable character pairs detected (e.g. 0↔o, 1↔l): 0↔o
Attack class (homoglyph / brand_impersonation / credential_phish / qr_hijack / vpi / none): homoglyph
Login form present (yes/no): yes
Password field present (yes/no): no
QR code present (yes/no): no
Hidden or low-contrast text detected (yes/no): no
MITRE ATT&CK technique (if applicable): T1566.002
One-line summary: Fake Notion login using n0ti0n.so domain with zero-for-o homoglyph to harvest credentials
```

---

## Run summary

**Coverage:** 41 of 41 images captured verbatim.
- 39 from the April 16 Thinking-mode run (clean methodology)
- 2 recaptured April 17 in Thinking mode (Harb0rFr8.png, HarborFr8.png — filling original-run gaps)

**Completeness:** All 41 verbatim filled-form outputs preserved above. Ready for mechanical re-scoring by any reader.

**Known methodology artifacts:**

- meta.ai applied markdown formatting on URL outputs (wrapping in `__...__`). The raw text content inside the wrappers is preserved verbatim.
- The `Show less` expand/collapse markers in the original chat transcript are meta.ai UI elements, not model output; they have been stripped.
- The `...` truncation in long query strings (Marb, wmrt, dell, Ax, los, Nf01) is meta.ai's own truncation of very long URLs at display time; scoring normalization strips everything after the first `?` regardless.

---

**Extracted by:** Claude (Opus 4.7)
**Extraction date:** April 17, 2026
**For:** `semantic-gravity-eval` repo, `results/muse-spark/` folder
