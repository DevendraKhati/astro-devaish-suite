---
name: vedic-numerology
description: "Authentic Indian Vedic Anka-Jyotish & Comparative Numerology skill featuring all 12 Vedic Anka-Jyotish capabilities (Century-Free Vedic Surya Grid 3-1-9/6-7-5/2-8-4, 37 Vedic Grid Yogas, 81 Driver-Conductor combinations + Bridge Number + Friendly/Neutral/Anti numbers, Age-35 Transition rule, 45-Year Vedic Mahadasha/Antardasha + Weekday-linked Annual Dasha, Compound Birth-Date sub-personalities 10-31, Sunrise Mulank rule, First Name vs Full Name audit with 10-52 Chaldean compounds, Katapayadi Sankhya & Svara/Avakahada phonetics, and Lo Shu Grid with 1x/2x/3x/4x+ over-repetition remedies). Generates Astro DevAish Hindi (Devanagari) PDF reports in 8-Page (Default), 12-Page (Extended), and Full (16-20 Pages Master) modes."
---

# Vedic Numerology (`vedic-numerology`) — Authentic Indian Anka-Jyotish, Katapayadi, Svara Shastra & Comparative Numerology

This skill provides end-to-end **Authentic Indian Vedic Anka-Jyotish (वैदिक अंक-ज्योतिष)** alongside **Katapayadi Sankhya**, **Svara Shastra / Avakahada Phonetics**, **Chaldean (10–52 Compound System)**, **Pythagorean Core**, and **Lo Shu Grid Diagnostics**, clearly distinguishing authentic Indian Navagraha numerical traditions from imported systems while delivering both with mathematical precision.

---

## 1. `Astro DevAish` Brand & Output Standard

Unless the user explicitly requests a different format or language:
1. **Brand Identity:** Always brand reports as **`Astro DevAish`** and embed the circular logo (`/home/antigravity/channels4_profile.jpg`) as a base64 data URI in the header banner and page footers (fall back cleanly to a styled SVG emblem if the image file is absent).
2. **Default Language:** **Hindi (देवनागरी — Simple, clear, traditional & practical Hindi)** by default. Switch to **Hinglish** or **English** only when explicitly requested by the user.
3. **Mandatory Devanagari Font Embedding:** Always embed `/home/antigravity/.local/share/fonts/NotoSansDevanagari_0.woff2` as a base64 `@font-face` data URI inside the HTML before compiling via headless Chrome (`google-chrome --headless --disable-gpu --no-sandbox --no-pdf-header-footer --print-to-pdf=...`) so Hindi text never renders as tofu boxes (`[][]`). Visually verify rendered pages with `pdftoppm -png -r 150` + `view_file`.
4. **No Marketing or Meta Labels:** Keep predictions direct, honest, and grounded, but **NEVER** print meta-labels like `(बिना शुगरकोटिंग)` or `(No-Sugarcoating)` anywhere in the title, header, footer, or body.
5. **Compute with `scripts/numerology.py` — Never from Memory:** Always execute `scripts/numerology.py` and read its complete JSON output before writing any analysis or building a PDF.

---

## 2. Running the Computation Engine (`vedic-numerology` / `numerology.py` — Accessible from Any Directory)

The engine is installed globally on `PATH` (`vedic-numerology`, `numerology`, `astro-devaish`) and also bundled at `/home/antigravity/.gemini/skills/vedic-numerology/scripts/numerology.py`. Run it from **any working directory**:

```bash
# 1. Global Vedic Anka-Jyotish + Comparative Numerology Run from ANY directory
vedic-numerology \
  --name "Chandan Singh Bisht" \
  --dob 1995-08-26 \
  --tob 22:35 \
  --sunrise 05:56 \
  --gender male > numerology.json

# 2. Unified One-Command Run with Natal Chart Cross-Verification (when birth time & place are also known)
astro-devaish \
  --name "Chandan Singh Bisht" \
  --dob 1995-08-26 \
  --tob 22:35 \
  --lat 29.2183 \
  --lon 79.5130 \
  --place "Haldwani" \
  --gender male > master.json
```

---

## 3. The 12 Core Pillars of Vedic Anka-Jyotish

### 1. Navagraha Graha-Anka Mapping & Compound Birth-Date Sub-Personalities (1–31)
- **Navagraha Rulers:**
  - $1 = \text{Surya (सूर्य — Sun)}$
  - $2 = \text{Chandra (चंद्र — Moon)}$
  - $3 = \text{Guru / Brihaspati (गुरु — Jupiter)}$
  - $4 = \text{Rahu (राहु — North Node)}$
  - $5 = \text{Budha (बुध — Mercury)}$
  - $6 = \text{Shukra (शुक्र — Venus)}$
  - $7 = \text{Ketu (केतु — South Node)}$
  - $8 = \text{Shani (शनि — Saturn)}$
  - $9 = \text{Mangala (मंगल — Mars)}$
- **Compound Birth-Date Sub-Personalities (`birth_number.sub_personality`):**
  - Never treat all birthdays of the same Mulank identically! For example, within Mulank $8$ (Saturn):
    - **8th:** Pure Saturnian duty and structural endurance.
    - **17th ($1 + 7 \rightarrow 8$):** Solar authority ($1$) + Ketu mystic intuition ($7$) producing spiritually protected leadership ($8$).
    - **26th ($2 + 6 \rightarrow 8$):** Lunar sensitivity ($2$) + Venusian relational devotion ($6$) outwardly carrying Saturn's heavy karmic duty ($8$) — requires strict written clarity in partnerships and finances.
  - Also highlight **Master Numbers ($11/2, 22/4, 33/6$)** and **Karmic Debt Numbers ($13/4, 14/5, 16/7, 19/1$)**.

### 2. Sunrise Mulank Rule (*Surya Siddhanta Savana Dina* — `sunrise_mulank_rule`)
- In authentic Vedic Jyotish and Anka-Jyotish, a Vedic day (*Savana Dina* / *Vara*) begins at **local apparent sunrise**, not midnight (`00:00`).
- If `tob < local_sunrise` (`born_before_sunrise == True`), report **both**:
  - **Vedic Savana Mulank** (previous day's reduced number — governs inner soul, intuition, and spiritual temperament).
  - **Civil Mulank** (calendar date's reduced number — governs official documents, social identity, and public interactions).

### 3. Bhagyank (Conductor / Destiny Number) & The Age-35 Transition Rule (`life_path.age_35_transition`)
- **Bhagyank** is computed from the full Date of Birth (`Day + Month + Year`), tracking both the digit-sum chain and the 3-cycle sum (`Mulank + Month_Anka + Year_Anka`).
- **Age-35 Transition Rule:**
  - **Ages $0–31$:** **Mulank (Driver)** dominates ($\sim 70\%$ Mulank, $30\%$ Bhagyank).
  - **Ages $32–35$:** **Transition Threshold Window** ($50\%–50\%$ shift from inner habit to destiny structure).
  - **Age $35+$ (`birth_year + 35` onwards):** **Bhagyank (Conductor)** takes primary command ($\sim 70\%$ Bhagyank, $30\%$ Mulank).

### 4. All 81 Driver–Conductor (Mulank–Bhagyank) Combinations & Bridge Number (`driver_conductor_synergy`)
- Report the exact **81-pair combination (`M-B`)**, its **compatibility rating out of 5.0 (and score out of 10)**, classical Graha relationship between Mulank Lord and Bhagyank Lord, and Hindi synthesis.
- **Bridge Number (`|Mulank - Bhagyank|`):** Explains the exact planetary quality (`bridge_number.ruler_hi`) required to bridge the native's inner nature (Mulank) and outer destiny (Bhagyank).

### 5. Friendly, Neutral & Anti (Enemy) Numbers Table (`driver_conductor_synergy.number_relationships`)
- Provide the complete planetary friendship table for:
  1. **Mulank Friendly / Neutral / Anti numbers**
  2. **Bhagyank Friendly / Neutral / Anti numbers**
  3. **Combined Intersection (`combined_mutual_friendly_numbers`, `combined_neutral_numbers`, `combined_anti_avoid_numbers`)** — used for selecting auspicious dates, house/flat numbers, vehicle digits, and name vibration targets.

### 6. Century-Free Vedic Surya Grid (`3-1-9 / 6-7-5 / 2-8-4` — `vedic_surya_grid`)
- **Authentic Indian Vedic Grid Layout (*Surya Yantra*):**
  ```
  3 (Guru)    | 1 (Surya) | 9 (Mangala)
  6 (Shukra)  | 7 (Ketu)  | 5 (Budha)
  2 (Chandra) | 8 (Shani) | 4 (Rahu)
  ```
- **Why Century-Free?** In traditional Indian Anka-Jyotish, the fixed century digits (`19` in `1900–1999` or `20` in `2000–2099`) are **excluded** because every person born in a century shares them; including `1` and `9` automatically in every 20th-century chart creates false `1-9` and `3-1-9` yogas!
- **Digits Populated in the Vedic Surya Grid:**
  1. **Day digits** (nonzero)
  2. **Month digits** (nonzero)
  3. **Last two digits of Birth Year** (nonzero)
  4. **Mulank** (added if `day > 9`)
  5. **Bhagyank** (always added as life-path anchor)
  6. **Active Dasha Overlay (`MD` = Active 45-Yr Mahadasha number, `AD` = Active Annual Dasha number)** shown as dynamic temporal activations inside the grid.

### 7. The 37 Vedic Anka-Jyotish Grid Yogas (`vedic_surya_grid.vedic_yogas_summary`)
- Evaluate the populated Century-Free Vedic Surya Grid against all **37 Vedic Yogas**:
  - **8 Primary 3-Number Planes:**
    1. `3-1-9` Guru-Surya-Mangal Top Rajayoga Row (Intellectual Sovereignty & Executive Command)
    2. `6-7-5` Shukra-Ketu-Budha Middle Intuitive Commerce Row (Diplomacy, Research & Trade)
    3. `2-8-4` Chandra-Shani-Rahu Bottom Grounded Karma Row (Grassroots Realism & Systemic Endurance)
    4. `3-6-2` Guru-Shukra-Chandra Left Wisdom & Grace Column
    5. `1-7-8` Surya-Ketu-Shani Center Tapasya & Justice Axis
    6. `9-5-4` Mangal-Budha-Rahu Right Action & Tech Execution Column
    7. `3-7-4` Guru-Ketu-Rahu NW-SE Occult & Deep-Tech Diagonal
    8. `9-7-2` Mangal-Ketu-Chandra NE-SW Intuitive Courage Diagonal
  - **4 Strategic Triads:** `1-5-9` Royal Execution Triad, `3-5-6` Vidya-Lakshmi Triad, `2-5-6` Public & Financial Grace Triad, `4-7-8` Deep Engineering & Karma Triad.
  - **25 Classical 2-Number Graha-Anka Yogas:** Including both auspicious yogas (`1-3` Guru-Aditya, `1-9` Aditya-Kuja, `3-9` Guru-Mangal, `1-5` Budhaditya, `3-5` Saraswati-Vidya, `5-6` Lakshmi-Vyapara, `2-3` Gajakesari, `4-5` Chatura-Tech, `3-7` Prana-Pragya, `6-8` Sthira-Sampada) and karmic testing yogas (`1-8` Surya-Shani Sangharsha, `2-8` Chandra-Shani Vish-Tapasya, `4-8` Rahu-Shani Shrama-Tantra, `8-9` Shani-Mangal Dhairya-Shakti, `2-4` Kalpana-Vistara, `2-7` Antardrishti).

### 8. 45-Year Vedic Numerology Dasha + Weekday-Linked Annual Dasha (`vedic_45yr_dasha`)
- **45-Year Mahadasha Cycle ($\sum_{n=1}^{9} n = 45\text{ years}$):**
  - Begins at birth from the native's **Mulank** number.
  - Each Graha-Anka $N$ rules for **$N$ years** ($1\text{ Sun}=1\text{y}, 2\text{ Moon}=2\text{y}, 3\text{ Jupiter}=3\text{y}, 4\text{ Rahu}=4\text{y}, 5\text{ Mercury}=5\text{y}, 6\text{ Venus}=6\text{y}, 7\text{ Ketu}=7\text{y}, 8\text{ Saturn}=8\text{y}, 9\text{ Mars}=9\text{y}$) in ascending cyclic order $M \rightarrow (M \bmod 9)+1 \dots$
  - Includes proportional **Antardashas** ($\frac{M \times A}{45}\text{ years}$) with exact start and end dates.
- **Weekday-Linked Annual Dasha (*Varsha Dasha*):**
  - Runs from birthday to birthday each year:
    $$\text{Vedic Annual Dasha} = \text{reduce}\big(\text{Day} + \text{Month} + (\text{Target Year} \bmod 100) + \text{Birthday Weekday Anka}\big)$$
    where Sunday $=1$, Monday $=2$, Tuesday $=9$, Wednesday $=5$, Thursday $=3$, Friday $=6$, Saturday $=8$.

### 9. First Name vs Full Name Audit with 10–52 Chaldean Compounds (`name_audit_chaldean_10_52`)
- Always audit **First Name** (personal/social call vibration) and **Full Name** (official signature/destiny vibration) separately!
- Interpret the exact **Chaldean Compound Number ($10–52$)** for both First Name and Full Name (e.g., `24` *Love, Money & Patronage* vs `26/35` *Partnerships Caution* or `19` *Prince of Heaven* or `23` *Royal Star of the Lion*).
- Provide pragmatic, non-destructive guidance (when to emphasize First Name vs Full Name in daily call, signature, or professional branding without changing legal documents unnecessarily).

### 10. Katapayadi Sankhya & Svara Shastra / Avakahada Phonetics (`katapayadi_and_svara`)
- **Katapayadi Sankhya:** Encodes the name's Sanskrit consonants into digits ($ka\text{-group } 1–9,0$; $ta\text{-group } 1–9,0$; $pa\text{-group } 1–5$; $ya\text{-group } 1–8$), applies the conjunct rule (*"मिश्रिते तु परो हल् स्यात्"*) and right-to-left reversal (*"अङ्कानां वामतो गतिः"*), and computes the **Katapayadi Nama-Anka ($\bmod 9$)** and **Katapayadi Rashi ($\bmod 12$)**.
- **Svara Shastra & Avakahada:** Maps the opening vowel (*Svara*) to its **Pancha-Tatva** element and the opening syllable (*Adya-Akshara*) to its **Nakshatra, Rashi, and Ruling Graha**.

### 11. Comparative Lo Shu Grid (`4-9-2 / 3-5-7 / 8-1-6`) & Over-Repetition Diagnostics (`1x/2x/3x/4x+`)
- Render the full-date Lo Shu Grid side-by-side with the Century-Free Vedic Surya Grid so the user sees why the two systems differ.
- Evaluate all **8 Lo Shu Planes of Expression** (Mental, Emotional, Practical, Thought, Will, Action, Golden Rajyog `4-5-6`, Silver Rajat Yog `2-5-8`) and **Kua Number**.
- **Over-Repetition Rules (`repetition_diagnostics`):** Explicitly diagnose every digit's frequency (`0x` Missing, `1x` Balanced, `2x` Strong, `3x` Excessive/Volatile, `4x+` Extreme Over-Concentration) with non-commercial behavioral and elemental remedies.

### 12. Pythagorean Core, 4 Life Pinnacles/Challenges & Personal Year/Months
- Report **Pythagorean Expression, Soul Urge (Heart's Desire), and Personality Numbers**, the **4 Life Pinnacles & 4 Challenges** with exact age spans, and the **4-Year Personal Year Forecast + 12 Personal Months**.

---

## 4. Three `Astro DevAish` Hindi PDF Report Modes

Select the report mode based on user request (default is **Mode 1: 8-Page Report**):

### Mode 1: 8-Page Report (Standard Default — `पृष्ठ X / 8`)
- **Page 1:** `Astro DevAish` Branded Header Banner + 4 KPI Cards (Mulank, Bhagyank, Active 45-Yr Dasha, Name Number) + Core Executive Summary + **Section 1: Mulank, Compound Birth-Date Sub-Personality & Sunrise Mulank Rule**.
- **Page 2:** **Section 2: Bhagyank (3-Cycle Reduction), Age-35 Transition Timeline, 81 Driver–Conductor Synergy Rating & Bridge Number** + **Section 3: Friendly, Neutral & Anti Numbers Matrix**.
- **Page 3:** **Section 4: Century-Free Vedic Surya Grid (`3-1-9 / 6-7-5 / 2-8-4`) SVG/Visual Matrix with Active Dasha Overlay** + **Section 5: Analysis of Active Yogas from the 37 Vedic Grid Yogas Catalog**.
- **Page 4:** **Section 6: Comparative Lo Shu Grid (`4-9-2 / 3-5-7 / 8-1-6`), 8 Planes of Expression & Kua Number** + **Section 7: Digit Repetition Diagnostics (`0x`, `1x`, `2x`, `3x`, `4x+`) & Missing/Excess Remedies**.
- **Page 5:** **Section 8: First Name vs Full Name Audit (Chaldean 10–52 Compound Breakdown & Signature/Branding Verdict)** + **Section 9: Katapayadi Sankhya, Svara Tatva & Avakahada Nama-Akshara Analysis**.
- **Page 6:** **Section 10: Pythagorean Core Profile (Expression, Soul Urge, Personality) & 4 Life Pinnacles / 4 Challenges Timeline**.
- **Page 7:** **Section 11: 45-Year Vedic Mahadasha & Active Antardasha Timeline** + **Section 12: Weekday-Linked Annual Dasha (Varshaphal) & 12-Month Personal Month Calendar**.
- **Page 8:** **Section 13: Career, Finance, Relationship & Lucky Parameters (Dates, Colors, Directions, House/Vehicle Numbers) + Non-Commercial Sattvika Remedies & Self-Reflection Disclaimer**.

### Mode 2: 12-Page Report (Extended Deep-Dive — `पृष्ठ X / 12`)
Expands the 8-Page report into 12 detailed A4 pages:
- **Pages 1–2:** Detailed Mulank sub-personality, Sunrise Savana analysis, Bhagyank 3-cycle reduction, Age-35 maturity curve, 81-combination deep dive, and Bridge Number execution plan.
- **Pages 3–4:** Full Century-Free Vedic Surya Grid (`3-1-9 / 6-7-5 / 2-8-4`) + complete audit of **all 37 Vedic Grid Yogas** (separating Complete Active Yogas, 2/3 Partial Planes activated by Dasha, and Missing Planes).
- **Page 5:** Comparative Lo Shu Grid + all 9 Digits (`1–9`) `0x/1x/2x/3x/4x+` repetition psychology and balancing protocols.
- **Pages 6–7:** Comprehensive **First Name, Middle Name, Surname & Full Name Chaldean (10–52) + Pythagorean + Katapayadi + Svara Shastra Audit**, including letter-by-letter vibration tables and non-destructive signature/business branding alignment.
- **Page 8:** **45-Year Vedic Mahadasha (Cycle 1 & Cycle 2) Full Lifetime Table** + Detailed Antardasha breakdown of the current Mahadasha.
- **Page 9:** **7-Year Weekday-Linked Vedic Annual Dasha (Varshaphal) + Personal Year + 12-Month Tactical Calendar**.
- **Page 10:** **4 Life Pinnacles & 4 Challenges Deep-Dive** + Career, Business vs Job & Financial Risk Windows.
- **Page 11:** **Relationship, Marriage & Business Partner Number Compatibility Guide (1–9 Matrix)** + Mobile/House/Vehicle/Account Number Audit rules.
- **Page 12:** **Sattvika Navagraha-Anka Lifestyle & Behavioral Action Plan** + Methodology & Self-Reflection Note.

### Mode 3: Full Report (16–20 Pages Master Edition — `पृष्ठ X / N`)
Includes all 12 pages of Mode 2 PLUS:
- Complete **37-Yoga Encyclopedia Table** personalized to the native's grid counts and upcoming Dasha activations.
- **9-Year Complete Antardasha & Monthly Varshaphal Micro-Timeline**.
- **Graha-Anka Natal Chart Cross-Verification Annex** (when birth time/place are available via `scripts/jyotish.py chart`), mapping every number `1–9` in the Vedic Grid to its ruling planet's actual house, sign, Shadbala, and SAV bindus in the natal horoscope.
