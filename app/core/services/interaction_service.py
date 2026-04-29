from app.core.models.interaction import Interaction
from app.core.models.substance import Substance

class InteractionService:
    @staticmethod
    def analyze_interactions(substance_names):
        """
        Detects and explains interactions between a list of substances.
        """
        if not substance_names or len(substance_names) < 2:
            return []

        # Find substance IDs
        substances = Substance.query.filter(Substance.name.in_(substance_names)).all()
        substance_ids = [s.id for s in substances]
        id_to_name = {s.id: s.name for s in substances}

        if len(substance_ids) < 2:
            return []

        # Query interactions where both substances are in our list
        # Since interactions are stored as (A, B), we check both combinations or just ensure a < b
        interactions = Interaction.query.filter(
            Interaction.substance_a_id.in_(substance_ids),
            Interaction.substance_b_id.in_(substance_ids)
        ).all()

        results = []
        for interaction in interactions:
            results.append({
                "substances": [id_to_name[interaction.substance_a_id], id_to_name[interaction.substance_b_id]],
                "severity": interaction.severity,
                "risk_score": interaction.risk_score,
                "mechanism": interaction.mechanism,
                "description": interaction.description,
                "confidence": interaction.confidence,
                "source": interaction.source
            })

        return results
