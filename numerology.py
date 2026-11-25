#!/usr/bin/env python3
"""Authentic Indian Vedic Anka-Jyotish & Comparative Numerology Engine (Astro DevAish Edition).

Implements all 12 Vedic Anka-Jyotish upgrades:
  1. Navagraha Graha-Anka Mapping (1=Surya..9=Mangala) & Compound Birth-Date Sub-Personalities (10-31)
  2. Sunrise Mulank Rule (Surya Siddhanta Savana Dina: pre-sunrise births flagged with Vedic vs Civil Mulank)
  3. Bhagyank (Conductor / Destiny) 3-cycle reduction + Master/Karmic Debt tags + Age-35 Transition Rule
  4. All 81 Driver-Conductor (Mulank-Bhagyank) Combinations & Bridge Number (|M - B|)
  5. Friendly, Neutral & Anti (Enemy) Numbers Table (Mulank, Bhagyank & Combined Intersection)
  6. Century-Free Vedic Surya Grid (3-1-9 / 6-7-5 / 2-8-4) without century digits + Dasha overlay
  7. 37 Vedic Anka-Jyotish Grid Yogas (8 Primary 3-Number Planes + 29 Classical Graha-Anka Yogas)
  8. 45-Year Vedic Mahadasha & Antardasha Cycle (Sun 1y..Mars 9y) + Weekday-Linked Annual Dasha (Varshaphal)
  9. First Name vs Full Name Audit with Complete 10-52 Chaldean Compound Dictionary
 10. Lo Shu Grid (4-9-2 / 3-5-7 / 8-1-6) with 1x/2x/3x/4x+ Over-Repetition Diagnostics & Remedies
 11. Katapayadi Sankhya (Sanskrit Phonetic Encoding) & Svara Shastra / Avakahada 108-Pada Nama-Akshara
 12. Pythagorean Core (Expression/Soul Urge/Personality), 4 Pinnacles/Challenges, Kua, Personal Years/Months
     + Optional Natal Chart Graha-Anka Cross-Verification (--chart-json)

Usage:
  python3 numerology.py --name "Chandan Singh Bisht" --dob 1995-08-26 [--tob 22:35] [--sunrise 05:56] [--gender male] [--chart-json chart.json]
"""
import argparse
import json
import math
from datetime import date, datetime, timedelta

# ---------------------------------------------------------------------------
# 1. NAVAGRAHA GRAHA-ANKA MAPPING & PLANETARY FRIENDSHIP TABLE
# ---------------------------------------------------------------------------
RULER = {
    1: "Sun",
    2: "Moon",
    3: "Jupiter",
    4: "Rahu",
    5: "Mercury",
    6: "Venus",
    7: "Ketu",
    8: "Saturn",
    9: "Mars",
}

RULER_HI = {
    1: "सूर्य (Surya)",
    2: "चंद्र (Chandra)",
    3: "गुरु / बृहस्पति (Guru)",
    4: "राहु (Rahu)",
    5: "बुध (Budha)",
    6: "शुक्र (Shukra)",
    7: "केतु (Ketu)",
    8: "शनि (Shani)",
    9: "मंगल (Mangala)",
}

GRAHA_PROFILE = {
    1: {
        "sanskrit": "Surya (सूर्य)",
        "tatva": "Agni (Fire)",
        "guna": "Sattva",
        "varna": "Kshatriya (Royal)",
        "direction": "East (पूर्व)",
        "archetype_en": "Sovereign Authority, Leadership, Initiative, Independent Will",
        "archetype_hi": "नेतृत्व, आत्मबल, स्वाभिमान, प्रशासनिक क्षमता और स्वतंत्र निर्णय",
    },
    2: {
        "sanskrit": "Chandra (चंद्र)",
        "tatva": "Jala (Water)",
        "guna": "Sattva",
        "varna": "Vaishya (Nurturing)",
        "direction": "North-West (वायव्य)",
        "archetype_en": "Emotional Intelligence, Adaptability, Empathy, Public Connection",
        "archetype_hi": "संवेदनशीलता, कल्पनाशीलता, जन-संपर्क, मातृत्व और मानसिक लचीलापन",
    },
    3: {
        "sanskrit": "Guru / Brihaspati (गुरु)",
        "tatva": "Akasha (Ether)",
        "guna": "Sattva",
        "varna": "Brahmana (Sage/Advisor)",
        "direction": "North-East (ईशान)",
        "archetype_en": "Dharma, Wisdom, Teaching, Expansion, Ethical Counsel",
        "archetype_hi": "ज्ञान, धर्म, शिक्षण, परामर्श, नैतिक अनुशासन और दूरदर्शिता",
    },
    4: {
        "sanskrit": "Rahu (राहु)",
        "tatva": "Vayu/Chhaya (Air/Shadow)",
        "guna": "Tamas",
        "varna": "Out-of-Box / Reformer",
        "direction": "South-West (नैऋत्य)",
        "archetype_en": "Unconventional Innovation, Systems Engineering, Disruption, Foreign Reach",
        "archetype_hi": "तकनीकी नवाचार, लीक से हटकर सोच, आकस्मिक परिवर्तन और व्यावहारिक तर्क",
    },
    5: {
        "sanskrit": "Budha (बुध)",
        "tatva": "Prithvi (Earth)",
        "guna": "Rajas",
        "varna": "Vaishya (Commerce/Intellect)",
        "direction": "North (उत्तर)",
        "archetype_en": "Analytical Intelligence, Commerce, Communication, Agility, Balance",
        "archetype_hi": "बुद्धि, व्यापार कौशल, वाक्पटुता, गणना और त्वरित अनुकूलन",
    },
    6: {
        "sanskrit": "Shukra (शुक्र)",
        "tatva": "Jala (Water)",
        "guna": "Rajas",
        "varna": "Brahmana (Art/Diplomacy)",
        "direction": "South-East (आग्नेय)",
        "archetype_en": "Harmony, Aesthetics, Prosperity, Diplomacy, Family Devotion",
        "archetype_hi": "सौंदर्य, कला, भौतिक सुख-सुविधा, कूटनीति और पारिवारिक सामंजस्य",
    },
    7: {
        "sanskrit": "Ketu (केतु)",
        "tatva": "Agni/Chhaya (Mystic Fire)",
        "guna": "Tamas/Moksha",
        "varna": "Tapasvi (Researcher/Seeker)",
        "direction": "North-East / Zenith",
        "archetype_en": "Deep Research, Intuition, Detachment, Root-Cause Diagnostics, Spirituality",
        "archetype_hi": "गहन शोध, अंतर्ज्ञान, आध्यात्मिकता, सूक्ष्म विश्लेषण और वैराग्य",
    },
    8: {
        "sanskrit": "Shani (शनि)",
        "tatva": "Vayu (Air)",
        "guna": "Tamas",
        "varna": "Sevaka / Nyayadhisha (Judge/Builder)",
        "direction": "West (पश्चिम)",
        "archetype_en": "Karmic Justice, Endurance, Long-Term Architecture, Discipline, Realism",
        "archetype_hi": "कर्मफल, न्याय, धैर्य, दीर्घकालिक संघर्ष से स्थायी सफलता और अनुशासन",
    },
    9: {
        "sanskrit": "Mangala (मंगल)",
        "tatva": "Agni (Fire)",
        "guna": "Tamas/Kshatra",
        "varna": "Kshatriya (Commander)",
        "direction": "South (दक्षिण)",
        "archetype_en": "Courage, Execution, Protection, High Energy, Decisive Action",
        "archetype_hi": "साहस, पराक्रम, त्वरित क्रियान्वयन, नेतृत्व और संकट में अडिग ऊर्जा",
    },
}

# Friendly, Neutral, and Anti (Enemy) Numbers in Vedic Anka-Jyotish
NUMBER_RELATIONS = {
    1: {"friendly": [1, 2, 3, 5, 9], "neutral": [4, 7], "anti": [6, 8]},
    2: {"friendly": [1, 2, 3, 5], "neutral": [6, 7, 9], "anti": [4, 8]},
    3: {"friendly": [1, 2, 3, 5, 9], "neutral": [4, 7, 8], "anti": [6]},
    4: {"friendly": [1, 5, 6, 7, 8], "neutral": [3], "anti": [2, 4, 9]},
    5: {"friendly": [1, 2, 3, 5, 6], "neutral": [4, 7, 8, 9], "anti": []},
    6: {"friendly": [4, 5, 6, 7, 8], "neutral": [2, 9], "anti": [1, 3]},
    7: {"friendly": [1, 2, 3, 4, 5, 6], "neutral": [7, 8, 9], "anti": []},
    8: {"friendly": [4, 5, 6, 7, 8], "neutral": [3], "anti": [1, 2, 9]},
    9: {"friendly": [1, 2, 3, 5, 9], "neutral": [6, 7], "anti": [4, 8]},
}

# ---------------------------------------------------------------------------
# 2. COMPOUND BIRTH-DATE SUB-PERSONALITIES (DAYS 1 TO 31)
# ---------------------------------------------------------------------------
BIRTH_DAY_SUBPERSONALITIES = {
    1: {"mulank": 1, "title": "Pure Solar Pioneer (शुद्ध सूर्य नेतृत्व)", "blend": "1 (Sun)", "note_hi": "स्वतंत्र इच्छाशक्ति, सीधा नेतृत्व और किसी के अधीन न झुकने वाला स्वभाव।", "note_en": "Direct, unmediated solar authority; pioneering independence and strong personal identity."},
    2: {"mulank": 2, "title": "Pure Lunar Mirror (शुद्ध चंद्र संवेदनशीलता)", "blend": "2 (Moon)", "note_hi": "कोमल हृदय, सहयोगी स्वभाव, भावनात्मक गहराई और कलात्मक अभिरुचि।", "note_en": "Gentle, cooperative, emotionally perceptive, needs harmony and supportive environment."},
    3: {"mulank": 3, "title": "Pure Brihaspati Counselor (शुद्ध गुरु ज्ञान)", "blend": "3 (Jupiter)", "note_hi": "स्वाभाविक शिक्षक, अनुशासित, ज्ञान-प्रिय और सिद्धांतवादी मार्गदर्शक।", "note_en": "Orthodox wisdom, ethical ambition, structured expansion, natural teacher and advisor."},
    4: {"mulank": 4, "title": "Pure Rahu Rebel-Builder (शुद्ध राहु सुधारक)", "blend": "4 (Rahu)", "note_hi": "व्यावहारिक, लीक से हटकर सोचने वाला, सिस्टम और तकनीक में दक्ष।", "note_en": "Unconventional builder, challenges status quo, practical problem-solver with sudden shifts."},
    5: {"mulank": 5, "title": "Pure Budha Strategist (शुद्ध बुध बुद्धि)", "blend": "5 (Mercury)", "note_hi": "तीव्र गणना, व्यापारिक समझ, संवाद कौशल और त्वरित निर्णय क्षमता।", "note_en": "Quick-witted communicator, versatile, commercial acumen and mental agility."},
    6: {"mulank": 6, "title": "Pure Shukra Harmonizer (शुद्ध शुक्र आकर्षण)", "blend": "6 (Venus)", "note_hi": "सौंदर्य-प्रिय, परिवार-केंद्रित, आकर्षक व्यक्तित्व और संसाधन-संपन्न।", "note_en": "Magnetism, aesthetic taste, relational warmth, caregiving and material comfort."},
    7: {"mulank": 7, "title": "Pure Ketu Seeker (शुद्ध केतु अन्वेषक)", "blend": "7 (Ketu)", "note_hi": "अंतर्मुखी शोधकर्ता, गहन अंतर्ज्ञान, आध्यात्मिक और सत्य का खोजी।", "note_en": "Introspective philosopher, strong intuition, analytical depth and detachment from superficiality."},
    8: {"mulank": 8, "title": "Pure Shani Architect (शुद्ध शनि कर्मयोगी)", "blend": "8 (Saturn)", "note_hi": "गंभीर, न्यायप्रिय, कठिन परिश्रम से स्थायी साम्राज्य खड़ा करने वाला।", "note_en": "Deep sense of duty, slow-burn endurance, institutional builder, tested early by responsibility."},
    9: {"mulank": 9, "title": "Pure Mangala Commander (शुद्ध मंगल सेनापति)", "blend": "9 (Mars)", "note_hi": "साहसी, स्पष्टवादी, संकट में आगे बढ़कर रक्षा करने वाला कर्मठ व्यक्तित्व।", "note_en": "Fearless action, protective discipline, humanitarian drive and high physical/mental stamina."},
    10: {"mulank": 1, "title": "Amplified Solar Wheel (1+0 -> 1: चक्रवर्ती सूर्य)", "blend": "1 (Sun) + 0 (Infinite Potential)", "note_hi": "1 की तुलना में अधिक लचीला और भाग्यशाली नेतृत्व; उतार-चढ़ाव के बाद उच्च पद।", "note_en": "Softer yet wider reach than Day 1; cyclic rise to prominence through self-reliance."},
    11: {"mulank": 2, "title": "Master Intuitive Dynamo (1+1 -> 2: मास्टर अंतर्ज्ञान)", "blend": "1 (Sun) + 1 (Sun) -> 2 (Moon) [Master 11]", "note_hi": "दो सूर्यों की ऊर्जा से बना चंद्रमा: तीव्र अंतर्ज्ञान, पर भीतर द्वंद्व या बेचैनी से बचना आवश्यक।", "note_en": "Master number 11: double Sun feeding Moon gives electric intuition, visionary insight, and high sensitivity."},
    12: {"mulank": 3, "title": "Solar-Lunar Guru (1+2 -> 3: सृजनात्मक गुरु)", "blend": "1 (Sun) + 2 (Moon) -> 3 (Jupiter)", "note_hi": "नेतृत्व (1) और संवेदना (2) के मेल से बना ज्ञान (3); दूसरों के लिए त्याग करने की प्रवृत्ति से संतुलन रखें।", "note_en": "Blends initiative (1) and empathy (2) into wisdom (3); must avoid sacrificing own goals for others' plans."},
    13: {"mulank": 4, "title": "Karmic Transformer (1+3 -> 4: कर्म-रूपांतरण राहु)", "blend": "1 (Sun) + 3 (Jupiter) -> 4 (Rahu) [Karmic 13/4]", "note_hi": "सूर्य और गुरु के अनुशासन से नियंत्रित राहु; कड़ी मेहनत और ढांचागत बदलाव से बड़ी सफलता।", "note_en": "Karmic 13/4: Sun+Jupiter discipline channels Rahu into methodical engineering and transformative rebuilding."},
    14: {"mulank": 5, "title": "Dynamic Reformer-Merchant (1+4 -> 5: गतिशील बुध)", "blend": "1 (Sun) + 4 (Rahu) -> 5 (Mercury) [Karmic 14/5]", "note_hi": "मीडिया, तकनीक, जन-संपर्क और व्यापार में तीव्र गति; जोखिम और आवेग पर नियंत्रण आवश्यक।", "note_en": "Karmic 14/5: High-speed adaptability in tech, media, and trade; thrives through moderation and grounding."},
    15: {"mulank": 6, "title": "Alchemical Magnet (1+5 -> 6: वाक्-सिद्ध शुक्र)", "blend": "1 (Sun) + 5 (Mercury) -> 6 (Venus)", "note_hi": "सूर्य के तेज और बुध की बुद्धि से युक्त शुक्र; वाणी, कला, प्रबंधन और धन-आकर्षण में अत्यंत शुभ।", "note_en": "Sun+Mercury producing Venus: persuasive charisma, financial resourcefulness, and artistic/executive talent."},
    16: {"mulank": 7, "title": "Awakened Mystic Analyst (1+6 -> 7: आत्म-जागृति केतु)", "blend": "1 (Sun) + 6 (Venus) -> 7 (Ketu) [Karmic 16/7]", "note_hi": "अहं (1) और भोग (6) के पार जाकर गूढ़ सत्य (7) को समझने वाला; शोध व आध्यात्मिक अंतर्दृष्टि में श्रेष्ठ।", "note_en": "Karmic 16/7: Ego (1) and attachment (6) refined into deep spiritual and technical insight (7)."},
    17: {"mulank": 8, "title": "Mystic Star of Saturn (1+7 -> 8: आध्यात्मिक-राजयोग शनि)", "blend": "1 (Sun) + 7 (Ketu) -> 8 (Saturn)", "note_hi": "8 के समूह में सबसे सौम्य व अंतर्ज्ञानी; प्रारंभिक संघर्ष के बाद स्थायी नाम और उच्च अधिकार।", "note_en": "Most spiritually protected 8: Sun (1) + Ketu (7) give integrity, research depth, and lasting legacy."},
    18: {"mulank": 9, "title": "Dharma-Sangharsha Warrior (1+8 -> 9: संघर्ष-विजयी मंगल)", "blend": "1 (Sun) + 8 (Saturn) -> 9 (Mars)", "note_hi": "सूर्य (1) और शनि (8) के घर्षण से निकला मंगल (9); व्यवस्थागत चुनौतियों को जीतकर नेतृत्व स्थापित करता है।", "note_en": "Sun (1) + Saturn (8) forging Mars (9): forged through institutional friction, excels in law, defense, and reform."},
    19: {"mulank": 1, "title": "Sovereign Karmic Sun (1+9 -> 10 -> 1: राज-तेज सूर्य)", "blend": "1 (Sun) + 9 (Mars) -> 1 (Sun) [Karmic 19/1]", "note_hi": "सूर्य और मंगल का द्विगुणित अग्नि-तेज; उच्च आत्मनिर्भरता, सम्मान और साहसिक नेतृत्व।", "note_en": "Sun (1) + Mars (9) -> 1: commanding royal fire; achieves honour when power is used with humility."},
    20: {"mulank": 2, "title": "Awakened Counselor Moon (2+0 -> 2: भावनात्मक जागृति)", "blend": "2 (Moon) + 0", "note_hi": "शांत कूटनीति, परामर्श और सामूहिक कार्यों में सफलता; जीवन के मध्य भाग में विशेष उन्नति।", "note_en": "Peacemaker and intuitive coordinator; blossoms through collaborative and advisory roles."},
    21: {"mulank": 3, "title": "Crowned Jupiterian Achiever (2+1 -> 3: राजमुकुट गुरु)", "blend": "2 (Moon) + 1 (Sun) -> 3 (Jupiter)", "note_hi": "संवेदना (2) के बाद नेतृत्व (1) से बना गुरु (3); शिक्षा, प्रबंधन और सम्मान प्राप्ति के लिए अत्यंत शुभ।", "note_en": "Harmonious blend of adaptability (2) and ambition (1) culminating in Jupiterian honour (3)."},
    22: {"mulank": 4, "title": "Master Architect (2+2 -> 4: मास्टर निर्माता)", "blend": "2 (Moon) + 2 (Moon) -> 4 (Rahu) [Master 22]", "note_hi": "कल्पना (2+2) को ठोस धरातल (4) पर उतारने की क्षमता; भ्रम से बचकर व्यावहारिक रहने पर बड़ी उपलब्धि।", "note_en": "Master number 22: turns visionary intuition into large-scale practical structures when grounded."},
    23: {"mulank": 5, "title": "Royal Star of Mercury (2+3 -> 5: राज-कृपा बुध)", "blend": "2 (Moon) + 3 (Jupiter) -> 5 (Mercury)", "note_hi": "चंद्रमा और गुरु (गजकेसरी) के योग से बना बुध; उच्च अधिकारियों का सहयोग, तीक्ष्ण बुद्धि और व्यावसायिक उन्नति।", "note_en": "Moon (2) + Jupiter (3) -> Mercury (5): favored by mentors and authority; exceptional professional versatility."},
    24: {"mulank": 6, "title": "Fortunate Patron Venus (2+4 -> 6: सौभाग्यशाली शुक्र)", "blend": "2 (Moon) + 4 (Rahu) -> 6 (Venus)", "note_hi": "परिवार, कला, प्रशासन और आर्थिक उन्नति में वरिष्ठों व विपरीत लिंग से विशेष सहयोग।", "note_en": "Magnetic and diplomatic 6; attracts institutional backing, domestic prosperity, and executive grace."},
    25: {"mulank": 7, "title": "Experiential Sage Ketu (2+5 -> 7: अनुभव-सिद्ध केतु)", "blend": "2 (Moon) + 5 (Mercury) -> 7 (Ketu)", "note_hi": "चंद्रमा की संवेदना और बुध के तर्क से परिपक्व केतु; जीवन के प्रत्यक्ष अनुभवों से उच्च विवेक और विशेषज्ञता।", "note_en": "Moon (2) + Mercury (5) -> Ketu (7): discernment forged through lived experience; diagnostic and research mastery."},
    26: {"mulank": 8, "title": "Karmic Diplomat-Realist (2+6 -> 8: भावनात्मक-व्यावहारिक शनि)", "blend": "2 (Moon) + 6 (Venus) -> 8 (Saturn)", "note_hi": "भीतर से संवेदनशील (2) और परिवार-निष्ठ (6), पर बाहर से शनि (8) का कठोर कर्तव्य-भार। साझेदारी और धन लेन-देन में लिखित स्पष्टता रखें; 35 वर्ष बाद बड़ी स्थिरता।", "note_en": "Moon (2) + Venus (6) -> Saturn (8): inwardly caring and aesthetic, outwardly carrying heavy karmic duty; requires due diligence in partnerships and finances."},
    27: {"mulank": 9, "title": "Spiritual Sceptre Mars (2+7 -> 9: विवेकशील मंगल)", "blend": "2 (Moon) + 7 (Ketu) -> 9 (Mars)", "note_hi": "अंतर्ज्ञान (2+7) से संचालित मंगल (9); केवल बल नहीं बल्कि सूक्ष्म रणनीति और नैतिक साहस से विजय।", "note_en": "Moon (2) + Ketu (7) -> Mars (9): intuitive commander; combines perceptive wisdom with decisive courage."},
    28: {"mulank": 1, "title": "Tested Sovereign Sun (2+8 -> 10 -> 1: संघर्ष-तपा सूर्य)", "blend": "2 (Moon) + 8 (Saturn) -> 1 (Sun)", "note_hi": "चंद्रमा (2) और शनि (8) के अनुभवों से तपा हुआ सूर्य (1); दूसरों पर अंध-विश्वास न कर स्वयं के नियंत्रण से बड़ी सफलता।", "note_en": "Moon (2) + Saturn (8) -> Sun (1): resilient leader who learns to rely on self-governance and legal foresight."},
    29: {"mulank": 2, "title": "Intense Karmic Moon (2+9 -> 11 -> 2: ऊर्जावान चंद्र)", "blend": "2 (Moon) + 9 (Mars) -> 11 -> 2 (Moon)", "note_hi": "चंद्रमा (2) और मंगल (9) के लक्ष्मी-योग से युक्त पर भावनात्मक उतार-चढ़ाव वाला; स्पष्ट लक्ष्य रखने पर असाधारण सफलता।", "note_en": "Moon (2) + Mars (9) -> 11/2: passionate emotional drive; requires calm emotional anchoring to harness Master-11 intuition."},
    30: {"mulank": 3, "title": "Focused Sage Jupiter (3+0 -> 3: एकाग्र बृहस्पति)", "blend": "3 (Jupiter) + 0", "note_hi": "उच्च बौद्धिक क्षमता, शिक्षा, लेखन और नीति-निर्माण में स्वतंत्र पहचान।", "note_en": "High mental command and philosophical clarity; excels in advisory, academic, and strategic spheres."},
    31: {"mulank": 4, "title": "Self-Contained Specialist (3+1 -> 4: स्वावलंबी विशेषज्ञ राहु)", "blend": "3 (Jupiter) + 1 (Sun) -> 4 (Rahu)", "note_hi": "गुरु (3) के ज्ञान और सूर्य (1) के आत्मबल से युक्त राहु (4); अपनी अलग तकनीकी या प्रशासनिक राह खुद बनाने वाला।", "note_en": "Jupiter (3) + Sun (1) -> Rahu (4): independent technical/institutional specialist who builds enduring original systems."},
}

# ---------------------------------------------------------------------------
# 3. COMPLETE 81 DRIVER-CONDUCTOR (MULANK-BHAGYANK) COMBINATIONS
# ---------------------------------------------------------------------------
# Ratings (out of 5.0) and classical synergy notes for all 81 (M, B) pairs
DRIVER_CONDUCTOR_RATINGS = {
    (1, 1): (4.5, "Double Solar Command (द्विगुणित सूर्य तेज)", "उच्च नेतृत्व, स्वतंत्र पहचान और प्रशासनिक प्रभुत्व; अहं के टकराव से बचें।"),
    (1, 2): (4.0, "Raja-Rani Harmony (सूर्य-चंद्र संतुलन)", "नेतृत्व (1) और भावनात्मक समझ (2) का सुंदर मेल; जन-संपर्क व प्रबंधन में श्रेष्ठ।"),
    (1, 3): (4.5, "Surya-Guru Rajayoga (सूर्य-गुरु धर्म-राजयोग)", "अधिकार और ज्ञान का श्रेष्ठ संगम; शिक्षा, प्रशासन, नीति और परामर्श में उच्च सम्मान।"),
    (1, 4): (3.5, "Solar-Rahu Political/Tech Drive (सूर्य-राहु नवाचार योग)", "परंपरा और आधुनिक तकनीक का मेल; अचानक उतार-चढ़ाव के बाद विशिष्ट पहचान।"),
    (1, 5): (5.0, "Budhaditya Commercial Apex (बुधादित्य व्यापार-प्रशासन योग)", "नेतृत्व और तीव्र बुद्धि का सर्वोच्च योग; वित्त, व्यवसाय और उच्च पद में अत्यंत सफल।"),
    (1, 6): (3.0, "Royal-Aesthetic Tension (सूर्य-शुक्र स्वाभिमान-सौंदर्य द्वंद्व)", "अनुशासन (1) और विलासिता/कला (6) में संतुलन आवश्यक; रिश्तों में लचीलापन रखें।"),
    (1, 7): (4.0, "Solar-Mystic Research Authority (सूर्य-केतु शोध-नेतृत्व)", "बाहरी नेतृत्व और भीतरी अंतर्ज्ञान का संगम; तकनीकी शोध व गुप्त रणनीति में दक्ष।"),
    (1, 8): (2.0, "Surya-Shani Karmic Friction (सूर्य-शनि पिता-पुत्र संघर्ष योग)", "अधिकार (1) और कठोर कर्म-परीक्षा (8) का टकराव; धैर्य, पारदर्शिता और 35 वर्ष बाद बड़ी परिपक्वता।"),
    (1, 9): (5.0, "Surya-Mangal Commander Crest (सूर्य-मंगल सेनापति राजयोग)", "अदम्य साहस, प्रशासनिक शक्ति और निर्णायक क्रियान्वयन; रक्षा, प्रबंधन व उद्यम में शीर्ष।"),

    (2, 1): (4.5, "Lunar-Solar Ascent (चंद्र-सूर्य उन्नति योग)", "सहयोगी स्वभाव (2) से शुरू होकर मजबूत नेतृत्व (1) तक की यात्रा; वरिष्ठों का पूर्ण सहयोग।"),
    (2, 2): (3.0, "Double Lunar Sensitivity (द्विगुणित चंद्र संवेदना)", "उच्च कल्पनाशीलता और सहानुभूति, पर अति-सोच (overthinking) व मूड-स्विंग से बचाव आवश्यक।"),
    (2, 3): (4.0, "Gajakesari Wisdom Flow (चंद्र-गुरु गजकेसरी अंक-योग)", "संवेदना और ज्ञान का शुभ संगम; शिक्षण, परामर्श, वित्त और सामाजिक प्रतिष्ठा में उन्नति।"),
    (2, 4): (2.0, "Chandra-Rahu Grahan Tension (चंद्र-राहु मानसिक द्वंद्व योग)", "कल्पना (2) और भ्रम/अचानक बदलाव (4) का घर्षण; लिखित योजना और मानसिक ग्राउंडिंग अनिवार्य।"),
    (2, 5): (4.5, "Lunar-Mercurial Financial Grace (चंद्र-बुध वाणिज्य-चातुर्य योग)", "भावनात्मक समझ और व्यापारिक बुद्धि का श्रेष्ठ मेल; बैंकिंग, संचार व व्यापार में लाभ।"),
    (2, 6): (4.0, "Rasa-Saundarya Harmony (चंद्र-शुक्र कला-सौभाग्य योग)", "कला, आतिथ्य, परिवार और सौंदर्य के क्षेत्रों में सहज आकर्षण व सुख-समृद्धि।"),
    (2, 7): (3.5, "Mirrored Intuition (चंद्र-केतु अंतर्ज्ञान-शोध योग)", "तीव्र छठी इंद्री (6th sense) और सूक्ष्म विश्लेषण; भावनात्मक अलगाव के बजाय ध्यान व शोध में ऊर्जा लगाएं।"),
    (2, 8): (2.0, "Chandra-Shani Vish-Tapasya (चंद्र-शनि भावनात्मक-कर्म परीक्षा)", "कोमल मन (2) पर शनि (8) के कठोर यथार्थ का भार; भावनात्मक निर्णयों के बजाय अनुशासन से काम लें।"),
    (2, 9): (4.0, "Chandra-Mangal Lakshmi Drive (चंद्र-मंगल लक्ष्मी-साहस योग)", "संवेदना के साथ साहसिक कर्म; संपत्ति, प्रबंधन और सामाजिक कार्यों में प्रगति।"),

    (3, 1): (4.5, "Guru-Aditya Sovereign Counsel (गुरु-सूर्य राज-परामर्श योग)", "ज्ञान (3) से अधिकार (1) की प्राप्ति; उच्च प्रशासनिक, शैक्षणिक और नेतृत्व पदों में सफलता।"),
    (3, 2): (4.0, "Sage-Nurturer Balance (गुरु-चंद्र ज्ञान-करुणा योग)", "परामर्श, जन-कल्याण, शिक्षा और शांत नेतृत्व से स्थायी सम्मान।"),
    (3, 3): (4.0, "Double Brihaspati Orthodoxy (द्विगुणित गुरु विद्वत्ता)", "गहन ज्ञान, नैतिकता और शिक्षण क्षमता; व्यवहार में लचीलापन रखने से और बड़ी उन्नति।"),
    (3, 4): (3.0, "Guru-Rahu Chandal-Reform (गुरु-राहु परंपरा बनाम नवाचार)", "शास्त्रीय ज्ञान (3) को आधुनिक तकनीक (4) से जोड़ने पर विशेष सफलता; शॉर्टकट से बचें।"),
    (3, 5): (4.5, "Guru-Budha Saraswati-Vyapara (गुरु-बुध ज्ञान-वाणिज्य योग)", "गंभीर ज्ञान और व्यावहारिक संचार का उत्तम मेल; वित्त, कानून, आईटी व प्रबंधन में श्रेष्ठ।"),
    (3, 6): (2.5, "Deva-Daitya Guru Tension (गुरु-शुक्र सिद्धांत-भोग द्वंद्व)", "आदर्शवाद (3) और भौतिक आकर्षण (6) के बीच खिंचाव; वैवाहिक व वित्तीय संतुलन पर ध्यान दें।"),
    (3, 7): (4.5, "Guru-Ketu Moksha-Jnana Crest (गुरु-केतु उच्च शोध-प्रज्ञा योग)", "ज्ञान और अंतर्ज्ञान का सर्वोच्च संगम; गहन शोध, दर्शन, डेटा-साइंस और आध्यात्मिकता में शीर्ष।"),
    (3, 8): (3.5, "Dharma-Karma Judge (गुरु-शनि न्याय-व्यवस्था योग)", "नीति (3) और न्याय/परिश्रम (8) का गंभीर मेल; कानून, प्रशासन व दीर्घकालिक प्रोजेक्ट्स में स्थिरता।"),
    (3, 9): (5.0, "Guru-Mangal Dharma-Parakrama (गुरु-मंगल धर्म-पराक्रम राजयोग)", "ज्ञान और साहस का अजेय संगम; उच्च नेतृत्व, रणनीति और राष्ट्र/संस्थान निर्माण में सफलता।"),

    (4, 1): (4.0, "Rebel-to-Ruler Ascent (राहु-सूर्य व्यवस्था-निर्माण योग)", "लीक से हटकर तकनीकी/व्यावहारिक कौशल (4) जो आगे चलकर शीर्ष नेतृत्व (1) दिलाता है।"),
    (4, 2): (2.5, "Structure-Emotion Friction (राहु-चंद्र तर्क बनाम भावना)", "तर्कशील दिमाग (4) और संवेदनशील भाग्य (2); मानसिक चिंता छोड़कर नियमित दिनचर्या अपनाएं।"),
    (4, 3): (3.5, "Tech-Wisdom Integration (राहु-गुरु नवाचार-ज्ञान योग)", "आधुनिक कौशल (4) को नैतिक मार्गदर्शन (3) मिलने से करियर में स्थिर उन्नति।"),
    (4, 4): (2.5, "Double Rahu Disruption (द्विगुणित राहु अति-संघर्ष/नवाचार)", "अत्यधिक विद्रोही या आकस्मिक उतार-चढ़ाव; कठोर अनुशासन और पूर्ण पारदर्शिता से ही स्थिरता।"),
    (4, 5): (4.5, "Rahu-Budha Tech-Commerce Dynamo (राहु-बुध डिजिटल-व्यापार योग)", "तकनीक, कोडिंग, ट्रेडिंग, मीडिया और आधुनिक व्यवसाय में तीव्र सफलता।"),
    (4, 6): (4.5, "Rahu-Shukra Glamour & Wealth (राहु-शुक्र आधुनिक ऐश्वर्य योग)", "डिजाइन, मीडिया, विलासिता, सिनेमा और कॉर्पोरेट क्षेत्र में बड़ा भौतिक लाभ।"),
    (4, 7): (4.0, "Rahu-Ketu Axis Mastery (राहु-केतु गूढ़-तकनीकी सिद्धि)", "नेटवर्किंग (4) और डीप-रिसर्च (7) का अनूठा मेल; साइबर, ऑकल्ट व डायग्नोस्टिक्स में श्रेष्ठ।"),
    (4, 8): (2.0, "Rahu-Shani Shrapit-Engineering (राहु-शनि कठोर कर्म-संघर्ष योग)", "अत्यधिक परिश्रम और विलंब के बाद ही परिणाम; शॉर्टकट या क्रोध से बचें, तकनीकी/कानूनी अनुशासन रखें।"),
    (4, 9): (2.5, "Rahu-Mangal Angaraka Surge (राहु-मंगल आक्रामक-उद्यम योग)", "उच्च ऊर्जा और जोखिम लेने की प्रवृत्ति; जल्दबाजी व विवाद से बचकर ऊर्जा को इंजीनियरिंग/रक्षा में लगाएं।"),

    (5, 1): (5.0, "Mercurial-Solar Executive Crest (बुध-सूर्य राज-वाणिज्य योग)", "तीव्र बुद्धि (5) से शीर्ष अधिकार (1) की प्राप्ति; कॉर्पोरेट, प्रशासन व उद्यम में सर्वोच्च सफलता।"),
    (5, 2): (4.0, "Adaptive Diplomat (बुध-चंद्र संवाद-सौम्यता योग)", "व्यापारिक समझ और भावनात्मक जुड़ाव; जन-संपर्क, परामर्श व तरल धन प्रवाह में शुभ।"),
    (5, 3): (4.5, "Intellect-Wisdom Synergy (बुध-गुरु विद्वान-प्रबंधक योग)", "तर्क (5) और दूरदर्शिता (3) का संगम; शिक्षा, परामर्श, वित्त और नेतृत्व में निरंतर प्रगति।"),
    (5, 4): (4.0, "Agile Systems Architect (बुध-राहु स्मार्ट-टेक योग)", "पारंपरिक व्यापार को आधुनिक तकनीक से जोड़ने में माहिर।"),
    (5, 5): (4.5, "Double Mercury Velocity (द्विगुणित बुध तीव्र-बुद्धि योग)", "असाधारण मानसिक गति, बहुमुखी प्रतिभा और व्यापारिक सफलता; एक समय में एक लक्ष्य पर टिके रहें।"),
    (5, 6): (5.0, "Budha-Shukra Lakshmi-Kala Apex (बुध-शुक्र महालक्ष्मी-वाणिज्य योग)", "बुद्धि और सौभाग्य का अत्यंत शुभ संगम; धन, कला, कॉर्पोरेट और सुख-सुविधाओं में सहज उन्नति।"),
    (5, 7): (4.0, "Analytical Mystic (बुध-केतु डेटा-अंतर्ज्ञान योग)", "तर्क और अंतर्ज्ञान का मेल; अनुसंधान, लेखन, ऑडिट और विशेषज्ञता वाले क्षेत्रों में श्रेष्ठ।"),
    (5, 8): (3.5, "Pragmatic Institution Builder (बुध-शनि कॉर्पोरेट-संरचना योग)", "बुद्धि (5) और दीर्घकालिक धैर्य (8) का समन्वय; रियल-एस्टेट, वित्त व उद्योग में स्थायी लाभ।"),
    (5, 9): (4.0, "Tarka-Parakrama Strategist (बुध-मंगल रणनीतिक-साहस योग)", "तेज दिमाग और त्वरित एक्शन; प्रतिस्पर्धा, खेल, सर्जरी, इंजीनियरिंग व व्यापार में विजय।"),

    (6, 1): (3.5, "Diplomat-Leader Balance (शुक्र-सूर्य आकर्षण-अधिकार योग)", "कूटनीति (6) के माध्यम से नेतृत्व (1) तक पहुंच; रचनात्मक प्रबंधन में सफलता।"),
    (6, 2): (4.0, "Venus-Moon Harmony (शुक्र-चंद्र माधुर्य-सौभाग्य योग)", "पारिवारिक सुख, कलात्मकता, आतिथ्य और सामाजिक लोकप्रियता में शुभ।"),
    (6, 3): (3.0, "Aesthetic-Ethical Bridge (शुक्र-गुरु भौतिक-आध्यात्मिक संतुलन)", "भौतिक सुख (6) और नैतिक अनुशासन (3) दोनों का समन्वय करने पर सम्मानजनक प्रगति।"),
    (6, 4): (4.5, "Modern Media & Wealth Magnet (शुक्र-राहु आधुनिक-संपदा योग)", "क्रिएटिव टेक, ब्रांडिंग, फिल्म और आधुनिक व्यवसाय में तीव्र उन्नति।"),
    (6, 5): (5.0, "Shukra-Budha Prosperity Crest (शुक्र-बुध आकर्षण-व्यापार राजयोग)", "चुंबकीय व्यक्तित्व और तीक्ष्ण व्यापारिक समझ; वित्तीय समृद्धि व संबंधों में उत्कृष्ट।"),
    (6, 6): (4.0, "Double Venus Luxury & Charm (द्विगुणित शुक्र ऐश्वर्य योग)", "उच्च कलात्मकता, प्रेम और भौतिक सुख; अति-भोग या आलस्य से बचकर अनुशासन बनाए रखें।"),
    (6, 7): (4.0, "Refined Spiritual Artist (शुक्र-केतु सूक्ष्म-कला योग)", "सौंदर्य बोध और गहन अंतर्ज्ञान; हीलिंग, डिजाइन, दर्शन और सूक्ष्म कलाओं में विशिष्ट।"),
    (6, 8): (4.0, "Shukra-Shani Kala-Karma Alliance (शुक्र-शनि मित्र-संपदा योग)", "शुक्र और शनि की नैसर्गिक मित्रता; धैर्यपूर्ण परिश्रम से बड़ी संपत्ति और स्थायी वैभव।"),
    (6, 9): (3.5, "Passion & Action Fire-Water (शुक्र-मंगल आकर्षण-ऊर्जा योग)", "उच्च ऊर्जा, आकर्षण और महत्वाकांक्षा; भावनात्मक आवेग व खर्चों पर संतुलन रखें।"),

    (7, 1): (4.0, "Intuitive Leader (केतु-सूर्य प्रज्ञा-नेतृत्व योग)", "गहन शोध और अंतर्दृष्टि (7) जो आगे चलकर प्रामाणिक अधिकार (1) में बदलती है।"),
    (7, 2): (3.5, "Psychic Depth (केतु-चंद्र गूढ़-संवेदना योग)", "आध्यात्मिकता, मनोविज्ञान और रचनात्मक लेखन में गहराई; अकेलेपन या संशय से बचें।"),
    (7, 3): (4.5, "Ketu-Guru Spiritual Scholar (केतु-गुरु ध्वज-ज्ञान राजयोग)", "शास्त्रीय व तकनीकी शोध, शिक्षण और उच्च परामर्श में अद्वितीय प्रामाणिकता।"),
    (7, 4): (4.0, "Shadow-Tech Innovator (केतु-राहु अनुसंधान-तंत्र योग)", "जटिल समस्याओं की जड़ तक पहुंचने और नए सिस्टम बनाने में माहिर।"),
    (7, 5): (4.0, "Specialist Communicator (केतु-बुध सूक्ष्म-विश्लेषण योग)", "गूढ़ विषयों को सरल भाषा व व्यापारिक रूप में प्रस्तुत करने की क्षमता।"),
    (7, 6): (4.0, "Graceful Seeker (केतु-शुक्र सात्विक-सौभाग्य योग)", "आध्यात्मिक संतोष के साथ भौतिक सुख-सुविधाओं का सहज संतुलन।"),
    (7, 7): (3.0, "Double Ketu Hermit-Genius (द्विगुणित केतु अति-वैराग्य/शोध)", "असाधारण अंतर्ज्ञान और शोध क्षमता, पर सामाजिक कटाव व भ्रम से बचना आवश्यक।"),
    (7, 8): (3.0, "Tapasya & Endurance (केतु-शनि गहन-तपस्या योग)", "एकांत परिश्रम, कानून, पुरातत्व या डीप-टेक में धीमी पर ठोस उपलब्धि।"),
    (7, 9): (3.5, "Ketu-Mangal Precision Strike (केतु-मंगल लक्षित-पराक्रम योग)", "सूक्ष्म विश्लेषण के बाद सटीक प्रहार; सर्जरी, रक्षा, ऑडिट और संकट-प्रबंधन में दक्ष।"),

    (8, 1): (2.0, "Shani-Surya Authority Struggle (शनि-सूर्य कर्म-सत्ता संघर्ष)", "प्रारंभिक जीवन में कड़ा परिश्रम और वरिष्ठों से मतभेद; 35 वर्ष बाद स्व-अर्जित उच्च अधिकार।"),
    (8, 2): (2.0, "Shani-Chandra Duty vs Emotion (शनि-चंद्र कर्तव्य-संवेदना द्वंद्व)", "कठोर यथार्थ (8) और भावनात्मक अपेक्षाओं (2) में खिंचाव; धैर्य और मानसिक प्रसन्नता बनाए रखें।"),
    (8, 3): (4.0, "Shani-Guru Nyaya-Dharma (शनि-गुरु न्याय-धर्म संतुलन)", "शनि के परिश्रम को गुरु के ज्ञान का मार्गदर्शन; कानून, वित्त, शिक्षा व प्रशासन में उच्च सम्मान।"),
    (8, 4): (2.5, "Shani-Rahu Heavy Infrastructure (शनि-राहु जटिल-तंत्र संघर्ष)", "बड़े प्रोजेक्ट्स और तकनीकी/औद्योगिक कार्यों में क्षमता, पर कानूनी व वित्तीय पारदर्शिता अनिवार्य।"),
    (8, 5): (4.5, "Shani-Budha Strategic Empire (शनि-बुध दीर्घकालिक-वाणिज्य योग)", "शनि के धैर्य (8) और बुध की व्यावसायिक बुद्धि (5) का श्रेष्ठ संगम;35 वर्ष बाद बड़ी आर्थिक स्थिरता व प्रबंधन सफलता।"),
    (8, 6): (4.5, "Shani-Shukra Royal Material Rise (शनि-शुक्र स्थायी-ऐश्वर्य राजयोग)", "शनि और शुक्र की परम मित्रता; संघर्ष के बाद उच्च भौतिक सुख, संपत्ति और प्रतिष्ठित जीवन।"),
    (8, 7): (3.5, "Deep Structure Researcher (शनि-केतु गहन-संरचना शोध)", "तकनीकी गहराई, ऑडिट, खनन, डेटा या आध्यात्मिक अनुशासन में ठोस पहचान।"),
    (8, 8): (2.5, "Double Saturn Iron Karma (द्विगुणित शनि कठोर-तपस्या योग)", "अत्यधिक जिम्मेदारी और विलंब से सफलता; निराशा छोड़कर निरंतर न्यायपूर्ण कर्म करने पर विशाल उपलब्धि।"),
    (8, 9): (2.5, "Shani-Mangal Agni-Maruta Friction (शनि-मंगल धैर्य-आवेग संघर्ष)", "रोक (8) और वेग (9) का द्वंद्व; क्रोध व जल्दबाजी नियंत्रित करने पर इंजीनियरिंग/सेना/उद्योग में बड़ी जीत।"),

    (9, 1): (5.0, "Mangal-Surya Victorious Command (मंगल-सूर्य विजय-प्रभुत्व राजयोग)", "साहस (9) और राजसत्ता (1) का सर्वोच्च संगम; प्रशासन, रक्षा और उद्यम में अजेय नेतृत्व।"),
    (9, 2): (4.0, "Warrior-Protector Moon (मंगल-चंद्र रक्षक-संपदा योग)", "बाहर से साहसी और भीतर से करुणामय; जन-नेतृत्व और संपत्ति निर्माण में शुभ।"),
    (9, 3): (5.0, "Mangal-Guru Dharma-Senapati (मंगल-गुरु धर्म-सेनापति राजयोग)", "ऊर्जा (9) को ज्ञान व नीति (3) की दिशा; उच्च पद, सम्मान और सिद्धांतवादी विजय।"),
    (9, 4): (2.5, "Mangal-Rahu High-Voltage Risk (मंगल-राहु साहसिक-परिवर्तन योग)", "असाधारण साहस पर आकस्मिक विवाद/जोखिम की आशंका; शांत रणनीति से काम लें।"),
    (9, 5): (4.0, "Action-Intellect Precision (मंगल-बुध त्वरित-कौशल योग)", "साहस और व्यापारिक/तकनीकी बुद्धि का संतुलन; उद्यम व प्रतिस्पर्धा में सफलता।"),
    (9, 6): (3.5, "Valour-Grace Synthesis (मंगल-शुक्र पराक्रम-ऐश्वर्य योग)", "कठोर परिश्रम से सुख-साधनों और प्रतिष्ठित जीवनशैली का निर्माण।"),
    (9, 7): (4.0, "Spiritual Warrior (मंगल-केतु अंतर्ज्ञानी-योद्धा योग)", "निःस्वार्थ सेवा, गहन शोध और सटीक क्रियान्वयन से सम्मान।"),
    (9, 8): (2.5, "Mangal-Shani Tested Endurance (मंगल-शनि संघर्ष-विजय योग)", "तेज ऊर्जा (9) को शनि (8) के धैर्य की परीक्षा से गुजरना पड़ता है; संयम रखने पर स्थायी सफलता।"),
    (9, 9): (3.5, "Double Mars Blazing Courage (द्विगुणित मंगल प्रचंड-पराक्रम)", "असीम ऊर्जा और नेतृत्व क्षमता; क्रोध व आवेग को रचनात्मक लक्ष्यों में मोड़ना आवश्यक।"),
}

# ---------------------------------------------------------------------------
# 4. VEDIC SURYA GRID (3-1-9 / 6-7-5 / 2-8-4) & 37 VEDIC YOGAS
# ---------------------------------------------------------------------------
VEDIC_GRID_LAYOUT = [
    [3, 1, 9],  # Top Row: Guru (3) - Surya (1) - Mangala (9)
    [6, 7, 5],  # Middle Row: Shukra (6) - Ketu (7) - Budha (5)
    [2, 8, 4],  # Bottom Row: Chandra (2) - Shani (8) - Rahu (4)
]

# 37 Authentic Vedic Anka-Jyotish Yogas in the 3-1-9 / 6-7-5 / 2-8-4 Grid
VEDIC_37_YOGAS = [
    # --- A. 8 Primary 3-Number Planes (3 Rows, 3 Columns, 2 Diagonals) ---
    {"id": 1, "pattern": [3, 1, 9], "category": "Primary 3-Number Row (Top)", "name_en": "Guru-Surya-Mangal Rajayoga Plane", "name_hi": "गुरु-सूर्य-मंगल शीर्ष राजयोग पंक्ति (3-1-9)", "effect_hi": "बौद्धिक तेज, प्रशासनिक अधिकार, नेतृत्व और निर्णायक साहस का सर्वोच्च संगम।", "effect_en": "Intellectual sovereignty, administrative authority, leadership, and decisive courage."},
    {"id": 2, "pattern": [6, 7, 5], "category": "Primary 3-Number Row (Middle)", "name_en": "Shukra-Ketu-Budha Intuitive Commerce Plane", "name_hi": "शुक्र-केतु-बुध मध्य व्यवहार-अंतर्ज्ञान पंक्ति (6-7-5)", "effect_hi": "व्यापारिक समझ, कूटनीति, सूक्ष्म शोध और संसाधन-प्रबंधन का संतुलित योग।", "effect_en": "Commercial acumen, diplomacy, deep diagnostic intuition, and resource management."},
    {"id": 3, "pattern": [2, 8, 4], "category": "Primary 3-Number Row (Bottom)", "name_en": "Chandra-Shani-Rahu Grounded Karma Plane", "name_hi": "चंद्र-शनि-राहु धरातलीय संघर्ष-यथार्थ पंक्ति (2-8-4)", "effect_hi": "गहन जमीनी यथार्थ, तकनीकी/व्यवस्थागत पकड़ और कड़े संघर्ष से स्थायी निर्माण (अति-चिंता से बचें)।", "effect_en": "Deep grassroots realism, technical/systemic grip, and enduring construction through hard testing."},
    {"id": 4, "pattern": [3, 6, 2], "category": "Primary 3-Number Column (Left)", "name_en": "Guru-Shukra-Chandra Wisdom & Grace Column", "name_hi": "गुरु-शुक्र-चंद्र ज्ञान-सौम्यता स्तंभ (3-6-2)", "effect_hi": "शिक्षा, कला, सामाजिक लोकप्रियता, परामर्श और पारिवारिक सामंजस्य का शुभ स्तंभ।", "effect_en": "Counsel, aesthetics, social harmony, emotional intelligence, and family devotion."},
    {"id": 5, "pattern": [1, 7, 8], "category": "Primary 3-Number Column (Center)", "name_en": "Surya-Ketu-Shani Tapasya & Justice Axis", "name_hi": "सूर्य-केतु-शनि तपस्या-न्याय मध्य स्तंभ (1-7-8)", "effect_hi": "गंभीर आत्म-अनुशासन, कानून/शोध क्षमता और कठिन कर्म-परीक्षाओं के बाद प्रामाणिक सत्ता।", "effect_en": "Deep self-discipline, investigative/legal mastery, and authentic authority forged through trials."},
    {"id": 6, "pattern": [9, 5, 4], "category": "Primary 3-Number Column (Right)", "name_en": "Mangal-Budha-Rahu Action & Tech Execution Column", "name_hi": "मंगल-बुध-राहु क्रियान्वयन व तकनीकी रणनीति स्तंभ (9-5-4)", "effect_hi": "तीव्र गणना, तकनीकी नवाचार, साहसिक निर्णय और जटिल प्रोजेक्ट्स को पूरा करने की शक्ति।", "effect_en": "Rapid analytical execution, technical disruption, and bold tactical problem-solving."},
    {"id": 7, "pattern": [3, 7, 4], "category": "Primary 3-Number Diagonal (NW-SE)", "name_en": "Guru-Ketu-Rahu Occult & Research Diagonal", "name_hi": "गुरु-केतु-राहु गूढ़ शोध व नवाचार विकर्ण (3-7-4)", "effect_hi": "परंपरागत ज्ञान (3), अंतर्ज्ञान (7) और आधुनिक तकनीक (4) का अनूठा मेल; डीप-टेक व ज्योतिष/शोध में सिद्धि।", "effect_en": "Synthesis of classical wisdom (3), intuition (7), and unconventional tech/systems (4)."},
    {"id": 8, "pattern": [9, 7, 2], "category": "Primary 3-Number Diagonal (NE-SW)", "name_en": "Mangal-Ketu-Chandra Intuitive Courage Diagonal", "name_hi": "मंगल-केतु-चंद्र अंतर्ज्ञानी पराक्रम विकर्ण (9-7-2)", "effect_hi": "तीव्र छठी इंद्री, भावनात्मक गहराई और संकट में सटीक साहसिक निर्णय लेने की क्षमता।", "effect_en": "Penetrating sixth sense combined with emotional depth and protective courage."},

    # --- B. 4 Strategic 3-Number Triads ---
    {"id": 9, "pattern": [1, 5, 9], "category": "Royal Triad", "name_en": "Surya-Budha-Mangal Sovereign Execution Triad", "name_hi": "सूर्य-बुध-मंगल राज-वाणिज्य-पराक्रम त्रिकोण (1-5-9)", "effect_hi": "नेतृत्व (1), बुद्धि (5) और साहस (9) का पूर्ण राजयोग; प्रशासन व उद्यम में शीर्ष सफलता।", "effect_en": "Commanding leadership (1), sharp intellect (5), and decisive execution (9)."},
    {"id": 10, "pattern": [3, 5, 6], "category": "Prosperity Triad", "name_en": "Guru-Budha-Shukra Vidya-Lakshmi Triad", "name_hi": "गुरु-बुध-शुक्र विद्या-लक्ष्मी त्रिकोण (3-5-6)", "effect_hi": "ज्ञान, व्यापारिक कौशल और आर्थिक समृद्धि का अत्यंत शुभ समन्वय।", "effect_en": "Harmonious union of wisdom (3), commerce (5), and material prosperity (6)."},
    {"id": 11, "pattern": [2, 5, 6], "category": "Diplomatic Triad", "name_en": "Chandra-Budha-Shukra Public & Financial Grace Triad", "name_hi": "चंद्र-बुध-शुक्र जन-संपर्क व तरल संपदा योग (2-5-6)", "effect_hi": "मधुर संवाद, जन-आकर्षण, बैंकिंग/व्यापार और पारिवारिक सुख में सहज उन्नति।", "effect_en": "Liquid cash flow, persuasive diplomacy, hospitality, and social magnetism."},
    {"id": 12, "pattern": [4, 7, 8], "category": "Mastery Triad", "name_en": "Rahu-Ketu-Shani Deep Engineering & Karma Triad", "name_hi": "राहु-केतु-शनि गहन तकनीकी-कर्म त्रिकोण (4-7-8)", "effect_hi": "कठिन तकनीकी, औद्योगिक या शोध कार्यों में असाधारण पकड़; धैर्य से स्थायी निर्माण।", "effect_en": "Hardcore systems engineering, root-cause diagnostics, and long-term structural endurance."},

    # --- C. 25 Classical 2-Number Graha-Anka Yogas ---
    {"id": 13, "pattern": [1, 3], "category": "Surya-Guru Yoga", "name_en": "Guru-Aditya Dharma-Adhikara Yoga", "name_hi": "गुरु-आदित्य धर्म-अधिकार योग (1-3)", "effect_hi": "नैतिक नेतृत्व, वरिष्ठों का सम्मान और शिक्षा/प्रशासन में प्रामाणिक प्रतिष्ठा।", "effect_en": "Principled leadership, mentorship, and institutional respect."},
    {"id": 14, "pattern": [1, 9], "category": "Surya-Mangal Yoga", "name_en": "Aditya-Kuja Parakrama Rajayoga", "name_hi": "सूर्य-मंगल पराक्रम राजयोग (1-9)", "effect_hi": "प्रबल आत्मबल, साहसिक निर्णय और किसी भी चुनौती का सामना करने की क्षमता।", "effect_en": "High vitality, fearless initiative, and executive command."},
    {"id": 15, "pattern": [3, 9], "category": "Guru-Mangal Yoga", "name_en": "Guru-Mangala Dharma-Senapati Yoga", "name_hi": "गुरु-मंगल धर्म-सेनापति योग (3-9)", "effect_hi": "ज्ञान और ऊर्जा का संतुलित प्रयोग; न्यायपूर्ण नेतृत्व और रणनीतिक विजय।", "effect_en": "Righteous action guided by strategic wisdom."},
    {"id": 16, "pattern": [1, 5], "category": "Surya-Budha Yoga", "name_en": "Budhaditya Ganita-Prashasana Yoga", "name_hi": "बुधादित्य गणना-प्रशासन योग (1-5)", "effect_hi": "तीक्ष्ण बौद्धिक विश्लेषण, स्पष्ट संवाद और उच्च प्रबंधकीय दक्षता।", "effect_en": "Sharp administrative intelligence and articulate authority."},
    {"id": 17, "pattern": [3, 5], "category": "Guru-Budha Yoga", "name_en": "Guru-Budha Saraswati-Vidya Yoga", "name_hi": "गुरु-बुध सरस्वती-विद्या योग (3-5)", "effect_hi": "अध्ययन, लेखन, परामर्श, कानून और वित्तीय नियोजन में उत्कृष्टता।", "effect_en": "Academic excellence, advisory precision, and structured communication."},
    {"id": 18, "pattern": [5, 6], "category": "Budha-Shukra Yoga", "name_en": "Lakshmi-Vyapara Samriddhi Yoga", "name_hi": "बुध-शुक्र लक्ष्मी-व्यापार समृद्धि योग (5-6)", "effect_hi": "व्यापारिक चातुर्य, ब्रांडिंग, वित्तीय लाभ और सुख-सुविधाओं का आकर्षण।", "effect_en": "Commercial magnetism, financial diplomacy, and aesthetic refinement."},
    {"id": 19, "pattern": [2, 3], "category": "Chandra-Guru Yoga", "name_en": "Gajakesari Anka-Soumya Yoga", "name_hi": "चंद्र-गुरु गजकेसरी सौम्य योग (2-3)", "effect_hi": "संवेदनशील ज्ञान, सात्विक सोच और समाज में विश्वसनीय छवि।", "effect_en": "Compassionate wisdom, emotional maturity, and public trust."},
    {"id": 20, "pattern": [2, 5], "category": "Chandra-Budha Yoga", "name_en": "Chandra-Budha Vaani-Kushalata Yoga", "name_hi": "चंद्र-बुध वाणी-कुशलता योग (2-5)", "effect_hi": "व्यावहारिक कल्पनाशीलता, त्वरित अनुकूलन और मधुर संवाद से कार्य-सिद्धि।", "effect_en": "Adaptable communication, emotional tact, and commercial fluidity."},
    {"id": 21, "pattern": [2, 6], "category": "Chandra-Shukra Yoga", "name_en": "Rasa-Kala Saundarya Yoga", "name_hi": "चंद्र-शुक्र रस-कला सौंदर्य योग (2-6)", "effect_hi": "सहज स्नेह, कलात्मक अभिरुचि और पारिवारिक व सामाजिक सौहार्द।", "effect_en": "Emotional warmth, artistic sensibility, and relational harmony."},
    {"id": 22, "pattern": [2, 9], "category": "Chandra-Mangal Yoga", "name_en": "Chandra-Mangala Dhana-Udyama Yoga", "name_hi": "चंद्र-मंगल धन-उद्यम योग (2-9)", "effect_hi": "भावनात्मक संकल्प के साथ सक्रिय कर्म; संसाधन व संपत्ति अर्जन की ऊर्जा।", "effect_en": "Resourceful drive combining emotional care with proactive effort."},
    {"id": 23, "pattern": [5, 9], "category": "Budha-Mangal Yoga", "name_en": "Budha-Mangala Tarka-Kriya Yoga", "name_hi": "बुध-मंगल तर्क-क्रिया योग (5-9)", "effect_hi": "त्वरित निर्णय, तकनीकी/इंजीनियरिंग कौशल और प्रतिस्पर्धा में बढ़त।", "effect_en": "Fast tactical execution, debate/engineering skill, and competitive edge."},
    {"id": 24, "pattern": [6, 9], "category": "Shukra-Mangal Yoga", "name_en": "Shukra-Mangala Aishwarya-Utsaha Yoga", "name_hi": "शुक्र-मंगल ऐश्वर्य-उत्साह योग (6-9)", "effect_hi": "रचनात्मक ऊर्जा, आकर्षक व्यक्तित्व और महत्वाकांक्षी जीवनशैली।", "effect_en": "Passionate ambition, creative vitality, and magnetic presence."},
    {"id": 25, "pattern": [4, 5], "category": "Rahu-Budha Yoga", "name_en": "Rahu-Budha Chatura-Tech Yoga", "name_hi": "राहु-बुध चतुर-तकनीक योग (4-5)", "effect_hi": "आईटी, सॉफ्टवेयर, डेटा, ट्रेडिंग और आधुनिक संचार माध्यमों में विशेष दक्षता।", "effect_en": "Clever system optimization, digital/IT mastery, and unconventional business logic."},
    {"id": 26, "pattern": [4, 6], "category": "Rahu-Shukra Yoga", "name_en": "Rahu-Shukra Adhunika-Vaibhava Yoga", "name_hi": "राहु-शुक्र आधुनिक-वैभव योग (4-6)", "effect_hi": "मीडिया, डिजाइन, आधुनिक विलासिता और बड़े कॉर्पोरेट नेटवर्क से लाभ।", "effect_en": "Modern media/design flair and material amplification."},
    {"id": 27, "pattern": [3, 7], "category": "Guru-Ketu Yoga", "name_en": "Guru-Ketu Prana-Pragya Yoga", "name_hi": "गुरु-केतु सूक्ष्म-प्रज्ञा योग (3-7)", "effect_hi": "गहन अध्ययन, शोध, ज्योतिष/दर्शन और जटिल विषयों की मूल समझ।", "effect_en": "Deep scholarly intuition, research integrity, and spiritual insight."},
    {"id": 28, "pattern": [5, 7], "category": "Budha-Ketu Yoga", "name_en": "Budha-Ketu Sukshma-Vishleshana Yoga", "name_hi": "बुध-केतु सूक्ष्म-विश्लेषण योग (5-7)", "effect_hi": "डेटा-ऑडिट, कोड-डीबगिंग, लेखन और गुप्त पैटर्न पकड़ने की क्षमता।", "effect_en": "Diagnostic precision, pattern recognition, and investigative analysis."},
    {"id": 29, "pattern": [6, 7], "category": "Shukra-Ketu Yoga", "name_en": "Shukra-Ketu Sattvika-Kala Yoga", "name_hi": "शुक्र-केतु सात्विक-कला योग (6-7)", "effect_hi": "सौंदर्य में आध्यात्मिक गहराई, हीलिंग और सूक्ष्म रचनात्मकता।", "effect_en": "Detached elegance, healing aesthetics, and refined intuition."},
    {"id": 30, "pattern": [6, 8], "category": "Shukra-Shani Yoga", "name_en": "Shukra-Shani Sthira-Sampada Yoga", "name_hi": "शुक्र-शनि स्थायी-संपदा योग (6-8)", "effect_hi": "दीर्घकालिक परिश्रम और अनुशासन से स्थायी संपत्ति, वाहन व संस्थागत सफलता।", "effect_en": "Enduring asset creation through disciplined craftsmanship and loyalty."},
    {"id": 31, "pattern": [5, 8], "category": "Budha-Shani Yoga", "name_en": "Budha-Shani Vyavasaya-Niyamana Yoga", "name_hi": "बुध-शनि व्यवसाय-नियमन योग (5-8)", "effect_hi": "व्यावहारिक गणना, जोखिम-प्रबंधन और बड़े संगठनों में स्थिर कार्यक्षमता।", "effect_en": "Calculated risk management, compliance, and long-term commercial planning."},
    {"id": 32, "pattern": [1, 8], "category": "Surya-Shani Karmic Yoga", "name_en": "Surya-Shani Adhikara-Sangharsha Yoga", "name_hi": "सूर्य-शनि अधिकार-संघर्ष परीक्षा योग (1-8)", "effect_hi": "वरिष्ठों/व्यवस्था से वैचारिक घर्षण के बाद स्व-निर्मित अनुशासन से स्थायी नेतृत्व।", "effect_en": "Authority tested by institutional friction, forging self-made resilience."},
    {"id": 33, "pattern": [2, 8], "category": "Chandra-Shani Karmic Yoga", "name_en": "Chandra-Shani Gambhira-Tapasya Yoga", "name_hi": "चंद्र-शनि गंभीर-तपस्या (विष-संयम) योग (2-8)", "effect_hi": "भीतर भावनात्मक संवेदनशीलता और बाहर कठोर जिम्मेदारी; अति-चिंता छोड़कर कर्म पर ध्यान दें।", "effect_en": "Emotional sensitivity carrying heavy realism; requires mindfulness to prevent melancholy."},
    {"id": 34, "pattern": [4, 8], "category": "Rahu-Shani Karmic Yoga", "name_en": "Rahu-Shani Shrama-Tantra Yoga", "name_hi": "राहु-शनि कठोर श्रम-तंत्र योग (4-8)", "effect_hi": "अत्यधिक परिश्रम और बाधाओं को पार कर जटिल तकनीकी/कानूनी क्षेत्रों में महारत।", "effect_en": "Mastery over complex mechanical/legal systems through relentless perseverance."},
    {"id": 35, "pattern": [8, 9], "category": "Shani-Mangal Karmic Yoga", "name_en": "Shani-Mangala Dhairya-Shakti Yoga", "name_hi": "शनि-मंगल धैर्य-शक्ति संतुलन योग (8-9)", "effect_hi": "तीव्र ऊर्जा (9) और संयम (8) का एक साथ होना; धैर्य रखने पर कठिनतम कार्यों में विजय।", "effect_en": "High-pressure drive balanced by endurance; excels when impulse yields to strategy."},
    {"id": 36, "pattern": [2, 4], "category": "Chandra-Rahu Karmic Yoga", "name_en": "Chandra-Rahu Kalpana-Vistara Yoga", "name_hi": "चंद्र-राहु कल्पना-विस्तार (भ्रम-नियंत्रण) योग (2-4)", "effect_hi": "तीव्र कल्पनाशक्ति और लीक से हटकर सोच, पर निर्णय हमेशा तथ्यों व लिखित प्रमाण पर लें।", "effect_en": "Vivid out-of-the-box imagination; must anchor decisions in verified facts."},
    {"id": 37, "pattern": [2, 7], "category": "Chandra-Ketu Karmic Yoga", "name_en": "Chandra-Ketu Antardrishti Yoga", "name_hi": "चंद्र-केतु अंतर्दृष्टि-ध्यान योग (2-7)", "effect_hi": "गूढ़ मनोवैज्ञानिक समझ और पूर्वानुमान क्षमता; ध्यान व शोध से मानसिक स्पष्टता।", "effect_en": "Deep psychological intuition and clairvoyant sensitivity."},
]

# ---------------------------------------------------------------------------
# 5. CHALDEAN & PYTHAGOREAN TABLES + COMPLETE 10-52 CHALDEAN COMPOUNDS
# ---------------------------------------------------------------------------
CH = {
    **dict.fromkeys("AIJQY", 1),
    **dict.fromkeys("BKR", 2),
    **dict.fromkeys("CGLS", 3),
    **dict.fromkeys("DMT", 4),
    **dict.fromkeys("EHNX", 5),
    **dict.fromkeys("UVW", 6),
    **dict.fromkeys("OZ", 7),
    **dict.fromkeys("FP", 8),
}
PY = {c: (i % 9) + 1 for i, c in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ")}
VOWELS = set("AEIOU")

CHALDEAN_COMPOUNDS_10_52 = {
    10: {"title": "Wheel of Fortune (भाग्य-चक्र)", "status": "Auspicious", "hi": "सम्मान, आत्मविश्वास और उतार-चढ़ाव के बाद निश्चित उत्थान का अंक।", "en": "Honour, faith, and self-determined rise; cyclic turns leading to prominence."},
    11: {"title": "Hidden Trials & Master Intuition (गुप्त परीक्षा व अंतर्ज्ञान)", "status": "Caution / Master", "hi": "तीव्र अंतर्ज्ञान पर गुप्त विरोध या द्विविधा से सावधानी आवश्यक।", "en": "High psychic intuition, but warns of hidden opposition or dual loyalties if unfocused."},
    12: {"title": "The Sacrifice / Victim of Plans (त्याग व पर-हित चिंता)", "status": "Caution", "hi": "दूसरों की योजनाओं या बोझ के कारण मानसिक तनाव; अपने हितों की स्पष्ट सीमा बनाएं।", "en": "Intellectual wisdom, yet prone to carrying others' burdens or anxiety."},
    13: {"title": "Upheaval & Transformation (रचनात्मक रूपांतरण)", "status": "Transformative", "hi": "पुराने ढांचे को बदलकर नई शक्ति व अधिकार खड़ा करने वाला अंक; शॉर्टकट से बचें।", "en": "Power of reconstruction and deep change; demands strict ethical discipline."},
    14: {"title": "Magnetic Movement & Commerce (गतिशील व्यापार व जन-संपर्क)", "status": "Mixed / Fortunate with Caution", "hi": "मीडिया, व्यापार और जन-संपर्क में बड़ा आकर्षण; प्राकृतिक/वित्तीय जोखिम में संयम रखें।", "en": "Fortunate for communication, finance, and public dealings; guard against speculative excess."},
    15: {"title": "Alchemy of Grace & Eloquence (वाक्-सिद्धि व आकर्षण)", "status": "Highly Auspicious", "hi": "वाणी, कला, प्रबंधन और वरिष्ठों से धन-सहयोग प्राप्त करने के लिए अत्यंत शुभ।", "en": "eloquent magnetism, artistic charm, and material favour from others."},
    16: {"title": "The Shattered Citadel / Awakening (अहं-भंग व आत्म-जागृति)", "status": "Caution", "hi": "अति-आत्मविश्वास या गलत साझेदारी से अचानक झटका; विनम्रता व आध्यात्मिक सतर्कता रखें।", "en": "Warns against overconfidence in material status; calls for humility and foresight."},
    17: {"title": "Star of the Magi (अमर कीर्ति व आध्यात्मिक तारा)", "status": "Highly Auspicious", "hi": "प्रारंभिक संघर्ष के बाद स्थायी नाम, आध्यात्मिक सुरक्षा और उच्च सम्मान दिलाने वाला श्रेष्ठ अंक।", "en": "Spiritual protection, immortality of name, and triumph over early hardships."},
    18: {"title": "Spiritual-Material Conflict (धर्म-अर्थ संघर्ष)", "status": "Challenging", "hi": "कठोर प्रतिस्पर्धा, विवाद या अपनों से मतभेद से धन-अर्जन; शांत व न्यायपूर्ण रहें।", "en": "Material gain through fierce contest or institutional friction; requires calm integrity."},
    19: {"title": "Prince of Heaven (सूर्य-तेज व राज-सम्मान)", "status": "Highly Auspicious", "hi": "सूर्य और मंगल का विजय-अंक; सम्मान, सफलता, नेतृत्व और प्रगति।", "en": "Victory, happiness, honour, and self-earned administrative elevation."},
    20: {"title": "The Awakening of Purpose (उद्देश्य-जागृति)", "status": "Auspicious / Spiritual", "hi": "भौतिक लाभ से अधिक नई चेतना, परामर्श और जीवन के उत्तरार्ध में विशेष सम्मान।", "en": "New call to duty, regeneration, and spiritual/advisory maturity over pure materialism."},
    21: {"title": "Crown of the Magi (विजय-मुकुट)", "status": "Highly Auspicious", "hi": "लंबे प्रयास के बाद निश्चित उन्नति, शैक्षणिक/प्रशासनिक सम्मान और स्थायी प्रतिष्ठा।", "en": "Advancement, general honour, and crowning success after steady effort."},
    22: {"title": "Good Person in Illusion / Master Builder (भ्रम-सावधानी व निर्माण)", "status": "Caution / Master", "hi": "दूसरों पर अंध-विश्वास से हानि की आशंका; व्यावहारिक व सतर्क रहकर बड़े कार्य करें।", "en": "High structural potential, but warns against misplaced trust or daydreaming."},
    23: {"title": "Royal Star of the Lion (राज-सिंह तारा)", "status": "Supreme Auspicious", "hi": "उच्च अधिकारियों का संरक्षण, तीक्ष्ण बुद्धि और हर क्षेत्र में सफलता दिलाने वाला राजयोग अंक।", "en": "Protection from high authority, professional versatility, and assured success."},
    24: {"title": "Love, Money & Patronage (प्रेम, संपदा व वरिष्ठ-कृपा)", "status": "Highly Auspicious", "hi": "परिवार, प्रशासन और वरिष्ठों/विपरीत लिंग के सहयोग से निरंतर आर्थिक व सामाजिक उन्नति।", "en": "Gain through patrons, harmonious family life, and executive advancement."},
    25: {"title": "Strength Through Experience (अनुभव-जन्य प्रज्ञा)", "status": "Auspicious (After Early Trial)", "hi": "प्रारंभिक जीवन के प्रत्यक्ष अनुभवों व शोध से उच्च विवेक और विशेषज्ञता।", "en": "Discrimination and mastery won through early observation and lived trials."},
    26: {"title": "Partnerships & Karmic Gravitas (साझेदारी-सावधानी व गंभीर कर्म)", "status": "Caution", "hi": "गलत साझेदारी या बिना जांच के निवेश से सावधानी; स्वतंत्र निर्णय व लिखित अनुबंध से सफलता।", "en": "Warns against blind partnerships or speculative advice; thrives on independent due diligence."},
    27: {"title": "The Sceptre of Command (अधिकार-दंड व प्रज्ञा)", "status": "Highly Auspicious", "hi": "मौलिक विचार, अंतर्ज्ञान और साहसिक नेतृत्व से उच्च अधिकार व पुरस्कार।", "en": "Commanding authority, productive intellect, and reward through original ideas."},
    28: {"title": "The Contradiction / Legal Foresight (विरोधाभास व विधिक सतर्कता)", "status": "Caution", "hi": "अच्छी शुरुआत के बाद साझेदारों या कानून से जुड़े मामलों में सतर्कता आवश्यक; अपने हाथ में नियंत्रण रखें।", "en": "Great promise that requires strict legal/financial buffers against loss through trust."},
    29: {"title": "Emotional Trials & Uncertainties (भावनात्मक परीक्षा)", "status": "Caution", "hi": "अविश्वसनीय मित्रों या भावनात्मक उतार-चढ़ाव से सावधानी; आत्मनिर्भर रहें।", "en": "Warns of emotional tests and unreliable associates; requires calm self-reliance."},
    30: {"title": "Thoughtful Retrospection (बौद्धिक श्रेष्ठता व एकाग्रता)", "status": "Neutral / Mental", "hi": "भौतिक दौड़ से ऊपर उच्च वैचारिक व शैक्षणिक दक्षता; अपने ज्ञान पर पूर्ण विश्वास।", "en": "Mental superiority and analytical depth; neither purely fortunate nor unfortunate."},
    31: {"title": "Self-Contained Specialist (स्वावलंबी विशेषज्ञ)", "status": "Neutral / Independent", "hi": "भीड़ से अलग अपनी स्वतंत्र तकनीकी या वैचारिक दुनिया बनाने वाला।", "en": "Self-reliant, solitary specialist who succeeds on original terms."},
    32: {"title": "Magical Communication & Alliance (संवाद-चमत्कार व जन-समर्थन)", "status": "Highly Auspicious", "hi": "तेजस्वी23 के समान शुभ; जन-समूह, संचार और मित्र राष्ट्रों/संस्थानों से बड़ा लाभ।", "en": "Magical harmony with groups and public communications when holding to own judgment."},
    33: {"title": "Master Blessing of Venus (महा-सौभाग्य शुक्र)", "status": "Highly Auspicious", "hi": "24 के समान अत्यंत शुभ; करुणा, कला, धन और पारिवारिक समृद्धि का आशीर्वाद।", "en": "Master vibration of grace, prosperity, and elevated domestic/artistic fortune."},
    34: {"title": "Wisdom Through Disciplined Trial (अनुभव-तपा विवेक)", "status": "Auspicious (Mature)", "hi": "25 के समान; परिश्रम और सूक्ष्म निरीक्षण से जीवन के मध्य भाग में ठोस उपलब्धि।", "en": "Mature discernment and technical mastery earned through patient observation."},
    35: {"title": "Karmic Partnership Test (साझेदारी व निवेश सतर्कता)", "status": "Caution", "hi": "26 के समान; संयुक्त व्यवसाय या उधार में पूर्ण लिखित पारदर्शिता रखें।", "en": "Echoes 26; requires strict independent verification in finance and partnerships."},
    36: {"title": "Self-Made Ascent (स्व-अर्जित उत्थान)", "status": "Auspicious", "hi": "27 के समान; परिवार से दूर या स्वयं के पराक्रम व मौलिक बुद्धि से उच्च पद।", "en": "Self-made authority, creative enterprise, and distinction through personal merit."},
    37: {"title": "Royal Friendship & Devoted Love (राज-मित्रता व अटूट स्नेह)", "status": "Supreme Auspicious", "hi": "मित्रों, जीवनसाथी और जन-संपर्क में असाधारण सौभाग्य व स्थायी समृद्धि।", "en": "Fortunate friendships, devoted partnerships, and enduring social/material success."},
    38: {"title": "Emotional & Relational Friction (संबंध-संयम)", "status": "Caution", "hi": "29 के समान; भावनात्मक आवेग या गलत सलाहकारों से दूरी बनाए रखें।", "en": "Echoes 29; guard against emotional reactive decisions or deceptive allies."},
    39: {"title": "Intellectual Responsibility (बौद्धिक दायित्व)", "status": "Auspicious / Mental", "hi": "उच्च वैचारिक क्षमता और परामर्श से सम्मान; मानसिक विश्राम का ध्यान रखें।", "en": "High mental output and principled advisory standing."},
    40: {"title": "Solitary Eccentricity (स्वतंत्र चिंतन)", "status": "Neutral", "hi": "अपनी ही कार्यशैली में मग्न; तकनीकी शोध में अच्छा पर सामाजिक समन्वय बढ़ाएं।", "en": "Methodical yet solitary thinker; benefits from collaborative warmth."},
    41: {"title": "Dynamic Solar-Rahu Command (गतिशील नेतृत्व)", "status": "Auspicious", "hi": "तेज निर्णय और आधुनिक प्रबंधन से कार्यक्षेत्र में प्रभावशाली पकड़।", "en": "Dynamic organizational authority and modern executive reach."},
    42: {"title": "Harmonious Patronage (सौम्य ऐश्वर्य)", "status": "Highly Auspicious", "hi": "24/33 की श्रेणी का शुभ अंक; सहयोग, कला और आर्थिक स्थिरता।", "en": "Favourable Venusian vibration bringing diplomatic and material success."},
    43: {"title": "Reform & Structural Tension (संरचनात्मक सुधार व संघर्ष)", "status": "Caution", "hi": "बदलाव और संघर्ष का अंक; शांतिपूर्ण रणनीति और धैर्य से ही लक्ष्य सिद्ध करें।", "en": "Signifies reform through friction; avoid impulsive confrontations."},
    44: {"title": "Material Architecture Caution (संस्थागत अनुशासन)", "status": "Caution", "hi": "बड़े वित्तीय व कानूनी मामलों में अत्यधिक अनुशासन और पारदर्शिता अनिवार्य।", "en": "Heavy material responsibility; demands strict ethical and legal discipline."},
    45: {"title": "Intellectual Honour & Reward (बौद्धिक सम्मान)", "status": "Highly Auspicious", "hi": "27/36 की श्रृंखला का शुभ अंक; बुद्धिमत्ता और साहसिक कर्म से स्थायी पुरस्कार।", "en": "Reward and authority earned through disciplined intellect and leadership."},
    46: {"title": "Balanced Sovereign Wisdom (संतुलित राज-प्रज्ञा)", "status": "Highly Auspicious", "hi": "10/19/37 के समान शुभ; नेतृत्व और मित्रता के संतुलन से उन्नति।", "en": "Fortunate solar synthesis bringing executive harmony and trustworthy alliances."},
    47: {"title": "Inner Dualism Caution (अंतर्द्वंद्व सतर्कता)", "status": "Caution", "hi": "तर्क और भावना के द्वंद्व से बचें; स्पष्ट लिखित प्राथमिकताओं के साथ कार्य करें।", "en": "Requires clear boundaries to avoid divided counsel."},
    48: {"title": "Karmic Justice & Endurance (कर्म-न्याय व धैर्य)", "status": "Neutral / Karmic", "hi": "कठोर परिश्रम और न्यायप्रियता से दीर्घकालिक स्थायित्व।", "en": "Demands patient perseverance and strict fairness."},
    49: {"title": "Fiery Restructuring (ऊर्जावान नव-निर्माण)", "status": "Mixed", "hi": "तीव्र ऊर्जा से पुराने अवरोध तोड़कर नया मार्ग बनाना।", "en": "High energy that clears stagnation when directed constructively."},
    50: {"title": "Universal Eloquence & Freedom (वैश्विक संवाद व मुक्ति)", "status": "Highly Auspicious", "hi": "बौद्धिक विस्तार, शिक्षा, संचार और स्वतंत्र व्यापार में अत्यंत शुभ।", "en": "Broad intellectual freedom, persuasive reach, and commercial prosperity."},
    51: {"title": "Warrior's Crown (योद्धा-विजय)", "status": "Highly Auspicious", "hi": "प्रशासन, रक्षा, रणनीति और साहसिक उपक्रमों में अचानक बड़ी उन्नति।", "en": "Sudden elevation in leadership, defense, and strategic enterprise."},
    52: {"title": "Revolutionary Cycle (क्रांतिकारी परिवर्तन)", "status": "Transformative", "hi": "बड़े व्यवस्थागत बदलाव और गहन शोध से जुड़ी ऊर्जा।", "en": "Large-scale systemic transformation requiring grounded execution."},
}

# ---------------------------------------------------------------------------
# 6. LO SHU GRID (4-9-2 / 3-5-7 / 8-1-6) & OVER-REPETITION RULES (1x, 2x, 3x, 4x+)
# ---------------------------------------------------------------------------
LOSHU_LAYOUT = [
    [4, 9, 2],
    [3, 5, 7],
    [8, 1, 6],
]

LOSHU_PLANES = [
    ("Mental Plane (मानसिक तल — Top Row)", [4, 9, 2], "बौद्धिक विश्लेषण, स्मरण शक्ति और वैचारिक स्पष्टता।"),
    ("Emotional Plane (भावनात्मक तल — Middle Row)", [3, 5, 7], "संवेदनशीलता, अंतर्ज्ञान, पारिवारिक जुड़ाव और हृदय की स्थिरता।"),
    ("Practical Plane (व्यावहारिक तल — Bottom Row)", [8, 1, 6], "जमीनी क्रियान्वयन, वित्तीय अनुशासन और भौतिक संसाधन निर्माण।"),
    ("Thought Plane (विचार स्तंभ — Left Col)", [4, 3, 8], "योजना निर्माण, दूरदर्शिता और तार्किक ढांचा खड़ा करने की क्षमता।"),
    ("Will Plane (इच्छाशक्ति स्तंभ — Center Col)", [9, 5, 1], "अडिग संकल्प, संकट में टिके रहने की शक्ति और लक्ष्य-प्राप्ति।"),
    ("Action Plane (कर्म स्तंभ — Right Col)", [2, 7, 6], "विचारों को तुरंत धरातल पर उतारने और परिणाम देने की तत्परता।"),
    ("Golden Yog / Rajyog (स्वर्ण राजयोग — 4-5-6 Diagonal)", [4, 5, 6], "संपत्ति, संतुलन, प्रबंधन और उच्च सामाजिक-आर्थिक सफलता।"),
    ("Silver Yog / Rajat Yog (रजत योग — 2-5-8 Diagonal)", [2, 5, 8], "भूमि, भवन, धैर्य और भावनात्मक-व्यावहारिक स्थिरता का योग।"),
]

REPETITION_RULES = {
    1: {
        0: "Missing (0x): अपनी बात खुलकर कहने और स्वतंत्र निर्णय लेने का अभ्यास करें; प्रातः सूर्य प्रकाश में रहें।",
        1: "Balanced (1x): स्वस्थ स्वाभिमान, स्पष्ट संवाद और संतुलित नेतृत्व क्षमता।",
        2: "Strong (2x): प्रखर अभिव्यक्ति, प्रभावशाली संवाद और लोगों को प्रेरित करने की उत्तम क्षमता।",
        3: "Excessive (3x): अत्यधिक बोलने या कभी-कभी शांत रहने का द्वंद्व; अहं के टकराव से बचकर दूसरों को भी सुनें।",
        4: "Extreme (4x+): अति-स्वाभिमान, अधिकार-संघर्ष या भीतर अकेलापन; विनम्रता और टीम-वर्क को प्राथमिकता दें।",
    },
    2: {
        0: "Missing (0x): दूसरों की भावनाओं के प्रति धैर्य और संवेदनशीलता विकसित करें; जल तत्व व चांदी/सफेद रंग का संतुलन रखें।",
        1: "Balanced (1x): सहज संवेदनशीलता, सहयोग और भावनात्मक समझ।",
        2: "Strong (2x): तीव्र अंतर्ज्ञान, दूसरों के मन को पढ़ने की क्षमता और मधुर जन-संपर्क।",
        3: "Excessive (3x): अति-संवेदनशीलता, छोटी बातों को दिल पर लेना और मूड-स्विंग; प्राणायाम व ग्राउंडिंग करें।",
        4: "Extreme (4x+): भावनात्मक आवेग, काल्पनिक चिंता और मानसिक अस्थिरता; निर्णय हमेशा तथ्यों पर आधारित रखें।",
    },
    3: {
        0: "Missing (0x): निरंतर स्वाध्याय, गुरुओं/वरिष्ठों का सम्मान और रचनात्मक कल्पनाशीलता बढ़ाएं।",
        1: "Balanced (1x): अच्छी सीखने की क्षमता, नैतिक दृष्टि और सकारात्मक सोच।",
        2: "Strong (2x): प्रखर बुद्धि, लेखन/शिक्षण कौशल और श्रेष्ठ परामर्श क्षमता।",
        3: "Excessive (3x): विचारों की अधिकता, बहस में उलझना या अपनी ही बात को अंतिम मानना; व्यावहारिक क्रियान्वयन पर ध्यान दें।",
        4: "Extreme (4x+): अति-कल्पनाशीलता या मानसिक बिखराव; एक समय में एक ही ठोस कार्य पूरा करें।",
    },
    4: {
        0: "Missing (0x): दैनिक कार्य-सूची (checklist) और समय-प्रबंधन से अनुशासन बनाएं।",
        1: "Balanced (1x): व्यावहारिक कौशल, व्यवस्था-प्रियता और तार्किक कार्यशैली।",
        2: "Strong (2x): उत्कृष्ट संगठनात्मक व तकनीकी दक्षता; जटिल कार्यों को व्यवस्थित करने में माहिर।",
        3: "Excessive (3x): विचारों में जड़ता (rigidity) या अनावश्यक शंका; लचीलापन और मानसिक विश्राम अपनाएं।",
        4: "Extreme (4x+): अति-भौतिकवाद या मानसिक तनाव व भ्रम; शारीरिक श्रम/योग से ऊर्जा को संतुलित करें।",
    },
    5: {
        0: "Missing (0x): जीवन के विभिन्न क्षेत्रों में संवाद और भावनात्मक-व्यावहारिक संतुलन consciously बनाएं।",
        1: "Balanced (1x): उत्तम भावनात्मक संतुलन, संवाद कौशल और अनुकूलन क्षमता।",
        2: "Strong (2x): प्रबल इच्छाशक्ति, व्यापारिक उत्साह और हर परिस्थिति में रास्ता निकालने का गुण।",
        3: "Excessive (3x): अनावश्यक जोखिम लेने या एक साथ बहुत से काम शुरू करने की प्रवृत्ति; संयम रखें।",
        4: "Extreme (4x+): तीव्र मानसिक बेचैनी और जल्दबाजी; ध्यान व स्थिर दिनचर्या से मन को केंद्रित करें।",
    },
    6: {
        0: "Missing (0x): परिवार और जीवनसाथी के साथ भावनात्मक समय बिताएं; कला व सौंदर्य को जीवन में स्थान दें।",
        1: "Balanced (1x): परिवार-निष्ठ, सौंदर्य-प्रिय और जिम्मेदार व्यक्तित्व।",
        2: "Strong (2x): रचनात्मकता, आतिथ्य, धन-प्रबंधन और अपनों के प्रति गहरा समर्पण।",
        3: "Excessive (3x): अपनों की अति-चिंता (over-possessiveness) या सुख-सुविधाओं पर अधिक खर्च; संतुलन रखें।",
        4: "Extreme (4x+): भावनात्मक निर्भरता या भौतिक दिखावे का दबाव; सात्विक जीवनशैली अपनाएं।",
    },
    7: {
        0: "Missing (0x): आत्म-चिंतन, शोध और आध्यात्मिक/दार्शनिक अध्ययन के लिए समय निकालें।",
        1: "Balanced (1x): स्वस्थ जिज्ञासा, अंतर्ज्ञान और अनुभव से सीखने की प्रवृत्ति।",
        2: "Strong (2x): गहन विश्लेषणात्मक व आध्यात्मिक दृष्टि; समस्याओं की जड़ तक पहुंचने की क्षमता।",
        3: "Excessive (3x): संबंधों या साझेदारी में संशय/अलगाव की भावना; विश्वास और खुला संवाद बढ़ाएं।",
        4: "Extreme (4x+): अति-अंतर्मुखी स्वभाव या भावनात्मक निराशा; रचनात्मक शोध व प्रकृति-संपर्क में रहें।",
    },
    8: {
        0: "Missing (0x): वित्तीय अनुशासन, धैर्य और दीर्घकालिक बचत की आदत विकसित करें।",
        1: "Balanced (1x): न्यायप्रियता, परिश्रम, तार्किकता और धन-प्रबंधन की समझ।",
        2: "Strong (2x): सूक्ष्म निरीक्षण क्षमता, संस्थागत अनुशासन और स्थायी संपत्ति निर्माण का बल।",
        3: "Excessive (3x): अति-आत्म-आलोचना, कार्य-बोझ या भौतिक बेचैनी; वर्तमान क्षण का आनंद लेना सीखें।",
        4: "Extreme (4x+): कठोर मानसिक दबाव, हर चीज को नियंत्रित करने की जिद; सेवा और विश्वास से मन हल्का रखें।",
    },
    9: {
        0: "Missing (0x): दूसरों की सहायता और अपने लक्ष्यों के प्रति सक्रिय उत्साह बनाए रखें।",
        1: "Balanced (1x): साहस, मानवतावादी दृष्टिकोण और लक्ष्य के प्रति ऊर्जा।",
        2: "Strong (2x): उच्च बौद्धिक-क्रियात्मक ऊर्जा, नेतृत्व और संकट में अडिग साहस।",
        3: "Excessive (3x): आवेग, तीखी वाणी या क्रोध की अधिकता; नियमित व्यायाम और शांत संवाद अपनाएं।",
        4: "Extreme (4x+): विस्फोटक ऊर्जा, अधीरता या विवाद; ऊर्जा को खेल, रक्षा या कठिन तकनीकी लक्ष्यों में मोड़ें।",
    },
}

# ---------------------------------------------------------------------------
# 7. KATAPAYADI SANKHYA & SVARA SHASTRA / AVAKAHADA PHONETICS
# ---------------------------------------------------------------------------
# Classical Katapayadi consonant mapping (Devanagari & Romanized phonetic tokens)
DEVANAGARI_KATAPAYADI = {
    "क": 1, "ख": 2, "ग": 3, "घ": 4, "ङ": 5, "च": 6, "छ": 7, "ज": 8, "झ": 9, "ञ": 0,
    "ट": 1, "ठ": 2, "ड": 3, "ढ": 4, "ण": 5, "त": 6, "थ": 7, "द": 8, "ध": 9, "न": 0,
    "प": 1, "फ": 2, "ब": 3, "भ": 4, "म": 5,
    "य": 1, "र": 2, "ल": 3, "व": 4, "श": 5, "ष": 6, "स": 7, "ह": 8, "ळ": 3,
}

# Ordered longest-first Roman phonetic consonant clusters for accurate Indian name parsing
ROMAN_KATAPAYADI_TOKENS = [
    ("chh", 7), ("ksh", 6), ("dny", 0), ("gya", 8), ("shri", 2), ("shr", 2),
    ("kh", 2), ("gh", 4), ("ch", 6), ("jh", 9), ("th", 7), ("dh", 9),
    ("ph", 2), ("bh", 4), ("sh", 5), ("ng", 5), ("ny", 0),
    ("k", 1), ("q", 1), ("c", 1), ("g", 3), ("j", 8), ("z", 8),
    ("t", 6), ("d", 8), ("n", 0),
    ("p", 1), ("f", 2), ("b", 3), ("m", 5),
    ("y", 1), ("r", 2), ("l", 3), ("v", 4), ("w", 4), ("s", 7), ("h", 8),
]

# Avakahada Chakra prefix-to-Nakshatra/Rashi phonetic map (Muhurta Chintamani)
AVAKAHADA_PREFIXES = [
    (["chu", "che", "cho", "la"], "Ashwini", "Aries (मेष)", "Mars (मंगल)", "Ketu (केतु)"),
    (["li", "lu", "le", "lo"], "Bharani", "Aries (मेष)", "Mars (मंगल)", "Venus (शुक्र)"),
    (["a", "aa", "i", "ee", "u", "oo", "e"], "Krittika", "Aries/Taurus (मेष/वृषभ)", "Mars/Venus", "Sun (सूर्य)"),
    (["o", "va", "vi", "vu", "wa", "wi"], "Rohini", "Taurus (वृषभ)", "Venus (शुक्र)", "Moon (चंद्र)"),
    (["ve", "vo", "ka", "ki"], "Mrigashira", "Taurus/Gemini (वृषभ/मिथुन)", "Venus/Mercury", "Mars (मंगल)"),
    (["ku", "gha", "nga", "chha"], "Ardra", "Gemini (मिथुन)", "Mercury (बुध)", "Rahu (राहु)"),
    (["ke", "ko", "ha", "hi"], "Punarvasu", "Gemini/Cancer (मिथुन/कर्क)", "Mercury/Moon", "Jupiter (गुरु)"),
    (["hu", "he", "ho", "da"], "Pushya", "Cancer (कर्क)", "Moon (चंद्र)", "Saturn (शनि)"),
    (["di", "du", "de", "do"], "Ashlesha", "Cancer (कर्क)", "Moon (चंद्र)", "Mercury (बुध)"),
    (["ma", "mi", "mu", "me"], "Magha", "Leo (सिंह)", "Sun (सूर्य)", "Ketu (केतु)"),
    (["mo", "ta", "ti", "tu"], "Purva Phalguni", "Leo (सिंह)", "Sun (सूर्य)", "Venus (शुक्र)"),
    (["te", "to", "pa", "pi"], "Uttara Phalguni", "Leo/Virgo (सिंह/कन्या)", "Sun/Mercury", "Sun (सूर्य)"),
    (["pu", "sha", "na", "tha"], "Hasta", "Virgo (कन्या)", "Mercury (बुध)", "Moon (चंद्र)"),
    (["pe", "po", "ra", "ri"], "Chitra", "Virgo/Libra (कन्या/तुला)", "Mercury/Venus", "Mars (मंगल)"),
    (["ru", "re", "ro", "taa"], "Swati", "Libra (तुला)", "Venus (शुक्र)", "Rahu (राहु)"),
    (["ti", "tu", "te", "to", "vi"], "Vishakha", "Libra/Scorpio (तुला/वृश्चिक)", "Venus/Mars", "Jupiter (गुरु)"),
    (["na", "ni", "nu", "ne"], "Anuradha", "Scorpio (वृश्चिक)", "Mars (मंगल)", "Saturn (शनि)"),
    (["no", "ya", "yi", "yu"], "Jyeshtha", "Scorpio (वृश्चिक)", "Mars (मंगल)", "Mercury (बुध)"),
    (["ye", "yo", "bha", "bhi"], "Mula", "Sagittarius (धनु)", "Jupiter (गुरु)", "Ketu (केतु)"),
    (["bhu", "dha", "pha", "fa"], "Purva Ashadha", "Sagittarius (धनु)", "Jupiter (गुरु)", "Venus (शुक्र)"),
    (["bhe", "bho", "ja", "ji"], "Uttara Ashadha", "Sagittarius/Capricorn (धनु/मकर)", "Jupiter/Saturn", "Sun (सूर्य)"),
    (["khi", "khu", "khe", "kho", "ju", "je", "jo"], "Shravana", "Capricorn (मकर)", "Saturn (शनि)", "Moon (चंद्र)"),
    (["ga", "gi", "gu", "ge"], "Dhanishta", "Capricorn/Aquarius (मकर/कुंभ)", "Saturn (शनि)", "Mars (मंगल)"),
    (["go", "sa", "si", "su"], "Shatabhisha", "Aquarius (कुंभ)", "Saturn (शनि)", "Rahu (राहु)"),
    (["se", "so", "da", "di"], "Purva Bhadrapada", "Aquarius/Pisces (कुंभ/मीन)", "Saturn/Jupiter", "Jupiter (गुरु)"),
    (["du", "tha", "jha", "nya"], "Uttara Bhadrapada", "Pisces (मीन)", "Jupiter (गुरु)", "Saturn (शनि)"),
    (["de", "do", "cha", "chi", "ch"], "Revati", "Pisces (मीन)", "Jupiter (गुरु)", "Mercury (बुध)"),
]

SVARA_TATVA = {
    "A": ("Agni / Akasha (अग्नि/आकाश — सूर्य स्वर)", "नेतृत्व व स्पष्टता"),
    "E": ("Vayu (वायु — गतिशील स्वर)", "बौद्धिकता व अनुकूलन"),
    "I": ("Jala (जल — भावनात्मक स्वर)", "अंतर्ज्ञान व संवेदनशीलता"),
    "O": ("Prithvi (पृथ्वी — स्थिर स्वर)", "व्यावहारिकता व स्थायित्व"),
    "U": ("Akasha / Vayu (आकाश/वायु — विस्तार स्वर)", "उदारता व रचनात्मकता"),
}

# ---------------------------------------------------------------------------
# HELPER FUNCTIONS
# ---------------------------------------------------------------------------
def reduce_chain(n):
    """Reduce positive integer n to single digit 1..9, returning full reduction chain."""
    n = abs(int(n))
    if n == 0:
        return [0]
    chain = [n]
    while n > 9:
        n = sum(map(int, str(n)))
        chain.append(n)
    return chain


def reduce_keep_master(n):
    """Reduce integer n, noting Master numbers (11, 22, 33) and Karmic Debts (13, 14, 16, 19)."""
    chain = reduce_chain(n)
    masters = [x for x in chain if x in (11, 22, 33)]
    karmic = [x for x in chain if x in (13, 14, 16, 19)]
    return {
        "final": chain[-1],
        "chain": chain,
        "master_number": masters[0] if masters else None,
        "karmic_debt": karmic[0] if karmic else None,
    }


def word_score(w, table):
    return sum(table.get(c, 0) for c in w.upper() if c.isalpha())


def parse_hhmm(s):
    if not s:
        return None
    parts = s.strip().split(":")
    return int(parts[0]) * 60 + int(parts[1])


def compute_katapayadi_and_svara(name):
    """Compute classical Katapayadi Sankhya and Svara/Avakahada phonetics for the first name."""
    if not name or not name.strip():
        return None
    first_word = name.strip().split()[0]
    w_low = first_word.lower()

    # Check if Devanagari characters are present
    dev_digits = [DEVANAGARI_KATAPAYADI[ch] for ch in first_word if ch in DEVANAGARI_KATAPAYADI]
    if dev_digits:
        digits = dev_digits
    else:
        # Parse Roman phonetic syllables (conjunct rule: if consecutive consonants without vowel, take last consonant before vowel)
        i = 0
        raw_consonants = []
        vowels_rom = set("aeiouy")
        while i < len(w_low):
            if not w_low[i].isalpha():
                i += 1
                continue
            if w_low[i] in "aeiou":
                i += 1
                continue
            matched = False
            for tok, val in ROMAN_KATAPAYADI_TOKENS:
                if w_low.startswith(tok, i):
                    after = i + len(tok)
                    has_vowel_after = after < len(w_low) and w_low[after] in vowels_rom
                    raw_consonants.append((tok, val, has_vowel_after))
                    i = after
                    matched = True
                    break
            if not matched:
                i += 1
        # Apply "मिश्रिते तु परो हल् स्यात्" (in conjuncts, only the consonant attached to a vowel counts)
        digits = [val for idx, (_, val, has_v) in enumerate(raw_consonants) if has_v or idx == len(raw_consonants) - 1]
        if not digits and raw_consonants:
            digits = [raw_consonants[0][1]]

    # "अङ्कानां वामतो गतिः" (digits are read right-to-left)
    reversed_digits = list(reversed(digits))
    katapayadi_number = int("".join(map(str, reversed_digits))) if reversed_digits else 0
    mod9 = (katapayadi_number % 9) or (9 if katapayadi_number > 0 else 1)
    rashi_idx = (katapayadi_number % 12) or 12
    rashis = [
        "Aries (मेष)", "Taurus (वृषभ)", "Gemini (मिथुन)", "Cancer (कर्क)",
        "Leo (सिंह)", "Virgo (कन्या)", "Libra (तुला)", "Scorpio (वृश्चिक)",
        "Sagittarius (धनु)", "Capricorn (मकर)", "Aquarius (कुंभ)", "Pisces (मीन)",
    ]

    # Svara & Avakahada lookup
    first_vowel = next((c.upper() for c in first_word if c.upper() in VOWELS), "A")
    svara_elem, svara_meaning = SVARA_TATVA.get(first_vowel, SVARA_TATVA["A"])

    avakahada_match = {
        "matched_syllable": w_low[:2],
        "nakshatra": "General Nama-Nakshatra",
        "rashi": rashis[rashi_idx - 1],
        "rashi_lord": "Derived via Katapayadi",
        "nakshatra_lord": RULER[mod9],
    }
    # Match longest prefix first
    best_len = 0
    for prefs, nak_name, r_name, r_lord, n_lord in AVAKAHADA_PREFIXES:
        for p in prefs:
            if w_low.startswith(p) and len(p) > best_len:
                best_len = len(p)
                avakahada_match = {
                    "matched_syllable": p,
                    "nakshatra": nak_name,
                    "rashi": r_name,
                    "rashi_lord": r_lord,
                    "nakshatra_lord": n_lord,
                }

    return {
        "first_name": first_word,
        "katapayadi_consonant_digits_ltr": digits,
        "katapayadi_reversed_number_rtl": katapayadi_number,
        "katapayadi_anka": mod9,
        "katapayadi_ruler": RULER[mod9],
        "katapayadi_ruler_hi": RULER_HI[mod9],
        "katapayadi_rashi": rashis[rashi_idx - 1],
        "svara_first_vowel": first_vowel,
        "svara_tatva": svara_elem,
        "svara_effect_hi": svara_meaning,
        "avakahada_nama_akshara": avakahada_match,
    }


def evaluate_name_audit(full_name, friendly_set, anti_set):
    """Audit First Name vs Full Name with Chaldean 10-52 compound meanings."""
    if not full_name or not full_name.strip():
        return None
    words = [w for w in full_name.strip().split() if any(c.isalpha() for c in w)]
    if not words:
        return None

    def analyze_segment(label, text):
        w_scores = [word_score(w, CH) for w in text.split()]
        total = sum(w_scores)
        red = reduce_keep_master(total)
        val = red["final"]
        lookup_comp = total
        if lookup_comp > 52:
            # First check if digit sum is in 10..52 (e.g. 56 -> 11), else step down by 9-octave into 10..52
            d_sum = sum(map(int, str(lookup_comp)))
            if 10 <= d_sum <= 52:
                lookup_comp = d_sum
            else:
                while lookup_comp > 52:
                    lookup_comp -= 9
        comp_info = CHALDEAN_COMPOUNDS_10_52.get(
            lookup_comp,
            {
                "title": f"Compound {total} -> {val} ({RULER[val]})",
                "status": "Neutral",
                "hi": f"कुल अंक {total} से मूलांक {val} ({RULER_HI[val]}) की ऊर्जा सक्रिय होती है।",
                "en": f"Compound {total} channels the planetary vibration of {val} ({RULER[val]}).",
            },
        )
        if val in friendly_set:
            alignment = "Harmonious / Friendly (मित्र अंक — शुभ)"
        elif val in anti_set:
            alignment = "Challenging / Anti-Number (विरोधी अंक — सावधानी)"
        else:
            alignment = "Neutral / Balanced (सम अंक — सामान्य)"

        return {
            "label": label,
            "name": text,
            "words": text.split(),
            "word_scores_chaldean": w_scores,
            "compound_number": total,
            "reduced_number": val,
            "reduction_chain": red["chain"],
            "ruler": RULER[val],
            "ruler_hi": RULER_HI[val],
            "compound_title": comp_info["title"],
            "compound_status": comp_info["status"],
            "compound_meaning_hi": comp_info["hi"],
            "compound_meaning_en": comp_info["en"],
            "alignment_with_birth_numbers": alignment,
        }

    first_audit = analyze_segment("First Name (प्रथम नाम — दैनिक पुकार व व्यक्तिगत ऊर्जा)", words[0])
    full_audit = analyze_segment("Full Name (पूर्ण नाम — आधिकारिक पहचान व भाग्य हस्ताक्षर)", " ".join(words))

    # Comparison & actionable advice
    first_ok = first_audit["reduced_number"] in friendly_set and first_audit["compound_status"] != "Caution"
    full_ok = full_audit["reduced_number"] in friendly_set and full_audit["compound_status"] != "Caution"

    if first_ok and full_ok:
        verdict_hi = (
            f"प्रथम नाम ({first_audit['compound_number']}/{first_audit['reduced_number']}) और पूर्ण नाम "
            f"({full_audit['compound_number']}/{full_audit['reduced_number']}) दोनों आपके मूलांक-भाग्यांक के अनुकूल हैं। नाम बदलने की कोई आवश्यकता नहीं है।"
        )
    elif first_ok and not full_ok:
        verdict_hi = (
            f"आपका प्रथम नाम '{words[0]}' ({first_audit['compound_number']}/{first_audit['reduced_number']}) शुभ व अनुकूल है, "
            f"जबकि पूर्ण नाम ({full_audit['compound_number']}/{full_audit['reduced_number']}) थोड़ा भारी/संघर्षपूर्ण है। "
            f"दैनिक व्यवहार और परिचय में प्रथम नाम '{words[0]}' का अधिक प्रयोग करें; आधिकारिक दस्तावेजों में नाम बदलने की आवश्यकता नहीं है।"
        )
    elif not first_ok and full_ok:
        verdict_hi = (
            f"आपका पूर्ण नाम ({full_audit['compound_number']}/{full_audit['reduced_number']}) आपके भाग्यांक के साथ उत्तम सामंजस्य में है। "
            f"महत्वपूर्ण कार्यों, हस्ताक्षर और प्रोफाइल में हमेशा अपना पूर्ण नाम ('{' '.join(words)}') ही लिखें।"
        )
    else:
        best_targets = sorted(list(friendly_set))
        verdict_hi = (
            f"प्रथम नाम ({first_audit['compound_number']}/{first_audit['reduced_number']}) और पूर्ण नाम "
            f"({full_audit['compound_number']}/{full_audit['reduced_number']}) में कर्म-संघर्ष की अधिकता है। "
            f"बिना सरकारी दस्तावेज बदले, अपने हस्ताक्षर या ब्रांड/प्रोफाइल को मित्र अंकों ({', '.join(map(str, best_targets))}; "
            f"विशेषकर यौगिक 15, 17, 19, 21, 23, 24, 27, 32, 37) के अनुरूप संरेखित करना सहायक रहेगा।"
        )

    return {
        "first_name_audit": first_audit,
        "full_name_audit": full_audit,
        "verdict_hi": verdict_hi,
        "recommended_lucky_compounds": [
            {"compound": c, "single": reduce_chain(c)[-1], "title": CHALDEAN_COMPOUNDS_10_52[c]["title"]}
            for c in (15, 17, 19, 21, 23, 24, 27, 32, 33, 37, 41, 45, 46, 50, 51)
            if reduce_chain(c)[-1] in friendly_set
        ],
    }


def compute_vedic_45yr_dasha(dob_date, mulank, target_date=None):
    """Compute the 45-year Vedic Numerology Mahadasha & Antardasha cycle + Weekday-linked Annual Dasha."""
    if target_date is None:
        target_date = date.today()

    # 1. 45-Year Mahadasha & Antardasha Tree (covering 95 years from birth)
    cur_date = dob_date
    mahadashas = []
    active_maha = None
    active_antar = None

    for cycle in range(1, 3):  # Two 45-year cycles = 90 years + 1 extra
        for step in range(9):
            m_num = ((mulank - 1 + step) % 9) + 1
            duration_years = m_num  # Planet N runs for N years! Total = 1+2+..+9 = 45 years
            duration_days = duration_years * 365.2425
            m_end = cur_date + timedelta(days=duration_days)

            # Antardashas inside Mahadasha m_num: sub-lord a_num runs for (m_num * a_num / 45) years
            a_cur = cur_date
            antardashas = []
            for a_step in range(9):
                a_num = ((m_num - 1 + a_step) % 9) + 1
                a_days = duration_days * (a_num / 45.0)
                a_end = a_cur + timedelta(days=a_days)
                antar_entry = {
                    "antar_number": a_num,
                    "antar_ruler": RULER[a_num],
                    "antar_ruler_hi": RULER_HI[a_num],
                    "start": a_cur.isoformat(),
                    "end": a_end.isoformat(),
                    "duration_months": round(a_days / 30.437, 1),
                }
                antardashas.append(antar_entry)
                if a_cur <= target_date < a_end:
                    active_antar = antar_entry
                a_cur = a_end

            maha_entry = {
                "cycle": cycle,
                "maha_number": m_num,
                "maha_ruler": RULER[m_num],
                "maha_ruler_hi": RULER_HI[m_num],
                "duration_years": duration_years,
                "start": cur_date.isoformat(),
                "end": m_end.isoformat(),
                "age_start": round((cur_date - dob_date).days / 365.2425, 1),
                "age_end": round((m_end - dob_date).days / 365.2425, 1),
                "antardashas": antardashas,
            }
            mahadashas.append(maha_entry)
            if cur_date <= target_date < m_end:
                active_maha = maha_entry
            cur_date = m_end

    # 2. Weekday-Linked Vedic Annual Dasha (Varsha Dasha / Pratyantardasha) for current_year - 1 .. current_year + 5
    # Python weekday(): Monday=0 .. Sunday=6
    # Vedic Weekday Graha-Anka: Monday=2 (Moon), Tuesday=9 (Mars), Wednesday=5 (Mercury),
    # Thursday=3 (Jupiter), Friday=6 (Venus), Saturday=8 (Saturn), Sunday=1 (Sun)
    WEEKDAY_ANKA = {
        0: (2, "Monday (सोमवार — चंद्र)"),
        1: (9, "Tuesday (मंगलवार — मंगल)"),
        2: (5, "Wednesday (बुधवार — बुध)"),
        3: (3, "Thursday (गुरुवार — गुरु)"),
        4: (6, "Friday (शुक्रवार — शुक्र)"),
        5: (8, "Saturday (शनिवार — शनि)"),
        6: (1, "Sunday (रविवार — सूर्य)"),
    }

    annual_dashas = []
    active_annual = None
    cy = target_date.year
    for yr in range(cy - 1, cy + 6):
        try:
            bday = date(yr, dob_date.month, dob_date.day)
        except ValueError:
            bday = date(yr, dob_date.month, 28)
        try:
            next_bday = date(yr + 1, dob_date.month, dob_date.day)
        except ValueError:
            next_bday = date(yr + 1, dob_date.month, 28)

        wd_num, wd_label = WEEKDAY_ANKA[bday.weekday()]
        yr_last2 = yr % 100
        # Classical Vedic Varsha Dasha formula: Day + Month + Target_Year_Last_2_Digits + Birthday_Weekday_Anka
        vedic_varsha_total = dob_date.day + dob_date.month + yr_last2 + wd_num
        vedic_varsha_num = reduce_chain(vedic_varsha_total)[-1]
        # Western/Standard Personal Year: Day + Month + sum_digits(Year)
        personal_yr_num = reduce_chain(dob_date.day + dob_date.month + sum(map(int, str(yr))))[-1]

        entry = {
            "year": yr,
            "period_start": bday.isoformat(),
            "period_end": next_bday.isoformat(),
            "birthday_weekday": wd_label,
            "weekday_anka": wd_num,
            "vedic_annual_dasha_number": vedic_varsha_num,
            "vedic_annual_dasha_ruler": RULER[vedic_varsha_num],
            "vedic_annual_dasha_ruler_hi": RULER_HI[vedic_varsha_num],
            "personal_year_number": personal_yr_num,
            "personal_year_ruler": RULER[personal_yr_num],
            "theme_hi": GRAHA_PROFILE[vedic_varsha_num]["archetype_hi"],
        }
        annual_dashas.append(entry)
        if bday <= target_date < next_bday:
            active_annual = entry

    return {
        "system": "45-Year Vedic Graha-Anka Mahadasha (1+2+3+4+5+6+7+8+9 = 45 Years) + Weekday-Linked Varsha Dasha",
        "target_date": target_date.isoformat(),
        "active_mahadasha": {k: v for k, v in (active_maha or {}).items() if k != "antardashas"},
        "active_antardasha": active_antar,
        "active_annual_dasha": active_annual,
        "annual_dasha_timeline": annual_dashas,
        "mahadasha_timeline": mahadashas,
    }


def build_century_free_vedic_grid(d, mth, y, mulank, bhagyank, active_maha_num=None, active_annual_num=None):
    """Build the authentic Century-Free Vedic Surya Grid (3-1-9 / 6-7-5 / 2-8-4) and evaluate all 37 Vedic Yogas."""
    # Digits included in Century-Free Vedic Grid:
    # 1. Day digits (nonzero)
    # 2. Month digits (nonzero)
    # 3. Last two digits of Year (nonzero) -- century digits (19/20) are strictly excluded!
    # 4. Mulank (if day > 9, otherwise already counted once in day digits)
    # 5. Bhagyank (always added as destiny anchor)
    day_digits = [int(c) for c in str(d) if c != "0"]
    month_digits = [int(c) for c in str(mth) if c != "0"]
    year_last2_str = f"{y % 100:02d}" if y is not None else ""
    year_last2_digits = [int(c) for c in year_last2_str if c != "0"]

    natal_digits = list(day_digits) + list(month_digits) + list(year_last2_digits)
    if d > 9:
        natal_digits.append(mulank)
    if y is not None:
        natal_digits.append(bhagyank)

    counts = {i: natal_digits.count(i) for i in range(1, 10)}
    present_set = {i for i, c in counts.items() if c > 0}
    missing_list = [i for i, c in counts.items() if c == 0]

    # Visual 3x3 matrix representation (3-1-9 / 6-7-5 / 2-8-4)
    visual_rows = []
    for row in VEDIC_GRID_LAYOUT:
        visual_rows.append([
            {
                "cell_number": num,
                "ruler": RULER[num],
                "ruler_hi": RULER_HI[num],
                "count": counts[num],
                "display": str(num) * counts[num] if counts[num] > 0 else "·",
                "dasha_overlay": [
                    tag for tag, dn in (("MD", active_maha_num), ("AD", active_annual_num)) if dn == num
                ],
            }
            for num in row
        ])

    # Evaluate all 37 Vedic Yogas
    active_yogas = []
    partial_8_planes = []
    for yg in VEDIC_37_YOGAS:
        pat = yg["pattern"]
        have = [x for x in pat if x in present_set]
        if len(have) == len(pat):
            # Weight strength by repetition count of constituent numbers
            total_reps = sum(counts[x] for x in pat)
            active_yogas.append({
                **yg,
                "status": "Active / Complete (पूर्ण सक्रिय योग)",
                "total_digit_repetitions": total_reps,
            })
        elif yg["id"] <= 8 and len(have) == 2:
            missing_in_plane = [x for x in pat if x not in present_set][0]
            partial_8_planes.append({
                **yg,
                "status": "Partial (2/3 — 67%)",
                "present_numbers": have,
                "missing_number": missing_in_plane,
                "activated_by_dasha": missing_in_plane in (active_maha_num, active_annual_num),
            })

    return {
        "grid_name": "Vedic Surya Grid (वैदिक सूर्य यंत्र ग्रिड: 3-1-9 / 6-7-5 / 2-8-4 — Century-Free)",
        "layout": VEDIC_GRID_LAYOUT,
        "century_digits_excluded": str(y)[:2] if (y and y >= 1000) else None,
        "input_breakdown": {
            "day_digits": day_digits,
            "month_digits": month_digits,
            "year_last_two_digits": year_last2_digits,
            "mulank_added": mulank if d > 9 else "(included in single-digit day)",
            "bhagyank_added": bhagyank if y is not None else None,
            "all_natal_grid_digits": natal_digits,
        },
        "digit_counts": counts,
        "present_numbers": sorted(list(present_set)),
        "missing_numbers": missing_list,
        "visual_grid": visual_rows,
        "vedic_yogas_summary": {
            "total_catalog_yogas": len(VEDIC_37_YOGAS),
            "active_count": len(active_yogas),
            "active_yogas": active_yogas,
            "nearly_complete_primary_planes": partial_8_planes,
        },
    }


def build_loshu_and_repetitions(d, mth, y, mulank, bhagyank, gender="male"):
    """Build comparative Lo Shu Grid (4-9-2 / 3-5-7 / 8-1-6) with Kua and 1x/2x/3x/4x+ repetition diagnostics."""
    full_str = f"{y or ''}{mth:02d}{d:02d}"
    raw_digits = [int(c) for c in full_str if c.isdigit() and c != "0"]
    if d > 9:
        raw_digits.append(mulank)
    if y is not None:
        raw_digits.append(bhagyank)

    # Kua Number
    kua = None
    if y is not None:
        y_sum = reduce_chain(y)[-1]
        k_male = reduce_chain(11 - y_sum)[-1]
        k_female = reduce_chain(y_sum + 4)[-1]
        kua = {
            "male": k_male,
            "female": k_female,
            "selected_gender": gender,
            "active_kua": k_female if str(gender).lower().startswith("f") else k_male,
        }

    counts = {i: raw_digits.count(i) for i in range(1, 10)}
    present_set = {i for i, c in counts.items() if c > 0}

    planes_eval = []
    for p_name, pat, meaning_hi in LOSHU_PLANES:
        have = [x for x in pat if x in present_set]
        pct = round(len(have) / 3 * 100)
        planes_eval.append({
            "plane": p_name,
            "pattern": pat,
            "present": have,
            "missing": [x for x in pat if x not in present_set],
            "completion_percent": pct,
            "status": "Complete (100%)" if pct == 100 else f"Partial ({pct}%)" if pct > 0 else "Missing (0%)",
            "meaning_hi": meaning_hi,
        })

    # Repetition & Missing Diagnostics (0x, 1x, 2x, 3x, 4x+)
    repetition_diagnostics = {}
    over_repeated_alerts = []
    for num in range(1, 10):
        c = counts[num]
        tier = min(c, 4)
        rule_text = REPETITION_RULES[num][tier]
        repetition_diagnostics[num] = {
            "number": num,
            "ruler": RULER[num],
            "ruler_hi": RULER_HI[num],
            "count": c,
            "tier": "Missing (0x)" if c == 0 else "Balanced (1x)" if c == 1 else "Strong (2x)" if c == 2 else "Excessive (3x)" if c == 3 else f"Extreme ({c}x)",
            "diagnostic_hi": rule_text,
        }
        if c >= 3:
            over_repeated_alerts.append(repetition_diagnostics[num])

    return {
        "grid_name": "Lo Shu Grid (लो-शू ग्रिड: 4-9-2 / 3-5-7 / 8-1-6 — Full YYYY-MM-DD)",
        "layout": LOSHU_LAYOUT,
        "all_loshu_digits": raw_digits,
        "digit_counts": counts,
        "kua_number": kua,
        "planes_of_expression": planes_eval,
        "repetition_diagnostics": repetition_diagnostics,
        "over_repetition_alerts_3x_plus": over_repeated_alerts,
    }


def compute_pythagorean_and_pinnacles(name, d, mth, y, cy):
    """Compute Pythagorean Expression/Soul Urge/Personality, 4 Life Pinnacles & Challenges, and 12 Personal Months."""
    pyth = None
    if name and name.strip():
        words = name.strip().split()
        exp_words = [word_score(w, PY) for w in words]
        exp_tot = sum(exp_words)
        soul_tot = sum(PY.get(c, 0) for c in name.upper() if c in VOWELS)
        pers_tot = sum(PY.get(c, 0) for c in name.upper() if c.isalpha() and c not in VOWELS)

        exp_red = reduce_keep_master(exp_tot)
        soul_red = reduce_keep_master(soul_tot)
        pers_red = reduce_keep_master(pers_tot)

        pyth = {
            "expression_destiny": {
                "total": exp_tot,
                "value": exp_red["final"],
                "chain": exp_red["chain"],
                "master": exp_red["master_number"],
                "ruler": RULER.get(exp_red["final"]),
            },
            "soul_urge_hearts_desire": {
                "total": soul_tot,
                "value": soul_red["final"],
                "chain": soul_red["chain"],
                "master": soul_red["master_number"],
                "ruler": RULER.get(soul_red["final"]),
            },
            "personality_outer_persona": {
                "total": pers_tot,
                "value": pers_red["final"],
                "chain": pers_red["chain"],
                "master": pers_red["master_number"],
                "ruler": RULER.get(pers_red["final"]),
            },
        }

    # 4 Pinnacles & 4 Challenges
    pinnacles = None
    if y is not None:
        m_r = reduce_chain(mth)[-1]
        d_r = reduce_chain(d)[-1]
        y_r = reduce_chain(y)[-1]
        lp = reduce_chain(m_r + d_r + y_r)[-1]

        p1 = reduce_keep_master(m_r + d_r)
        p2 = reduce_keep_master(d_r + y_r)
        p3 = reduce_keep_master(p1["final"] + p2["final"])
        p4 = reduce_keep_master(m_r + y_r)

        c1 = abs(m_r - d_r)
        c2 = abs(d_r - y_r)
        c3 = abs(c1 - c2)
        c4 = abs(m_r - y_r)

        p1_end = 36 - lp
        p2_end = p1_end + 9
        p3_end = p2_end + 9

        pinnacles = [
            {"stage": 1, "ages": f"0 to {p1_end}", "years": f"{y}–{y + p1_end}", "pinnacle": p1["final"], "master": p1["master_number"], "pinnacle_ruler": RULER[p1["final"]], "challenge": c1},
            {"stage": 2, "ages": f"{p1_end + 1} to {p2_end}", "years": f"{y + p1_end + 1}–{y + p2_end}", "pinnacle": p2["final"], "master": p2["master_number"], "pinnacle_ruler": RULER[p2["final"]], "challenge": c2},
            {"stage": 3, "ages": f"{p2_end + 1} to {p3_end}", "years": f"{y + p2_end + 1}–{y + p3_end}", "pinnacle": p3["final"], "master": p3["master_number"], "pinnacle_ruler": RULER[p3["final"]], "challenge": c3},
            {"stage": 4, "ages": f"{p3_end + 1}+", "years": f"{y + p3_end + 1} onwards", "pinnacle": p4["final"], "master": p4["master_number"], "pinnacle_ruler": RULER[p4["final"]], "challenge": c4},
        ]

    # Personal Year & 12 Personal Months
    py_cur = reduce_chain(d + mth + sum(map(int, str(cy))))[-1]
    month_names_hi = [
        "जनवरी", "फरवरी", "मार्च", "अप्रैल", "मई", "जून",
        "जुलाई", "अगस्त", "सितंबर", "अक्टूबर", "नवंबर", "दिसंबर",
    ]
    personal_months = []
    for m_idx in range(1, 13):
        pm = reduce_chain(py_cur + m_idx)[-1]
        personal_months.append({
            "month": m_idx,
            "month_name_hi": month_names_hi[m_idx - 1],
            "personal_month_number": pm,
            "ruler": RULER[pm],
            "ruler_hi": RULER_HI[pm],
        })

    return pyth, pinnacles, personal_months


def cross_verify_with_chart(mulank, bhagyank, chart_data):
    """Cross-verify Mulank and Bhagyank planetary rulers against actual natal D1/D9/SAV chart data."""
    if not chart_data or "planets" not in chart_data:
        return None
    planets = chart_data["planets"]
    sav = chart_data.get("ashtakavarga", {}).get("sarvashtakavarga_houses", {})

    def check_ruler(role_label, num):
        p_name = RULER[num]
        p_info = planets.get(p_name, {})
        h = p_info.get("house")
        dig = p_info.get("dignity") or "neutral/normal"
        d9_s = p_info.get("d9_sign")
        d9_d = p_info.get("d9_dignity") or ""
        retro = p_info.get("retrograde", False)
        combust = p_info.get("combust", False)
        vargottama = p_info.get("vargottama", False)
        shadbala_ratio = p_info.get("shadbala_ratio")
        house_sav = sav.get(str(h)) or sav.get(h)

        strength_tags = []
        if dig in ("exalted", "own sign", "moolatrikona"):
            strength_tags.append(f"D1 {dig}")
        if vargottama:
            strength_tags.append("Vargottama (D1=D9)")
        if d9_d in ("exalted", "own sign"):
            strength_tags.append(f"D9 {d9_d}")
        if retro and p_name not in ("Rahu", "Ketu"):
            strength_tags.append("Vakri (High Cheshta Bala)")
        if combust:
            strength_tags.append("Combust (Asta)")

        is_strong = (
            dig in ("exalted", "own sign", "moolatrikona")
            or vargottama
            or d9_d in ("exalted", "own sign")
            or (shadbala_ratio and shadbala_ratio >= 1.0)
        ) and dig != "debilitated"

        verdict_hi = (
            f"{role_label} {num} का स्वामी ग्रह **{RULER_HI[num]}** जन्म कुंडली (D1) में **भाव {h} ({p_info.get('sign')})** में "
            f"**{dig}** अवस्था में तथा नवांश (D9) में **{d9_s}** राशि में स्थित है। "
            + (
                f"कुंडली में {RULER_HI[num]} बली होने के कारण अंक {num} के उच्च और सकारात्मक गुण (नेतृत्व/स्थायित्व/सफलता) पूर्ण रूप से फलित होते हैं।"
                if is_strong
                else f"कुंडली में {RULER_HI[num]} को अतिरिक्त बल व अनुशासन की आवश्यकता है, अतः अंक {num} के परिणाम धैर्य और सचेत प्रयास से ही खुलते हैं।"
            )
        )

        return {
            "role": role_label,
            "number": num,
            "planet": p_name,
            "planet_hi": RULER_HI[num],
            "d1_sign": p_info.get("sign"),
            "d1_house": h,
            "d1_dignity": dig,
            "d9_sign": d9_s,
            "d9_dignity": d9_d,
            "vargottama": vargottama,
            "retrograde": retro,
            "combust": combust,
            "shadbala_ratio": shadbala_ratio,
            "house_sav_bindus": house_sav,
            "strength_tags": strength_tags,
            "natal_support_strong": is_strong,
            "synthesis_hi": verdict_hi,
        }

    return {
        "mulank_chart_synergy": check_ruler("मूलांक (Driver)", mulank),
        "bhagyank_chart_synergy": check_ruler("भाग्यांक (Conductor)", bhagyank),
    }


# ---------------------------------------------------------------------------
# MAIN RUNNER (BACKWARD-COMPATIBLE + ALL 12 VEDIC UPGRADES)
# ---------------------------------------------------------------------------
def run(name="", dob="", tob=None, sunrise="06:00", gender="male", chart_data=None):
    out = {}
    parts = dob.strip().split("-")
    y = int(parts[0]) if len(parts) == 3 else None
    mth = int(parts[-2])
    d = int(parts[-1])

    # 1. Civil Mulank & Sunrise Mulank Rule (Surya Siddhanta Savana Dina)
    civil_mulank_chain = reduce_chain(d)
    civil_mulank = civil_mulank_chain[-1]

    tob_min = parse_hhmm(tob)
    sun_min = parse_hhmm(sunrise or "06:00")
    pre_sunrise = (tob_min is not None and sun_min is not None and tob_min < sun_min)

    if y is not None:
        civil_date = date(y, mth, d)
        savana_date = civil_date - timedelta(days=1) if pre_sunrise else civil_date
    else:
        civil_date = None
        savana_date = None

    savana_day = savana_date.day if savana_date else (d - 1 if (pre_sunrise and d > 1) else d)
    savana_mulank = reduce_chain(savana_day)[-1]

    sub_p = BIRTH_DAY_SUBPERSONALITIES.get(d, BIRTH_DAY_SUBPERSONALITIES[civil_mulank])

    # Keep top-level backward-compatible keys while enriching them
    out["birth_number"] = {
        "value": civil_mulank,
        "chain": civil_mulank_chain,
        "ruler": RULER[civil_mulank],
        "ruler_hi": RULER_HI[civil_mulank],
        "day": d,
        "sub_personality": sub_p,
        "graha_profile": GRAHA_PROFILE[civil_mulank],
    }

    out["sunrise_mulank_rule"] = {
        "tob": tob,
        "local_sunrise": sunrise,
        "born_before_sunrise": pre_sunrise,
        "civil_day": d,
        "civil_mulank": civil_mulank,
        "civil_mulank_ruler": RULER[civil_mulank],
        "vedic_savana_day": savana_day,
        "vedic_savana_mulank": savana_mulank,
        "vedic_savana_mulank_ruler": RULER[savana_mulank],
        "note_hi": (
            f"जन्म समय ({tob}) सूर्योदय ({sunrise}) से पूर्व होने के कारण सूर्य सिद्धांत (सावन दिन) के अनुसार "
            f"आंतरिक/आध्यात्मिक मूलांक {savana_mulank} ({RULER_HI[savana_mulank]}) तथा व्यावहारिक/दस्तावेजी मूलांक "
            f"{civil_mulank} ({RULER_HI[civil_mulank]}) दोनों का प्रभाव रहेगा।"
            if pre_sunrise
            else f"जन्म सूर्योदय ({sunrise}) के पश्चात (अथवा मानक दिन में) होने से वैदिक सावन मूलांक और सिविल मूलांक दोनों एक ही हैं: {civil_mulank} ({RULER_HI[civil_mulank]})।"
        ),
    }

    out["birth_month_number"] = {
        "value": reduce_chain(mth)[-1],
        "ruler": RULER[reduce_chain(mth)[-1]],
        "ruler_hi": RULER_HI[reduce_chain(mth)[-1]],
    }

    # 2. Bhagyank (Life Path / Conductor), Age-35 Transition, 81 Combinations & Bridge Number
    cy = date.today().year
    bhagyank = civil_mulank
    if y is not None:
        # Digit sum and 3-cycle sum always yield the same final digit mod 9, but 3-cycle preserves intermediate master/karmic sums accurately
        digit_sum_total = sum(map(int, f"{d:02d}{mth:02d}{y}"))
        cycle_sum_total = reduce_chain(d)[-1] + reduce_chain(mth)[-1] + reduce_chain(y)[-1]
        lp_red = reduce_keep_master(digit_sum_total)
        bhagyank = lp_red["final"]
        current_age = cy - y
        transition_year = y + 35

        out["life_path"] = {
            "value": bhagyank,
            "chain": lp_red["chain"],
            "three_cycle_sum": cycle_sum_total,
            "master_number": lp_red["master_number"],
            "karmic_debt": lp_red["karmic_debt"],
            "ruler": RULER[bhagyank],
            "ruler_hi": RULER_HI[bhagyank],
            "graha_profile": GRAHA_PROFILE[bhagyank],
            "age_35_transition": {
                "transition_age": 35,
                "transition_calendar_year": transition_year,
                "current_age": current_age,
                "current_phase": (
                    "Bhagyank / Conductor Dominant Phase (70% भाग्यांक + 30% मूलांक)"
                    if current_age >= 35
                    else "Transition Threshold Window (मूलांक से भाग्यांक में रूपांतरण काल: 50%-50%)"
                    if 32 <= current_age < 35
                    else "Mulank / Driver Dominant Phase (70% मूलांक + 30% भाग्यांक)"
                ),
                "explanation_hi": (
                    f"वैदिक अंक-ज्योतिष में 35 वर्ष की आयु (वर्ष {transition_year}) से भाग्यांक {bhagyank} ({RULER_HI[bhagyank]}) "
                    f"जीवन की मुख्य कमान (70% प्रभाव) संभालता है, जबकि मूलांक {civil_mulank} ({RULER_HI[civil_mulank]}) 30% आंतरिक स्वभाव के रूप में कार्य करता है।"
                ),
            },
        }
        out["birth_year_number"] = reduce_chain(y)[-1]

    # 3. 81 Driver-Conductor Combination & Bridge Number
    dc_rating, dc_title, dc_note_hi = DRIVER_CONDUCTOR_RATINGS[(civil_mulank, bhagyank)]
    bridge_raw = abs(civil_mulank - bhagyank)
    bridge_num = bridge_raw if bridge_raw > 0 else civil_mulank

    m_rel = NUMBER_RELATIONS[civil_mulank]
    b_rel = NUMBER_RELATIONS[bhagyank]
    mutual_friendly = sorted(list((set(m_rel["friendly"]) & set(b_rel["friendly"])) - set(m_rel["anti"]) - set(b_rel["anti"])))
    mutual_anti = sorted(list(set(m_rel["anti"]) | set(b_rel["anti"])))
    mutual_neutral = sorted([n for n in range(1, 10) if n not in mutual_friendly and n not in mutual_anti])

    out["driver_conductor_synergy"] = {
        "driver_mulank": civil_mulank,
        "driver_ruler": RULER[civil_mulank],
        "conductor_bhagyank": bhagyank,
        "conductor_ruler": RULER[bhagyank],
        "combination_code": f"{civil_mulank}-{bhagyank}",
        "compatibility_rating_out_of_5": dc_rating,
        "compatibility_score_out_of_10": int(dc_rating * 2),
        "archetype_title": dc_title,
        "synthesis_hi": dc_note_hi,
        "bridge_number": {
            "value": bridge_num,
            "formula": f"|{civil_mulank} - {bhagyank}| = {bridge_raw}" + (f" (Self-Harmonic {bridge_num})" if bridge_raw == 0 else ""),
            "ruler": RULER[bridge_num],
            "ruler_hi": RULER_HI[bridge_num],
            "how_to_use_hi": (
                f"मूलांक {civil_mulank} ({RULER_HI[civil_mulank]}) और भाग्यांक {bhagyank} ({RULER_HI[bhagyank]}) के बीच सेतु अंक "
                f"**{bridge_num} ({RULER_HI[bridge_num]})** है। अपने आंतरिक स्वभाव और बाहरी भाग्य में सामंजस्य बैठाने के लिए "
                f"{RULER_HI[bridge_num]} के गुण ({GRAHA_PROFILE[bridge_num]['archetype_hi']}) को अपनी कार्यशैली का माध्यम बनाएं।"
            ),
        },
        "number_relationships": {
            "mulank_relations": m_rel,
            "bhagyank_relations": b_rel,
            "combined_mutual_friendly_numbers": mutual_friendly,
            "combined_neutral_numbers": mutual_neutral,
            "combined_anti_avoid_numbers": mutual_anti,
        },
    }

    # 4. 45-Year Vedic Dasha & Weekday-Linked Annual Dasha
    vedic_dasha = None
    active_maha_num = None
    active_annual_num = None
    if civil_date is not None:
        vedic_dasha = compute_vedic_45yr_dasha(civil_date, civil_mulank)
        active_maha_num = (vedic_dasha.get("active_mahadasha") or {}).get("maha_number")
        active_annual_num = (vedic_dasha.get("active_annual_dasha") or {}).get("vedic_annual_dasha_number")
        out["vedic_45yr_dasha"] = vedic_dasha

    # 5. Century-Free Vedic Surya Grid (3-1-9 / 6-7-5 / 2-8-4) & 37 Vedic Yogas
    out["vedic_surya_grid"] = build_century_free_vedic_grid(
        d, mth, y, civil_mulank, bhagyank, active_maha_num, active_annual_num
    )

    # 6. Comparative Lo Shu Grid (4-9-2 / 3-5-7 / 8-1-6) & Over-Repetition Diagnostics
    out["loshu_grid"] = build_loshu_and_repetitions(d, mth, y, civil_mulank, bhagyank, gender=gender)

    # 7. First Name vs Full Name Audit (Chaldean 10-52 Compounds) & Katapayadi/Svara
    if name and name.strip():
        for k, tb in (("name_chaldean", CH), ("name_pythagorean", PY)):
            w_parts = [word_score(w, tb) for w in name.split()]
            tot = sum(w_parts)
            c = reduce_chain(tot)
            out[k] = {
                "letters_per_word": w_parts,
                "total": tot,
                "chain": c,
                "value": c[-1],
                "ruler": RULER[c[-1]],
                "ruler_hi": RULER_HI[c[-1]],
            }
        out["name_audit_chaldean_10_52"] = evaluate_name_audit(
            name, set(mutual_friendly), set(mutual_anti)
        )
        out["katapayadi_and_svara"] = compute_katapayadi_and_svara(name)

    # 8. Pythagorean Core, 4 Pinnacles/Challenges & Personal Year/Months
    pyth_core, pinnacles, personal_months = compute_pythagorean_and_pinnacles(name, d, mth, y, cy)
    if pyth_core:
        out["pythagorean_core_profile"] = pyth_core
    if pinnacles:
        out["pinnacles_and_challenges"] = pinnacles

    py = reduce_chain(d + mth + sum(map(int, str(cy))))[-1]
    py_next = reduce_chain(d + mth + sum(map(int, str(cy + 1))))[-1]
    py_next2 = reduce_chain(d + mth + sum(map(int, str(cy + 2))))[-1]
    out["personal_year"] = {
        "year": cy,
        "value": py,
        "ruler": RULER[py],
        "ruler_hi": RULER_HI[py],
        "next": py_next,
        "next_ruler": RULER[py_next],
        "forecast_4_years": [
            {
                "year": cy + offset,
                "personal_year": reduce_chain(d + mth + sum(map(int, str(cy + offset))))[-1],
                "ruler": RULER[reduce_chain(d + mth + sum(map(int, str(cy + offset))))[-1]],
                "ruler_hi": RULER_HI[reduce_chain(d + mth + sum(map(int, str(cy + offset))))[-1]],
                "theme_hi": GRAHA_PROFILE[reduce_chain(d + mth + sum(map(int, str(cy + offset))))[-1]]["archetype_hi"],
            }
            for offset in range(4)
        ],
        "personal_months_current_year": personal_months,
    }

    # 9. Optional Graha-Anka Birth Chart Cross-Verification
    if chart_data:
        out["graha_anka_chart_synergy"] = cross_verify_with_chart(civil_mulank, bhagyank, chart_data)

    out["caveat"] = (
        "Vedic Anka-Jyotish and comparative numerology are traditional symbolic self-reflection frameworks "
        "with no empirical scientific validation."
    )
    return out


def cli_main():
    ap = argparse.ArgumentParser(description="Vedic Anka-Jyotish & Comparative Numerology Engine")
    ap.add_argument("--name", default="", help="Full Name of the native")
    ap.add_argument("--dob", required=True, help="Date of Birth YYYY-MM-DD (or MM-DD)")
    ap.add_argument("--tob", default=None, help="Optional Time of Birth HH:MM (for Sunrise Mulank rule)")
    ap.add_argument("--sunrise", default="06:00", help="Optional local sunrise HH:MM (default 06:00)")
    ap.add_argument("--gender", default="male", help="male or female (for Kua calculation)")
    ap.add_argument("--chart-json", default=None, help="Optional path to jyotish.py chart JSON output for Graha-Anka cross-verification")
    a = ap.parse_args()

    c_data = None
    if a.chart_json:
        with open(a.chart_json) as f:
            c_data = json.load(f)

    print(json.dumps(run(a.name, a.dob, tob=a.tob, sunrise=a.sunrise, gender=a.gender, chart_data=c_data), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    cli_main()
