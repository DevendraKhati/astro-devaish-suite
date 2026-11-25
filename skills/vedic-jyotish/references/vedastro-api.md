# VedAstro API quick reference (optional online source)

Base: `https://vedastro.zaishi.net/api/Calculate/{Method}` (POST JSON recommended). Free tier: 5 calls/min/IP, no key. Premium: `x-api-key` header.
Default ayanamsa is **RAMAN**; this suite's offline engine uses **LAHIRI**. Say which one a given number used; differences of ~1.5 degrees can move Moon nakshatra/pada.

Body:
```json
{"Time":{"StdTime":"HH:MM DD/MM/YYYY +05:30","Location":{"Name":"Nashik","Longitude":73.7898,"Latitude":19.9975}},"Ayanamsa":"LAHIRI"}
```
Useful methods: `HoroscopePredictions` (200+ rule-based predictions), `MatchReport` (body has `MaleTime`, `FemaleTime`; 16 Kuta factors),
`NameNumberPrediction` (GET `/Name/{name}`; Chaldean), `AllPlanetData` (`"PlanetName":"All"`), `AllHouseData` (`"HouseName":"All"`),
`GeneralAstroData`, `DasaAtRange` (`StartTime`, `EndTime` as DD/MM/YYYY, `Levels` 1-3), `ListAllCalls` (GET, discover 596+ methods).
GET form: `/Calculate/{Method}/Location/{lat},{lon}/Time/{HH:MM}/{DD-MM-YYYY}/{+HH:MM}/Ayanamsa/{NAME}` (dates use `-`, not `/`).
MCP: `https://mcp.vedastro.org/api/mcp` (tools: get_horoscope_predictions, get_match_report, get_numerology_prediction, get_context_based_astrology_data, search_calculate_methods).
Python: `pip install vedastro`.

Treat VedAstro output as a second opinion: `HoroscopePredictions` are generic rule texts, not a tailored reading. Cross-check against `jyotish.py chart`.
In sandboxes with restricted egress the host may be unreachable: use `scripts/vedastro_client.py` (returns a clear error) and fall back to `scripts/jyotish.py`.
