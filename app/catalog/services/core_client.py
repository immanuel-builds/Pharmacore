from app.core.services.interaction_service import InteractionService

def analyze_interactions(substances):
    """
    Actual CORE API integration.
    Calls the Core Intelligence InteractionService.
    """
    results = InteractionService.analyze_interactions(substances)

    # Calculate aggregate confidence and sources
    confidence = 0.0
    sources = set()
    if results:
        confidence = sum(r['confidence'] for r in results) / len(results)
        for r in results:
            if r['source']:
                sources.add(r['source'])
    else:
        confidence = 1.0 # default for no interactions
        sources.add("mechanism_database")

    return {
        "interactions": results,
        "confidence": round(confidence, 2),
        "sources": list(sources)
    }
