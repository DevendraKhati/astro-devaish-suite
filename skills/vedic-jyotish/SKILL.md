---
name: vedic-jyotish
description: Authentic Classical Indian Vedic Astrology (Jyotish Shastra — Parashari, Jaimini, KP, Ashtakavarga & Ganita Skandha) grounded in Brihat Parashara Hora Shastra (BPHS), Surya Siddhanta, Brihat Jataka, Phaladeepika, Jaimini Sutras, Saravali, Jataka Parijata, Uttara Kalamrita, Prasna Marga, and Muhurta Chintamani. Computes Sunrise Vedic Vara, Gati/Asta/Graha Yuddha, Rashi Sandhi/Gandanta, D1-D60 Shodashavarga, Sripati Bhava Chalit, Shadbala, Ishta/Kashta Phala, Baladi/Jagradadi/Lajjitadi Avasthas, strict Parashari Mangal Dosha, Badhakesh/Maraka, 337 SAV & BAV, Career/Runa-Debt/Marriage/Personality diagnostics, and BPHS Ch. 84-97 Sattvika Upayas. Generates Astro DevAish Hindi (Devanagari) PDF reports in 8-Page (Default), 12-Page (Extended), and Full (16-20 Pages Master) modes.
---

# Vedic Jyotish (`vedic-jyotish`) — Classical Parashari, Jaimini, KP & Ganita Astronomy

This skill provides end-to-end **Authentic Indian Vedic Astrology (Jyotish Shastra)** and **Scientific Positional Astronomy (Ganita Skandha)** grounded strictly in classical Sanskrit treatises (**Brihat Parashara Hora Shastra, Surya Siddhanta, Brihat Jataka, Phaladeepika, Jaimini Sutras, Saravali, Jataka Parijata, Uttara Kalamrita, Prasna Marga, Muhurta Chintamani**) and NASA JPL / Swiss Ephemeris precision.

---

## 1. `Astro DevAish` Brand & Output Standard

Unless the user explicitly requests a different format or language:
1. **Brand Identity:** Always brand reports as **`Astro DevAish`** and embed the circular logo (`/home/antigravity/channels4_profile.jpg`) as a base64 data URI in the header banner and page footers (fall back cleanly to a styled SVG emblem if the image file is absent).
2. **Default Language:** **Hindi (देवनागरी — Simple, clear, traditional & practical Hindi)** by default. Switch to **Hinglish** or **English** only when explicitly requested by the user.
3. **Mandatory Devanagari Font Embedding:** Always embed `/home/antigravity/.local/share/fonts/NotoSansDevanagari_0.woff2` as a base64 `@font-face` data URI inside the HTML before compiling via headless Chrome (`google-chrome --headless --disable-gpu --no-sandbox --no-pdf-header-footer --print-to-pdf=...`) so Hindi text never renders as tofu boxes (`[][]`). Visually verify rendered pages with `pdftoppm -png -r 150` + `view_file`.
4. **No Marketing or Meta Labels:** Keep predictions direct, honest, and scripturally accurate, but **NEVER** print meta-labels like `(बिना शुगरकोटिंग)` or `(No-Sugarcoating)` anywhere in the title, header, footer, or body.
5. **Compute with Scripts — Never from Memory:** Always run `scripts/jyotish.py` (`chart`, `dasha`, `transit`, `match`, `sky`) and read the exact JSON output before writing prose or generating HTML/PDF.

---

## 2. Running the Computation Engine (`vedic-jyotish` / `jyotish.py` — Accessible from Any Directory)

The engine is installed globally on `PATH` (`vedic-jyotish`, `jyotish`, `astro-devaish`) and also bundled at `/home/antigravity/.gemini/skills/vedic-jyotish/scripts/jyotish.py`. You can run it from **any working directory** either with inline flags or with `--input person.json`:

```bash
# Option A: Direct inline CLI from ANY directory (no JSON file required)
vedic-jyotish chart --name "Chandan Singh Bisht" --dob 1995-08-26 --tob 22:35 --lat 29.2183 --lon 79.5130 --place "Haldwani" > chart.json
vedic-jyotish dasha --dob 1995-08-26 --tob 22:35 --lat 29.2183 --lon 79.5130 --at 2026-11-25 > dasha.json
vedic-jyotish transit --dob 1995-08-26 --tob 22:35 --lat 29.2183 --lon 79.5130 --from 2026-01-01 --years 4 > transit.json

# Option B: Using a person.json file
# {"name":"Chandan Singh Bisht","dob":"1995-08-26","tob":"22:35","lat":29.2183,"lon":79.5130,"tz":5.5,"place":"Haldwani","birth_time_accuracy":"exact"}
vedic-jyotish chart --input person.json > chart.json
vedic-jyotish match --a bride.json --b groom.json > match.json
```

---

## 3. Scientific Ganita Skandha + Classical Phalita Skandha Doctrine

### A. Ganita Skandha (Positional Astronomy — *Surya Siddhanta*)
1. **Ayanamsa:** Default **Chitrapaksha / Lahiri Ayanamsa** (`SE_SIDM_LAHIRI`).
2. **Sunrise & Vedic Savana Vara (*Surya Siddhanta*):**
   - A Vedic weekday (*Vara*) begins at local **apparent sunrise**, not midnight (`00:00`).
   - Any birth between `00:00` and local sunrise (`panchanga.born_before_sunrise == True`) belongs to the **previous civil day's Vedic Vara and Hora lord** (`panchanga.vedic_savana_vara`). Always report both Civil Weekday and Vedic Savana Vara.
3. **Planetary Motion States (*Gati* — *Surya Siddhanta* & *BPHS*):**
   - Report exact daily angular velocity (`speed_deg_per_day`) and classical *Gati*:
     - **Vakra (वक्री / Retrograde):** High Cheshta Bala; internalized, repetitive, or unconventional karmic execution.
     - **Vikala / Stambhana (स्तंभन / Stationary):** Intense focal point near station.
     - **Manda (मंद / Slow):** Deliberate, delayed delivery.
     - **Sama (सम गति / Mean Speed):** Balanced delivery.
     - **Sheeghra / Atichara (शीघ्र / Accelerated):** Rapid, early delivery of results.
4. **Combustion (*Asta / Moudhya* — *Surya Siddhanta* Ch. 9):**
   - Classical orbs from the Sun: **Moon $12^\circ$**, **Mars $17^\circ$**, **Mercury $14^\circ$ (Direct) / $12^\circ$ (Retrograde)**, **Jupiter $11^\circ$**, **Venus $10^\circ$ (Direct) / $8^\circ$ (Retrograde)**, **Saturn $15^\circ$**.
5. **Planetary War (*Graha Yuddha* — *Surya Siddhanta* & *Brihat Samhita*):**
   - Two true planets (**Mars, Mercury, Jupiter, Venus, Saturn**) within **$1^\circ$ ecliptic longitude**. The planet with northern latitude ($\beta$) is the victor (*Jayee*); the other is defeated (*Parajita*).
6. **Rashi Sandhi & Gandanta:**
   - **Rashi Sandhi:** First $1^\circ$ ($0^\circ–1^\circ$) or last $1^\circ$ ($29^\circ–30^\circ$) of any sign.
   - **Gandanta:** Water-to-Fire junctions — last $3^\circ 20'$ (core $0^\circ 48'$) of **Cancer (Ashlesha), Scorpio (Jyeshtha), Pisces (Revati)** and first $3^\circ 20'$ (core $0^\circ 48'$) of **Aries (Ashwini), Leo (Magha), Sagittarius (Mula)**.

### B. Dual House System: Whole Sign (Rashi Tulya Bhava) + Sripati Bhava Chalit
- Use **Whole Sign (Rashi Tulya Bhava)** for primary Parashari lordships, aspects, yogas, and Ashtakavarga.
- Check **Sripati Bhava Chalit** (`bhava_chalit.shifted_planets`): if any planet shifts into an adjacent Bhava in Chalit (`chalit_shifted == True`), explain how its Dasha modifies tangible house delivery (*Phaladeepika*).

### C. Shadbala, Ishta/Kashta Phala & 3-Tier Avasthas (BPHS Ch. 27 & Ch. 45)
1. **Shadbala (in Virupas & Rupas):**
   - **Sthana Bala + Dig Bala + Kala Bala + Cheshta Bala + Naisargika Bala + Drik Bala**.
   - Compare against **BPHS Minimum Required Rupas**: Mercury `7.0`, Sun `6.5`, Jupiter `6.5`, Moon `6.0`, Venus `5.5`, Mars `5.0`, Saturn `5.0` (`shadbala_ratio >= 1.0`).
2. **Ishta Phala vs Kashta Phala:**
   - $\text{Ishta} = \sqrt{\text{Uchcha} \times \text{Cheshta}}$; $\text{Kashta} = \sqrt{(60 - \text{Uchcha}) \times (60 - \text{Cheshta})}$. Explains why a planet's Mahadasha feels smooth ($\text{Ishta} > \text{Kashta}$) or effort-intensive ($\text{Kashta} > \text{Ishta}$).
3. **Planetary Avasthas (BPHS Ch. 45):**
   - **Baladi (5 Degree States):** *Bala* (25%), *Kumara* (50%), *Yuva* (100%), *Vriddha* (low), *Mrita* (dormant) — reversed in even signs.
   - **Jagradadi (3 Dignity States):** *Jagrat* (Awake — own/exalted), *Swapna* (Dreaming — friend/neutral), *Sushupti* (Sleeping — enemy/debilitated).
   - **Lajjitadi (6 Psychological/Relational States):** *Garvita, Mudita, Lajjita, Kshobhita, Kshudhita, Trishita*.

### D. Strict Parashari Mangal Dosha (Kuja Dosha — BPHS & Phaladeepika)
Never collapse severe Lagna Manglik placements into "Non-Manglik" due to generic internet cancellation lists:
1. **Saptama Manglik (7th House Mars from Lagna) & Ashtama Manglik (8th House Mars from Lagna):**
   - Severe Parashari Lagna Manglik placements (`present: True`, `present_from_lagna: True`).
   - Benefic aspect (Jupiter) or dignity (own/exalted) **mitigates harshness** (`mitigations`), but **NEVER cancels the Manglik status to Non-Manglik**. Always advise Manglik-to-Manglik balance and Shastric Kumbha/Ark Vivaha or Mangal Shanti.
2. **Lagna Manglik in 1st, 2nd, 4th, 12th Houses:**
   - Moderate Lagna Manglik (`present: True`), graded by house and dignity.
3. **Moon-Chart-Only (*Chandra-Manglik*) Placements:**
   - If Mars is **NOT** in $\{1, 2, 4, 7, 8, 12\}$ from **Lagna** (e.g., Mars in 9th house conjoined with Jupiter/Lagna Lord) and only falls in a Manglik house from Moon, classify clearly as **Non-Manglik from Lagna (`लग्न से अमांगलिक`) / Mild Chandra-Manglik (`आंशिक चंद्र-मांगलिक`)** (`present: False`).

### E. Functional Nature, Kendradhipati Dosha, Badhakesh & Maraka (BPHS Ch. 34 & Prasna Marga)
- **Functional Benefics, Malefics & Yogakaraka:** Determined strictly by Trikona ($1, 5, 9$) vs Trishadaya ($3, 6, 11$) and Dusthana ($6, 8, 12$) lordships for the native's Lagna.
- **Badhaka Sthana & Badhakesh:** **11th house** for Chara Lagnas ($1, 4, 7, 10$), **9th house** for Sthira Lagnas ($2, 5, 8, 11$), **7th house** for Dwiswabhava Lagnas ($3, 6, 9, 12$).
- **Maraka Sthana:** **2nd and 7th Lords** and their occupants.

### F. Shodashavarga (D1–D60), Jaimini Sutras & 337 Sarvashtakavarga
- **16 Divisional Charts:** D1, D2 (wealth), D3 (siblings/courage), D4 (property/fortune), D7 (progeny), D9 (Navamsa — marriage & dharma confirm/deny), D10 (Dasamsa — career authority), D12 (parents), D16 (vehicles/inner happiness), D20 (upasana), D24 (siddhi/learning), D27 (stamina), D30 (arista/obstacles), D40, D45, D60 (past-life root karma — interpret D60 only when birth time is exact).
- **Vargottama, Pushkara Navamsa & Pushkara Bhaga:** Flag every planet holding these regenerative strengths.
- **Jaimini System:** 7 Chara Karakas (**AK, AmK, BK, MK, PK, GK, DK**), **Karakamsha** (10th from Karakamsha for vocation; 12th for *Ishta Devata*), and **Arudha Padas** (**AL, UL, A7, A10** with classical 1st/7th $\rightarrow$ 10th/4th exception).
- **Ashtakavarga:** 7 Planet **Bhinna Ashtakavarga (BAV, $0–8$ bindus)** + **Sarvashtakavarga (SAV = exact $337$ bindus)**.

### G. Life-Dimension Diagnostics & Authentic BPHS Ch. 84–97 Sattvika Upayas
- **Career (Technical vs Managerial):** Cross-verify 10th House, 10th Lord, D10, Jaimini **AmK**, and 10th SAV bindus.
- **Wealth & Debt (*Runa Yoga* Audit):** Compare **2nd + 11th houses (Dhana/Labha)** against **6th + 12th houses (Runa/Vyaya)** in both lord placements and SAV bindus.
- **Marriage & Spouse Profile:** Synthesize 7th House, 7th Lord, **D9 Navamsa**, Jaimini **Darakaraka (DK)**, **Upapada Lagna (UL)**, and strict Mangal Dosha status.
- **Personality & Psychology:** Synthesize Lagna/Lagna Lord (outer stride), Moon/Nakshatra (emotional mind), and **Atmakaraka (AK)** (soul compass).
- **Authentic BPHS Ch. 84–97 Upayas (Zero Commercial Gemstone Selling):**
  1. **Avatara / Ishta & Graha Shanti Mantras** (Vedic/Puranic Stotras & Japa)
  2. **Sattvika Dana & Seva** (Targeted charity and service on the planet's Vara)
  3. **Aushadhi Snana & Lifestyle Discipline** (Herbal/sacred water bath, Prana/Surya discipline)
  4. **Behavioral Karma Alignment** (Practical ethical/behavioral corrections matching the planet's house)

---

## 4. Three `Astro DevAish` Hindi PDF Report Modes

Select the report mode based on user request (default is **Mode 1: 8-Page Report**):

### Mode 1: 8-Page Report (Standard Default — `पृष्ठ X / 8`)
- **Page 1:** `Astro DevAish` Branded Header Banner + 4 KPI Summary Cards + Core Chart Summary Box + **Section 1: Janma Panchanga, Sunrise Vedic Vara, Gati/Combustion & Rashi Sandhi / Gandanta**.
- **Page 2:** **Section 2: North Indian SVG Charts (D1 Lagna, D9 Navamsa, D10 Dasamsa)** + **Section 3: 9 Grahas + Lagna Master Table** (Rashi, House, Chalit shift, Degrees, Nakshatra-Pada, KP Sub-Lord, Dignity/Vargottama/Pushkara/Asta tags & Hindi analysis).
- **Page 3:** **Section 4: Strict Parashari Mangal Dosha Analysis** + **Section 5: Classical Rajayogas, Functional Benefics/Malefics, Badhakesh/Maraka & Jaimini Karakas (AK, AmK, DK, Karakamsha, AL, UL)**.
- **Page 4:** **Section 6: Shadbala (Rupas/Ratio), Ishta vs Kashta Phala & Avasthas (Baladi, Jagradadi, Lajjitadi)** + **Section 7: Sarvashtakavarga (SAV = 337 Bindus) Visual Bar Chart & House-by-House Strength**.
- **Page 5:** **Section 8: Shodashavarga (D1–D60) Table & Key Varga Verdicts** + **Section 9: Career (Technical vs Managerial), Education & Runa/Debt vs Wealth Audit (2H/11H vs 6H/12H)**.
- **Page 6:** **Section 10: Marriage, Spouse Nature (7H + D9 + DK + UL) & Family/Progeny (D7)** + **Section 11: Personality, Health & Psychological Blueprint (Lagna + Moon + AK)**.
- **Page 7:** **Section 12: Vimshottari Mahadasha, Active Antardasha & Pratyantardasha Timeline + Yogini Dasha Cross-Check** + **Section 13: 3-to-5 Year Transits (Gochara), Sade Sati/Dhaiya/Ashtama Shani (with Moorthi Nirnaya & BAV/SAV) & Double Transit Activations**.
- **Page 8:** **Section 14: Authentic BPHS Ch. 84–97 Sattvika Upayas (Mantra, Dana/Seva, Aushadhi & Behavioral Karma)** + Year-by-Year Action Roadmap + Self-Reflection Disclaimer.

### Mode 2: 12-Page Report (Extended Deep-Dive — `पृष्ठ X / 12`)
Expands the 8-Page structure into 12 dedicated A4 pages:
- **Pages 1–3:** Same foundation as Mode 1 with expanded Bhava Chalit cusp table and Graha Yuddha / Gati / Avastha commentary.
- **Page 4:** Dedicated **Shadbala (6-fold Virupa breakdown) + Ishta/Kashta Phala + 3-Tier Avastha Deep-Dive** for all 7 true planets + Rahu/Ketu.
- **Page 5:** Complete **16-Varga Shodashavarga Matrix (D1–D60)** with separate SVG diagrams for **D2 (Hora), D7 (Saptamsa), D9 (Navamsa), D10 (Dasamsa), D12 (Dwadasamsa), D30 (Trimsamsa)**.
- **Page 6:** Full **Bhinna Ashtakavarga (BAV 7-Planet Grid) + 337 Sarvashtakavarga (SAV)** + Kakshya transit implications.
- **Page 7:** **12-Bhava House-by-House Detailed Phalita Reading** (Houses 1 to 12: Lord, Occupants, Aspects, Chalit shifts, SAV bindus, and tangible life results).
- **Page 8:** **Career, Vocation, Authority & Business vs Job Deep-Dive** (10th House, D10, AmK, A10 Rajyapada, 6th/7th/10th SAV).
- **Page 9:** **Wealth, Asset Creation (D4), & Runa/Debt Risk Mitigation** (2nd/11th vs 6th/12th audit, D2 Hora, Indu/Arudha Lagna AL).
- **Page 10:** **Marriage, Relationships, Spouse Profile & Compatibility Blueprint** (7th House, D9, DK, UL, A7, Mangal Dosha & timing windows).
- **Page 11:** **Multi-Dasha Synthesis (Vimshottari Maha/Antar/Pratyantar + Yogini Dasha) & 5-Year Gochara Calendar** (Jupiter, Saturn, Rahu-Ketu ingresses, Moorthi Nirnaya & Double Transit windows).
- **Page 12:** **BPHS Ch. 84–97 Shastric Upaya Protocol + Preventive Health (D30/Maraka/Badhakesh) & Practical Life Roadmap**.

### Mode 3: Full Report (16–20 Pages Master Edition — `पृष्ठ X / N`)
When the user requests a **Full Report / Master Report**, include every section of the 12-Page Report PLUS:
- Dedicated pages for **each of the 12 Houses & 9 Grahas** with full Parashari + Jaimini (Rashi Drishti & Argala) commentary.
- Dedicated **Varga-by-Varga Deep-Dive** covering **D1, D2, D3, D4, D7, D9, D10, D12, D16, D20, D24, D27, D30, D60** (with birth-time sensitivity note on D60).
- Complete **9-Mahadasha Lifetime Timeline** + **5-Year Month-by-Month Pratyantardasha & Transit Calendar**.
- Full **Vedic Anka-Jyotish & Graha-Anka Cross-Verification Annex** (calling `scripts/numerology.py --chart-json chart.json`).

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
   - All calculations match `scripts/jyotish.py` JSON output 100%.
