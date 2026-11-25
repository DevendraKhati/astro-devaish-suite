# Life-dimension recipes (condensed)

Always read in this order: **D1 promise -> D9 (or the dimension's varga) confirm/deny -> yogas -> dasha + transit timing.**
State conflicts between D1 and D9 honestly. Every finding must be traceable ("her 7th lord Mercury sits in the 8th in D1...").
Use `scripts/jyotish.py chart` output fields: `houses[h].lord / lord_in_house / occupants / aspected_by`, `planets[p].dignity / d9_sign`, `yogas`, `dasha`.

| Dimension | Houses / lords | Karakas | D1 checks | Varga | Timing |
|---|---|---|---|---|---|
| Marriage | 7th, its lord, 2nd, 8th, UL if used | Venus (Jupiter for women's charts in some schools) | lord of 7 placement, aspects on 7 (`aspected_by`), Moon/Venus condition, Mangal | D9: Venus, 7th lord, D9 7th | Dasha/antardasha of 7th lord, Venus, Jupiter, planets in 7th; Jupiter/Saturn transit over 7th or Moon |
| Career | 10th, lord, 6th, 2nd, 11th; Sun/Saturn/Mercury | Saturn, Sun | 10th lord house, aspects on 10, 9th-10th links | D10 (needs exact time) | 10th lord/9th lord dashas; Saturn/Jupiter transit |
| Wealth | 2nd, 11th, 5th, 9th and lords | Jupiter, Venus | 2/11 lords, dhana links, 8th for inheritance, 12th for outflow | D2 (optional) | Dashas of 2/11/5/9 lords |
| Children | 5th, lord, 9th, 2nd | Jupiter | 5th lord placement, planets in/aspecting 5th, Jupiter strength | D7 (time-sensitive) | Dashas of 5th lord/Jupiter; Jupiter transit to 5th/9th from Moon |
| Health (preventive only) | Lagna, 6th, 8th, 12th, lagna lord | Sun, Moon | Lagna lord strength, malefics on lagna/6/8, Moon condition | D6/D30 (time-sensitive) | Phrase as "vulnerable periods" with preventive care |
| Education | 4th, 5th, 9th, 2nd | Mercury, Jupiter | 4/5 lords, Jupiter/Mercury | D24 (time-sensitive) | Dashas of 4/5 lords |
| Property/home | 4th, lord, Mars, Saturn | Mars (property), Venus (vehicles) | 4th lord, planets in 4 | D4 | Dashas of 4th lord/Mars |
| Family | 2nd, 4th (mother), 9th (father), 3rd (siblings) | Sun, Moon | Lords and occupants | - | - |
| Travel/foreign | 3rd, 9th, 12th, Rahu | Rahu | 9/12 lords, Rahu placement | - | Dashas of 9/12 lords, Rahu |
| Obstacles | 6th, 8th, 12th, Saturn, Rahu, Mars | - | Markers only, with elevated-risk language | D30 | Marker -> activating dasha -> transit window; always pair with mitigation/agency |
| Karma / past life | 5th, 9th, 12th, nodes | Rahu, Ketu, Saturn | - | D60: **refuse unless birth time is exact** | - |
| Timing | meta-dimension | - | - | - | `dasha`, `transit` commands; Sade Sati = Saturn in 12/1/2 from Moon |

## Reading cautions
- A yoga is a tendency; weigh strength against D1 promise and dasha.
- Mangal Dosha is over-diagnosed. Always list the engine's cancellations (`mangal_dosha.cancellations`) and traditions that differ. Never alarm.
- Kaal Sarp Dosha is later tradition, not classical BPHS: mention cautiously if at all.
- Do not claim yogas the engine did not return. If a classical source is ambiguous, say so.
- No remedies (gems, mantras, rituals) unless the user explicitly asks and the context clearly allows; default is to omit.
- Never predict death, terminal illness, or exact time of death. Use "elevated risk" language only.

## Compatibility (Ashtakoota) reading
36 points. 18+ acceptable, 24+ good. Report each koota with its meaning, flag the weak ones in plain language, check Mangal on both charts, check cross-links (A's 7th lord vs B's lagna lord), then check dasha overlap for marriage timing. Mention that Gana/Tara scoring conventions vary by source.
