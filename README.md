<div align="center">

# 🕉️ Astro DevAish Master Suite (`v2.0.0`)
### Authentic Classical Indian Vedic Astrology (Jyotish Shastra), Ganita Astronomy & 12-Pillar Vedic Anka-Jyotish (Numerology) AI Agent Skills + Global CLI

[![GitHub Stars](https://img.shields.io/github/stars/DevendraKhati/astro-devaish-suite?style=for-the-badge&logo=github&color=f59e0b)](https://github.com/DevendraKhati/astro-devaish-suite/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/DevendraKhati/astro-devaish-suite?style=for-the-badge&logo=github&color=3b82f6)](https://github.com/DevendraKhati/astro-devaish-suite/network/members)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-10b981?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Swiss Ephemeris](https://img.shields.io/badge/Ephemeris-Swiss%20Ephemeris%20(NASA%20JPL)-8b5cf6?style=for-the-badge)](https://www.astro.com/swisseph/)
[![AI Skills](https://img.shields.io/badge/AI%20Agent%20Skills-Gemini%20%7C%20Claude%20%7C%20Cursor-ec4899?style=for-the-badge)](https://github.com/DevendraKhati/astro-devaish-suite/tree/main/dist)

**If you use these Vedic Astrology & Numerology AI Skills or Python engines, please click the ⭐ Star button at the top-right of [DevendraKhati/astro-devaish-suite](https://github.com/DevendraKhati/astro-devaish-suite) to support the project and get future Shastric updates!**

[⭐ **Star This Repo on GitHub**](https://github.com/DevendraKhati/astro-devaish-suite) · [📦 **Download `.skill` Files**](./dist/) · [🚀 **1-Command Install**](#-step-2-install-in-1-command-gemini--claude--global-cli) · [📖 **12 Vedic Numerology Pillars**](#part-ii-all-12-pillars-of-vedic-anka-jyotish-vedic-numerology--numerologypy)

</div>

---

## ⭐ Step 1: Star This Repository First!

> **[👉 Click Here to Star `DevendraKhati/astro-devaish-suite` on GitHub](https://github.com/DevendraKhati/astro-devaish-suite)**
>
> Building an authentic, non-commercialized **Classical Sanskrit Shastra + NASA JPL Swiss Ephemeris + 12-Pillar Indian Anka-Jyotish** engine takes deep research across *Brihat Parashara Hora Shastra (BPHS)*, *Surya Siddhanta*, *Phaladeepika*, *Jaimini Sutras*, *Prasna Marga*, *Muhurta Chintamani*, and *Katapayadi Sankhya*.
>
> **Before installing or downloading the `.skill` packages, please drop a ⭐ Star on this repository!** Starring also bookmarks the repo in your GitHub account so you can easily pull updates in any cloud workspace or AI agent session.

---

## 🔍 Why `astro-devaish-suite`? (What Makes It Different)

Most astrology and numerology scripts or LLM prompts hallucinate planetary positions, mix up Western Lo Shu grids with Indian Vedic grids, or falsely cancel severe Manglik placements. **`astro-devaish-suite`** solves this with **deterministic Python engines** (`jyotish.py`, `numerology.py`, `astro_devaish.py`) and **4 ready-to-use AI Agent Skills**:

| Skill Package (`.skill`) | Purpose & Best Use Case | Direct Download |
|---|---|---|
| **`astro-devaish-suite.skill`** | **Combined Master Skill:** Full Parashari + Jaimini + KP + 337 SAV + All 12 Vedic Numerology Pillars + **Graha-Anka Birth Chart Cross-Verification** + Unified 3-Clock Timing. | [`dist/astro-devaish-suite.skill`](./dist/astro-devaish-suite.skill) |
| **`vedic-jyotish.skill`** | **Pure Classical Vedic Astrology & Ganita Astronomy:** D1–D60 Shodashavarga, Sunrise Vedic Vara, Sripati Bhava Chalit, Shadbala, Ishta/Kashta, 3-Tier Avasthas, Strict Parashari Mangal Dosha, 337 SAV/BAV, Jaimini Karakas/Arudhas & BPHS Ch. 84–97 Sattvika Upayas. | [`dist/vedic-jyotish.skill`](./dist/vedic-jyotish.skill) |
| **`vedic-numerology.skill`** | **Authentic Indian Vedic Anka-Jyotish & Comparative Numerology:** Century-Free Vedic Surya Grid (`3-1-9 / 6-7-5 / 2-8-4`), 37 Vedic Grid Yogas, 81 Driver–Conductor Combinations & Bridge Number, Age-35 Rule, 45-Year Vedic Dasha + Weekday Varshaphal, 10–52 Chaldean Name Audit, Katapayadi & Svara Shastra. | [`dist/vedic-numerology.skill`](./dist/vedic-numerology.skill) |
| **`jyotish-suite.skill`** | **Drop-in Upgraded Suite:** Backward-compatible `jyotish-suite` skill upgraded with all `v2.0` Astro DevAish engines. | [`dist/jyotish-suite.skill`](./dist/jyotish-suite.skill) |

---

## 🚀 Step 2: Install in 1 Command (Gemini / Claude / Global CLI)

### Option A: One-Line Terminal / Agent Workspace Installer
After **[starring the repository](https://github.com/DevendraKhati/astro-devaish-suite)**, run this single command in **Gemini Task Mode**, **Claude Code**, or **any Linux / macOS / WSL terminal**:

```bash
git clone https://github.com/DevendraKhati/astro-devaish-suite.git && cd astro-devaish-suite && bash install_astro_devaish.sh
```

*(Or just paste this prompt to your AI agent: **"First star or open https://github.com/DevendraKhati/astro-devaish-suite, clone it, and run `bash install_astro_devaish.sh` to install the skills and global CLI."**)*

**What `install_astro_devaish.sh` sets up automatically:**
1. Installs all 4 skills (`astro-devaish-suite`, `vedic-jyotish`, `vedic-numerology`, `jyotish-suite`) into **`~/.gemini/skills/`** and **`~/.claude/skills/`**.
2. Installs `pyswisseph` and registers the global CLI commands (`astro-devaish`, `vedic-jyotish`, `vedic-numerology`, `jyotish`, `numerology`) onto your system `PATH` (`~/.local/bin`) so you can run them from **any directory**.

### Option B: Upload `.skill` Files Directly in Gemini (Task Settings / Customizations)
1. Star the repo and open the **[`dist/`](./dist/)** folder.
2. Download [`astro-devaish-suite.skill`](./dist/astro-devaish-suite.skill), [`vedic-jyotish.skill`](./dist/vedic-jyotish.skill), and [`vedic-numerology.skill`](./dist/vedic-numerology.skill).
3. In Gemini, open **Task settings / Customizations $\rightarrow$ Skills** (or attach the `.skill` file in **Task** mode) to import it directly into your account.

### Option C: Use in Gemini Chat Mode (`💎 Gems`)
1. On `gemini.google.com`, open the left menu $\rightarrow$ click **`💎 Gems`** $\rightarrow$ **`+ New Gem`**.
2. Name it **`Astro DevAish`**.
3. Paste the contents of [`skills/astro-devaish-suite/SKILL.md`](./skills/astro-devaish-suite/SKILL.md) into **Instructions**.
4. Upload [`jyotish.py`](./jyotish.py) and [`numerology.py`](./numerology.py) into **Knowledge** files and click **Save**.

---

## 💻 Global CLI Usage (Run from Any Directory)

### 1. Unified Master CLI (`astro-devaish`)
Computes the complete Vedic Natal Chart, true local apparent sunrise, active Vimshottari Mahadasha/Antardasha/Pratyantardasha, 4-year Gochara transits, all 12 Vedic Anka-Jyotish pillars, and automatic **Graha-Anka Natal Chart Cross-Verification** in a single command:

```bash
astro-devaish \
  --name "Chandan Singh Bisht" \
  --dob 1995-08-26 \
  --tob 22:35 \
  --lat 29.2183 \
  --lon 79.5130 \
  --place "Haldwani" \
  --gender male > master.json
```

### 2. Classical Vedic Jyotish CLI (`vedic-jyotish` / `jyotish`)

```bash
# Full Natal Chart (Panchanga, Sunrise Savana Vara, D1-D60, Sripati Bhava Chalit, Shadbala, Avasthas, Jaimini, 337 SAV/BAV, Yogas, Strict Mangal Dosha, Diagnostics & BPHS Upayas)
vedic-jyotish chart --name "Chandan Singh Bisht" --dob 1995-08-26 --tob 22:35 --lat 29.2183 --lon 79.5130 --place "Haldwani" > chart.json

# Active Vimshottari Maha / Antar / Pratyantar Dasha at any target date
vedic-jyotish dasha --dob 1995-08-26 --tob 22:35 --lat 29.2183 --lon 79.5130 --at 2026-11-25 > dasha.json

# Multi-Year Gochara Transits (Sade Sati, Kantaka Dhaiya, Ashtama Shani, Moorthi Nirnaya & Double Transit)
vedic-jyotish transit --dob 1995-08-26 --tob 22:35 --lat 29.2183 --lon 79.5130 --from 2026-01-01 --years 4 > transit.json

# 36-Point Ashtakoota Marriage Compatibility + Dual Mangal Dosha + Cross-Links
vedic-jyotish match --a bride.json --b groom.json > match.json
```

### 3. Vedic Anka-Jyotish CLI (`vedic-numerology` / `numerology`)

```bash
# Run all 12 Vedic Numerology Pillars (with optional --chart-json for Graha-Anka Birth Chart Cross-Verification)
vedic-numerology \
  --name "Chandan Singh Bisht" \
  --dob 1995-08-26 \
  --tob 22:35 \
  --sunrise 05:56 \
  --gender male \
  --chart-json chart.json > numerology.json
```

---

## 🏛️ Core Capabilities & Classical Shastric Doctrine

### Part I: Classical Vedic Jyotish (`vedic-jyotish` / `jyotish.py`)
Grounded in **Brihat Parashara Hora Shastra (BPHS)**, **Surya Siddhanta**, **Brihat Jataka**, **Phaladeepika**, **Jaimini Sutras**, **Saravali**, **Jataka Parijata**, **Uttara Kalamrita**, **Prasna Marga**, and **Muhurta Chintamani**:

1. **Ganita Skandha (*Surya Siddhanta* Positional Astronomy):**
   - Swiss Ephemeris (`pyswisseph`) with **Chitrapaksha / Lahiri Ayanamsa**.
   - **True Local Apparent Sunrise & Vedic Savana Vara:** Pre-sunrise births (`00:00` to local sunrise) are automatically assigned the previous civil day's Vedic Vara and Hora sequence.
   - **5-State Planetary Motion (*Gati*):** *Vakra* (Retrograde), *Vikala/Stambhana* (Stationary), *Manda* (Slow), *Sama* (Mean), *Sheeghra/Atichara* (Accelerated).
   - **Exact Combustion Orbs (*Asta / Moudhya* — *Surya Siddhanta* Ch. 9):** Moon $12^\circ$, Mars $17^\circ$, Mercury $14^\circ$ (Direct) / $12^\circ$ (Retrograde), Jupiter $11^\circ$, Venus $10^\circ$ (Direct) / $8^\circ$ (Retrograde), Saturn $15^\circ$.
   - **Planetary War (*Graha Yuddha*):** True planets within $1^\circ$ longitude resolved by northern ecliptic latitude ($\beta$).
   - **Rashi Sandhi & Gandanta:** Flags first/last $1^\circ$ sign boundaries and Water-to-Fire Gandanta junctions ($3^\circ 20'$ and core $0^\circ 48'$).
2. **Shodashavarga (16 Divisional Charts D1–D60) & Special Degrees:**
   - Computes **D1, D2, D3, D4, D7, D9, D10, D12, D16, D20, D24, D27, D30, D40, D45, D60**, plus **Vargottama**, **Pushkara Navamsa**, **Pushkara Bhaga**, and **KP Sub-Lords**.
3. **Dual House Assessment:**
   - **Whole Sign (Rashi Tulya Bhava)** + **Sripati Bhava Chalit (Porphyry midpoint cusps)** flagging any planet that shifts house in Bhava Chalit.
4. **Shadbala, Ishta/Kashta Phala & 3-Tier Avasthas (BPHS Ch. 27 & Ch. 45):**
   - 6-fold **Shadbala** in Virupas and Rupas benchmarked against BPHS minimum required Rupas (`shadbala_ratio`).
   - **Ishta Phala vs Kashta Phala** ($\sqrt{\text{Uchcha} \times \text{Cheshta}}$).
   - **Baladi** (*Bala, Kumara, Yuva, Vriddha, Mrita*), **Jagradadi** (*Jagrat, Swapna, Sushupti*), and **Lajjitadi** (*Garvita, Mudita, Lajjita, Kshobhita, Kshudhita, Trishita*) Avasthas.
5. **Strict Parashari Mangal Dosha (BPHS Ch. 80 & Phaladeepika):**
   - **7th House (*Saptama*) & 8th House (*Ashtama*) Lagna Mars:** Always classified as Severe Lagna Manglik (`present: True`); benefic aspect or dignity reduces harshness (`mitigations`) without falsely cancelling Manglik status to Non-Manglik.
   - **Moon-Chart-Only Mars:** When Mars is not in $\{1, 2, 4, 7, 8, 12\}$ from Lagna (e.g., 9th house Mars with Jupiter), clearly classified as **Non-Manglik from Lagna (`लग्न से अमांगलिक`) / Mild Chandra-Manglik**.
6. **Functional Nature, Badhakesh, Maraka, Jaimini System & 337 Sarvashtakavarga:**
   - Functional Benefics/Malefics/Yogakaraka, Kendradhipati Dosha, Badhaka House & Badhakesh (Chara $\rightarrow 11\text{th}$, Sthira $\rightarrow 9\text{th}$, Dwiswabhava $\rightarrow 7\text{th}$), and Maraka Lords ($2\text{nd}$ & $7\text{th}$).
   - **Jaimini 7 Chara Karakas (AK–DK)**, **Karakamsha**, and **Arudha Padas (AL, UL, A7, A10)** with classical 1st/7th $\rightarrow$ 10th/4th exception.
   - Exact **Bhinna Ashtakavarga (BAV)** for 7 planets + **Sarvashtakavarga (SAV = 337 Bindus)**.
7. **Life Diagnostics & Authentic BPHS Ch. 84–97 Sattvika Upayas:**
   - Career (Technical vs Managerial), Wealth vs Debt (*Runa Yoga* $6\text{H}/12\text{H}$ vs $2\text{H}/11\text{H}$ SAV & Lords), Marriage ($7\text{H} + \text{D9} + \text{DK} + \text{UL}$), and BPHS Sattvika Upayas (Avatara/Vedic Mantra, Dana/Seva, Aushadhi Snana, Behavioral Karma — zero commercial gemstone selling).

---

### Part II: All 12 Pillars of Vedic Anka-Jyotish (`vedic-numerology` / `numerology.py`)

| # | Vedic Anka-Jyotish Pillar | Implementation Detail |
|---|---|---|
| **1** | **Navagraha Graha-Anka & Compound Birth-Date Sub-Personalities (`1–31`)** | Maps $1=\text{Sun}, 2=\text{Moon}, 3=\text{Jupiter}, 4=\text{Rahu}, 5=\text{Mercury}, 6=\text{Venus}, 7=\text{Ketu}, 8=\text{Saturn}, 9=\text{Mars}$ and differentiates every birth date ($10–31$) by its internal planetary blend, Master Numbers ($11, 22, 33$), and Karmic Debts ($13, 14, 16, 19$). |
| **2** | **Sunrise Mulank Rule (*Surya Siddhanta Savana Dina*)** | Flags pre-sunrise births (`tob < sunrise`) and computes both **Vedic Savana Mulank** (previous day) and **Civil Mulank** (calendar date). |
| **3** | **Bhagyank (3-Cycle Reduction) & Age-35 Transition** | Tracks 3-cycle and digit-sum reductions and computes the exact calendar year (`birth_year + 35`) where Bhagyank (Conductor) takes $70\%$ command over Mulank (Driver). |
| **4** | **All 81 Driver–Conductor Combinations & Bridge Number** | Complete $9 \times 9 = 81$ (`M-B`) matrix with compatibility ratings out of 5.0 (and score out of 10), archetype titles, Hindi synthesis, and **Bridge Number** ($|M - B|$). |
| **5** | **Friendly, Neutral & Anti Numbers Matrix** | Computes individual and **Combined Intersection** (`combined_mutual_friendly_numbers`, `combined_neutral_numbers`, `combined_anti_avoid_numbers`). |
| **6** | **Century-Free Vedic Surya Grid (`3-1-9 / 6-7-5 / 2-8-4`)** | Excludes fixed century digits (`19`/`20`), populates day + month + last 2 year digits + Mulank + Bhagyank, and overlays active `MD` (45-Yr Mahadasha) and `AD` (Annual Dasha) numbers. |
| **7** | **37 Vedic Grid Yogas Catalog** | Evaluates 8 Primary 3-Number Planes (`3-1-9`, `6-7-5`, `2-8-4`, `3-6-2`, `1-7-8`, `9-5-4`, `3-7-4`, `9-7-2`), 4 Strategic Triads (`1-5-9`, `3-5-6`, `2-5-6`, `4-7-8`), and 25 Classical 2-Number Graha-Anka Yogas. |
| **8** | **45-Year Vedic Dasha + Weekday-Linked Annual Dasha** | 45-year cycle ($\text{Sun } 1\text{y} \dots \text{Mars } 9\text{y}$ starting from Mulank) with proportional Antardashas ($\frac{M \times A}{45}\text{y}$) + Weekday-Linked Varsha Dasha ($\text{Day} + \text{Month} + \text{Year}_2 + \text{Weekday Anka}$). |
| **9** | **First Name vs Full Name Audit (`10–52` Chaldean Compounds)** | Audits First Name and Full Name separately against the classical `10–52` Chaldean compound dictionary with non-destructive usage/signature guidance. |
| **10** | **Comparative Lo Shu Grid & Over-Repetition Diagnostics (`0x–4x+`)** | Evaluates the 8 Lo Shu Planes, Kua Number, and `0x` (Missing), `1x` (Balanced), `2x` (Strong), `3x` (Excessive), and `4x+` (Extreme) digit repetition remedies. |
| **11** | **Katapayadi Sankhya & Svara / Avakahada Phonetics** | Classical right-to-left Sanskrit consonant encoding ($\bmod 9$ Anka & $\bmod 12$ Rashi), opening vowel Pancha-Tatva (*Svara*), and Avakahada 108-Pada Nama-Akshara mapping. |
| **12** | **Pythagorean Core, 4 Pinnacles/Challenges & Graha-Anka Chart Synergy** | Expression, Soul Urge, Personality, 4 Life Pinnacles/Challenges, 12 Personal Months, and automatic D1/D9/SAV/Shadbala verification of Mulank & Bhagyank rulers (`--chart-json`). |

---

## 📄 Three `Astro DevAish` Hindi (Devanagari) PDF Report Modes

All skills generate `Astro DevAish` branded Hindi (Devanagari) A4 Portrait PDF reports with base64-embedded `NotoSansDevanagari_0.woff2` font and circular `Astro DevAish` logo:
1. **8-Page Report (Standard Default — `पृष्ठ X / 8`)**
2. **12-Page Report (Extended Deep-Dive — `पृष्ठ X / 12`)**
3. **Full Report (16–20 Pages Master Edition — `पृष्ठ X / N`)**

---

## 📂 Repository Structure

```text
astro-devaish-suite/
├── astro_devaish.py             # Unified Master CLI (Chart + Sunrise + Dasha + Transits + 12 Numerology Pillars + Cross-Verification)
├── jyotish.py                   # Classical Parashari, Jaimini, KP, 337 SAV/BAV, Shadbala, Avasthas, D1-D60 & Ganita Engine
├── numerology.py                # All 12 Vedic Anka-Jyotish Pillars (Century-Free Vedic Grid, 37 Yogas, 81 Pairs, 45-Yr Dasha, 10-52 Chaldean, Katapayadi)
├── vedastro_client.py           # Optional VedAstro REST API fallback client
├── pyproject.toml               # Global Python package & CLI entry points (astro-devaish, vedic-jyotish, vedic-numerology, jyotish, numerology)
├── install_astro_devaish.sh     # One-command portable installer for skills (~/.gemini/skills, ~/.claude/skills) & global PATH binaries
├── skills/                      # Full AI Agent Skill directories (SKILL.md + scripts/ + references/)
│   ├── astro-devaish-suite/     # Combined Master Skill (Vedic Jyotish + Vedic Numerology + Graha-Anka Cross-Verification)
│   ├── vedic-jyotish/           # Classical Vedic Astrology & Ganita Astronomy Skill
│   ├── vedic-numerology/        # Authentic Indian Vedic Anka-Jyotish & Comparative Numerology Skill
│   └── jyotish-suite/           # Upgraded Drop-in Original Jyotish Suite Skill
└── dist/                        # Ready-to-import .skill packages
    ├── astro-devaish-suite.skill
    ├── vedic-jyotish.skill
    ├── vedic-numerology.skill
    └── jyotish-suite.skill
```

---

## 🔎 Topics & Keywords (For Discoverability)

`vedic-astrology` · `jyotish` · `kundli` · `vedic-numerology` · `anka-jyotish` · `ai-agent-skills` · `gemini-skills` · `claude-skills` · `mcp-skills` · `swiss-ephemeris` · `pyswisseph` · `brihat-parashara-hora-shastra` · `jaimini-sutras` · `ashtakavarga` · `shadbala` · `shodashavarga` · `katapayadi` · `chaldean-numerology` · `loshu-grid` · `surya-siddhanta`

---

<div align="center">

### ⭐ Enjoying Astro DevAish Master Suite?
**Don't forget to [⭐ Star `DevendraKhati/astro-devaish-suite` on GitHub](https://github.com/DevendraKhati/astro-devaish-suite) and share it with fellow Jyotish & AI enthusiasts!**

</div>
