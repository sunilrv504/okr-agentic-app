import json
from typing import Dict

def validator(structure: Dict) -> str:
    """
    Sanity check OKR structure. Return JSON: {"warnings":[...]}
    """
    warnings = []
    try:
        krs = structure.get("krs", [])
        if not (4 <= len(krs) <= 6):
            warnings.append("Recommend 4-6 Key Results.")
        # simple checks
        for epic in structure.get("epics", []):
            for feat in epic.get("features", []):
                if not feat.get("stories"):
                    warnings.append(f"Feature {feat.get('title')} has no stories.")
        return json.dumps({"warnings": warnings})
    except Exception as e:
        return json.dumps({"warnings":[f"Validation failed: {str(e)}"]})