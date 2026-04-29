from app.core.models.symptom import Symptom
from app.core.models.mapping import SymptomMapping
from app.core.models.substance import Substance

class ClinicalService:
    @staticmethod
    def analyze_symptoms(symptom_names):
        """
        Maps symptoms to possible substances.
        """
        if not symptom_names:
            return []

        # Find symptoms
        symptoms = Symptom.query.filter(Symptom.name.in_(symptom_names)).all()
        symptom_ids = [s.id for s in symptoms]

        if not symptom_ids:
            return []

        # Find mappings
        mappings = SymptomMapping.query.filter(SymptomMapping.symptom_id.in_(symptom_ids)).all()

        # Group by substance
        substance_results = {}
        for m in mappings:
            sub_id = m.substance_id
            if sub_id not in substance_results:
                substance_results[sub_id] = {
                    "substance": m.substance.name,
                    "matched_symptoms": [],
                    "total_relevance": 0
                }
            substance_results[sub_id]["matched_symptoms"].append({
                "symptom": m.symptom.name,
                "relevance": m.relevance_score
            })
            substance_results[sub_id]["total_relevance"] += m.relevance_score

        # Convert to list and sort by total relevance
        results = list(substance_results.values())
        results.sort(key=lambda x: x["total_relevance"], reverse=True)

        return results
