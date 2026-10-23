"""
OSMOverpassClient: OpenStreetMap Live Healthcare Registry Query Client
Extracts real registered hospitals, clinics, and doctors within geographic radius.
"""

import requests
from typing import List, Dict, Any, Optional

class OSMOverpassClient:
    """
    Queries public OpenStreetMap Overpass servers with automatic multi-mirror failover.
    Zero API credentials or billing setup needed.
    """

    MIRRORS = [
        "https://overpass-api.de/api/interpreter",
        "https://overpass.kumi.systems/api/interpreter",
        "https://maps.mail.ru/osm/tools/overpass/api/interpreter"
    ]

    HEADERS = {
        "User-Agent": "DermaVision-Overpass-Client/2.0 (medical@dermavision.ai)"
    }

    @classmethod
    def query_nearby_healthcare(
        cls,
        lat: float,
        lon: float,
        radius_meters: int = 15000,
        timeout_seconds: int = 12
    ) -> List[Dict[str, Any]]:
        """Queries Overpass API for amenities: hospital, clinic, doctors."""
        query = f"""
        [out:json][timeout:{timeout_seconds}];
        (
          node["amenity"="hospital"](around:{radius_meters}, {lat}, {lon});
          node["amenity"="clinic"](around:{radius_meters}, {lat}, {lon});
          node["amenity"="doctors"](around:{radius_meters}, {lat}, {lon});
          way["amenity"="hospital"](around:{radius_meters}, {lat}, {lon});
          way["amenity"="clinic"](around:{radius_meters}, {lat}, {lon});
        );
        out center 15;
        """

        for mirror_url in cls.MIRRORS:
            try:
                resp = requests.post(mirror_url, data={"data": query}, headers=cls.HEADERS, timeout=timeout_seconds)
                if resp.status_code == 200:
                    data = resp.json()
                    elements = data.get("elements", [])
                    if elements:
                        return elements
            except Exception:
                continue

        return []
