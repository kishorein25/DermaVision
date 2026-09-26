import os
import json
import math
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

_CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config.json")
_GOOGLE_KEY = None
_PLACES_URL = "https://places.googleapis.com/v1/places:searchText"


def _get_google_key():
    global _GOOGLE_KEY
    if _GOOGLE_KEY is not None:
        return _GOOGLE_KEY
    _GOOGLE_KEY = os.environ.get("GOOGLE_MAPS_API_KEY", "")
    if not _GOOGLE_KEY:
        try:
            with open(_CONFIG_PATH, "r", encoding="utf-8") as f:
                _GOOGLE_KEY = json.load(f).get("google_maps_api_key", "")
        except Exception:
            _GOOGLE_KEY = ""
    return _GOOGLE_KEY


def find_nearby_doctors(location=None, lat=None, lon=None, radius_km=10):
    """Find nearby dermatologists. Tries Google Places API (if key set),
    then falls back to free OpenStreetMap.
    """
    try:
        key = _get_google_key()
        if key:
            doctors = _search_google(location=location, lat=lat, lon=lon, radius_km=radius_km)
            if doctors:
                return {"success": True, "source": "google", "doctors": doctors}
        doctors = _search_osm(location=location, lat=lat, lon=lon, radius_km=radius_km)
        if doctors:
            return {"success": True, "source": "openstreetmap", "doctors": doctors}
        return {
            "success": False,
            "message": "No dermatologists found nearby. Please use Google Maps and search 'dermatologist near me'.",
            "doctors": [],
        }
    except Exception as e:
        logger.warning("Doctor finder error: %s", e)
        return {
            "success": False,
            "message": "Doctor lookup unavailable. Please search Google Maps for 'dermatologist near me'.",
            "doctors": [],
        }


def _geocode(location):
    """Returns (lat, lon) for a place name via OSM Nominatim (free)."""
    import urllib.request
    import urllib.parse

    query = f"https://nominatim.openstreetmap.org/search?q={urllib.parse.quote(location)}&format=json&limit=1"
    req = urllib.request.Request(query, headers={"User-Agent": "skin-disease-detector/1.0"})
    with urllib.request.urlopen(req, timeout=8) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    if data:
        return float(data[0]["lat"]), float(data[0]["lon"])
    return None, None


def _search_google(location=None, lat=None, lon=None, radius_km=10, max_results=5):
    import urllib.request

    if lat is None or lon is None:
        if not location:
            return []
        lat, lon = _geocode(location)
        if lat is None:
            return []

    payload = {
        "textQuery": "dermatologist skin specialist",
        "locationBias": {
            "circle": {
                "center": {"latitude": lat, "longitude": lon},
                "radius": max(radius_km * 1000, 1000),
            }
        },
        "pageSize": max_results,
    }
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": _get_google_key(),
        "X-Goog-FieldMask": (
            "places.displayName,places.formattedAddress,places.location,"
            "places.nationalPhoneNumber,places.rating,places.userRatingCount,"
            "places.businessStatus,places.websiteUri"
        ),
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(_PLACES_URL, data=data, headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=15) as resp:
        body = json.loads(resp.read().decode("utf-8"))

    results = []
    for place in body.get("places", []):
        name_obj = place.get("displayName", {}) or {}
        loc = place.get("location") or {}
        status = place.get("businessStatus", "")
        if status == "CLOSED_PERMANENTLY":
            continue
        dist_km = _haversine(lat, lon, loc.get("latitude", lat), loc.get("longitude", lon))
        results.append({
            "name": name_obj.get("text") or "Dermatology Clinic",
            "address": place.get("formattedAddress", "Address unavailable"),
            "distance_km": round(dist_km, 1),
            "phone": place.get("nationalPhoneNumber", "Not available"),
            "specialty": "Dermatology",
            "opening_hours": "Call to confirm",
            "rating": place.get("rating"),
            "reviews": place.get("userRatingCount", 0),
            "website": place.get("websiteUri", ""),
        })
    results.sort(key=lambda x: x["distance_km"])
    return results[:max_results]


def _search_osm(location=None, lat=None, lon=None, radius_km=10):
    import urllib.request
    import urllib.parse

    if lat is None or lon is None:
        if not location:
            return []
        lat, lon = _geocode(location)
        if lat is None:
            return []

    overpass_query = f"""
    [out:json];
    (
      nwr["healthcare:speciality"~"dermatology|skin"](around:{int(radius_km*1000)},{lat},{lon});
      nwr["amenity"="doctors"](around:{int(radius_km*1000)},{lat},{lon});
      nwr["amenity"="clinic"](around:{int(radius_km*1000)},{lat},{lon});
      nwr["healthcare"="clinic"](around:{int(radius_km*1000)},{lat},{lon});
      nwr["healthcare"="doctor"](around:{int(radius_km*1000)},{lat},{lon});
    );
    out center 20;
    """
    query_url = "https://overpass-api.de/api/interpreter"
    req = urllib.request.Request(
        query_url,
        data=urllib.parse.urlencode({"data": overpass_query}).encode("utf-8"),
        headers={"User-Agent": "skin-disease-detector/1.0"},
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read().decode("utf-8"))

    results = []
    for el in data.get("elements", []):
        tags = el.get("tags", {})
        name = tags.get("name") or tags.get("operator") or "Medical Clinic"
        el_lat, el_lon = _coords(el)
        if el_lat is None:
            continue
        dist_km = _haversine(lat, lon, el_lat, el_lon)
        results.append({
            "name": name,
            "address": (tags.get("addr:street", "") + ", " + tags.get("addr:city", "")).strip(", "),
            "distance_km": round(dist_km, 1),
            "phone": tags.get("phone", tags.get("contact:phone", "Not available")),
            "specialty": tags.get("healthcare:speciality", tags.get("healthcare", "General")),
            "opening_hours": tags.get("opening_hours", "Call to confirm"),
        })
    results.sort(key=lambda x: x["distance_km"])
    return results[:5]


def _coords(element):
    if "lat" in element and "lon" in element:
        return element["lat"], element["lon"]
    if "center" in element:
        return element["center"]["lat"], element["center"]["lon"]
    return None, None


def _haversine(lat1, lon1, lat2, lon2):
    r = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    return r * 2 * math.asin(math.sqrt(a))