# 📍 DermaVision `referral/` Geospatial Specialist Referral System

This package manages patient location auto-detection, OpenStreetMap healthcare registry queries, and direct Google Maps turn-by-turn navigation links with **zero required API keys, zero billing, and zero credit cards**.

---

## 📂 Architecture

```
referral/
├── __init__.py               # Package exposure
├── geo_locator.py            # Free network IP geolocation & Nominatim geocoding
├── osm_overpass.py           # Multi-mirror OpenStreetMap Overpass client
├── clinic_ranker.py          # Haversine distance calculation and facility sorting
├── navigation_router.py      # Google Maps turn-by-turn routing generator
└── README.md                 # Geospatial system documentation
```

---

## 🧭 Zero-Cost Geospatial Workflow

1. **Auto-Detection (`geo_locator.py`)**:
   Resolves the patient's approximate coordinates via IP geolocation without requiring browser permission prompts.

2. **Healthcare Registry Query (`osm_overpass.py`)**:
   Queries live OpenStreetMap Overpass nodes within a 15 km radius for `amenity=hospital`, `amenity=clinic`, and `amenity=doctors`.

3. **Geodesic Distance Ranking (`clinic_ranker.py`)**:
   Filters non-human/veterinary amenities and sorts genuine medical centers by real Haversine distance in kilometers.

4. **Navigation Routing (`navigation_router.py`)**:
   Generates deep-link URLs to launch native Google Maps with directions and local phone/hours data.
