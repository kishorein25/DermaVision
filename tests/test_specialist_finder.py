# ==============================================================================
# DermaVision: Unit Tests for 100% Free Forever Specialist Finder
# ==============================================================================

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from specialist_finder import SpecialistFinder

def test_geolocation_and_routing():
    print("[TEST] Testing 100% Free Forever IP Geolocation & Specialist Routing...")
    finder = SpecialistFinder()
    
    # 1. Location detection
    loc, lat, lon = finder.detect_user_location()
    print(f" -> Auto-detected location: {loc} ({lat}, {lon})")
    assert loc is not None and len(loc) > 0, "FAIL: Location detection returned empty string!"

    # 2. Healthcare finding
    res = finder.find_specialists(location=loc, lat=lat, lon=lon)
    print(f" -> Success: {res.get('success')}")
    print(f" -> Source: {res.get('source')}")
    print(f" -> Total Found: {res.get('total_found')}")
    print(f" -> Maps Search URL: {res.get('maps_search_url')}")

    assert res.get("success") is True, "FAIL: Specialist finder did not return success!"
    assert "maps_search_url" in res, "FAIL: Maps search URL missing!"
    print("[PASSED] Free Forever Specialist Finder successfully tested!")

if __name__ == "__main__":
    test_geolocation_and_routing()
    print("\nALL SPECIALIST FINDER TESTS PASSED SUCCESSFULLY!")
