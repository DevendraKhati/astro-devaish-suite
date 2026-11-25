---
name: astro-devaish-suite
description: Combined Master Vedic Jyotish (Parashari, Jaimini, KP, Ashtakavarga & Ganita Skandha) + Authentic Indian Vedic Anka-Jyotish (Numerology, Katapayadi & Svara Shastra) skill with Astro DevAish branding. Integrates D1-D60 Shodashavarga, Sripati Bhava Chalit, Shadbala, Ishta/Kashta Phala, Avasthas, strict Parashari Mangal Dosha, 337 SAV/BAV, Century-Free Vedic Surya Grid (3-1-9/6-7-5/2-8-4), 37 Vedic Yogas, 81 Driver-Conductor combinations, 45-Year Vedic Dasha, First vs Full Name 10-52 Chaldean compounds, Graha-Anka Natal Chart Cross-Verification, and Unified Dasha + Transit + Personal Year Timing. Generates Astro DevAish Hindi (Devanagari) PDF reports in 8-Page (Default), 12-Page (Extended), and Full (16-20 Pages Master) modes.
---

# Astro DevAish Master Suite (`astro-devaish-suite`) — Unified Classical Vedic Jyotish + Vedic Anka-Jyotish

This master skill integrates **`vedic-jyotish`** (Parashari, Jaimini, KP, Ashtakavarga, Shadbala, Avasthas, D1–D60 & Ganita Astronomy) and **`vedic-numerology`** (All 12 Vedic Anka-Jyotish Pillars: Century-Free Vedic Surya Grid `3-1-9 / 6-7-5 / 2-8-4`, 37 Vedic Yogas, 81 Driver–Conductor Matrix & Bridge Number, 45-Year Vedic Dasha + Weekday-Linked Varshaphal, First vs Full Name 10–52 Chaldean Compounds, Katapayadi & Svara Shastra, and Lo Shu Over-Repetition Diagnostics) into a single, cross-verified synthesis engine.

---

## 1. `Astro DevAish` Brand & Output Standard

Unless the user explicitly requests a different format or language:
1. **Brand Identity:** Always brand reports as **`Astro DevAish`** and embed the circular logo (`/home/antigravity/channels4_profile.jpg`) as a base64 data URI in the header banner and page footers (fall back cleanly to a styled SVG emblem if the image file is absent).
2. **Default Language:** **Hindi (देवनागरी — Simple, clear, traditional & practical Hindi)** by default. Switch to **Hinglish** or **English** only when explicitly requested by the user.
3. **Default Length & 3 Report Modes:**
   - **8-Page A4 Portrait PDF Report (`पृष्ठ X / 8`)** — Standard Default when page count is not specified.
   - **12-Page A4 Portrait PDF Report (`पृष्ठ X / 12`)** — Extended Deep-Dive Mode.
   - **Full Report (`16–20 Pages` Master Edition — `पृष्ठ X / N`)** — Complete Shastric + Anka-Jyotish Master Edition.
4. **Mandatory Devanagari Font Embedding:** Always embed `/home/antigravity/.local/share/fonts/NotoSansDevanagari_0.woff2` as a base64 `@font-face` data URI inside the HTML before compiling via headless Chrome (`google-chrome --headless --disable-gpu --no-sandbox --no-pdf-header-footer --print-to-pdf=...`) so Hindi text never renders as tofu boxes (`[][]`). Visually verify rendered pages with `pdftoppm -png -r 150` + `view_file`.
5. **No Marketing or Meta Labels:** Keep predictions direct, honest, and scripturally accurate, but **NEVER** print meta-labels like `(बिना शुगरकोटिंग)` or `(No-Sugarcoating)` anywhere in the title, header, footer, or body.

---

## 2. Unified Computation Pipeline (`astro-devaish` / `vedic-jyotish` + `vedic-numerology` — Accessible from Any Directory)

All commands are installed globally on `PATH` (`astro-devaish`, `vedic-jyotish`, `vedic-numerology`, `jyotish`, `numerology`) and bundled in `/home/antigravity/.gemini/skills/astro-devaish-suite/scripts/`. You can run the unified pipeline from **any working directory**:

```bash
# Option A: Single Unified Master Command from ANY directory (automatically computes Chart + True Local Sunrise + Dasha + Transits + All 12 Vedic Numerology Pillars + Graha-Anka Chart Cross-Verification)
astro-devaish \
  --name "Chandan Singh Bisht" \
  --dob 1995-08-26 \
  --tob 22:35 \
  --lat 29.2183 \
  --lon 79.5130 \
  --place "Haldwani" \
  --gender male > master.json

# Option B: Step-by-Step Global CLI Commands
vedic-jyotish chart --name "Chandan Singh Bisht" --dob 1995-08-26 --tob 22:35 --lat 29.2183 --lon 79.5130 > chart.json
vedic-jyotish dasha --dob 1995-08-26 --tob 22:35 --lat 29.2183 --lon 79.5130 --at 2026-11-25 > dasha.json
vedic-jyotish transit --dob 1995-08-26 --tob 22:35 --lat 29.2183 --lon 79.5130 --from 2026-01-01 --years 4 > transit.json
vedic-numerology --name "Chandan Singh Bisht" --dob 1995-08-26 --tob 22:35 --sunrise 05:56 --gender male --chart-json chart.json > numerology.json
```

---

## 3. Master Synthesis Rules (Where Jyotish & Anka-Jyotish Meet)

### A. Graha-Anka Birth Chart Cross-Verification (`graha_anka_chart_synergy`)
Never interpret a Mulank or Bhagyank number in isolation when a birth chart is available:
- **Mulank (Driver) & Bhagyank (Conductor) Rulers Verified in D1/D9/SAV:**
  - Look up `graha_anka_chart_synergy.mulank_chart_synergy` and `bhagyank_chart_synergy`.
  - Check the ruling planet's **D1 House, Sign, Dignity (Exalted/Own/Vargottama/Debilitated), D9 Navamsa Dignity, Shadbala Ratio, and House SAV Bindus**.
  - *Example:* A native with **Mulank 8 (Saturn)** whose natal Saturn is **Own-Sign & Vargottama in the 11th House (Aquarius)** with high Shadbala experiences Saturn's institutional endurance, technical depth, and long-term gains ($11\text{th}$ house) at a much higher octave than someone whose Saturn is debilitated in the 1st/8th/12th house. Conversely, if **Bhagyank 4 (Rahu)** sits in the **7th House (Libra)**, the post-Age-35 Bhagyank phase strongly activates partnerships, public/client interactions, and unconventional career expansion, while requiring strict written clarity in agreements.

### B. Unified 3-Layer Timing Convergence
Cross-verify every major life prediction (Marriage, Career Leap, Financial/Property Milestone, Caution Window) across three independent clocks:
1. **Parashari Dasha Clock:** Active **Vimshottari Mahadasha $\rightarrow$ Antardasha $\rightarrow$ Pratyantardasha** (cross-checked with **36-Year Yogini Dasha**).
2. **Gochara (Transit) Clock:** **Double Transit of Jupiter + Saturn** over the relevant house/lord, **Sade Sati / Kantaka Dhaiya ($4\text{th}$) / Ashtama Shani ($8\text{th}$ from Moon)** modulated by **Moorthi Nirnaya** (*Swarna, Rajata, Tamra, Loha*) and **BAV/SAV Bindus**.
3. **Vedic Anka-Jyotish Clock:** Active **45-Year Vedic Mahadasha & Antardasha** + **Weekday-Linked Vedic Annual Dasha (*Varsha Dasha*)** + **Personal Year & Personal Months**.
- When all 3 clocks activate the same planetary ruler or house theme simultaneously, flag it as a **High-Convergence Milestone Window (त्रि-स्तरीय काल-संगम)**.

### C. Strict Classical Guardrails (Zero Contradictions)
1. **Sunrise Vedic Vara & Sunrise Mulank (*Surya Siddhanta*):** Both engines use true local sunrise (`panchanga.local_sunrise`). Pre-sunrise births (`00:00` to `sunrise`) are flagged consistently across Panchanga Vara and Sunrise Savana Mulank.
2. **Strict Parashari Mangal Dosha:**
   - **7th House (*Saptama*) & 8th House (*Ashtama*) Lagna Mars:** Always `present: True` (Severe Lagna Manglik). Benefic aspect or dignity mitigates harshness (`mitigations`) but never turns the verdict into "Non-Manglik".
   - **Moon-Chart-Only Mars (when Lagna Mars is NOT in $\{1, 2, 4, 7, 8, 12\}$):** Clearly classified as **Non-Manglik from Lagna (`लग्न से अमांगलिक`) / Mild Chandra-Manglik (`आंशिक चंद्र-मांगलिक`)**.
3. **Century-Free Vedic Surya Grid (`3-1-9 / 6-7-5 / 2-8-4`) + 37 Vedic Yogas:** Always present the authentic Century-Free Vedic Surya Grid as the primary Indian numerology grid, and show the full-date Lo Shu Grid (`4-9-2 / 3-5-7 / 8-1-6`) with `0x/1x/2x/3x/4x+` repetition diagnostics as the comparative secondary grid.
4. **First Name vs Full Name (10–52 Chaldean Compounds) + Katapayadi & Avakahada:** Audit First Name and Full Name separately and cross-check the Avakahada birth syllable (`panchanga.janma_nakshatra.avakahada_nama_akshara`) against the native's actual name (`katapayadi_and_svara`).
5. **Authentic BPHS Ch. 84–97 Sattvika Upayas:** Provide Vedic/Puranic Mantras, Sattvika Dana/Seva, Aushadhi/Lifestyle discipline, and Behavioral Karma alignment — **never sell commercial gemstones**.

---

## 4. Three `Astro DevAish` Hindi PDF Report Modes

Select the report mode based on user request (default is **Mode 1: 8-Page Report**):

### Mode 1: 8-Page Report (Standard Default — `पृष्ठ X / 8`)
- **Page 1:** `Astro DevAish` Branded Header Banner + 4 KPI Summary Cards (Lagna/Rashi, Mulank–Bhagyank & 81-Score, Active Vimshottari + 45-Yr Vedic Dasha, SAV/Shadbala Crest) + Core Synthesis Box + **Section 1: Janma Panchanga, Sunrise Vedic Vara & Sunrise Mulank, Gati/Combustion & Rashi Sandhi / Gandanta**.
- **Page 2:** **Section 2: North Indian SVG Charts (D1 Lagna, D9 Navamsa, D10 Dasamsa)** + **Section 3: 9 Grahas + Lagna Master Table** (Rashi, House, Sripati Chalit shift, Degrees, Nakshatra-Pada, KP Sub-Lord, Dignity/Vargottama/Pushkara/Asta tags & Hindi analysis).
- **Page 3:** **Section 4: Strict Parashari Mangal Dosha Verdict** + **Section 5: Classical Rajayogas, Functional Benefics/Malefics, Badhakesh/Maraka, Shadbala/Ishta-Kashta/Avasthas & Jaimini Karakas (AK, AmK, DK, Karakamsha, AL, UL)**.
- **Page 4:** **Section 6: All 16 Divisional Charts (Shodashavarga D1–D60)** + **Section 7: Sarvashtakavarga (SAV = 337 Bindus) Visual Bar Chart & House-by-House Strength Analysis**.
- **Page 5:** **Section 8: Career (Technical vs Managerial), Education, Business vs Job & Wealth/Runa-Debt Audit (D1 + D10 + AmK + 2H/11H vs 6H/12H SAV)** + **Section 9: Marriage, Spouse Profile (7H + D9 + DK + UL) & Personality Blueprint**.
- **Page 6:** **Section 10: Unified Timing I — Vimshottari Mahadasha/Antardasha/Pratyantardasha + Yogini Dasha + 2026–2029 Gochara Transits (Sade Sati/Dhaiya/Ashtama Shani with Moorthi Nirnaya & Double Transit)**.
- **Page 7:** **Section 11: Vedic Anka-Jyotish I — Mulank Sub-Personality, Bhagyank & Age-35 Transition, 81 Driver–Conductor Synergy & Bridge Number, Friendly/Anti Numbers, Graha-Anka Natal Chart Cross-Verification, and 45-Year Vedic Dasha + Weekday Annual Dasha**.
- **Page 8:** **Section 12: Vedic Anka-Jyotish II — Century-Free Vedic Surya Grid (`3-1-9 / 6-7-5 / 2-8-4`) & Active Yogas (from 37 Vedic Yogas), Comparative Lo Shu Grid (`0x–4x+` Repetition Rules), First vs Full Name (10–52 Chaldean) + Katapayadi/Svara Audit** + **Section 13: BPHS Ch. 84–97 Sattvika Upayas & Practical Action Plan** + Self-Reflection Disclaimer.

### Mode 2: 12-Page Report (Extended Deep-Dive — `पृष्ठ X / 12`)
Gives full breathing room to both Classical Jyotish (Pages 1–7) and Vedic Anka-Jyotish + Unified Synthesis (Pages 8–12):
- **Page 1:** `Astro DevAish` Header + Executive Synthesis + Janma Panchanga, Sunrise Savana Vara & Mulank, Gati/Combustion/Graha Yuddha & Sandhi/Gandanta.
- **Page 2:** North Indian SVG Charts (**D1, D9, D10, Bhava Chalit**) + 9 Grahas + Lagna Master Table.
- **Page 3:** **Shadbala (Virupas/Rupas/Ratio), Ishta vs Kashta Phala & 3-Tier Avasthas (Baladi, Jagradadi, Lajjitadi)** + **Functional Nature, Kendradhipati Dosha, Badhakesh & Maraka**.
- **Page 4:** **Shodashavarga (D1–D60) Matrix** + **Bhinna Ashtakavarga (7-Planet BAV) & 337 Sarvashtakavarga (SAV) Visual Analysis**.
- **Page 5:** **Strict Parashari Mangal Dosha + Classical Rajayogas/Parivartana/Vipareeta Yogas + Jaimini System (7 Chara Karakas AK–DK, Karakamsha, AL, UL, A7, A10)**.
- **Page 6:** **Career (Technical vs Managerial), Vocation & Wealth vs Runa/Debt Deep-Dive** (10H, D10, AmK, A10, 2H/11H vs 6H/12H SAV & Lords) + **Marriage, Spouse Nature & Family (7H, D9, DK, UL, D7)**.
- **Page 7:** **Vimshottari Mahadasha, Active Antardasha & Pratyantardasha Timeline + Yogini Dasha + 4-Year Gochara Transits (Moorthi Nirnaya, Sade Sati/Dhaiya/Ashtama Shani & Double Transit)**.
- **Page 8:** **Vedic Anka-Jyotish Core & Graha-Anka Birth Chart Cross-Verification:** Mulank Sub-Personality, Bhagyank 3-Cycle & Age-35 Transition, 81 Driver–Conductor Combination, Bridge Number, Friendly/Neutral/Anti Table, and D1/D9/SAV verification of Mulank & Bhagyank lords.
- **Page 9:** **Century-Free Vedic Surya Grid (`3-1-9 / 6-7-5 / 2-8-4`) with Dasha Overlay + Comprehensive Audit of the 37 Vedic Grid Yogas**.
- **Page 10:** **Comparative Lo Shu Grid (`4-9-2 / 3-5-7 / 8-1-6`), 8 Planes, Kua Number, Digit Repetition Diagnostics (`0x, 1x, 2x, 3x, 4x+`) & 4 Life Pinnacles/Challenges**.
- **Page 11:** **First Name vs Full Name Audit (Chaldean 10–52 Compounds + Pythagorean Core) + Katapayadi Sankhya & Svara/Avakahada Birth-Syllable Synergy + 45-Year Vedic Mahadasha/Antardasha & Weekday-Linked Annual Dasha (Varshaphal)**.
- **Page 12:** **Unified 3-Clock Convergence Calendar (Vimshottari + Gochara + 45-Yr Vedic Dasha/Personal Months) + Authentic BPHS Ch. 84–97 Sattvika Upayas & Behavioral Roadmap**.

### Mode 3: Full Report (16–20 Pages Master Edition — `पृष्ठ X / N`)
Expands Mode 2 into a comprehensive 16–20 page Master Edition:
- **Pages 1–10 (Complete Jyotish Shastra Volume):** Adds dedicated pages for **12-Bhava House-by-House Phalita Analysis**, **Multi-Varga SVG Charts (D1, D2, D3, D4, D7, D9, D10, D12, D30)**, and **Full Lifetime Vimshottari + 5-Year Pratyantardasha & Transit Calendar**.
- **Pages 11–18 (Complete Vedic Anka-Jyotish & Master Synthesis Volume):** Adds the **Full 37 Vedic Grid Yogas Personalized Encyclopedia**, **All 9 Graha-Anka (1–9) Natal Chart & Grid Cross-Verification Matrix**, **Letter-by-Letter Chaldean/Pythagorean/Katapayadi Name Architecture**, **Complete 45-Year Cycle 1 & Cycle 2 Mahadasha + Antardasha Tables**, **12-Month Personal Month & Varshaphal Tactical Planner**, and **BPHS Ch. 84–97 Sattvika Upaya & Life Strategy Blueprint**.

---

## 5. PDF Compilation & Visual Verification Checklist

1. Build self-contained HTML with `@page { size: A4 portrait; margin: 10mm 11mm 12mm 11mm; }` and embedded base64 `@font-face` (`NotoSansDevanagari_0.woff2`) and logo (`channels4_profile.jpg`).
2. Compile to PDF via headless Chrome:
   ```bash
   google-chrome --headless --disable-gpu --no-sandbox --no-pdf-header-footer --print-to-pdf=/path/to/output.pdf file:///path/to/report.html
   ```
3. Render pages to PNG (`pdftoppm -png -r 150 /path/to/output.pdf /tmp/page`) and inspect with `view_file` to guarantee:
   - Exact page count (`8`, `12`, or `16–20` pages) with zero trailing blank or overflow page.
   - Zero tofu boxes (`[][]`) and zero text clipping.
   - Every astrological and numerological number matches `chart.json`, `dasha.json`, `transit.json`, and `numerology.json` 100%.
