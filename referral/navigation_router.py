"""
NavigationRouter: Google Maps Live Turn-by-Turn Navigation & Routing Generator
Generates direct navigation intent URLs for mobile and web Google Maps.
"""

import urllib.parse
from typing import Optional

class NavigationRouter:
    """
    Constructs Google Maps navigation and geographic search URLs.
    No API key or billing required.
    """

    @staticmethod
    def build_direct_navigation_url(lat: float, lon: float) -> str:
        """Generates direct turn-by-turn routing URL to coordinates."""
        return f"https://www.google.com/maps/dir/?api=1&destination={lat},{lon}"

    @staticmethod
    def build_specialist_search_url(
        location_name: Optional[str] = None,
        lat: Optional[float] = None,
        lon: Optional[float] = None
    ) -> str:
        """
        Generates Google Maps specialist search URL.
        Uses exact GPS coordinate centering when available.
        """
        if lat is not None and lon is not None:
            return f"https://www.google.com/maps/search/dermatologists+near+me/@{lat},{lon},13z"
        
        loc_str = location_name or "Current Location"
        encoded = urllib.parse.quote(f"dermatologists near {loc_str}")
        return f"https://www.google.com/maps/search/{encoded}"
