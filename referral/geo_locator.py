"""
GeoLocator: Network IP Geolocation & OpenStreetMap Nominatim Geocoder
100% Free Forever - Zero API Key, Zero Credit Card, Zero Billing.
"""

import urllib.parse
import requests
from typing import Tuple, Optional

class GeoLocator:
    """
    Resolves patient geographic location via free IP geolocation and OpenStreetMap Nominatim.
    """

    HEADERS = {
        "User-Agent": "DermaVision-Referral-Engine/2.0 (healthcare-referral; info@dermavision.ai)"
    }

    @classmethod
    def detect_ip_location(cls) -> Tuple[str, Optional[float], Optional[float]]:
        """
        Auto-detects city and GPS latitude/longitude via public network IP lookup.
        Returns: (display_location, latitude, longitude)
        """
        try:
            r = requests.get('http://ip-api.com/json/?fields=status,city,regionName,country,lat,lon', timeout=3.5)
            if r.status_code == 200:
                d = r.json()
                if d.get('status') == 'success':
                    city = d.get('city', '')
                    region = d.get('regionName', '')
                    country = d.get('country', '')
                    loc_name = f"{city}, {region}" if city and region else (city or region or country or "Current Location")
                    return loc_name, float(d.get('lat')), float(d.get('lon'))
        except Exception:
            pass
        return "Current Location", None, None

    @classmethod
    def geocode_address(cls, place_name: str) -> Tuple[Optional[float], Optional[float], str]:
        """
        Converts city, postal code, or area string to (lat, lon) coordinates using Nominatim.
        """
        if not place_name or place_name.strip().lower() in ["current location", "nearby"]:
            return None, None, place_name

        try:
            url = f"https://nominatim.openstreetmap.org/search?q={urllib.parse.quote(place_name)}&format=json&limit=1"
            r = requests.get(url, headers=cls.HEADERS, timeout=4.0)
            if r.status_code == 200:
                data = r.json()
                if len(data) > 0:
                    d = data[0]
                    return float(d["lat"]), float(d["lon"]), d.get("display_name", place_name)
        except Exception:
            pass
        return None, None, place_name
