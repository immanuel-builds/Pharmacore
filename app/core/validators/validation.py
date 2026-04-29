def validate_substance(data):
    """
    Validates substance data.
    Reject missing names, nonsense values, low-confidence junk.
    """
    if not data.get('name') or not isinstance(data['name'], str):
        return False, "Missing or invalid name"

    if data.get('confidence') is not None:
        try:
            conf = float(data['confidence'])
            if conf < 0 or conf > 1:
                return False, "Confidence must be between 0 and 1"
            if conf < 0.3: # Threshold for 'low-confidence junk'
                return False, "Confidence too low"
        except (ValueError, TypeError):
            return False, "Invalid confidence value"

    if data.get('half_life_hours') is not None:
        try:
            hl = float(data['half_life_hours'])
            if hl <= 0:
                return False, "Half life must be positive"
        except (ValueError, TypeError):
            return False, "Invalid half life value"

    return True, None

def validate_interaction(data):
    """
    Validates interaction data.
    """
    if not data.get('substance_a_id') or not data.get('substance_b_id'):
        return False, "Missing substance IDs"

    if data['substance_a_id'] == data['substance_b_id']:
        return False, "Substances must be different"

    if data.get('confidence') is not None:
        try:
            conf = float(data['confidence'])
            if conf < 0.3:
                return False, "Confidence too low"
        except (ValueError, TypeError):
            return False, "Invalid confidence value"

    return True, None
