#!/usr/bin/env python3
"""Unified Astro DevAish Master CLI (Vedic Jyotish + Vedic Anka-Jyotish + Graha-Anka Cross-Verification).

Can be run from anywhere as:
  astro-devaish --name "Chandan Singh Bisht" --dob 1995-08-26 --tob 22:35 --lat 29.2183 --lon 79.5130 --place "Haldwani"
or with an existing person.json:
  astro-devaish --input person.json
"""
import argparse
import json
from datetime import datetime
import jyotish
import numerology


def run_master(person, at_date=None, transit_years=4, gender="male"):
    if at_date is None:
        at_date = datetime.now().date().isoformat()
    chart_data = jyotish.chart(person)
    dasha_now = jyotish.dasha_at(person, at_date)
    transit_data = jyotish.transit(person, datetime.strptime(at_date, "%Y-%m-%d"), transit_years)
    local_sr = chart_data.get("panchanga", {}).get("local_sunrise", "06:00")

    num_data = numerology.run(
        name=person.get("name", ""),
        dob=person["dob"],
        tob=person.get("tob"),
        sunrise=local_sr,
        gender=gender,
        chart_data=chart_data,
    )

    return {
        "brand": "Astro DevAish",
        "person": person,
        "target_date": at_date,
        "vedic_jyotish_chart": chart_data,
        "active_vimshottari_dasha": dasha_now,
        "gochara_transits": transit_data,
        "vedic_anka_jyotish": num_data,
    }


def main():
    ap = argparse.ArgumentParser(description="Astro DevAish Unified Master CLI (Vedic Jyotish + Vedic Numerology)")
    ap.add_argument("--input", help="Path to person.json (optional if --dob is passed)")
    ap.add_argument("--name", default="", help="Full Name")
    ap.add_argument("--dob", help="Date of Birth YYYY-MM-DD")
    ap.add_argument("--tob", default="12:00", help="Time of Birth HH:MM")
    ap.add_argument("--lat", type=float, default=28.6139, help="Latitude (default 28.6139 New Delhi)")
    ap.add_argument("--lon", type=float, default=77.2090, help="Longitude (default 77.2090 New Delhi)")
    ap.add_argument("--tz", type=float, default=5.5, help="UTC offset hours (default 5.5 IST)")
    ap.add_argument("--place", default="India", help="Birth place name")
    ap.add_argument("--gender", default="male", help="male or female")
    ap.add_argument("--at", default=datetime.now().date().isoformat(), help="Target date YYYY-MM-DD for active Dasha/Transits")
    ap.add_argument("--years", type=float, default=4.0, help="Transit forecast years")
    ap.add_argument("--out", default=None, help="Optional output JSON file path")
    a = ap.parse_args()

    if a.input:
        with open(a.input) as f:
            person = json.load(f)
    elif a.dob:
        person = {
            "name": a.name,
            "dob": a.dob,
            "tob": a.tob,
            "lat": a.lat,
            "lon": a.lon,
            "tz": a.tz,
            "place": a.place,
            "birth_time_accuracy": "exact",
        }
    else:
        ap.error("Provide either --input person.json or --dob YYYY-MM-DD")
        return

    res = run_master(person, at_date=a.at, transit_years=a.years, gender=a.gender)
    formatted = json.dumps(res, indent=2, default=str, ensure_ascii=False)
    if a.out:
        with open(a.out, "w") as f:
            f.write(formatted)
    else:
        print(formatted)


if __name__ == "__main__":
    main()
