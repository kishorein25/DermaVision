"""
MedicalSearchAgent: Scientific Knowledge Cross-Referencing & PubMed Integration
Generates deep clinical verification links and cross-references authoritative archives.
"""

import urllib.parse
from typing import Dict, Any, List

class MedicalSearchAgent:
    """
    Interfaces with international dermatological knowledge repositories:
    - PubMed / NCBI
    - DermNet New Zealand
    - British Association of Dermatologists (BAD)
    - American Academy of Dermatology (AAD)
    """

    ARCHIVE_DATABASES = {
        "pubmed": "https://pubmed.ncbi.nlm.nih.gov/?term=",
        "dermnet": "https://dermnetnz.org/search?q=",
        "google_scholar": "https://scholar.google.com/scholar?q="
    }

    @classmethod
    def generate_verification_queries(cls, condition: str, region: str) -> Dict[str, str]:
        """Constructs clinical verification queries and direct academic search links."""
        clean_condition = condition.strip()
        encoded = urllib.parse.quote(f"{clean_condition} clinical presentation dermatology {region}")
        pubmed_query = urllib.parse.quote(f"{clean_condition}[Title/Abstract] AND {region}")

        return {
            "google_search": f"https://www.google.com/search?q={encoded}",
            "pubmed_search": f"{cls.ARCHIVE_DATABASES['pubmed']}{pubmed_query}",
            "dermnet_search": f"{cls.ARCHIVE_DATABASES['dermnet']}{urllib.parse.quote(clean_condition)}",
            "scholar_search": f"{cls.ARCHIVE_DATABASES['google_scholar']}{encoded}"
        }

    @classmethod
    def build_audit_entry(cls, candidate: str, region: str) -> Dict[str, str]:
        """Builds a query package for a single differential candidate."""
        query = f"dermatology {candidate} differential diagnosis {region}"
        url = f"https://www.google.com/search?q={urllib.parse.quote(query)}"
        return {
            "search_query": query,
            "google_url": url
        }
