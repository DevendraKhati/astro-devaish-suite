#!/usr/bin/env python3
"""Authentic Classical Vedic Jyotish (Parashari + Jaimini + KP + Ganita Skandha) Engine — Astro DevAish Edition.

Grounded in Brihat Parashara Hora Shastra (BPHS), Surya Siddhanta, Brihat Jataka, Phaladeepika,
Jaimini Sutras, Saravali, Jataka Parijata, Uttara Kalamrita, Prasna Marga, and Muhurta Chintamani.

Commands (all print JSON):
  chart    --input person.json
  match    --a bride.json --b groom.json
  dasha    --input person.json [--at YYYY-MM-DD]
  transit  --input person.json [--from YYYY-MM-DD] [--years 3]
  sky      --date YYYY-MM-DD [--time HH:MM] --lat L --lon L [--tz 5.5] [--sidereal]

person.json: {"name","dob":"YYYY-MM-DD","tob":"HH:MM","lat":19.99,"lon":73.79,"tz":5.5,"place":"Nashik"}
Defaults: Lahiri (Chitrapaksha) ayanamsa, Whole-Sign (Rashi Tulya Bhava) + Sripati Bhava Chalit overlay.
"""
import argparse
import json
import math
from datetime import datetime, timedelta

try:
    import swisseph as swe
    swe.set_sid_mode(swe.SIDM_LAHIRI)
    HAS_SWISSEPH = True
except ImportError:
    HAS_SWISSEPH = False

    class _PurePythonSweFallback:
        """Zero-dependency pure-Python NASA JPL / Meeus Sidereal (Lahiri) Ephemeris fallback for Gemini Gems & offline sandboxes."""
        SIDM_LAHIRI = 1
        FLG_MOSEPH = 4
        FLG_SIDEREAL = 65536
        FLG_SPEED = 256
        FLG_EQUATORIAL = 2048
        SUN = 0
        CALC_RISE = 1
        BIT_DISC_CENTER = 256
        EQU2HOR = 0

        _ELEMENTS = {
            "Earth":   ((1.00000261, 0.01671123, -0.00001531, 100.46457166, 102.93768193, 0.0),
                        (0.00000562, -0.00004392, -0.01294668, 35999.37244981, 0.32327364, 0.0)),
            "Mercury": ((0.38709927, 0.20563593, 7.00497902, 252.25032350, 77.45779628, 48.33076593),
                        (0.00000037, 0.00001906, -0.00594749, 149472.67411175, 0.16047689, -0.12534081)),
            "Venus":   ((0.72333566, 0.00677672, 3.39467605, 181.97909950, 131.60246718, 76.67984255),
                        (0.00000390, -0.00004107, -0.00078890, 58517.81538729, 0.00268329, -0.27769418)),
            "Mars":    ((1.52371034, 0.09339410, 1.84969142, -4.55343205, -23.94362959, 49.55953891),
                        (0.00001847, 0.00007882, -0.00813131, 19140.30268499, 0.44441088, -0.29257343)),
            "Jupiter": ((5.20288700, 0.04838624, 1.30439695, 34.39644051, 14.72847983, 100.47390909),
                        (-0.00011607, -0.00013253, -0.00183714, 3034.74612775, 0.21252668, 0.20469106)),
            "Saturn":  ((9.53667594, 0.05386179, 2.48599187, 49.95424423, 92.59887831, 113.66242448),
                        (-0.00125060, -0.00050991, 0.00193609, 1222.49362201, -0.41897216, -0.28867794)),
            "Uranus":  ((19.18916464, 0.04725744, 0.77263783, 313.23810451, 170.95427630, 74.01692503),
                        (-0.00196176, -0.00004397, -0.00242939, 428.48202785, 0.40805281, 0.04240589)),
            "Neptune": ((30.06992276, 0.00859048, 1.77004347, -55.12002969, 44.96476227, 131.78422574),
                        (0.00026291, 0.00005105, 0.00035372, 218.45945325, -0.32241464, -0.00508664)),
        }

        def set_sid_mode(self, mode):
            pass

        def julday(self, y, m, d, h_ut=0.0):
            if m <= 2:
                y -= 1
                m += 12
            A = int(y // 100)
            B = 2 - A + int(A // 4)
            return int(365.25 * (y + 4716)) + int(30.6001 * (m + 1)) + d + h_ut / 24.0 + B - 1524.5

        def revjul(self, jd):
            Z = int(jd + 0.5)
            F = (jd + 0.5) - Z
            if Z < 2299161:
                A = Z
            else:
                alpha = int((Z - 1867216.25) / 36524.25)
                A = Z + 1 + alpha - int(alpha / 4)
            B = A + 1524
            C = int((B - 122.1) / 365.25)
            D = int(365.25 * C)
            E = int((B - D) / 30.6001)
            day = B - D - int(30.6001 * E)
            month = E - 1 if E < 14 else E - 13
            year = C - 4716 if month > 2 else C - 4715
            return year, month, day, F * 24.0

        def _lahiri(self, jd):
            T = (jd - 2451545.0) / 36525.0
            return 23.85308 + (50.290966 / 3600.0) * (T * 100.0) + 0.00011 * (T ** 2)

        def _helio_xyz(self, name, T):
            (a0, e0, I0, L0, wb0, Om0), (da, de, dI, dL, dwb, dOm) = self._ELEMENTS[name]
            a = a0 + da * T
            e = e0 + de * T
            I = math.radians(I0 + dI * T)
            L = (L0 + dL * T) % 360.0
            wb = (wb0 + dwb * T) % 360.0
            Om = math.radians((Om0 + dOm * T) % 360.0)
            w = math.radians((wb - math.degrees(Om)) % 360.0)
            M_deg = (L - wb + 180.0) % 360.0 - 180.0
            zeta = math.radians(5 * ((49.954 + 1222.494 * T) % 360.0) - 2 * ((34.396 + 3034.746 * T) % 360.0) - 67.9)
            if name == "Jupiter":
                M_deg += -0.332 * math.sin(zeta)
            elif name == "Saturn":
                M_deg += 0.812 * math.sin(zeta)
            M = math.radians(M_deg)
            E = M + e * math.sin(M)
            for _ in range(8):
                E += (M - (E - e * math.sin(E))) / (1.0 - e * math.cos(E))
            xp = a * (math.cos(E) - e)
            yp = a * math.sqrt(1.0 - e * e) * math.sin(E)
            cw, sw = math.cos(w), math.sin(w)
            cO, sO = math.cos(Om), math.sin(Om)
            cI, sI = math.cos(I), math.sin(I)
            x = (cw * cO - sw * sO * cI) * xp + (-sw * cO - cw * sO * cI) * yp
            y = (cw * sO + sw * cO * cI) * xp + (-sw * sO + cw * cO * cI) * yp
            z = (sw * sI) * xp + (cw * sI) * yp
            return x, y, z

        def _pos_at(self, jd, body, sidereal=True):
            T = (jd - 2451545.0) / 36525.0
            ay = self._lahiri(jd) if sidereal else 0.0
            if body == 1:  # Moon
                Lp = (218.3164477 + 481267.88123421 * T) % 360.0
                D = math.radians((297.8501921 + 445267.1114034 * T) % 360.0)
                M = math.radians((357.5291092 + 35999.0502909 * T) % 360.0)
                Mp = math.radians((134.9633964 + 477198.8675055 * T) % 360.0)
                F = math.radians((93.2720950 + 483202.0175233 * T) % 360.0)
                Ec = 1.0 - 0.002516 * T
                dl = (
                    6.288774 * math.sin(Mp) + 1.274027 * math.sin(2 * D - Mp)
                    + 0.658314 * math.sin(2 * D) + 0.213618 * math.sin(2 * Mp)
                    - 0.185116 * Ec * math.sin(M) - 0.114332 * math.sin(2 * F)
                    + 0.058793 * math.sin(2 * D - 2 * Mp) + 0.057066 * Ec * math.sin(2 * D - M - Mp)
                    + 0.053322 * math.sin(2 * D + Mp) + 0.045758 * Ec * math.sin(2 * D - M)
                    - 0.040923 * Ec * math.sin(M - Mp) - 0.034720 * math.sin(D)
                    - 0.030383 * Ec * math.sin(M + Mp) + 0.015327 * math.sin(2 * D - 2 * F)
                )
                lat = 5.128 * math.sin(F) + 0.280 * math.sin(Mp + F) + 0.277 * math.sin(Mp - F)
                return (Lp + dl - ay) % 360.0, lat, 0.00257
            if body == 10:  # Rahu (Mean Node)
                lon = (125.0445550 - 1934.1361849 * T + 0.0020762 * T * T - ay) % 360.0
                return lon, 0.0, 0.00257
            ex, ey, ez = self._helio_xyz("Earth", T)
            if body == 0:
                gx, gy, gz = -ex, -ey, -ez
            else:
                bmap = {2: "Mercury", 3: "Venus", 4: "Mars", 5: "Jupiter", 6: "Saturn", 7: "Uranus", 8: "Neptune"}
                px, py, pz = self._helio_xyz(bmap.get(body, "Mars"), T)
                gx, gy, gz = px - ex, py - ey, pz - ez
            dist = math.sqrt(gx * gx + gy * gy + gz * gz)
            lon_trop = math.degrees(math.atan2(gy, gx)) % 360.0
            lat = math.degrees(math.atan2(gz, math.hypot(gx, gy)))
            return (lon_trop - ay) % 360.0, lat, dist

        def calc_ut(self, jd, body, flags=0):
            sid = bool(flags & self.FLG_SIDEREAL)
            lon0, lat0, dist0 = self._pos_at(jd, body, sidereal=sid)
            lon1, _, _ = self._pos_at(jd + 0.1, body, sidereal=sid)
            spd = ((lon1 - lon0 + 180.0) % 360.0 - 180.0) * 10.0
            return ((lon0, lat0, dist0, spd, 0.0, 0.0), flags)

        def houses_ex(self, jd, lat_deg, lon_deg, hsys=b'W', flags=0):
            T = (jd - 2451545.0) / 36525.0
            gmst = (280.46061837 + 360.98564736629 * (jd - 2451545.0) + 0.000387933 * T * T) % 360.0
            ramc = math.radians((gmst + lon_deg) % 360.0)
            eps = math.radians(23.4392911 - 0.0130042 * T)
            lat = math.radians(lat_deg)
            y = math.cos(ramc)
            x = -math.sin(ramc) * math.cos(eps) - math.tan(lat) * math.sin(eps)
            asc_trop = math.degrees(math.atan2(y, x)) % 360.0
            mc_trop = math.degrees(math.atan2(math.sin(ramc), math.cos(ramc) * math.cos(eps))) % 360.0
            ay = self._lahiri(jd) if (flags & self.FLG_SIDEREAL) else 0.0
            asc = (asc_trop - ay) % 360.0
            mc = (mc_trop - ay) % 360.0
            # Sripati (Porphyry) trisected cusps
            ic = (mc + 180.0) % 360.0
            dsc = (asc + 180.0) % 360.0
            s1 = ((ic - asc) % 360.0) / 3.0
            s2 = ((dsc - ic) % 360.0) / 3.0
            cusps = [
                asc, (asc + s1) % 360.0, (asc + 2 * s1) % 360.0,
                ic, (ic + s2) % 360.0, (ic + 2 * s2) % 360.0,
                dsc, (dsc + s1) % 360.0, (dsc + 2 * s1) % 360.0,
                mc, (mc + s2) % 360.0, (mc + 2 * s2) % 360.0,
            ]
            return (tuple(cusps), (asc, mc, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0))

        def rise_trans(self, jd, body, rsmi, geopos, atpress, attemp):
            return (-1, (0.0,))

        def azalt(self, jd, calc_flag, geopos, atpress, attemp, xin):
            return (180.0, 45.0, 0.0)

        def pheno_ut(self, jd, body, flags=0):
            return (0.0, 0.0, 45.0, 0.0, 0.0)

    swe = _PurePythonSweFallback()

FL = swe.FLG_MOSEPH | swe.FLG_SIDEREAL | swe.FLG_SPEED

SIGNS = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces",
]
SIGNS_HI = [
    "मेष (Aries)", "वृषभ (Taurus)", "मिथुन (Gemini)", "कर्क (Cancer)",
    "सिंह (Leo)", "कन्या (Virgo)", "तुला (Libra)", "वृश्चिक (Scorpio)",
    "धनु (Sagittarius)", "मकर (Capricorn)", "कुंभ (Aquarius)", "मीन (Pisces)",
]
NAK = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra",
    "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni",
    "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha",
    "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha",
    "Purva Bhadrapada", "Uttara Bhadrapada", "Revati",
]
NAK_HI = [
    "अश्विनी", "भरणी", "कृत्तिका", "रोहिणी", "मृगशिरा", "आर्द्रा",
    "पुनर्वसु", "पुष्य", "आश्लेषा", "मघा", "पूर्वाफाल्गुनी", "उत्तराफाल्गुनी",
    "हस्त", "चित्रा", "स्वाति", "विशाखा", "अनुराधा", "ज्येष्ठा",
    "मूल", "पूर्वाषाढ़ा", "उत्तराषाढ़ा", "श्रवण", "धनिष्ठा", "शतभिषा",
    "पूर्वाभाद्रपद", "उत्तराभाद्रपद", "रेवती",
]

# 108 Avakahada Nama-Aksharas (27 Nakshatras x 4 Padas)
AVAKAHADA_108 = [
    ["चु", "चे", "चो", "ला"], ["ली", "लू", "ले", "लो"], ["अ", "ई", "उ", "ए"],
    ["ओ", "वा", "वी", "वू"], ["वे", "वो", "का", "की"], ["कू", "घ", "ङ", "छ"],
    ["के", "को", "हा", "ही"], ["हू", "हे", "हो", "डा"], ["डी", "डू", "डे", "डो"],
    ["मा", "मी", "मू", "मे"], ["मो", "टा", "टी", "टू"], ["टे", "टो", "पा", "पी"],
    ["पू", "ष", "ण", "ठ"], ["पे", "पो", "रा", "री"], ["रू", "रे", "रो", "ता"],
    ["ती", "तू", "ते", "तो"], ["ना", "नी", "नू", "ने"], ["नो", "या", "यी", "यू"],
    ["ये", "यो", "भा", "भी"], ["भू", "धा", "फा", "ढा"], ["भे", "भो", "जा", "जी"],
    ["खी", "खू", "खे", "खो"], ["गा", "गी", "गू", "गे"], ["गो", "सा", "सी", "सू"],
    ["से", "सो", "दा", "दी"], ["दू", "थ", "झ", "ञ"], ["दे", "दो", "चा", "ची"],
]

LORD = ["Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"]
SIGNLORD = [
    "Mars", "Venus", "Mercury", "Moon", "Sun", "Mercury",
    "Venus", "Mars", "Jupiter", "Saturn", "Saturn", "Jupiter",
]
DYEARS = {
    "Ketu": 7, "Venus": 20, "Sun": 6, "Moon": 10, "Mars": 7,
    "Rahu": 18, "Jupiter": 16, "Saturn": 19, "Mercury": 17,
}
BODIES = [
    ("Sun", 0), ("Moon", 1), ("Mars", 4), ("Mercury", 2),
    ("Jupiter", 5), ("Venus", 3), ("Saturn", 6), ("Rahu", 10),
]
OWN = {
    "Sun": [4], "Moon": [3], "Mars": [0, 7], "Mercury": [2, 5],
    "Jupiter": [8, 11], "Venus": [1, 6], "Saturn": [9, 10],
}
EXA = {"Sun": 0, "Moon": 1, "Mars": 9, "Mercury": 5, "Jupiter": 3, "Venus": 11, "Saturn": 6}
EXA_DEG = {"Sun": 10.0, "Moon": 33.0, "Mars": 298.0, "Mercury": 165.0, "Jupiter": 95.0, "Venus": 357.0, "Saturn": 200.0}
DEB = {k: (v + 6) % 12 for k, v in EXA.items()}

MEAN_SPEED = {
    "Sun": 0.9856, "Moon": 13.1764, "Mars": 0.5240, "Mercury": 1.3833,
    "Jupiter": 0.0831, "Venus": 1.2000, "Saturn": 0.0335, "Rahu": 0.0530, "Ketu": 0.0530,
}

# Natural Friendship Table (Naisargika Maitri - BPHS Ch. 3)
FR = {
    "Sun": (["Moon", "Mars", "Jupiter"], ["Mercury"]),
    "Moon": (["Sun", "Mercury"], ["Mars", "Jupiter", "Venus", "Saturn"]),
    "Mars": (["Sun", "Moon", "Jupiter"], ["Venus", "Saturn"]),
    "Mercury": (["Sun", "Venus"], ["Mars", "Jupiter", "Saturn"]),
    "Jupiter": (["Sun", "Moon", "Mars"], ["Saturn"]),
    "Venus": (["Mercury", "Saturn"], ["Mars", "Jupiter"]),
    "Saturn": (["Mercury", "Venus"], ["Jupiter"]),
}

# Exact Parashari Bhinna Ashtakavarga (BAV) Benefic Houses (1-indexed offsets from each contributor)
# Total Bindus across all 7 planets = 48 + 49 + 39 + 54 + 56 + 52 + 39 = 337 Bindus (BPHS Ch. 66)
BAV_RULES = {
    "Sun": {
        "Sun": [1, 2, 4, 7, 8, 9, 10, 11],
        "Moon": [3, 6, 10, 11],
        "Mars": [1, 2, 4, 7, 8, 9, 10, 11],
        "Mercury": [3, 5, 6, 9, 10, 11, 12],
        "Jupiter": [5, 6, 9, 11],
        "Venus": [6, 7, 12],
        "Saturn": [1, 2, 4, 7, 8, 9, 10, 11],
        "Lagna": [3, 4, 6, 10, 11, 12],
    },
    "Moon": {
        "Sun": [3, 6, 7, 8, 10, 11],
        "Moon": [1, 3, 6, 7, 10, 11],
        "Mars": [2, 3, 5, 6, 9, 10, 11],
        "Mercury": [1, 3, 4, 5, 7, 8, 10, 11],
        "Jupiter": [1, 4, 7, 8, 10, 11, 12],
        "Venus": [3, 4, 5, 7, 9, 10, 11],
        "Saturn": [3, 5, 6, 11],
        "Lagna": [3, 6, 10, 11],
    },
    "Mars": {
        "Sun": [3, 5, 6, 10, 11],
        "Moon": [3, 6, 11],
        "Mars": [1, 2, 4, 7, 8, 10, 11],
        "Mercury": [3, 5, 6, 11],
        "Jupiter": [6, 10, 11, 12],
        "Venus": [6, 8, 11, 12],
        "Saturn": [1, 4, 7, 8, 9, 10, 11],
        "Lagna": [1, 3, 6, 10, 11],
    },
    "Mercury": {
        "Sun": [5, 6, 9, 11, 12],
        "Moon": [2, 4, 6, 8, 10, 11],
        "Mars": [1, 2, 4, 7, 8, 9, 10, 11],
        "Mercury": [1, 3, 5, 6, 9, 10, 11, 12],
        "Jupiter": [6, 8, 11, 12],
        "Venus": [1, 2, 3, 4, 5, 8, 9, 11],
        "Saturn": [1, 2, 4, 7, 8, 9, 10, 11],
        "Lagna": [1, 2, 4, 6, 8, 10, 11],
    },
    "Jupiter": {
        "Sun": [1, 2, 3, 4, 7, 8, 9, 10, 11],
        "Moon": [2, 5, 7, 9, 11],
        "Mars": [1, 2, 4, 7, 8, 10, 11],
        "Mercury": [1, 2, 4, 5, 6, 9, 10, 11],
        "Jupiter": [1, 2, 3, 4, 7, 8, 10, 11],
        "Venus": [2, 5, 6, 9, 10, 11],
        "Saturn": [3, 5, 6, 12],
        "Lagna": [1, 2, 4, 5, 6, 7, 9, 10, 11],
    },
    "Venus": {
        "Sun": [8, 11, 12],
        "Moon": [1, 2, 3, 4, 5, 8, 9, 11, 12],
        "Mars": [3, 5, 6, 9, 11, 12],
        "Mercury": [3, 5, 6, 9, 11],
        "Jupiter": [5, 8, 9, 10, 11],
        "Venus": [1, 2, 3, 4, 5, 8, 9, 10, 11],
        "Saturn": [3, 4, 5, 8, 9, 10, 11],
        "Lagna": [1, 2, 3, 4, 5, 8, 9, 11],
    },
    "Saturn": {
        "Sun": [1, 2, 4, 7, 8, 10, 11],
        "Moon": [3, 6, 11],
        "Mars": [3, 5, 6, 10, 11, 12],
        "Mercury": [6, 8, 9, 10, 11, 12],
        "Jupiter": [5, 6, 11, 12],
        "Venus": [6, 11, 12],
        "Saturn": [3, 5, 6, 11],
        "Lagna": [1, 3, 4, 6, 10, 11],
    },
}

PUSHKARA_BHAGA_DEG = {
    0: 21.0, 1: 14.0, 2: 18.0, 3: 8.0, 4: 19.0, 5: 9.0,
    6: 24.0, 7: 11.0, 8: 23.0, 9: 14.0, 10: 19.0, 11: 9.0,
}

# Classical BPHS Ch. 84-97 Sattvika & Shastric Upayas (No commercial gemstone selling)
BPHS_SHASTRIC_UPAYAS = {
    "Sun": {
        "avatara_deity": "भगवान श्रीराम / प्रत्यक्ष सूर्य नारायण (BPHS Ch. 84)",
        "vedic_mantra": "ॐ घृणि सूर्याय नमः / आदित्य हृदय स्तोत्र",
        "dana_seva": "रविवार को गेहूं, गुड़ या तांबे के पात्र का दान; पिता व वरिष्ठों का आदर",
        "aushadhi_lifestyle": "प्रातः सूर्योदय के समय 10 मिनट सूर्य-दर्शन व अर्घ्य; बेल-पत्र/इलायची जल स्नान",
        "behavioral_karma": "अहंकार त्यागे बिना नेतृत्व करें, सत्य बोलें और प्रशासनिक पारदर्शिता रखें",
    },
    "Moon": {
        "avatara_deity": "भगवान श्रीकृष्ण / भगवान शिव (चंद्रशेखर)",
        "vedic_mantra": "ॐ सों सोमाय नमः / नमः शिवाय पंचाक्षर जप",
        "dana_seva": "सोमवार को चावल, दूध या स्वच्छ जल की सेवा; माता व स्त्रियों का सम्मान",
        "aushadhi_lifestyle": "चांदी के पात्र में जल पीना, प्राणायाम और रात्रि में समय पर विश्राम",
        "behavioral_karma": "अति-सोच (overthinking) और भावनात्मक आवेग से बचें; मन को रचनात्मक सेवा में लगाएं",
    },
    "Mars": {
        "avatara_deity": "भगवान कार्तिकेय / श्री नरसिंह / हनुमान जी",
        "vedic_mantra": "ॐ अं अंगारकाय नमः / हनुमान चालीसा या सुंदरकांड पाठ",
        "dana_seva": "मंगलवार को मसूर दाल, गुड़ या रक्तदान/श्रमदान; छोटे भाइयों व सैनिकों/रक्षकों की सहायता",
        "aushadhi_lifestyle": "नियमित शारीरिक व्यायाम, भूमि पर नंगे पैर चलना और लाल चंदन/खस का प्रयोग",
        "behavioral_karma": "क्रोध, जल्दबाजी और तीखी वाणी पर संयम रखें; ऊर्जा को अनुशासित लक्ष्यों में मोड़ें",
    },
    "Mercury": {
        "avatara_deity": "भगवान श्रीविष्णु (त्रिविक्रम / बुद्ध अवतार)",
        "vedic_mantra": "ॐ बुं बुधाय नमः / विष्णु सहस्रनाम पाठ",
        "dana_seva": "बुधवार को हरी मूंग, शिक्षण सामग्री या पुस्तकों का दान; विद्यार्थियों की सहायता",
        "aushadhi_lifestyle": "तुलसी पत्र का सेवन, लेखन-अध्ययन और प्रातः हरियाली में भ्रमण",
        "behavioral_karma": "वाणी में सत्यता और वित्तीय/व्यापारिक अनुबंधों में पूर्ण लिखित स्पष्टता रखें",
    },
    "Jupiter": {
        "avatara_deity": "भगवान वामन / दक्षिणामूर्ति / गुरु तत्व",
        "vedic_mantra": "ॐ बृं बृहस्पतये नमः / गुरु स्तोत्र",
        "dana_seva": "गुरुवार को चने की दाल, हल्दी, केसर या ज्ञान/शिक्षा का दान; आचार्यों का सम्मान",
        "aushadhi_lifestyle": "माथे या कंठ पर केसर/हल्दी तिलक और पीपल/केले के वृक्ष का संरक्षण",
        "behavioral_karma": "नैतिकता, स्वाध्याय और विनम्रता बनाए रखें; अपने ज्ञान का दुरुपयोग या दंभ न करें",
    },
    "Venus": {
        "avatara_deity": "भगवान परशुराम / महालक्ष्मी",
        "vedic_mantra": "ॐ शुं शुक्राय नमः / श्रीसूक्त पाठ",
        "dana_seva": "शुक्रवार को दही, चावल, घी या श्वेत वस्त्र का दान; जीवनसाथी व महिलाओं का सम्मान",
        "aushadhi_lifestyle": "स्वच्छ व सुव्यवस्थित निवास, इलायची/गुलाब जल का प्रयोग और सात्विक आहार",
        "behavioral_karma": "संबंधों में निष्ठा, आर्थिक संयम और दिखावे से दूर रहकर कलात्मक संतुलन रखें",
    },
    "Saturn": {
        "avatara_deity": "भगवान कूर्म / कालभैरव / हनुमान जी",
        "vedic_mantra": "ॐ शं शनैश्चराय नमः / दशरथ कृत शनि स्तोत्र",
        "dana_seva": "शनिवार को काले तिल, उड़द, तेल या श्रमिकों/दिव्यांगजनों/वृद्धों की निःस्वार्थ सेवा",
        "aushadhi_lifestyle": "पीपल के नीचे सरसों तेल का दीपक, त्रिफला/काले तिल का प्रयोग और कठोर समय-पालन",
        "behavioral_karma": "शॉर्टकट, आलस्य और अन्याय से पूर्णतः दूर रहें; अधीनस्थों के साथ न्यायपूर्ण व्यवहार करें",
    },
    "Rahu": {
        "avatara_deity": "भगवान वराह / माँ दुर्गा",
        "vedic_mantra": "ॐ रां राहवे नमः / दुर्गा सप्तशती कवच या अर्गला स्तोत्र",
        "dana_seva": "सफाई कर्मियों की सहायता, सप्तधान्य या नारियल का दान और पक्षियों को दाना",
        "aushadhi_lifestyle": "दूर्वा/चंदन जल स्नान, डिजिटल डिटॉक्स और रात्रि जागरण से बचाव",
        "behavioral_karma": "भ्रम, सट्टेबाजी और अस्पष्ट योजनाओं से बचें; हर कार्य में तथ्य व अनुशासन रखें",
    },
    "Ketu": {
        "avatara_deity": "भगवान मत्स्य / भगवान श्रीगणेश",
        "vedic_mantra": "ॐ कें केतवे नमः / गणपति अथर्वशीर्ष पाठ",
        "dana_seva": "श्वान (कुत्तों) व निराश्रित जीवों को भोजन, कंबल दान और आध्यात्मिक/शोध संस्थाओं में सहयोग",
        "aushadhi_lifestyle": "कुशा/तुलसी जल स्नान, प्रतिदिन 15 मिनट मौन ध्यान और आत्म-निरीक्षण",
        "behavioral_karma": "अनावश्यक संशय और अलगाव छोड़कर अपने सूक्ष्म ज्ञान को समाज-उपयोगी कार्यों में लगाएं",
    },
}


def sign(l):
    return int((l % 360) // 30)


def nak(l):
    return int((l % 360) // (360 / 27))


def pada(l):
    return int(((l % 360) % (360 / 27)) // (360 / 27 / 4)) + 1


def rel(a, c):
    if a == c:
        return "F"
    if a in ("Rahu", "Ketu") or c in ("Rahu", "Ketu"):
        return "N"
    return "F" if c in FR[a][0] else "N" if c in FR[a][1] else "E"


def dignity(p, s):
    if p in ("Rahu", "Ketu"):
        return ""
    if s == EXA[p]:
        return "exalted"
    if s == DEB[p]:
        return "debilitated"
    if s in OWN[p]:
        return "own sign"
    lord = SIGNLORD[s]
    r = rel(p, lord)
    return "friendly" if r == "F" else "enemy" if r == "E" else "neutral"


def kp_sub_lord(l):
    """Compute KP (Krishnamurti Paddhati) Vimshottari Sub-Lord for ecliptic longitude l."""
    span = 360.0 / 27.0
    n_idx = nak(l)
    rem = (l % 360.0) - (n_idx * span)
    start_lord_idx = n_idx % 9
    acc = 0.0
    for i in range(9):
        sub_l = LORD[(start_lord_idx + i) % 9]
        sub_span = span * (DYEARS[sub_l] / 120.0)
        if acc + sub_span >= rem or i == 8:
            return sub_l
        acc += sub_span
    return LORD[start_lord_idx]


# ---------------------------------------------------------------------------
# SHODASHAVARGA (16 PARASHARI DIVISIONAL CHARTS: D1 TO D60 — BPHS CH. 6)
# ---------------------------------------------------------------------------
def d2_hora(l):
    s = sign(l)
    deg = l % 30
    odd = (s % 2 == 0)  # 0=Aries is 1st sign (odd)
    if odd:
        return 4 if deg < 15 else 3  # Leo (4) then Cancer (3)
    return 3 if deg < 15 else 4      # Cancer (3) then Leo (4)


def d3_drekkana(l):
    s = sign(l)
    part = int((l % 30) // 10)
    return (s + part * 4) % 12


def d4_chaturthamsa(l):
    s = sign(l)
    part = int((l % 30) // 7.5)
    return (s + part * 3) % 12


def d7_saptamsa(l):
    s = sign(l)
    part = int((l % 30) // (30.0 / 7.0))
    start = s if s % 2 == 0 else (s + 6) % 12
    return (start + part) % 12


def d9(l):
    s = sign(l)
    idx = int((l % 30) // (30.0 / 9.0))
    st = [s, (s + 8) % 12, (s + 4) % 12][s % 3]
    return (st + idx) % 12


def d10(l):
    s = sign(l)
    idx = int((l % 30) // 3.0)
    st = s if s % 2 == 0 else (s + 8) % 12
    return (st + idx) % 12


def d12_dwadasamsa(l):
    s = sign(l)
    idx = int((l % 30) // 2.5)
    return (s + idx) % 12


def d16_shodasamsa(l):
    s = sign(l)
    idx = int((l % 30) // (30.0 / 16.0))
    st = [0, 4, 8][s % 3]  # Chara->Aries(0), Sthira->Leo(4), Dwiswabhava->Sag(8)
    return (st + idx) % 12


def d20_vimsamsa(l):
    s = sign(l)
    idx = int((l % 30) // 1.5)
    st = [0, 8, 4][s % 3]  # Chara->Aries(0), Sthira->Sag(8), Dwiswabhava->Leo(4)
    return (st + idx) % 12


def d24_chaturvimsamsa(l):
    s = sign(l)
    idx = int((l % 30) // 1.25)
    st = 4 if s % 2 == 0 else 3  # Odd->Leo(4), Even->Cancer(3)
    return (st + idx) % 12


def d27_bhamsha(l):
    s = sign(l)
    idx = int((l % 30) // (30.0 / 27.0))
    st = [0, 3, 6, 9][s % 4]  # Fire->Aries, Earth->Cancer, Air->Libra, Water->Capricorn
    return (st + idx) % 12


def d30_trimsamsa(l):
    s = sign(l)
    deg = l % 30
    if s % 2 == 0:  # Odd signs: Mars 5(0), Sat 5(10), Jup 8(8), Mer 7(2), Ven 5(1)
        if deg < 5: return 0
        if deg < 10: return 10
        if deg < 18: return 8
        if deg < 25: return 2
        return 1
    else:  # Even signs: Ven 5(1), Mer 7(5), Jup 8(11), Sat 5(9), Mars 5(7)
        if deg < 5: return 1
        if deg < 12: return 5
        if deg < 20: return 11
        if deg < 25: return 9
        return 7


def d40_khavedamsa(l):
    s = sign(l)
    idx = int((l % 30) // 0.75)
    st = 0 if s % 2 == 0 else 6  # Odd->Aries(0), Even->Libra(6)
    return (st + idx) % 12


def d45_akshavedamsa(l):
    s = sign(l)
    idx = int((l % 30) // (30.0 / 45.0))
    st = [0, 4, 8][s % 3]
    return (st + idx) % 12


def d60_shashtyamsa(l):
    s = sign(l)
    idx = int((l % 30) // 0.5)
    return (s + idx) % 12


def all_vargas(l):
    return {
        "D1": SIGNS[sign(l)],
        "D2": SIGNS[d2_hora(l)],
        "D3": SIGNS[d3_drekkana(l)],
        "D4": SIGNS[d4_chaturthamsa(l)],
        "D7": SIGNS[d7_saptamsa(l)],
        "D9": SIGNS[d9(l)],
        "D10": SIGNS[d10(l)],
        "D12": SIGNS[d12_dwadasamsa(l)],
        "D16": SIGNS[d16_shodasamsa(l)],
        "D20": SIGNS[d20_vimsamsa(l)],
        "D24": SIGNS[d24_chaturvimsamsa(l)],
        "D27": SIGNS[d27_bhamsha(l)],
        "D30": SIGNS[d30_trimsamsa(l)],
        "D40": SIGNS[d40_khavedamsa(l)],
        "D45": SIGNS[d45_akshavedamsa(l)],
        "D60": SIGNS[d60_shashtyamsa(l)],
    }


def is_pushkara_navamsa(l):
    """Check if longitude l falls in one of the 24 auspicious Pushkara Navamsas."""
    s = sign(l)
    d9_s = d9(l)
    elem = s % 4  # 0=Fire, 1=Earth, 2=Air, 3=Water
    # Fire signs: Libra(6) & Sagittarius(8) navamsas; Earth: Pisces(11) & Taurus(1);
    # Air: Pisces(11) & Gemini(2); Water: Cancer(3) & Virgo(5)
    targets = {0: (6, 8), 1: (11, 1), 2: (11, 2), 3: (3, 5)}
    return d9_s in targets[elem]


def is_pushkara_bhaga(l):
    s = sign(l)
    deg = l % 30
    return abs(deg - PUSHKARA_BHAGA_DEG[s]) <= 1.0


def check_sandhi_and_gandanta(l):
    s = sign(l)
    deg = l % 30
    rashi_sandhi = (deg < 1.0 or deg > 29.0)
    # Gandanta: Water-to-Fire junctions (Cancer->Leo, Scorpio->Sagittarius, Pisces->Aries)
    gandanta = False
    core_gandanta = False
    gandanta_type = None
    if s in (3, 7, 11) and deg >= 26.6667:
        gandanta = True
        core_gandanta = deg >= 29.2
        gandanta_type = f"Water-End Gandanta ({SIGNS[s]} {deg:.2f}°)"
    elif s in (0, 4, 8) and deg <= 3.3333:
        gandanta = True
        core_gandanta = deg <= 0.8
        gandanta_type = f"Fire-Start Gandanta ({SIGNS[s]} {deg:.2f}°)"
    return {
        "rashi_sandhi": rashi_sandhi,
        "gandanta": gandanta,
        "core_gandanta_48min": core_gandanta,
        "gandanta_detail": gandanta_type,
    }


def classify_gati(p, speed):
    """Classify planetary motion state (Gati — Surya Siddhanta & BPHS)."""
    if p in ("Sun", "Moon"):
        return "Sama (Mean Direct)"
    if p in ("Rahu", "Ketu"):
        return "Vakra (Nitya Vakra / Mean Retrograde Node)"
    m = MEAN_SPEED.get(p, 0.5)
    if abs(speed) < 0.02 * m:
        return "Vikala / Stambhana (Stationary — स्तंभन/विकल)"
    if speed < 0:
        return "Vakra (Retrograde — वक्री)"
    if speed < 0.85 * m:
        return "Manda (Slow Direct — मंद)"
    if speed > 1.15 * m:
        return "Sheeghra / Atichara (Fast Direct — शीघ्र/अतिचारी)"
    return "Sama (Mean Direct — सम गति)"


def check_combustion(p, p_lon, sun_lon, is_retro):
    """Check Surya Siddhanta Ch. 9 exact combustion (Asta / Moudhya) orbs."""
    if p in ("Sun", "Rahu", "Ketu"):
        return {"combust": False, "orb_deg": None, "separation_deg": 0.0 if p == "Sun" else None}
    orbs = {
        "Moon": 12.0,
        "Mars": 17.0,
        "Mercury": 12.0 if is_retro else 14.0,
        "Jupiter": 11.0,
        "Venus": 8.0 if is_retro else 10.0,
        "Saturn": 15.0,
    }
    sep = abs((p_lon - sun_lon + 180) % 360 - 180)
    limit = orbs[p]
    return {
        "combust": sep <= limit,
        "orb_limit_deg": limit,
        "separation_from_sun_deg": round(sep, 2),
    }


def detect_graha_yuddha(P, Lats):
    """Detect Planetary War (Graha Yuddha — Surya Siddhanta) among Mars, Mercury, Jupiter, Venus, Saturn (< 1 deg)."""
    true_planets = ["Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
    wars = []
    for i in range(len(true_planets)):
        for j in range(i + 1, len(true_planets)):
            p1, p2 = true_planets[i], true_planets[j]
            sep = abs((P[p1] - P[p2] + 180) % 360 - 180)
            if sep <= 1.0:
                victor = p1 if Lats.get(p1, 0) >= Lats.get(p2, 0) else p2
                defeated = p2 if victor == p1 else p1
                wars.append({
                    "planets": [p1, p2],
                    "separation_deg": round(sep, 3),
                    "victor_jayee": victor,
                    "defeated_parajita": defeated,
                    "note_hi": f"{p1} और {p2} के मध्य ग्रह-युद्ध ({sep:.2f}° अंतर): उत्तरी अक्षांश के कारण {victor} विजयी (जयी) है।",
                })
    return wars


def parse_dt(p):
    return datetime.strptime(p["dob"] + " " + p["tob"], "%Y-%m-%d %H:%M")


def jd_of(dt_local, tz):
    ut = dt_local - timedelta(hours=tz)
    return swe.julday(ut.year, ut.month, ut.day, ut.hour + ut.minute / 60 + ut.second / 3600)


def compute_local_sunrise(dt_local, lat, lon, tz):
    """Compute true local sunrise time for birth date at (lat, lon, tz)."""
    midnight_local = datetime(dt_local.year, dt_local.month, dt_local.day, 0, 0)
    jd_midnight_ut = jd_of(midnight_local, tz)
    try:
        res, tret = swe.rise_trans(
            jd_midnight_ut, swe.SUN, swe.CALC_RISE | swe.BIT_DISC_CENTER, (lon, lat, 0.0), 1013.25, 15.0
        )
        if res == 0 and tret[0] > 0:
            sr_ut_jd = tret[0]
            y, m, d, hr_ut = swe.revjul(sr_ut_jd)
            sr_dt = datetime(y, m, d) + timedelta(hours=hr_ut + tz)
            return sr_dt.strftime("%H:%M")
    except Exception:
        pass
    # Analytical fallback using solar declination & equation of time
    day_of_year = dt_local.timetuple().tm_yday
    b = 2 * math.pi * (day_of_year - 81) / 365.0
    eot_min = 9.87 * math.sin(2 * b) - 7.53 * math.cos(b) - 1.5 * math.sin(b)
    decl = math.radians(23.45 * math.sin(2 * math.pi * (284 + day_of_year) / 365.0))
    lat_r = math.radians(max(-60.0, min(60.0, lat)))
    cos_ha = max(-1.0, min(1.0, -math.tan(lat_r) * math.tan(decl)))
    ha_deg = math.degrees(math.acos(cos_ha))
    sr_hours = 12.0 - (ha_deg / 15.0) - (lon / 15.0 - tz) - (eot_min / 60.0)
    sr_h = int(sr_hours) % 24
    sr_m = int(round((sr_hours - int(sr_hours)) * 60)) % 60
    return f"{sr_h:02d}:{sr_m:02d}"


def compute_panchanga(dt_local, P, sunrise_str):
    """Compute authentic 5-limb Janma Panchanga including Sunrise Vedic Vara (Savana Dina)."""
    sun_lon = P["Sun"]
    moon_lon = P["Moon"]
    diff = (moon_lon - sun_lon) % 360.0

    # 1. Tithi (1..30)
    tithi_idx = int(diff // 12.0) + 1
    paksha = "Shukla Paksha (शुक्ल पक्ष)" if tithi_idx <= 15 else "Krishna Paksha (कृष्ण पक्ष)"
    tithi_names = [
        "Pratipada (प्रतिपदा)", "Dwitiya (द्वितीया)", "Tritiya (तृतीया)", "Chaturthi (चतुर्थी)", "Panchami (पंचमी)",
        "Shashthi (षष्ठी)", "Saptami (सप्तमी)", "Ashtami (अष्टमी)", "Navami (नवमी)", "Dashami (दशमी)",
        "Ekadashi (एकादशी)", "Dwadashi (द्वादशी)", "Trayodashi (त्रयोदशी)", "Chaturdashi (चतुर्दशी)", "Purnima (पूर्णिमा)",
        "Pratipada (प्रतिपदा)", "Dwitiya (द्वितीया)", "Tritiya (तृतीया)", "Chaturthi (चतुर्थी)", "Panchami (पंचमी)",
        "Shashthi (षष्ठी)", "Saptami (सप्तमी)", "Ashtami (अष्टमी)", "Navami (नवमी)", "Dashami (दशमी)",
        "Ekadashi (एकादशी)", "Dwadashi (द्वादशी)", "Trayodashi (त्रयोदशी)", "Chaturdashi (चतुर्दशी)", "Amavasya (अमावस्या)",
    ]

    # 2. Sunrise & Vedic Vara (Savana Dina)
    tob_str = dt_local.strftime("%H:%M")
    tob_min = dt_local.hour * 60 + dt_local.minute
    sr_parts = [int(x) for x in sunrise_str.split(":")]
    sr_min = sr_parts[0] * 60 + sr_parts[1]
    before_sunrise = tob_min < sr_min

    weekdays = [
        ("Monday", "सोमवार (Somavara)", "Moon", 2),
        ("Tuesday", "मंगलवार (Mangalavara)", "Mars", 9),
        ("Wednesday", "बुधवार (Budhavara)", "Mercury", 5),
        ("Thursday", "गुरुवार (Guruvara)", "Jupiter", 3),
        ("Friday", "शुक्रवार (Shukravara)", "Venus", 6),
        ("Saturday", "शनिवार (Shanivara)", "Saturn", 8),
        ("Sunday", "रविवार (Ravivara)", "Sun", 1),
    ]
    civil_wd = weekdays[dt_local.weekday()]
    vedic_wd = weekdays[(dt_local.weekday() - 1) % 7] if before_sunrise else civil_wd

    # 3. Nakshatra, Pada & Avakahada Nama-Akshara
    n_idx = nak(moon_lon)
    p_idx = pada(moon_lon)
    nama_akshara = AVAKAHADA_108[n_idx][p_idx - 1]

    # 4. Nitya Yoga (1..27)
    yoga_idx = int(((sun_lon + moon_lon) % 360.0) // (360.0 / 27.0))
    yoga_names = [
        "Vishkumbha (विष्कुम्भ)", "Priti (प्रीति)", "Ayushman (आयुष्मान)", "Saubhagya (सौभाग्य)", "Shobhana (शोभन)",
        "Atiganda (अतिगण्ड)", "Sukarma (सुकर्मा)", "Dhriti (धृति)", "Shula (शूल)", "Ganda (गण्ड)",
        "Vriddhi (वृद्धि)", "Dhruva (ध्रुव)", "Vyaghata (व्याघात)", "Harshana (हर्षण)", "Vajra (वज्र)",
        "Siddhi (सिद्धि)", "Vyatipata (व्यतीपात)", "Variyan (वरीयान)", "Parigha (परिघ)", "Shiva (शिव)",
        "Siddha (सिद्ध)", "Sadhya (साध्य)", "Shubha (शुभ)", "Shukla (शुक्ल)", "Brahma (ब्रह्म)",
        "Indra (इन्द्र)", "Vaidhriti (वैधृति)",
    ]

    # 5. Karana (60 half-tithis)
    k_idx = int(diff // 6.0)
    movable_karanas = [
        "Bava (बव)", "Balava (बालव)", "Kaulava (कौलाव)", "Taitila (तैतिल)",
        "Gara (गर)", "Vanija (वणिज)", "Vishti / Bhadra (विष्टि/भद्रा)",
    ]
    if k_idx == 0:
        karana_name = "Kimstughna (किंस्तुघ्न)"
    elif k_idx == 57:
        karana_name = "Shakuni (शकुनि)"
    elif k_idx == 58:
        karana_name = "Chatushpada (चतुष्पाद)"
    elif k_idx == 59:
        karana_name = "Naga (नाग)"
    else:
        karana_name = movable_karanas[(k_idx - 1) % 7]

    return {
        "local_sunrise": sunrise_str,
        "birth_time": tob_str,
        "born_before_sunrise": before_sunrise,
        "civil_weekday": {"en": civil_wd[0], "hi": civil_wd[1], "lord": civil_wd[2], "anka": civil_wd[3]},
        "vedic_savana_vara": {"en": vedic_wd[0], "hi": vedic_wd[1], "lord": vedic_wd[2], "anka": vedic_wd[3]},
        "tithi": {"index": tithi_idx, "name": tithi_names[tithi_idx - 1], "paksha": paksha},
        "janma_nakshatra": {
            "name": NAK[n_idx],
            "name_hi": NAK_HI[n_idx],
            "pada": p_idx,
            "lord": LORD[n_idx % 9],
            "avakahada_nama_akshara": nama_akshara,
        },
        "nitya_yoga": {"index": yoga_idx + 1, "name": yoga_names[yoga_idx]},
        "karana": {"half_tithi_index": k_idx + 1, "name": karana_name},
    }


def raw_chart(p):
    tz = p.get("tz", 5.5)
    dt = parse_dt(p)
    jd = jd_of(dt, tz)
    P = {}
    retro = {}
    speeds = {}
    lats = {}
    for n, i in BODIES:
        r = swe.calc_ut(jd, i, FL)[0]
        P[n] = r[0] % 360
        lats[n] = r[1]
        speeds[n] = r[3]
        retro[n] = r[3] < 0
    P["Ketu"] = (P["Rahu"] + 180) % 360
    lats["Ketu"] = -lats["Rahu"]
    speeds["Ketu"] = speeds["Rahu"]
    retro["Rahu"] = retro["Ketu"] = True
    asc_res = swe.houses_ex(jd, p["lat"], p["lon"], b'W', swe.FLG_SIDEREAL)
    asc = asc_res[1][0] % 360
    return dt, jd, P, retro, asc, speeds, lats


def compute_sripati_chalit(jd, lat, lon, P, la):
    """Compute Sripati (Porphyry) Bhava Chalit cusps and check if any planet shifts house."""
    try:
        cusps, _ = swe.houses_ex(jd, lat, lon, b'O', swe.FLG_SIDEREAL)
        # swe.houses_ex returns 12 cusps (0-indexed 0..11 or 1..12 depending on binding)
        c_list = list(cusps[:12]) if len(cusps) == 12 else list(cusps[1:13])
    except Exception:
        c_list = [((la + i) * 30.0) % 360.0 for i in range(12)]

    # Midpoints (Bhava Sandhis) between adjacent cusps
    sandhis = []
    for i in range(12):
        prev_c = c_list[(i - 1) % 12]
        cur_c = c_list[i]
        span = (cur_c - prev_c) % 360.0
        sandhis.append((prev_c + span / 2.0) % 360.0)

    def chalit_house_of(lon_deg):
        for h_idx in range(12):
            start = sandhis[h_idx]
            end = sandhis[(h_idx + 1) % 12]
            if start < end:
                if start <= lon_deg < end:
                    return h_idx + 1
            else:
                if lon_deg >= start or lon_deg < end:
                    return h_idx + 1
        return (sign(lon_deg) - la) % 12 + 1

    planet_chalit = {}
    shifted = []
    for k, v in P.items():
        rashi_h = (sign(v) - la) % 12 + 1
        ch_h = chalit_house_of(v)
        planet_chalit[k] = {
            "rashi_house": rashi_h,
            "chalit_house": ch_h,
            "shifted": rashi_h != ch_h,
        }
        if rashi_h != ch_h:
            shifted.append({
                "planet": k,
                "from_rashi_house": rashi_h,
                "to_chalit_house": ch_h,
                "note_hi": f"{k} राशि कुंडली में भाव {rashi_h} में है, किंतु श्रीपति भाव चलित में भाव {ch_h} का फल भी देगा।",
            })

    return {
        "system": "Sripati Bhava Chalit (Porphyry Midpoint Cusps)",
        "bhava_madhya_deg": [round(x, 2) for x in c_list],
        "bhava_sandhi_start_deg": [round(x, 2) for x in sandhis],
        "planets": planet_chalit,
        "shifted_planets": shifted,
    }


def compute_shadbala_and_avasthas(P, speeds, retro, asc, dt_local, sunrise_str):
    """Compute BPHS Ch. 27 Shadbala (Virupas & Rupas), Ishta/Kashta Phala, and BPHS Ch. 45 Avasthas (Baladi, Jagradadi, Lajjitadi)."""
    la = sign(asc)
    house = lambda l: (sign(l) - la) % 12 + 1
    naisargika = {
        "Sun": 60.0, "Moon": 51.43, "Venus": 42.86, "Jupiter": 34.29,
        "Mercury": 25.71, "Mars": 17.14, "Saturn": 8.57,
    }
    min_rupas = {
        "Sun": 6.5, "Moon": 6.0, "Mars": 5.0, "Mercury": 7.0,
        "Jupiter": 6.5, "Venus": 5.5, "Saturn": 5.0,
    }
    dig_best_house = {
        "Jupiter": 1, "Mercury": 1, "Sun": 10, "Mars": 10,
        "Saturn": 7, "Moon": 4, "Venus": 4,
    }

    sr_parts = [int(x) for x in sunrise_str.split(":")]
    is_day = (sr_parts[0] * 60 + sr_parts[1]) <= (dt_local.hour * 60 + dt_local.minute) <= (18 * 60 + 15)
    paksha_angle = abs((P["Moon"] - P["Sun"] + 180) % 360 - 180)  # 0 at Amavasya, 180 at Purnima

    out = {}
    for p in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]:
        lon = P[p]
        s = sign(lon)
        deg = lon % 30
        h = house(lon)
        dig = dignity(p, s)

        # 1. Uchcha Bala (0..60 Virupas)
        deb_deg = (EXA_DEG[p] + 180.0) % 360.0
        arc_from_deb = abs((lon - deb_deg + 180.0) % 360.0 - 180.0)
        uchcha_bala = (arc_from_deb / 180.0) * 60.0

        # Saptavargaja + Kendradi + Ojhayugma + Drekkana -> Sthana Bala
        varga_base = 115.0 if dig in ("exalted", "own sign") else 85.0 if dig == "friendly" else 65.0 if dig == "neutral" else 45.0
        if d9(lon) == s or dignity(p, d9(lon)) in ("exalted", "own sign"):
            varga_base += 25.0
        kendradi = 60.0 if h in (1, 4, 7, 10) else 30.0 if h in (2, 5, 8, 11) else 15.0
        ojha = 15.0 if ((s % 2 == 1 and p in ("Moon", "Venus")) or (s % 2 == 0 and p not in ("Moon", "Venus"))) else 0.0
        sthana_bala = uchcha_bala + varga_base + kendradi + ojha

        # 2. Dig Bala (0..60 Virupas)
        best_h = dig_best_house[p]
        powerless_lon = ((la + best_h - 1 + 6) % 12) * 30.0 + 15.0
        dig_arc = abs((lon - powerless_lon + 180.0) % 360.0 - 180.0)
        dig_bala = (dig_arc / 180.0) * 60.0

        # 3. Kala Bala
        nathonnatha = 60.0 if p == "Mercury" else (60.0 if (is_day and p in ("Sun", "Jupiter", "Venus")) or (not is_day and p in ("Moon", "Mars", "Saturn")) else 20.0)
        paksha_bala = (paksha_angle / 180.0) * 60.0 if p in ("Moon", "Jupiter", "Venus", "Mercury") else ((180.0 - paksha_angle) / 180.0) * 60.0
        kala_bala = nathonnatha + paksha_bala + 35.0

        # 4. Cheshta Bala (0..60 Virupas)
        if p == "Sun":
            cheshta_bala = 40.0
        elif p == "Moon":
            cheshta_bala = paksha_bala
        else:
            if retro.get(p, False):
                cheshta_bala = 55.0
            else:
                sun_sep = abs((lon - P["Sun"] + 180.0) % 360.0 - 180.0)
                cheshta_bala = max(10.0, min(55.0, (sun_sep / 180.0) * 55.0))

        # 5. Naisargika Bala
        nais_bala = naisargika[p]

        # 6. Drik Bala
        drik_bala = 15.0 if sign(P["Jupiter"]) in ((s - 4) % 12, (s - 6) % 12, (s - 8) % 12, s) else 0.0

        total_virupas = round(sthana_bala + dig_bala + kala_bala + cheshta_bala + nais_bala + drik_bala, 1)
        total_rupas = round(total_virupas / 60.0, 2)
        req_rupas = min_rupas[p]
        ratio = round(total_rupas / req_rupas, 2)

        # Ishta Phala & Kashta Phala (BPHS Ch. 27)
        ishta = round(math.sqrt(max(0.0, uchcha_bala * cheshta_bala)), 1)
        kashta = round(math.sqrt(max(0.0, (60.0 - uchcha_bala) * (60.0 - cheshta_bala))), 1)

        # Avasthas (BPHS Ch. 45)
        # A. Baladi (Odd sign: 0-6 Bala, 6-12 Kumara, 12-18 Yuva, 18-24 Vriddha, 24-30 Mrita; reversed in Even)
        tier_idx = min(4, int(deg // 6.0))
        if s % 2 == 1:
            tier_idx = 4 - tier_idx
        baladi_names = [
            "Bala (बाल — 25% फल)",
            "Kumara (कुमार — 50% फल)",
            "Yuva (युवा — 100% पूर्ण फल)",
            "Vriddha (वृद्ध — परिपक्व/न्यून फल)",
            "Mrita (मृत — सुप्त फल)",
        ]

        # B. Jagradadi
        if dig in ("exalted", "own sign"):
            jagradadi = "Jagrat (जाग्रत — 100% सजग फल)"
        elif dig in ("friendly", "neutral"):
            jagradadi = "Swapna (स्वप्न — 50% मध्यम फल)"
        else:
            jagradadi = "Sushupti (सुषुप्ति — संघर्षपूर्ण फल)"

        # C. Lajjitadi (BPHS Ch. 45)
        same_sign_planets = [k for k, v in P.items() if k != p and sign(v) == s]
        malefics_with = [k for k in same_sign_planets if k in ("Sun", "Mars", "Saturn", "Rahu", "Ketu")]
        benefics_with = [k for k in same_sign_planets if k in ("Jupiter", "Venus", "Mercury")]
        if dig in ("exalted", "own sign"):
            lajjitadi = "Garvita (गर्वित — आत्मविश्वास व उच्च उपलब्धि)"
        elif h == 5 and any(k in same_sign_planets for k in ("Rahu", "Ketu", "Saturn", "Mars")):
            lajjitadi = "Lajjita (लज्जित — संकोच या पंचम भाव में सतर्कता)"
        elif "Sun" in same_sign_planets and abs((lon - P["Sun"] + 180) % 360 - 180) < 14:
            lajjitadi = "Kshobhita (क्षोभित — सूर्य सान्निध्य से आंतरिक बेचैनी)"
        elif benefics_with or dig == "friendly":
            lajjitadi = "Mudita (मुदित — प्रसन्न व सहयोगी अवस्था)"
        elif dig == "enemy" or malefics_with:
            lajjitadi = "Kshudhita (क्षुधित — अतिरिक्त प्रयास की आवश्यकता)"
        else:
            lajjitadi = "Svastha / Normal (स्वस्थ/सामान्य)"

        out[p] = {
            "sthana_bala": round(sthana_bala, 1),
            "dig_bala": round(dig_bala, 1),
            "kala_bala": round(kala_bala, 1),
            "cheshta_bala": round(cheshta_bala, 1),
            "naisargika_bala": round(nais_bala, 1),
            "drik_bala": round(drik_bala, 1),
            "uchcha_bala": round(uchcha_bala, 1),
            "total_virupas": total_virupas,
            "total_rupas": total_rupas,
            "minimum_required_rupas": req_rupas,
            "shadbala_ratio": ratio,
            "meets_bphs_threshold": ratio >= 1.0,
            "ishta_phala_virupas": ishta,
            "kashta_phala_virupas": kashta,
            "ishta_dominant": ishta >= kashta,
            "avasthas": {
                "baladi": baladi_names[tier_idx],
                "jagradadi": jagradadi,
                "lajjitadi": lajjitadi,
            },
        }
    return out


def compute_functional_nature_and_badhaka(la, P):
    """Compute functional benefics/malefics/yogakaraka, Kendradhipati Dosha, Badhaka & Maraka for Lagna la (BPHS Ch. 34)."""
    house_of_sign = lambda s: (s - la) % 12 + 1
    lord_houses = {}
    for h in range(1, 13):
        s = (la + h - 1) % 12
        L = SIGNLORD[s]
        lord_houses.setdefault(L, []).append(h)

    trikonas = {1, 5, 9}
    kendras = {1, 4, 7, 10}
    trishadayas = {3, 6, 11}
    dusthanas = {6, 8, 12}

    benefics = []
    malefics = []
    yogakarakas = []
    neutrals = []
    kendradhipati_notes = []

    for p, hs in lord_houses.items():
        h_set = set(hs)
        owns_trikona = bool(h_set & trikonas)
        owns_kendra = bool(h_set & {4, 7, 10})
        if owns_trikona and owns_kendra and 1 not in h_set:
            yogakarakas.append(p)
            benefics.append(p)
        elif owns_trikona:
            benefics.append(p)
        elif h_set <= trishadayas or (bool(h_set & {6, 8, 12}) and not owns_trikona):
            if p in ("Jupiter", "Venus", "Mercury") and owns_kendra:
                kendradhipati_notes.append(
                    f"{p} को केंद्राधिपति दोष (भाव {hs} का स्वामी) लगता है, अतः इसकी शुभता कुंडली में इसके बल व युति पर निर्भर करेगी।"
                )
            malefics.append(p)
        else:
            if p in ("Jupiter", "Venus", "Mercury") and owns_kendra and not owns_trikona:
                kendradhipati_notes.append(
                    f"नैसर्गिक शुभ ग्रह {p} केंद्र भाव ({hs}) का स्वामी होने से केंद्राधिपति दोष से प्रभावित (तटस्थ/मिश्रित फलदाता) है।"
                )
            neutrals.append(p)

    # Badhaka Sthana (Prasna Marga & Jataka Parijata): Chara (0,3,6,9)->11th, Sthira (1,4,7,10)->9th, Dwiswabhava (2,5,8,11)->7th
    modality = la % 3
    badhaka_house = 11 if modality == 0 else 9 if modality == 1 else 7
    badhaka_sign = (la + badhaka_house - 1) % 12
    badhakesh = SIGNLORD[badhaka_sign]
    badhakesh_in_house = house_of_sign(sign(P[badhakesh]))

    # Maraka Sthana (2nd and 7th houses)
    maraka_2_lord = SIGNLORD[(la + 1) % 12]
    maraka_7_lord = SIGNLORD[(la + 6) % 12]

    return {
        "lagna_sign": SIGNS[la],
        "lagna_modality": "Chara (चर राशि)" if modality == 0 else "Sthira (स्थिर राशि)" if modality == 1 else "Dwiswabhava (द्विस्वभाव राशि)",
        "planet_house_lordships": lord_houses,
        "yogakarakas": yogakarakas,
        "functional_benefics_shubha": benefics,
        "functional_malefics_papa": malefics,
        "functional_neutrals_sama": neutrals,
        "kendradhipati_dosha_notes": kendradhipati_notes,
        "badhaka": {
            "badhaka_house": badhaka_house,
            "badhaka_sign": SIGNS[badhaka_sign],
            "badhakesh_planet": badhakesh,
            "badhakesh_placed_in_house": badhakesh_in_house,
            "note_hi": f"{SIGNS_HI[la]} लग्न ({'चर' if modality == 0 else 'स्थिर' if modality == 1 else 'द्विस्वभाव'}) के लिए भाव {badhaka_house} बाधक स्थान तथा {badhakesh} बाधकेश्वर है (वर्तमान में भाव {badhakesh_in_house} में स्थित)।",
        },
        "maraka": {
            "second_lord": maraka_2_lord,
            "seventh_lord": maraka_7_lord,
            "primary_marakas": list(dict.fromkeys([maraka_2_lord, maraka_7_lord])),
        },
    }


def compute_jaimini_system(P, asc):
    """Compute Jaimini Sutras 7 Chara Karakas (AK..DK), Karakamsha, Swamsha, and Arudha Padas (AL, UL, A7, A10)."""
    la = sign(asc)
    d9_la = d9(asc)
    # 1. 7 Chara Karakas sorted by degree within sign (descending)
    seven = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
    ranked = sorted(seven, key=lambda k: P[k] % 30.0, reverse=True)
    karaka_labels = [
        ("AK", "Atmakaraka (आत्मकारक — आत्मा व जीवन का सर्वोच्च उद्देश्य)"),
        ("AmK", "Amatyakaraka (अमात्यकारक — करियर, पद व सलाहकार)"),
        ("BK", "Bhratrukaraka (भ्रातृकारक — गुरु, भाई-बहन व साहस)"),
        ("MK", "Matrukaraka (मातृकारक — माता, भूमि व भावनात्मक सुख)"),
        ("PK", "Putrakaraka (पुत्रकारक — बुद्धि, संतान व सृजन)"),
        ("GK", "Gnatikaraka (ज्ञातिकारक — प्रतिस्पर्धा, रोग व बाधा-निवारण)"),
        ("DK", "Darakaraka (दाराकारक — जीवनसाथी, विवाह व साझेदारी)"),
    ]
    chara_karakas = {}
    for idx, p_name in enumerate(ranked):
        code, title = karaka_labels[idx]
        chara_karakas[code] = {
            "code": code,
            "title": title,
            "planet": p_name,
            "deg_in_sign": round(P[p_name] % 30.0, 2),
            "d1_sign": SIGNS[sign(P[p_name])],
            "d1_house": (sign(P[p_name]) - la) % 12 + 1,
            "d9_sign": SIGNS[d9(P[p_name])],
        }

    ak_planet = ranked[0]
    ak_d9_sign_idx = d9(P[ak_planet])
    ishta_devata_sign_idx = (ak_d9_sign_idx + 11) % 12  # 12th from Karakamsha

    # 2. Arudha Padas A1..A12 with classical Jaimini 1st/7th -> 10th/4th exception
    arudhas = {}
    for h in range(1, 13):
        h_sign = (la + h - 1) % 12
        L = SIGNLORD[h_sign]
        l_sign = sign(P[L])
        dist = (l_sign - h_sign) % 12
        raw_arudha = (l_sign + dist) % 12
        # Classical exception: if Lord is in the house itself (dist == 0) or 7th from it (dist == 6),
        # the Arudha shifts 10 signs from the house (i.e. 10th from house if dist==0, 4th from house if dist==6)
        if dist == 0:
            arudha_sign = (h_sign + 9) % 12
            exception = "Lord in 1st from Bhava -> shifted to 10th"
        elif dist == 6:
            arudha_sign = (h_sign + 3) % 12
            exception = "Lord in 7th from Bhava -> shifted to 4th"
        else:
            arudha_sign = raw_arudha
            exception = None

        code = "AL" if h == 1 else "UL" if h == 12 else f"A{h}"
        arudhas[code] = {
            "house_number": h,
            "code": code,
            "sign": SIGNS[arudha_sign],
            "sign_hi": SIGNS_HI[arudha_sign],
            "house_from_lagna": (arudha_sign - la) % 12 + 1,
            "lord_of_arudha": SIGNLORD[arudha_sign],
            "occupants": [k for k, v in P.items() if sign(v) == arudha_sign],
            "exception_applied": exception,
        }

    return {
        "chara_karakas": chara_karakas,
        "karakamsha": {
            "atmakaraka_planet": ak_planet,
            "karakamsha_sign": SIGNS[ak_d9_sign_idx],
            "karakamsha_sign_hi": SIGNS_HI[ak_d9_sign_idx],
            "karakamsha_house_in_d1": (ak_d9_sign_idx - la) % 12 + 1,
            "karakamsha_house_in_d9": (ak_d9_sign_idx - d9_la) % 12 + 1,
            "tenth_from_karakamsha_sign": SIGNS[(ak_d9_sign_idx + 9) % 12],
            "twelfth_from_karakamsha_ishta_sign": SIGNS[ishta_devata_sign_idx],
            "ishta_sign_lord": SIGNLORD[ishta_devata_sign_idx],
        },
        "arudha_padas": arudhas,
        "key_padas": {
            "AL_arudha_lagna": arudhas["AL"],
            "UL_upapada_lagna": arudhas["UL"],
            "A7_darapada": arudhas["A7"],
            "A10_rajyapada": arudhas["A10"],
        },
    }


def compute_ashtakavarga(P, asc):
    """Compute exact Parashari Bhinna Ashtakavarga (BAV) and Sarvashtakavarga (SAV = 337 Bindus)."""
    la = sign(asc)
    contributors = {p: sign(P[p]) for p in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]}
    contributors["Lagna"] = la

    bav_by_sign = {}
    bav_by_house = {}
    sav_by_sign_idx = [0] * 12

    for target_p, rules in BAV_RULES.items():
        sign_scores = [0] * 12
        for contrib_name, offsets in rules.items():
            c_sign = contributors[contrib_name]
            for off in offsets:
                s_idx = (c_sign + off - 1) % 12
                sign_scores[s_idx] += 1
                sav_by_sign_idx[s_idx] += 1

        bav_by_sign[target_p] = {SIGNS[i]: sign_scores[i] for i in range(12)}
        bav_by_house[target_p] = {h: sign_scores[(la + h - 1) % 12] for h in range(1, 13)}

    sav_houses = {h: sav_by_sign_idx[(la + h - 1) % 12] for h in range(1, 13)}
    sav_signs = {SIGNS[i]: sav_by_sign_idx[i] for i in range(12)}

    # Key BPHS SAV diagnostics
    vitta_aya_ratio = f"11th House ({sav_houses[11]} bindus) vs 12th House ({sav_houses[12]} bindus) & 10th House ({sav_houses[10]} bindus)"
    strongest_houses = sorted(sav_houses.items(), key=lambda kv: kv[1], reverse=True)[:3]
    weakest_houses = sorted(sav_houses.items(), key=lambda kv: kv[1])[:3]

    return {
        "total_sav_bindus": sum(sav_by_sign_idx),
        "sarvashtakavarga_houses": sav_houses,
        "sarvashtakavarga_signs": sav_signs,
        "bhinna_ashtakavarga_houses": bav_by_house,
        "bhinna_ashtakavarga_signs": bav_by_sign,
        "planet_natal_bav_scores": {
            p: bav_by_sign[p][SIGNS[sign(P[p])]]
            for p in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
        },
        "summary": {
            "vitta_aya_balance": vitta_aya_ratio,
            "savings_surplus_favorable": sav_houses[11] > sav_houses[12] and sav_houses[2] >= 25,
            "strongest_houses": [{"house": h, "sign": SIGNS[(la + h - 1) % 12], "bindus": b} for h, b in strongest_houses],
            "weakest_houses": [{"house": h, "sign": SIGNS[(la + h - 1) % 12], "bindus": b} for h, b in weakest_houses],
        },
    }


def dasha_tree(moon, birth):
    """Compute Vimshottari Mahadasha -> Antardasha -> Pratyantardasha tree."""
    n = nak(moon)
    frac = (moon % (360 / 27)) / (360 / 27)
    idx = LORD.index(LORD[n % 9])
    t = birth
    out = []
    for k in range(9):
        L = LORD[(idx + k) % 9]
        yrs = DYEARS[L] * (1 - frac) if k == 0 else DYEARS[L]
        e = t + timedelta(days=yrs * 365.25)
        full_start = t - timedelta(days=DYEARS[L] * frac * 365.25) if k == 0 else t
        full_tot = DYEARS[L] * 365.25 * 86400
        ts = full_start
        sub = []
        for j in range(9):
            A = LORD[(idx + k + j) % 9]
            d = full_tot * DYEARS[A] / 120.0
            s2, e2 = ts, ts + timedelta(seconds=d)
            ts = e2
            if e2 <= t:
                continue
            # Pratyantardashas inside Antardasha A
            p_ts = s2
            pratyantars = []
            for m_idx in range(9):
                P_lord = LORD[(idx + k + j + m_idx) % 9]
                p_sec = d * DYEARS[P_lord] / 120.0
                ps, pe = p_ts, p_ts + timedelta(seconds=p_sec)
                p_ts = pe
                if pe <= t:
                    continue
                pratyantars.append({
                    "lord": P_lord,
                    "start": max(ps, t).date().isoformat(),
                    "end": pe.date().isoformat(),
                })
            sub.append({
                "lord": A,
                "start": max(s2, t).date().isoformat(),
                "end": e2.date().isoformat(),
                "pratyantardashas": pratyantars,
            })
        out.append({
            "lord": L,
            "start": t.date().isoformat(),
            "end": e.date().isoformat(),
            "antardashas": sub,
        })
        t = e
    return out


def compute_yogini_dasha(moon, birth, target_date=None):
    """Compute classical 36-year Yogini Dasha (BPHS Ch. 46) as a secondary conditional Dasha check."""
    if target_date is None:
        target_date = datetime.now().date().isoformat()
    yoginis = [
        ("Mangala (मंगला)", "Moon", 1),
        ("Pingala (पिंगला)", "Sun", 2),
        ("Dhanya (धान्या)", "Jupiter", 3),
        ("Bhramari (भ्रामरी)", "Mars", 4),
        ("Bhadrika (भद्रिका)", "Mercury", 5),
        ("Ulka (उल्का)", "Saturn", 6),
        ("Siddha (सिद्धा)", "Venus", 7),
        ("Sankata (संकटा)", "Rahu", 8),
    ]
    n_idx = nak(moon)  # 0..26 (Ashwini=1 -> +3 mod 8)
    frac = (moon % (360.0 / 27.0)) / (360.0 / 27.0)
    start_y_idx = ((n_idx + 1 + 3) % 8) - 1
    if start_y_idx < 0:
        start_y_idx = 7

    cur = birth
    periods = []
    active = None
    for step in range(24):  # 3 cycles = 108 years
        y_name, y_lord, y_yrs = yoginis[(start_y_idx + step) % 8]
        eff_yrs = y_yrs * (1.0 - frac) if step == 0 else y_yrs
        end = cur + timedelta(days=eff_yrs * 365.25)
        entry = {
            "yogini": y_name,
            "lord": y_lord,
            "years": round(eff_yrs, 2),
            "start": cur.date().isoformat(),
            "end": end.date().isoformat(),
        }
        periods.append(entry)
        if entry["start"] <= target_date < entry["end"]:
            active = entry
        cur = end
    return {"active_yogini": active, "timeline_sample": periods[:12]}


def aspects_on(P, asc, h):
    la = sign(asc)
    hs = (la + h - 1) % 12
    out = []
    A = {"Mars": [4, 7, 8], "Jupiter": [5, 7, 9], "Saturn": [3, 7, 10], "Rahu": [5, 7, 9], "Ketu": [5, 7, 9]}
    for k, v in P.items():
        d = (hs - sign(v)) % 12 + 1
        if (k not in ("Rahu", "Ketu") and d == 7) or d in A.get(k, []):
            out.append(k)
    return out


def yogas(P, asc):
    """Evaluate classical Parashari Rajayogas, Dhana Yogas, Pancha Mahapurusha, Lunar/Solar Yogas & Neecha Bhanga."""
    la = sign(asc)
    pos = {k: sign(v) for k, v in P.items()}
    H = lambda k: (pos[k] - la) % 12 + 1
    out = []

    # 1. Pancha Mahapurusha Yogas
    names = {"Mars": "Ruchaka", "Mercury": "Bhadra", "Jupiter": "Hamsa", "Venus": "Malavya", "Saturn": "Shasha"}
    for p, nm in names.items():
        if dignity(p, pos[p]) in ("own sign", "exalted") and H(p) in (1, 4, 7, 10):
            out.append({
                "name": f"{nm} (Pancha Mahapurusha Rajayoga)",
                "strength": "strong",
                "detail": f"{p} in {dignity(p, pos[p])} in Kendra house {H(p)}",
            })
        elif dignity(p, pos[p]) in ("own sign", "exalted") and (pos[p] - pos["Moon"]) % 12 in (0, 3, 6, 9):
            out.append({
                "name": f"{nm} (Chandra-Kendra Mahapurusha)",
                "strength": "medium-strong",
                "detail": f"{p} in {dignity(p, pos[p])} in Kendra from Moon (house {H(p)} from Lagna)",
            })

    # 2. Gaja Kesari, Budhaditya, Chandra-Mangala, Guru-Mangala
    if (pos["Jupiter"] - pos["Moon"]) % 12 in (0, 3, 6, 9):
        out.append({"name": "Gaja Kesari Yoga", "strength": "strong" if dignity("Jupiter", pos["Jupiter"]) != "debilitated" else "medium", "detail": "Jupiter in a Kendra from the Moon"})
    if pos["Sun"] == pos["Mercury"]:
        sep = abs((P["Sun"] - P["Mercury"] + 180) % 360 - 180)
        out.append({
            "name": "Budhaditya Yoga",
            "strength": "medium" if sep < 14 else "strong",
            "detail": f"Sun-Mercury conjunct in house {H('Sun')} ({sep:.1f}° apart)",
        })
    if pos["Moon"] == pos["Mars"] or (pos["Mars"] - pos["Moon"]) % 12 == 6:
        out.append({"name": "Chandra-Mangala Dhana Yoga", "strength": "medium-strong", "detail": "Moon and Mars conjunct or mutually aspecting"})
    if pos["Jupiter"] == pos["Mars"] or (pos["Mars"] - pos["Jupiter"]) % 12 == 6:
        out.append({"name": "Guru-Mangala Dharma-Karma Yoga", "strength": "strong", "detail": f"Jupiter and Mars linked in house {H('Jupiter')}/{H('Mars')}"})

    # 3. Classical Lunar Yogas: Sunapha, Anapha, Durudhura, Kemadruma (with cancellation)
    m_s = pos["Moon"]
    second_from_m = [p for p in ("Mars", "Mercury", "Jupiter", "Venus", "Saturn") if pos[p] == (m_s + 1) % 12]
    twelfth_from_m = [p for p in ("Mars", "Mercury", "Jupiter", "Venus", "Saturn") if pos[p] == (m_s - 1) % 12]
    if second_from_m and twelfth_from_m:
        out.append({"name": "Durudhura Yoga", "strength": "strong", "detail": f"Moon flanked by {second_from_m} (2nd) and {twelfth_from_m} (12th)"})
    elif second_from_m:
        out.append({"name": "Sunapha Yoga", "strength": "medium-strong", "detail": f"Self-earned wealth/intelligence via {second_from_m} in 2nd from Moon"})
    elif twelfth_from_m:
        out.append({"name": "Anapha Yoga", "strength": "medium-strong", "detail": f"Dignity and influence via {twelfth_from_m} in 12th from Moon"})

    # 4. Solar Yogas: Vesi, Vasi, Ubhayachari
    s_s = pos["Sun"]
    second_from_s = [p for p in ("Mars", "Mercury", "Jupiter", "Venus", "Saturn") if pos[p] == (s_s + 1) % 12]
    twelfth_from_s = [p for p in ("Mars", "Mercury", "Jupiter", "Venus", "Saturn") if pos[p] == (s_s - 1) % 12]
    if second_from_s and twelfth_from_s:
        out.append({"name": "Ubhayachari (Shubha Ubhayachari) Yoga", "strength": "strong", "detail": f"Sun flanked by {second_from_s} and {twelfth_from_s}"})

    # 5. Parashari Kendra-Trikona Rajayoga & Dharma-Karmadhipati (9L + 10L)
    l1 = SIGNLORD[la]
    l4 = SIGNLORD[(la + 3) % 12]
    l5 = SIGNLORD[(la + 4) % 12]
    l7 = SIGNLORD[(la + 6) % 12]
    l9 = SIGNLORD[(la + 8) % 12]
    l10 = SIGNLORD[(la + 9) % 12]
    if pos[l9] == pos[l10] or (pos[l9] == (la + 9) % 12 and pos[l10] == (la + 8) % 12):
        out.append({"name": "Dharma-Karmadhipati Rajayoga (9th & 10th Lords)", "strength": "strong", "detail": f"9th lord {l9} and 10th lord {l10} united in house {H(l9)}"})
    if pos[l1] == pos[l5] or pos[l1] == pos[l9]:
        partner = l5 if pos[l1] == pos[l5] else l9
        out.append({"name": "Lagnadhipati-Trikona Rajayoga", "strength": "strong", "detail": f"Lagna lord {l1} conjunct Trikona lord {partner} in house {H(l1)}"})

    # 6. Parivartana Yoga (Mutual Exchange of Signs)
    seven_p = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
    checked_pairs = set()
    for p1 in seven_p:
        s1 = pos[p1]
        p2 = SIGNLORD[s1]
        if p1 != p2 and (p2, p1) not in checked_pairs:
            s2 = pos[p2]
            if SIGNLORD[s2] == p1:
                checked_pairs.add((p1, p2))
                h1, h2 = H(p1), H(p2)
                p_type = "Dainya Parivartana" if (h1 in (6, 8, 12) or h2 in (6, 8, 12)) else "Khala Parivartana" if (3 in (h1, h2)) else "Maha Parivartana Rajayoga"
                out.append({
                    "name": f"{p_type} ({p1} <-> {p2})",
                    "strength": "strong" if "Maha" in p_type else "medium",
                    "detail": f"{p1} (in house {h1}) and {p2} (in house {h2}) exchange signs",
                })

    # 7. Neecha Bhanga Rajayoga
    for p in seven_p:
        if dignity(p, pos[p]) == "debilitated":
            disp = SIGNLORD[pos[p]]
            exa_lord = next((k for k, v in EXA.items() if v == pos[p]), None)
            ok = []
            if (pos[disp] - la) % 12 in (0, 3, 6, 9):
                ok.append(f"dispositor {disp} in Kendra from Lagna")
            if (pos[disp] - pos["Moon"]) % 12 in (0, 3, 6, 9):
                ok.append(f"dispositor {disp} in Kendra from Moon")
            if exa_lord and (pos[exa_lord] - la) % 12 in (0, 3, 6, 9):
                ok.append(f"exaltation lord {exa_lord} in Kendra from Lagna")
            if d9(P[p]) == EXA[p] or d9(P[p]) in OWN[p]:
                ok.append(f"{p} strong (own/exalted) in Navamsa D9")
            out.append({
                "name": "Neecha Bhanga Rajayoga" if ok else "Debilitation (Neecha)",
                "planet": p,
                "strength": "strong" if len(ok) >= 2 else "medium" if ok else "caution",
                "detail": "; ".join(ok) or f"{p} debilitated in house {H(p)}",
            })

    # 8. Vipareeta Rajayoga (Harsha, Sarala, Vimala)
    for h, nm in ((6, "Harsha"), (8, "Sarala"), (12, "Vimala")):
        L = SIGNLORD[(la + h - 1) % 12]
        if H(L) in (6, 8, 12):
            out.append({
                "name": f"{nm} (Vipareeta Raja Yoga)",
                "strength": "medium-strong",
                "detail": f"{h}th lord {L} placed in Dusthana house {H(L)}",
            })
    return out


def mangal(P, asc):
    """Strict Parashari Mangal Dosha (BPHS Ch. 80 & Phaladeepika):
    - 7th (Saptama) & 8th (Ashtama) house Mars from Lagna are severe Lagna Manglik placements.
      Benefic aspect or dignity mitigates harshness (mitigations), NEVER cancelling present_from_lagna to False.
    - 1st, 2nd, 4th, 12th house Mars from Lagna are moderate-to-strong Lagna Manglik placements.
    - If Mars is NOT in {1, 2, 4, 7, 8, 12} from Lagna (e.g., 9th house Mars with Jupiter), classify clearly as
      Non-Manglik from Lagna (अमांगलिक) or Mild Chandra-Manglik (Moon-chart only).
    """
    la = sign(asc)
    m = sign(P["Mars"])
    fl = (m - la) % 12 + 1
    fm = (m - sign(P["Moon"])) % 12 + 1
    fv = (m - sign(P["Venus"])) % 12 + 1
    bad = (1, 2, 4, 7, 8, 12)

    lagna_manglik = fl in bad
    moon_manglik = fm in bad
    venus_manglik = fv in bad

    mitigations = []
    jh = (m - sign(P["Jupiter"])) % 12 + 1
    if jh in (5, 7, 9) or sign(P["Jupiter"]) == m:
        mitigations.append("Jupiter aspects or conjoins Mars (बृहस्पति की शुभ दृष्टि/युति से उग्रता में कमी)")
    if dignity("Mars", m) in ("own sign", "exalted"):
        mitigations.append("Mars in own/exalted sign (स्वराशि/उच्च का मंगल — रचनात्मक ऊर्जा)")
    if sign(P["Venus"]) == m or sign(P["Moon"]) == m:
        mitigations.append("Benefic conjunction softens interpersonal friction")

    if fl in (7, 8):
        subtype = "Saptama Manglik (सप्तम भाव लग्न मांगलिक)" if fl == 7 else "Ashtama Manglik (अष्टम भाव लग्न मांगलिक)"
        severity = "High (Severe Parashari Lagna Manglik — Never Cancelled to Non-Manglik)"
        status_hi = (
            f"पूर्ण लग्न मांगलिक ({subtype}): मंगल लग्न से भाव {fl} में स्थित है। "
            f"शास्त्रीय नियम के अनुसार सप्तम/अष्टम मंगल में शुभ दृष्टि या राशि बल से कठोरता कम होती है, पर मांगलिक दोष समाप्त नहीं होता; "
            f"विवाह में मांगलिक/सम-बल मिलान एवं कुंभ/अर्क विवाह अथवा मंगल शांति आवश्यक है।"
        )
        present_primary = True
    elif fl in (1, 2, 4, 12):
        subtype = f"Lagna Manglik (House {fl})"
        severity = "Moderate Lagna Manglik (मध्यम लग्न मांगलिक)"
        status_hi = (
            f"लग्न मांगलिक (भाव {fl}): मंगल लग्न से भाव {fl} में स्थित है। "
            + ("शुभ प्रभावों से इसकी तीव्रता नियंत्रित है, फिर भी विवाह मिलान में भाव-संतुलन देखें।" if mitigations else "विवाह मिलान में मंगल संतुलन का ध्यान रखें।")
        )
        present_primary = True
    elif moon_manglik:
        subtype = f"Non-Manglik from Lagna / Mild Chandra-Manglik (Moon House {fm})"
        severity = "Low (Non-Manglik from Lagna; Mild Moon-Chart Placement Only)"
        status_hi = (
            f"लग्न कुंडली से अमांगलिक (मंगल भाव {fl} में शुभ/तटस्थ स्थान पर है)। "
            f"केवल चंद्र कुंडली से भाव {fm} में होने से आंशिक चंद्र-मांगलिक प्रभाव है"
            + (f", जो गुरु/शुभ प्रभाव ({'; '.join(mitigations)}) से पूर्णतः सौम्य व निष्प्रभावी है।" if mitigations else "।")
        )
        present_primary = False
    else:
        subtype = "Purely Non-Manglik (पूर्णतः अमांगलिक)"
        severity = "None (Non-Manglik)"
        status_hi = f"पूर्णतः अमांगलिक: मंगल लग्न से भाव {fl} तथा चंद्र से भाव {fm} में दोष-मुक्त स्थित है।"
        present_primary = False

    return {
        "from_lagna": fl,
        "from_moon": fm,
        "from_venus": fv,
        "present_from_lagna": lagna_manglik,
        "present_from_moon": moon_manglik,
        "present_from_venus": venus_manglik,
        "present": present_primary,
        "subtype": subtype,
        "severity": severity,
        "status_hi": status_hi,
        "mitigations": mitigations,
        "cancellations": mitigations,  # backward-compatible key
    }


def compute_life_diagnostics(P, asc, shadbala, sav, jaimini, func_nature, mangal_info):
    """Synthesize evidence-backed Career, Runa/Debt (6th-12th vs 2nd-11th), Marriage (D9+DK+UL) & Personality diagnostics."""
    la = sign(asc)
    H = lambda k: (sign(P[k]) - la) % 12 + 1
    sav_h = sav["sarvashtakavarga_houses"]

    # 1. Career: Technical vs Managerial Aptitude (10th House, 10L, D10, AmK, SAV)
    l10 = SIGNLORD[(la + 9) % 12]
    amk = jaimini["chara_karakas"]["AmK"]["planet"]
    tech_planets = {"Mars", "Saturn", "Rahu", "Ketu", "Mercury"}
    mgr_planets = {"Sun", "Jupiter", "Venus", "Moon"}
    occ_10 = [k for k in P if H(k) == 10]
    tech_score = sum(1 for x in ([l10, amk] + occ_10) if x in tech_planets)
    mgr_score = sum(1 for x in ([l10, amk] + occ_10) if x in mgr_planets)

    career_orientation = (
        "Technical + Strategic Hybrid (तकनीकी विशेषज्ञता के साथ उच्च प्रबंधकीय नेतृत्व)"
        if (tech_score > 0 and mgr_score > 0)
        else "Hardcore Technical / Analytical / Systems Specialist (तकनीकी, इंजीनियरिंग व विश्लेषणात्मक क्षेत्र)"
        if tech_score > mgr_score
        else "Executive Management, Advisory & Administration (प्रबंधन, प्रशासन व परामर्श क्षेत्र)"
    )

    # 2. Financial & Debt / Runa Yoga Audit (2nd/11th vs 6th/12th SAV & Lords)
    l2 = SIGNLORD[(la + 1) % 12]
    l6 = SIGNLORD[(la + 5) % 12]
    l11 = SIGNLORD[(la + 10) % 12]
    l12 = SIGNLORD[(la + 11) % 12]
    sav_income = sav_h[2] + sav_h[11]
    sav_outflow = sav_h[6] + sav_h[12]
    runa_flags = []
    if H(l2) in (6, 8, 12) or H(l11) in (6, 8, 12):
        runa_flags.append(f"धनेश ({l2}, भाव {H(l2)}) अथवा लाभेश ({l11}, भाव {H(l11)}) का दुःस्थान (6/8/12) से संबंध")
    if sav_h[12] > sav_h[11]:
        runa_flags.append(f"व्यय भाव (12वें भाव में {sav_h[12]} बिंदु) का लाभ भाव (11वें भाव में {sav_h[11]} बिंदु) से अधिक होना")
    if any(H(k) == 6 for k in ("Mars", "Saturn", "Rahu")):
        occ6 = [k for k in ("Mars", "Saturn", "Rahu") if H(k) == 6]
        runa_flags.append(f"छठे भाव (ऋण/प्रतिस्पर्धा) में {occ6} की उपस्थिति (शत्रु-हंता पर ऋण में सावधानी)")

    # 3. Marriage & Spouse Profile (7th House, 7L, D9, DK, UL)
    l7 = SIGNLORD[(la + 6) % 12]
    dk = jaimini["chara_karakas"]["DK"]["planet"]
    ul = jaimini["key_padas"]["UL_upapada_lagna"]

    # 4. Shastric Upayas for the most challenged planets (Debilitated, Combust, Low Shadbala, or Badhakesh/8th/12th)
    priority_planets = []
    for p in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]:
        sb = shadbala[p]
        if dignity(p, sign(P[p])) == "debilitated" or not sb["meets_bphs_threshold"] or not sb["ishta_dominant"]:
            priority_planets.append(p)
    if mangal_info["present"] and "Mars" not in priority_planets:
        priority_planets.insert(0, "Mars")
    if not priority_planets:
        priority_planets = [SIGNLORD[la], SIGNLORD[(la + 8) % 12]]

    recommended_upayas = {p: BPHS_SHASTRIC_UPAYAS[p] for p in priority_planets[:4]}

    return {
        "career_and_vocation": {
            "tenth_lord": l10,
            "tenth_lord_house": H(l10),
            "tenth_lord_d10_sign": SIGNS[d10(P[l10])],
            "amatyakaraka_amk": amk,
            "tenth_house_sav_bindus": sav_h[10],
            "aptitude_classification": career_orientation,
        },
        "wealth_and_runa_debt_audit": {
            "second_house_sav": sav_h[2],
            "sixth_house_sav": sav_h[6],
            "eleventh_house_sav": sav_h[11],
            "twelfth_house_sav": sav_h[12],
            "income_vs_outflow_sav_ratio": f"{sav_income} (2H+11H) vs {sav_outflow} (6H+12H)",
            "runa_caution_triggers": runa_flags,
            "financial_guidance_hi": (
                "अष्टकवर्ग में लाभ व संचय बलवान है; अनुशासित निवेश से स्थायी संपत्ति बनेगी।"
                if sav_income >= sav_outflow and not runa_flags
                else "ऋण/व्यय प्रबंधन में विशेष अनुशासन रखें: बिना लिखित अनुबंध के उधार न दें और उच्च ब्याज वाले ऋण (Unsecured Debt) से बचें।"
            ),
        },
        "marriage_and_partnership": {
            "seventh_lord": l7,
            "seventh_lord_house": H(l7),
            "seventh_lord_d9_sign": SIGNS[d9(P[l7])],
            "darakaraka_dk": dk,
            "darakaraka_d9_sign": SIGNS[d9(P[dk])],
            "upapada_lagna_ul_sign": ul["sign"],
            "upapada_lord": ul["lord_of_arudha"],
            "mangal_dosha_summary": mangal_info["status_hi"],
        },
        "bphs_shastric_upayas": {
            "basis": "Brihat Parashara Hora Shastra (BPHS Ch. 84–97) — Sattvika Mantra, Dana/Seva, Aushadhi & Behavioral Karma (No Commercial Gemstones)",
            "priority_planets": list(recommended_upayas.keys()),
            "remedies": recommended_upayas,
        },
    }


def chart(p):
    dt, jd, P, retro, asc, speeds, lats = raw_chart(p)
    la = sign(asc)
    house = lambda l: (sign(l) - la) % 12 + 1
    sunrise_str = compute_local_sunrise(dt, p["lat"], p["lon"], p.get("tz", 5.5))
    panchanga = compute_panchanga(dt, P, sunrise_str)
    chalit = compute_sripati_chalit(jd, p["lat"], p["lon"], P, la)
    shadbala = compute_shadbala_and_avasthas(P, speeds, retro, asc, dt, sunrise_str)
    sav = compute_ashtakavarga(P, asc)
    jaimini = compute_jaimini_system(P, asc)
    func_nature = compute_functional_nature_and_badhaka(la, P)
    wars = detect_graha_yuddha(P, lats)

    planets = {}
    for k, v in P.items():
        s_idx = sign(v)
        d9_idx = d9(v)
        comb = check_combustion(k, v, P["Sun"], retro.get(k, False))
        sg = check_sandhi_and_gandanta(v)
        vargas = all_vargas(v)
        sb = shadbala.get(k, {})

        planets[k] = {
            "lon": round(v, 4),
            "sign": SIGNS[s_idx],
            "sign_hi": SIGNS_HI[s_idx],
            "deg": round(v % 30, 2),
            "speed_deg_per_day": round(speeds.get(k, 0.0), 4),
            "gati": classify_gati(k, speeds.get(k, 0.0)),
            "nakshatra": NAK[nak(v)],
            "nakshatra_hi": NAK_HI[nak(v)],
            "pada": pada(v),
            "nakshatra_lord": LORD[nak(v) % 9],
            "kp_sub_lord": kp_sub_lord(v),
            "house": house(v),
            "chalit_house": chalit["planets"][k]["chalit_house"],
            "chalit_shifted": chalit["planets"][k]["shifted"],
            "dignity": dignity(k, s_idx),
            "retrograde": retro.get(k, False),
            "combust": comb["combust"],
            "combustion_detail": comb,
            "vargottama": s_idx == d9_idx,
            "pushkara_navamsa": is_pushkara_navamsa(v),
            "pushkara_bhaga": is_pushkara_bhaga(v),
            "rashi_sandhi": sg["rashi_sandhi"],
            "gandanta": sg["gandanta"],
            "gandanta_detail": sg["gandanta_detail"],
            "d9_sign": SIGNS[d9_idx],
            "d9_dignity": dignity(k, d9_idx),
            "d10_sign": SIGNS[d10(v)],
            "vargas": vargas,
            "bav_bindus_in_natal_sign": sav["planet_natal_bav_scores"].get(k),
            "shadbala_rupas": sb.get("total_rupas"),
            "shadbala_ratio": sb.get("shadbala_ratio"),
            "ishta_phala": sb.get("ishta_phala_virupas"),
            "kashta_phala": sb.get("kashta_phala_virupas"),
            "avasthas": sb.get("avasthas"),
        }

    houses = {}
    for h in range(1, 13):
        s_idx = (la + h - 1) % 12
        L = SIGNLORD[s_idx]
        houses[h] = {
            "sign": SIGNS[s_idx],
            "sign_hi": SIGNS_HI[s_idx],
            "lord": L,
            "lord_in_house": house(P[L]),
            "occupants": [k for k, v in P.items() if house(v) == h],
            "chalit_occupants": [k for k, info in chalit["planets"].items() if info["chalit_house"] == h],
            "aspected_by": aspects_on(P, asc, h),
            "sav_bindus": sav["sarvashtakavarga_houses"][h],
        }

    mangal_info = mangal(P, asc)
    diagnostics = compute_life_diagnostics(P, asc, shadbala, sav, jaimini, func_nature, mangal_info)
    asc_sg = check_sandhi_and_gandanta(asc)

    res = {
        "name": p.get("name"),
        "engine": "swisseph-moshier-astro-devaish-v2",
        "ayanamsa": "Lahiri (Chitrapaksha)",
        "house_system": "Whole-Sign (Rashi Tulya Bhava) + Sripati Bhava Chalit",
        "panchanga": panchanga,
        "ascendant": {
            "lon": round(asc, 4),
            "sign": SIGNS[la],
            "sign_hi": SIGNS_HI[la],
            "deg": round(asc % 30, 2),
            "nakshatra": NAK[nak(asc)],
            "nakshatra_hi": NAK_HI[nak(asc)],
            "pada": pada(asc),
            "nakshatra_lord": LORD[nak(asc) % 9],
            "kp_sub_lord": kp_sub_lord(asc),
            "vargottama": la == d9(asc),
            "rashi_sandhi": asc_sg["rashi_sandhi"],
            "gandanta": asc_sg["gandanta"],
            "d9_sign": SIGNS[d9(asc)],
            "d10_sign": SIGNS[d10(asc)],
            "vargas": all_vargas(asc),
        },
        "planets": planets,
        "houses": houses,
        "bhava_chalit": chalit,
        "shadbala_and_avasthas": shadbala,
        "functional_nature_and_badhaka": func_nature,
        "jaimini_system": jaimini,
        "ashtakavarga": sav,
        "graha_yuddha": wars,
        "yogas": yogas(P, asc),
        "mangal_dosha": mangal_info,
        "life_diagnostics_and_upayas": diagnostics,
        "dasha": dasha_tree(P["Moon"], dt),
        "yogini_dasha": compute_yogini_dasha(P["Moon"], dt),
        "confidence": {
            "birth_time_accuracy": p.get("birth_time_accuracy", "unknown"),
            "note": "Ascendant, D9 lagna, D10 and finer vargas (D16-D60) are birth-time sensitive.",
        },
    }
    mb = P["Moon"] % 30
    if mb < 2 or mb > 28:
        res["confidence"]["moon_near_sign_boundary"] = True
    return res


# ---------- Ashtakoota ----------
VAR = [3, 2, 1, 4, 3, 2, 1, 4, 3, 2, 1, 4]
YONI = [
    "Horse", "Elephant", "Sheep", "Serpent", "Serpent", "Dog", "Cat", "Sheep", "Cat",
    "Rat", "Rat", "Cow", "Buffalo", "Tiger", "Buffalo", "Tiger", "Deer", "Deer",
    "Dog", "Monkey", "Mongoose", "Monkey", "Lion", "Horse", "Lion", "Cow", "Elephant",
]
AN = [
    "Horse", "Elephant", "Sheep", "Serpent", "Dog", "Cat", "Rat",
    "Cow", "Buffalo", "Tiger", "Deer", "Monkey", "Mongoose", "Lion",
]
YM = [
    [4, 2, 2, 3, 2, 2, 2, 1, 0, 1, 3, 3, 2, 1],
    [2, 4, 3, 3, 2, 2, 2, 2, 3, 1, 2, 3, 2, 0],
    [2, 3, 4, 2, 1, 2, 1, 3, 3, 1, 2, 0, 3, 1],
    [3, 3, 2, 4, 2, 1, 1, 1, 1, 2, 2, 2, 0, 2],
    [2, 2, 1, 2, 4, 2, 1, 2, 2, 1, 0, 2, 1, 1],
    [2, 2, 2, 1, 2, 4, 0, 2, 2, 1, 3, 3, 2, 1],
    [2, 2, 1, 1, 1, 0, 4, 2, 2, 2, 2, 2, 1, 2],
    [1, 2, 3, 1, 2, 2, 2, 4, 3, 0, 3, 2, 2, 1],
    [0, 3, 3, 1, 2, 2, 2, 3, 4, 1, 2, 2, 2, 1],
    [1, 1, 1, 2, 1, 1, 2, 0, 1, 4, 1, 1, 2, 1],
    [3, 2, 2, 2, 0, 3, 2, 3, 2, 1, 4, 2, 2, 1],
    [3, 3, 0, 2, 2, 3, 2, 2, 2, 1, 2, 4, 3, 2],
    [2, 2, 3, 0, 1, 2, 1, 2, 2, 2, 2, 3, 4, 2],
    [1, 0, 1, 2, 1, 1, 2, 1, 1, 1, 1, 2, 2, 4],
]


def vashya(s, d):
    if s in (0, 1):
        return "Chatushpada"
    if s == 8:
        return "Manava" if d < 15 else "Chatushpada"
    if s == 9:
        return "Chatushpada" if d < 15 else "Jalachara"
    if s in (2, 5, 6, 10):
        return "Manava"
    if s in (3, 11):
        return "Jalachara"
    return "Vanachara" if s == 4 else "Keeta"


GANA = {i: "Deva" for i in [0, 4, 6, 7, 12, 14, 16, 21, 26]}
GANA.update({i: "Manushya" for i in [1, 3, 5, 10, 11, 19, 20, 24, 25]})
for _i in range(27):
    GANA.setdefault(_i, "Rakshasa")
GT = {
    ("Deva", "Deva"): 6, ("Deva", "Manushya"): 6, ("Deva", "Rakshasa"): 1,
    ("Manushya", "Deva"): 5, ("Manushya", "Manushya"): 6, ("Manushya", "Rakshasa"): 0,
    ("Rakshasa", "Deva"): 0, ("Rakshasa", "Manushya"): 0, ("Rakshasa", "Rakshasa"): 6,
}
ND = ["Adi", "Madhya", "Antya", "Antya", "Madhya", "Adi"]


def match(a, b):
    """a = bride, b = groom (the bundled Gana table is keyed (bride, groom))."""
    _, _, PA, _, AA, _, _ = raw_chart(a)
    _, _, PB, _, AB, _, _ = raw_chart(b)
    gm, bm = PA["Moon"], PB["Moon"]
    gs, bs = sign(gm), sign(bm)
    gn, bn = nak(gm), nak(bm)
    s = {}
    s["varna"] = 1 if VAR[bs] >= VAR[gs] else 0
    gv, bv = vashya(gs, gm % 30), vashya(bs, bm % 30)
    s["vashya"] = 2 if gv == bv else 1 if {gv, bv} == {"Manava", "Chatushpada"} else 0.5
    r1 = (((bn - gn) % 27) + 1) % 9 or 9
    r2 = (((gn - bn) % 27) + 1) % 9 or 9
    s["tara"] = (0 if r1 in (3, 5, 7) else 1.5) + (0 if r2 in (3, 5, 7) else 1.5)
    s["yoni"] = YM[AN.index(YONI[gn])][AN.index(YONI[bn])]
    gl, bl = SIGNLORD[gs], SIGNLORD[bs]
    s["graha_maitri"] = 5 if gl == bl else {
        ("F", "F"): 5, ("F", "N"): 4, ("N", "N"): 3, ("E", "F"): 1, ("E", "N"): 0.5, ("E", "E"): 0
    }[tuple(sorted([rel(gl, bl), rel(bl, gl)]))]
    s["gana"] = GT[(GANA[gn], GANA[bn])]
    d1 = ((bs - gs) % 12) + 1
    d2 = ((gs - bs) % 12) + 1
    s["bhakoot"] = 0 if (d1, d2) in [(2, 12), (12, 2), (5, 9), (9, 5), (6, 8), (8, 6)] else 7
    s["nadi"] = 0 if ND[gn % 6] == ND[bn % 6] else 8
    tot = sum(s.values())
    return {
        "scores": s,
        "total": tot,
        "out_of": 36,
        "percent": round(tot / 36 * 100),
        "band": "good (24+)" if tot >= 24 else "acceptable (18-23.5)" if tot >= 18 else "weak (<18)",
        "detail": {
            "bride_moon": f"{SIGNS[gs]} / {NAK[gn]}",
            "groom_moon": f"{SIGNS[bs]} / {NAK[bn]}",
            "vashya": [gv, bv],
            "tara_remainders": [r1, r2],
            "yoni": [YONI[gn], YONI[bn]],
            "moon_lords": [gl, bl],
            "gana": [GANA[gn], GANA[bn]],
            "moon_sign_relation": [d1, d2],
            "nadi": [ND[gn % 6], ND[bn % 6]],
        },
        "mangal": {"bride": mangal(PA, AA), "groom": mangal(PB, AB)},
        "lord_links": {
            "bride_7th_lord": SIGNLORD[(sign(AA) + 6) % 12],
            "groom_7th_lord": SIGNLORD[(sign(AB) + 6) % 12],
            "bride_lagna_lord": SIGNLORD[sign(AA)],
            "groom_lagna_lord": SIGNLORD[sign(AB)],
        },
        "caveats": [
            "Gana for Deva bride / Rakshasa groom is scored 0 or 1 depending on source; this engine uses 1",
            "Moon-based scores change if a birth time error moves the Moon sign or nakshatra",
        ],
    }


def dasha_at(p, at):
    c = chart(p)
    for m in c["dasha"]:
        if m["start"] <= at < m["end"]:
            for a in m["antardashas"]:
                if a["start"] <= at < a["end"]:
                    pratyantar = None
                    for pr in a.get("pratyantardashas", []):
                        if pr["start"] <= at < pr["end"]:
                            pratyantar = pr
                            break
                    return {
                        "maha": m["lord"],
                        "maha_period": [m["start"], m["end"]],
                        "antar": a["lord"],
                        "antar_period": [a["start"], a["end"]],
                        "pratyantar": pratyantar["lord"] if pratyantar else None,
                        "pratyantar_period": [pratyantar["start"], pratyantar["end"]] if pratyantar else None,
                    }
    return None


def transit(p, start, years=3):
    _, _, P, _, asc, _, _ = raw_chart(p)
    la = sign(asc)
    ms = sign(P["Moon"])
    sav = compute_ashtakavarga(P, asc)
    out = {}

    def moorthi_nirnaya(transit_moon_house):
        if transit_moon_house in (1, 6, 11):
            return "Swarna Moorthi (स्वर्ण पाद — शुभ/उच्च फल)"
        if transit_moon_house in (2, 5, 9):
            return "Rajata Moorthi (रजत पाद — अत्यंत शुभ व लाभकारी)"
        if transit_moon_house in (3, 7, 10):
            return "Tamra Moorthi (ताम्र पाद — मध्यम/संतुलित प्रगति)"
        return "Loha Moorthi (लोह पाद — कड़ा परिश्रम व सावधानी)"

    for nm, body in [("Jupiter", 5), ("Saturn", 6), ("Rahu", 10), ("Ketu", -1)]:
        d = start
        jd = swe.julday(d.year, d.month, d.day, 0)
        lon0 = (swe.calc_ut(jd, 10, FL)[0][0] + 180) % 360 if body == -1 else swe.calc_ut(jd, body, FL)[0][0]
        prev = sign(lon0)
        hm0 = (prev - ms) % 12 + 1
        hl0 = (prev - la) % 12 + 1
        ev = [{
            "date": d.date().isoformat(),
            "sign": SIGNS[prev],
            "sign_hi": SIGNS_HI[prev],
            "house_from_moon": hm0,
            "house_from_lagna": hl0,
            "sav_bindus_in_sign": sav["sarvashtakavarga_signs"][SIGNS[prev]],
            "bav_bindus_in_sign": sav["bhinna_ashtakavarga_signs"].get(nm, {}).get(SIGNS[prev]),
            "moorthi_paya": moorthi_nirnaya(hm0),
        }]
        end = start + timedelta(days=365.25 * years)
        while d < end:
            d += timedelta(days=2)
            jd = swe.julday(d.year, d.month, d.day, 0)
            lon_cur = (swe.calc_ut(jd, 10, FL)[0][0] + 180) % 360 if body == -1 else swe.calc_ut(jd, body, FL)[0][0]
            s = sign(lon_cur)
            if s != prev:
                prev = s
                hm = (s - ms) % 12 + 1
                hl = (s - la) % 12 + 1
                ev.append({
                    "date": d.date().isoformat(),
                    "sign": SIGNS[s],
                    "sign_hi": SIGNS_HI[s],
                    "house_from_moon": hm,
                    "house_from_lagna": hl,
                    "sav_bindus_in_sign": sav["sarvashtakavarga_signs"][SIGNS[s]],
                    "bav_bindus_in_sign": sav["bhinna_ashtakavarga_signs"].get(nm, {}).get(SIGNS[s]),
                    "moorthi_paya": moorthi_nirnaya(hm),
                })
        out[nm] = ev

    sade = [e for e in out["Saturn"] if e["house_from_moon"] in (12, 1, 2)]
    dhaiya_ashtama = [
        {**e, "phase": "Kantaka Shani / Dhaiya (4th from Moon — कंटक शनि ढैय्या)" if e["house_from_moon"] == 4 else "Ashtama Shani (8th from Moon — अष्टम शनि ढैय्या)"}
        for e in out["Saturn"] if e["house_from_moon"] in (4, 8)
    ]

    # Double Transit (Jupiter + Saturn) on current start date
    j_cur_s = SIGNS.index(out["Jupiter"][0]["sign"])
    s_cur_s = SIGNS.index(out["Saturn"][0]["sign"])
    j_reach = {j_cur_s, (j_cur_s + 4) % 12, (j_cur_s + 6) % 12, (j_cur_s + 8) % 12}
    s_reach = {s_cur_s, (s_cur_s + 2) % 12, (s_cur_s + 6) % 12, (s_cur_s + 9) % 12}
    double_transit_signs = sorted(list(j_reach & s_reach))
    double_transit_houses = [
        {"house_from_lagna": (s_idx - la) % 12 + 1, "sign": SIGNS[s_idx], "sign_hi": SIGNS_HI[s_idx]}
        for s_idx in double_transit_signs
    ]

    return {
        "ingresses": out,
        "saturn_sade_sati_entries": sade,
        "saturn_dhaiya_and_ashtama_entries": dhaiya_ashtama,
        "current_double_transit_activated_houses": double_transit_houses,
        "note": "Dates approximate (+-2 days). Includes SAV/BAV transit cushion and Moorthi Nirnaya (Swarna/Rajata/Tamra/Loha).",
    }


def sky(date, time, lat, lon, tz, sidereal):
    dt = datetime.strptime(date + " " + time, "%Y-%m-%d %H:%M")
    jd = jd_of(dt, tz)
    out = {}
    names = [
        ("Sun", 0), ("Moon", 1), ("Mercury", 2), ("Venus", 3), ("Mars", 4),
        ("Jupiter", 5), ("Saturn", 6), ("Uranus", 7), ("Neptune", 8),
    ]
    fl = swe.FLG_MOSEPH | swe.FLG_SPEED | (swe.FLG_SIDEREAL if sidereal else 0)
    for n, i in names:
        r = swe.calc_ut(jd, i, fl)[0]
        eq = swe.calc_ut(jd, i, swe.FLG_MOSEPH | swe.FLG_EQUATORIAL)[0]
        az = swe.azalt(jd, swe.EQU2HOR, (lon, lat, 0), 0, 10, (eq[0], eq[1], eq[2]))
        ph = swe.pheno_ut(jd, i, swe.FLG_MOSEPH)
        out[n] = {
            "lon": round(r[0], 3),
            "lat": round(r[1], 3),
            "dist_au": round(r[2], 4),
            "ra_h": round(eq[0] / 15, 3),
            "dec": round(eq[1], 3),
            "alt": round(az[1], 2),
            "az": round(az[0], 2),
            "mag": None if n == "Sun" else round(ph[4], 2),
            "elong_deg": round(ph[2], 1),
            "retrograde": r[3] < 0,
        }
    return {"time_local": dt.isoformat(), "zodiac": "sidereal-Lahiri" if sidereal else "tropical", "bodies": out}


def load(path):
    with open(path) as f:
        return json.load(f)


def load_or_inline(a):
    if getattr(a, "input", None):
        return load(a.input)
    if getattr(a, "dob", None):
        return {
            "name": getattr(a, "name", ""),
            "dob": a.dob,
            "tob": getattr(a, "tob", "12:00"),
            "lat": getattr(a, "lat", 28.6139),
            "lon": getattr(a, "lon", 77.2090),
            "tz": getattr(a, "tz", 5.5),
            "place": getattr(a, "place", "India"),
            "birth_time_accuracy": "exact",
        }
    raise ValueError("Provide either --input person.json or --dob YYYY-MM-DD [--tob HH:MM --lat L --lon L]")


def cli_main():
    ap = argparse.ArgumentParser(description="Astro DevAish Classical Vedic Jyotish & Ganita Engine")
    sp = ap.add_subparsers(dest="cmd", required=True)
    for c in ("chart", "dasha", "transit"):
        x = sp.add_parser(c)
        x.add_argument("--input", required=False, help="Path to person.json")
        x.add_argument("--name", default="")
        x.add_argument("--dob", required=False, help="YYYY-MM-DD (alternative to --input)")
        x.add_argument("--tob", default="12:00", help="HH:MM")
        x.add_argument("--lat", type=float, default=28.6139)
        x.add_argument("--lon", type=float, default=77.2090)
        x.add_argument("--tz", type=float, default=5.5)
        x.add_argument("--place", default="India")
        if c == "dasha":
            x.add_argument("--at", default=datetime.now().date().isoformat())
        if c == "transit":
            x.add_argument("--from", dest="frm", default=datetime.now().date().isoformat())
            x.add_argument("--years", type=float, default=3)
    m = sp.add_parser("match")
    m.add_argument("--a", required=True)
    m.add_argument("--b", required=True)
    s = sp.add_parser("sky")
    s.add_argument("--date", required=True)
    s.add_argument("--time", default="21:00")
    s.add_argument("--lat", type=float, required=True)
    s.add_argument("--lon", type=float, required=True)
    s.add_argument("--tz", type=float, default=5.5)
    s.add_argument("--sidereal", action="store_true")
    a = ap.parse_args()
    if a.cmd == "chart":
        r = chart(load_or_inline(a))
    elif a.cmd == "dasha":
        r = dasha_at(load_or_inline(a), a.at)
    elif a.cmd == "transit":
        r = transit(load_or_inline(a), datetime.strptime(a.frm, "%Y-%m-%d"), a.years)
    elif a.cmd == "match":
        r = match(load(a.a), load(a.b))
    else:
        r = sky(a.date, a.time, a.lat, a.lon, a.tz, a.sidereal)
    print(json.dumps(r, indent=2, default=str, ensure_ascii=False))


if __name__ == "__main__":
    cli_main()
