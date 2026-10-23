# 🗺️ 100% Free Forever Map & Healthcare Referral Architecture

DermaVision incorporates a zero-cost geospatial architecture that requires **no Google Maps API keys**, **no credit card**, and **no Google Cloud billing accounts**, while delivering real, verified medical centers and turn-by-turn navigation.

---

## 🚫 The Problem with Commercial Map APIs

* **Google Places API** requires active billing accounts, credit cards, and charges per query ($0.032 - $0.05 per Place Search).
* Projects run the risk of sudden rate-limit failures, expired keys, or unauthorized billing spikes during hackathon demonstrations.

---

## 💡 The DermaVision Zero-Cost Solution

Our architecture pairs open-source geospatial infrastructure with direct Google Maps deep-link routing:

```
[Patient Device]
      │
      ▼
1. Free IP Geolocation (ip-api.com, zero credentials)
      │
      ▼
2. OpenStreetMap Overpass Healthcare Query
   • amenity = hospital | clinic | doctors (within 15 km)
   • Multi-mirror fallback (overpass-api.de, overpass.kumi.systems)
      │
      ▼
3. Geodesic Haversine Distance Ranking (in km)
      │
      ▼
4. Direct Google Maps Navigation Link Generation
   • https://www.google.com/maps/dir/?api=1&destination={lat},{lon}
   • https://www.google.com/maps/search/dermatologists+near+me/@{lat},{lon},13z
```

---

## ✅ Advantages for Healthcare Deployments

1. **Permanently Free:** Zero ongoing costs, suitable for non-profit and public health deployments.
2. **Zero Dummy Data:** Displays real hospitals, genuine addresses, and true GPS-calculated distances.
3. **Turn-by-Turn Navigation:** One click opens native Google Maps on mobile devices or desktop browsers with walking/driving directions, live opening hours, and phone numbers.
4. **Resilient Failover:** If an OSM server is temporarily slow, the system automatically falls back to geocoded city queries and direct Google Maps search intent.
