---
name: jyotish-suite
description: Authentic Indian Vedic Astrology (Jyotish Shastra), Ganita Astronomy & Anka-Jyotish (Numerology) skill grounded in classical Sanskrit treatises (Brihat Parashara Hora Shastra, Surya Siddhanta, Brihat Jataka, Phaladeepika, Jaimini Sutras, Saravali, Jataka Parijata, Uttara Kalamrita, Muhurta Chintamani) and NASA JPL / Swiss Ephemeris precision. Generates 8-page Astro DevAish Hindi (Devanagari) PDF reports by default.
---
# Jyotish Suite — Classical Vedic Astrology (Jyotish Shastra), Ganita Astronomy & Anka-Jyotish

This skill provides end-to-end **Indian Vedic Astrology (Parashari + Jaimini + KP + Tajika)**, **Scientific Positional Astronomy (Ganita Skandha)**, and **Indian Anka-Jyotish / Numerology**, free of commercial marketing fluff and grounded strictly in authentic classical Sanskrit Shastras and high-precision ephemerides.

---

## 1. Default Report & Branding Standard (`Astro DevAish`)

Unless the user explicitly requests a different format or language:
1. **Brand Identity:** Always brand reports as **`Astro DevAish`** and embed the circular logo (`/home/antigravity/channels4_profile.jpg`) in the header banner and page footers.
2. **Default Language:** **Hindi (देवनागरी — Simple, clear, traditional & practical Hindi)** by default. Switch to **Hinglish** or **English** only when explicitly requested by the user.
3. **Default Length & Layout:** **8-Page A4 Portrait Detailed PDF Report** with `@page` page numbering (`पृष्ठ X / 8`) and zero text clipping.
4. **Mandatory Devanagari Font Embedding:** Always embed `/home/antigravity/.local/share/fonts/NotoSansDevanagari_0.woff2` as a base64 `@font-face` data URI inside the HTML before compiling via headless Chrome (`google-chrome --headless --disable-gpu --no-sandbox --no-pdf-header-footer`) so that Hindi text never renders as tofu boxes (`[][]`). Visually verify Page 1 with `pdftoppm -png` + `view_file`.
5. **No Marketing or Meta Labels:** Keep predictions honest, direct, and scripturally accurate, but **NEVER** print labels like `(बिना शुगरकोटिंग)` or `(No-Sugarcoating)` anywhere in the title, header, footer, or body.

---

## 2. Scientific Ganita Skandha (Positional Astronomy) + Vedic Siddhanta Weightage

Vedic Jyotish is divided into **Ganita Skandha** (mathematical astronomy) and **Phalita Skandha** (predictive astrology). Use high-precision modern planetary mechanics for *where* the planets are, and classical Indian Shastras for *what* they mean:

### A. Ephemeris & Coordinate Precision (Scientific Layer)
- **Ephemeris Engine:** Swiss Ephemeris (`pyswisseph`, based on NASA JPL DE431) computing true geocentric ecliptic longitudes ($\lambda$), latitudes ($\beta$), daily angular velocity ($\dot{\lambda}$ in deg/day), Right Ascension / Declination ($\alpha, \delta$), and topocentric Altitude/Azimuth.
- **Ayanamsa (Precession of Equinoxes):**
  - Default: **Chitrapaksha / Lahiri Ayanamsa** (`SE_SIDM_LAHIRI`, anchoring Spica / *Chitra* at $180^\circ$ / $0^\circ$ Libra, aligned with the Indian Rashtriya Panchanga and *Surya Siddhanta* tradition).
  - Also support **True Chitrapaksha**, **Raman**, and **KP (Krishnamurti)** when requested.
- **Sunrise & Vedic Weekday (*Savana Dina*):**
  - Compute true local apparent sunrise (upper limb / center of Sun disk at local horizon with atmospheric refraction) at the birth coordinates.
  - **Vedic Vara Rule (*Surya Siddhanta*):** A Vedic weekday (*Vara*) begins at local **sunrise**, not midnight (`00:00`). Any birth between `00:00` and local sunrise belongs to the **previous civil day's Vedic Vara and Hora sequence**.
- **Planetary Motion States (*Gati* — *Surya Siddhanta* & *BPHS*):**
  -Classify planetary speed ($\dot{\lambda}$) beyond simple retrograde (`Vakri`) vs direct (`Margi`):
    1. **Vakra (Retrograde):** $\dot{\lambda} < 0$ (high Cheshta Bala for outer/inner planets; internalized, repetitive, or unconventional karmic expression).
    2. **Anuvakra:** Entering previous sign while retrograde.
    3. **Vikala / Stambhana (Stationary):** $|\dot{\lambda}| \approx 0$ near station — intense, concentrated focal point in the chart.
    4. **Manda / Mandatara (Slow):** Below mean daily motion.
    5. **Sama (Mean Speed):** Near average angular velocity.
    6. **Sheeghra / Atichara (Accelerated / Very Fast):** Exceeding mean daily speed (sometimes entering the next sign early).
- **Combustion (*Moudhya / Asta* — *Surya Siddhanta* Ch. 9):**
  - Exact classical longitudinal orb from the Sun:
    - **Moon:** $12^\circ$
    - **Mars:** $17^\circ$
    - **Mercury:** $14^\circ$ (Direct) / $12^\circ$ (Retrograde)
    - **Jupiter:** $11^\circ$
    - **Venus:** $10^\circ$ (Direct) / $8^\circ$ (Retrograde)
    - **Saturn:** $15^\circ$
- **Planetary War (*Graha Yuddha* — *Surya Siddhanta* & *Brihat Samhita*):**
  - Occurs when two true planets (**Mars, Mercury, Jupiter, Venus, Saturn** — excluding Sun, Moon, Rahu, Ketu) are within **$1^\circ$ ecliptic longitude**.
  - The planet with the **northern ecliptic latitude ($\beta$)** or brighter visual magnitude (*bimba*) is the victor (*Jayee*); the defeated planet (*Parajita*) loses strength unless supported by dignity/benefic aspect.
- **Sensitive Boundaries (*Rashi Sandhi* & *Gandanta*):**
  - **Rashi Sandhi:** First $1^\circ$ ($0^\circ–1^\circ$) or last $1^\circ$ ($29^\circ–30^\circ$) of any sign.
  - **Gandanta (Water-to-Fire Nakshatra & Rashi Junctions):** Last $3^\circ 20'$ (especially $0^\circ 48'$) of **Revati (Pisces), Ashlesha (Cancer), Jyeshtha (Scorpio)** and first $3^\circ 20'$ (especially $0^\circ 48'$) of **Ashwini (Aries), Magha (Leo), Mula (Sagittarius)**.

---

## 3. Authentic Classical Vedic Astrology (Phalita Skandha — Primary Weightage)

Prioritize authentic rules from **Brihat Parashara Hora Shastra (BPHS)**, **Brihat Jataka (Varahamihira)**, **Phaladeepika (Mantreswara)**, **Jaimini Sutras**, **Saravali (Kalyana Varma)**, **Jataka Parijata (Vaidyanatha Dikshita)**, **Uttara Kalamrita (Kalidasa)**, and **Muhurta Chintamani (Daivajna Ramadayalu)**:

### A. Dual House Assessment: Rashi (Whole Sign) + Bhava Chalit (Sripati)
- **Rashi Tulya Bhava (Whole Sign):** Primary Parashari foundation for sign-based lordships, aspects, yogas, and Ashtakavarga.
- **Sripati Bhava Chalit (Porphyry / Midheaven-trisected Cusps):** Check whether any planet shifts into an adjacent Bhava in the Chalit chart (*Bhava Sandhi*), modifying how its Dasha delivers tangible house results (*Phaladeepika*).

### B. Shadbala, Vimshopaka Bala & Avasthas (BPHS Ch. 27 & Ch. 45)
1. **Six-Fold Planetary Strength (*Shadbala* in Virupas / Rupas):**
   - **Sthana Bala:** Uchcha (Exaltation) + Saptavargaja (D1, D2, D3, D7, D9, D12, D30) + Ojhayugma + Kendradi + Drekkana.
   - **Dig Bala (Directional Strength):** Jupiter & Mercury in **1st (East)**, Sun & Mars in **10th (South)**, Saturn in **7th (West)**, Moon & Venus in **4th (North)**.
   - **Kala Bala:** Nathonnatha (Day/Night), Paksha (Shukla/Krishna), Tribhaga, Varsha-Masa-Dina-Hora, Ayana Bala.
   - **Cheshta Bala:** Motional/retrograde strength (for Sun, Ayana Bala; for Moon, Paksha Bala).
   - **Naisargika Bala:** Fixed natural luminosity hierarchy ($\text{Sun } 60 > \text{Moon } 51.43 > \text{Venus } 42.85 > \text{Jupiter } 34.28 > \text{Mercury } 25.71 > \text{Mars } 17.14 > \text{Saturn } 8.57$ Virupas).
   - **Drik Bala:** Benefic minus malefic aspectual strength.
   - **Minimum Required Rupas (BPHS):** Mercury `7.0` (`420` Virupas), Sun `6.5` (`390`), Jupiter `6.5` (`390`), Moon `6.0` (`360`), Venus `5.5` (`330`), Mars `5.0` (`300`), Saturn `5.0` (`300`).
2. **Ishta Phala & Kashta Phala (BPHS):**
   - Derived from $\text{Uchcha Bala}$ and $\text{Cheshta Bala}$: $\text{Ishta} = \sqrt{\text{Uchcha} \times \text{Cheshta}}$; $\text{Kashta} = \sqrt{(60 - \text{Uchcha}) \times (60 - \text{Cheshta})}$. Explains *why* a planet's Mahadasha feels smooth ($\text{Ishta} > \text{Kashta}$) or effort-heavy ($\text{Kashta} > \text{Ishta}$).
3. **Planetary Avasthas (BPHS Ch. 45):**
   - **Baladi (5 Degree-Based States):** Odd signs: $0^\circ–6^\circ$ *Bala* (Infant, 25%), $6^\circ–12^\circ$ *Kumara* (Youth, 50%), $12^\circ–18^\circ$ *Yuva* (Adult, 100%), $18^\circ–24^\circ$ *Vriddha* (Old, low), $24^\circ–30^\circ$ *Mrita* (Dormant). Reversed in even signs.
   - **Jagradadi (3 Dignity States):** *Jagrat* (Awake — own/exalted, 100%), *Swapna* (Dreaming — friendly/neutral, 50%), *Sushupti* (Sleeping — enemy/debilitated, minimal).
   - **Lajjitadi (6 Psychological/Relational States):** *Lajjita*, *Garvita*, *Kshudhita*, *Trishita*, *Mudita*, *Kshobhita* — crucial for 5th/7th/10th house psychological realism.

### C. Functional Nature by Lagna, Badhaka, Maraka & Kendradhipati Dosha (BPHS Ch. 34 & Uttara Kalamrita)
- **Functional Benefics (*Shubha*), Malefics (*Papa*), & Yogakaraka:** Strictly determined by **Trikona ($1, 5, 9$)** vs **Trishadaya ($3, 6, 11$)** and **Dusthana ($6, 8, 12$)** lordships for each of the 12 Lagnas.
- **Kendradhipati Dosha:** Natural benefics (**Jupiter, Venus, Mercury**) owning angular houses ($4, 7, 10$) lose their natural beneficence unless they simultaneously own a Trikona or occupy own/exalted sign.
- **Badhaka Sthana & Badhakesh (Prasna Marga & Jataka Parijata):**
  - **Chara (Movable) Signs ($1, 4, 7, 10$):** **11th house** & its lord.
  - **Sthira (Fixed) Signs ($2, 5, 8, 11$):** **9th house** & its lord.
  - **Dwiswabhava (Dual) Signs ($3, 6, 9, 12$):** **7th house** & its lord.
- **Maraka Sthana ($2\text{nd}$ & $7\text{th}$ Lords/Occupants):** Crucial for health/vitality cautions during their Dasha/Bhukti.

### D. Authentic Mangal Dosha (Kuja Dosha) Classification (BPHS & Phaladeepika)
Never collapse severe Lagna Manglik placements into "Non-Manglik" due to generic internet cancellation lists:
1. **Saptama Manglik (7th House Mars from Lagna) & Ashtama Manglik (8th House Mars from Lagna):**
   - These are the two primary, severe Parashari Manglik placements affecting partnership harmony ($7\text{th}$) and *Mangalya / longevity / family peace* ($8\text{th}$).
   - Benefic aspect (Jupiter) or dignity (own/exalted sign) **mitigates harshness** (*intensity reduction*), but **NEVER cancels the Manglik status to Non-Manglik** (`present: True`). Always advise matching with a Manglik partner or performing proper Shastric Kumbha/Ark Vivaha / Gun-D9 matching.
2. **Lagna Manglik in $1\text{st}, 2\text{nd}$ (South/BPHS), $4\text{th}, 12\text{th}$ Houses:**
   - Moderate-to-strong Lagna Manglik (`present: True`), graded by house and dignity.
3. **Moon-Chart-Only (*Chandra-Manglik*) / Venus-Only Placements:**
   - If Mars is **NOT** in $\{1, 2, 4, 7, 8, 12\}$ from **Lagna**:
     - If Mars is conjoined with Jupiter / Lagna Lord in a auspicious trine (e.g., 9th house) and only falls in a Manglik house from Moon, classify clearly as **Non-Manglik from Lagna (`अमांगलिक`)** or **Mild Chandra-Manglik (Moon-chart only)** — never equate it with 7th/8th-house Lagna Manglik.

### E. Shodashavarga (Divisional Charts D1–D60) & Special Degrees
- Compute and cross-verify all 13–16 Parashariargas: **D1 (Rashi), D2 (Hora), D3 (Drekkana), D4 (Chaturthamsa), D7 (Saptamsa), D9 (Navamsa), D10 (Dasamsa), D12 (Dwadasamsa), D16 (Shodasamsa), D20 (Vimsamsa), D24 (Chaturvimsamsa), D27 (Bhamsha), D30 (Trimsamsa), D60 (Shashtyamsa)**.
- **Vargottama:** Planet in the same sign in **D1 and D9** (grants strength equivalent to own sign).
- **Pushkara Navamsa ($24$ auspicious $3^\circ 20'$ zones) & Pushkara Bhaga ($12$ exact degrees):** Gives regenerative grace and protection even if a planet is otherwise challenged.

### F. Jaimini Sutras System (Maharishi Jaimini & BPHS Ch. 31–33)
- **7 Chara Karakas (by degree in sign, excluding Rahu/Ketu):**
  - **AK (Atmakaraka)**, **AmK (Amatyakaraka)**, **BK (Bhratrukaraka)**, **MK (Matrukaraka)**, **PK (Putrakaraka)**, **GK (Gnatikaraka)**, **DK (Darakaraka)**.
- **Karakamsha & Swamsha (AK in D9 mapped to D1 & D9):**
  - $10\text{th}$ from Karakamsha for vocation; $12\text{th}$ from Karakamsha for *Ishta Devata* / spiritual liberation.
- **Arudha Padas (with Classical 1st/7th -> 10th/4th Exception):**
  - **AL (Arudha Lagna — A1)** for material perception/status.
  - **UL (Upapada Lagna — A12)** & $2\text{nd}$ from UL for marriage manifestation and sustenance.
  - **A7 (Darapada)** for business/partner interactions & **A10 (Rajyapada)** for workplace authority.
- **Rashi Drishti (Jaimini Sign Aspects):**
  - Chara signs aspect all Sthira signs except adjacent; Sthira signs aspect all Chara signs except adjacent; Dwiswabhava signs aspect each other.
- **Argala (Planetary Intervention):** Primary Argalas ($2\text{nd}, 4\text{th}, 11\text{th}$, and $5\text{th}$ secondary) vs Virodhargala obstructions ($12\text{th}, 10\text{th}, 3\text{rd}, 9\text{th}$).

### G. Ashtakavarga (BPHS Ch. 66–72 & Phaladeepika Ch. 23)
- **Bhinna Ashtakavarga (BAV, $0–8$ bindus)** for Sun, Moon, Mars, Mercury, Jupiter, Venus, Saturn + **Sarvashtakavarga (SAV, total $337$ bindus)**.
- **Kakshya Transit Timing ($3^\circ 45'$ subdivisions):** Each sign is divided into 8 Kakshyas (Saturn, Jupiter, Mars, Sun, Venus, Mercury, Moon, Lagna) to time exact sub-periods within a transit.

### H. Multi-Layered Dasha & Gochara (Transit) Synthesis
- **Vimshottari Dasha ($120\text{ years}$):** Maha $\rightarrow$ Antar $\rightarrow$ Pratyantar from exact Moon longitude in Nakshatra.
- **Conditional Classical Dashas (BPHS):** Note **Yogini Dasha ($36\text{ years}$)** or **Jaimini Chara Dasha** as cross-check when relevant.
- **Gochara (Transits):**
  - **Double Transit Principle (Jupiter + Saturn):** Major life milestones (marriage, promotion, child, relocation) occur when transiting Jupiter and Saturn both aspect or occupy the relevant house/lord ($1/7$ for marriage, $10/10\text{L}$ for career, $5/5\text{L}$ for progeny).
  - **Vedha (Transit Obstruction — Phaladeepika):** Check whether a favorable transit from Moon is blocked by a planet in its Vedha point.
  - **Sade Sati ($12\text{th}, 1\text{st}, 2\text{nd}$ from Moon), Kantaka/Dhaiya ($4\text{th}$ from Moon), & Ashtama Shani ($8\text{th}$ from Moon)** + **Moorthi Nirnaya** (*Swarna/Gold, Rajata/Silver, Tamra/Copper, Loha/Iron* based on Moon's Rashi at Saturn's ingress) + **BAV/SAV cushion**.

---

## 4. Authentic Indian Anka-Jyotish (Vedic Numerology) vs Imported Systems

Distinguish authentic Indian numerical/phonetic traditions from imported Western/Chinese systems while providing all tools transparently:
1. **Navagraha Graha-Anka Mapping (Indian Anka-Jyotish):**
   - $1 = \text{Surya (Sun)}$, $2 = \text{Chandra (Moon)}$, $3 = \text{Guru (Jupiter)}$, $4 = \text{Rahu}$, $5 = \text{Budha (Mercury)}$, $6 = \text{Shukra (Venus)}$, $7 = \text{Ketu}$, $8 = \text{Shani (Saturn)}$, $9 = \text{Mangala (Mars)}$.
   - **Mulank (Janmank / Psychic Number):** Reduced birth day ($1–9$) + compound number nuance.
   - **Bhagyank (Destiny / Life Path Number):** 3-cycle reduction ($\text{Month} + \text{Day} + \text{Year}$) preserving Master Numbers ($11, 22, 33$) and Karmic Debt indicators ($13/4, 14/5, 16/7, 19/1$).
   - **Graha-Anka Synergy with Natal Chart:** Always cross-verify Mulank and Bhagyank rulers against their **actual dignity, house, and Shadbala/SAV in the Vedic D1/D9 birth chart** (e.g., Mulank $8$ ruled by Saturn acts completely differently if natal Saturn is exalted in Kendra vs debilitated in 12th).
2. **Avakahada Chakra & Svara Shastra (Authentic Vedic Name Sound):**
   - Every Nakshatra Pada has a classical Sanskrit seed syllable (*Nama Akshara*, e.g., `'रा'` for Chitra-3, `'ते'` for Vishakha-3, `'रो'` for Swati-3).
   - **Katapayadi Sankhya (Classical Indian Sanskrit Encoding):** Ancient Indian mathematical-phonetic system used by Vararuchi and Aryabhata mapping consonants to $0–9$ ($ka\text{-group } 1–9$, $ta\text{-group } 1–9$, $pa\text{-group } 1–5$, $ya\text{-group } 1–8$).
3. **Chaldean, Pythagorean & Lo Shu Grid (Modern Complementary Systems):**
   - Compute **Chaldean Name Number** (sound-vibration $1–8$, compound meanings), **Pythagorean Expression/Soul Urge/Personality**, **Lo Shu $3\times 3$ Grid** (8 Planes of Expression, missing & repeated number remedies), **Kua Number**, **4 Life Pinnacles & Challenges**, and **Personal Year / Personal Months**.

---

## 5. Standard 8-Page `Astro DevAish` Hindi Report Structure

Every 8-page PDF report must follow this clean, non-overlapping 8-page architecture:
- **Page 1:** `Astro DevAish` Branded Header Banner (with base64 logo) + 4 KPI Summary Cards + Honest Core Summary Box + **Section 1: Janma Panchanga, Sunrise Vedic Vara, Gati/Combustion & Rashi Sandhi / Gandanta**.
- **Page 2:** **Section 2: North Indian SVG Charts (D1 Lagna, D9 Navamsa, D10 Dasamsa)** + **Section 3: 9 Grahas + Lagna Table** (Rashi, House, Degrees, Nakshatra-Pada, KP Sub-Lord, Dignity/Retrograde/Combust/Pushkara tags, and clear Hindi analysis).
- **Page 3:** **Section 4: Mangal Dosha (Clear Traditional Status — Saptama/Ashtama/Chandra-Manglik/Non-Manglik)** + **Section 5: Classical Rajayogas, Functional Benefics/Malefics/Badhakesh, & Jaimini Karakas (AK, AmK, DK, Karakamsha, AL, UL)**.
- **Page 4:** **Section 6: All 13 Divisional Charts (D2–D60)** + **Section 7: Sarvashtakavarga (SAV = 337 Bindus) Visual Bar Chart & House-by-House Strength Analysis**.
- **Page 5:** **Section 8: Career, Technical vs Managerial Aptitude, Education, Business vs Job & Wealth/Savings Deep-Dive (D1 + D10 + SAV + AmK)**.
- **Page 6:** **Section 9: Marriage, Spouse Nature (7th House + D9 + DK + UL) & Compatibility Guidelines** + **Section 10: Vimshottari Mahadasha, Active Antardasha & Pratyantardasha Timeline**.
- **Page 7:** **Section 11: Transits (Gochara 2026–2029) — Sade Sati, Dhaiya/Ashtama Shani (with Moorthi Nirnaya & SAV) & Double Transit Activations** + **Section 12: Vedic Anka-Jyotish (Mulank, Bhagyank, Graha-Chart Synergy, Name Numbers, Kua & Personal Year/Months)**.
- **Page 8:** **Section 13: Lo Shu Grid ($3\times 3$), 8 Planes of Expression & 4 Life Pinnacles/Challenges** + **Section 14: Practical Shastric & Behavioral Action Plan** + Non-scientific self-reflection disclaimer.