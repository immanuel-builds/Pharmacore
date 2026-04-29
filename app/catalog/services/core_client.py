def analyze_interactions(substances):
    """
    Mock CORE API call.
    In the future, this will call the actual CORE module.
    """
    # Simulate a response from CORE
    if "Paracetamol" in substances and "Ibuprofen" in substances:
         return {
            "interactions": [
                {
                    "severity": "Low",
                    "description": "Generally safe to take together, but monitor for stomach upset.",
                    "source": "Mock CORE"
                }
            ],
            "confidence": 0.8,
            "sources": ["Mock Clinical Database"]
        }

    return {
        "interactions": [],
        "confidence": 0.9,
        "sources": ["Mock Clinical Database"]
    }
