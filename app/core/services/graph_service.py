from app.core.models.substance import Substance
from app.core.models.mechanism import MechanismNode

class GraphService:
    @staticmethod
    def get_graph(substance_names):
        """
        Returns nodes and edges for the biological graph (BioScope).
        """
        substances = Substance.query.filter(Substance.name.in_(substance_names)).all()
        substance_ids = [s.id for s in substances]

        nodes = []
        edges = []
        seen_nodes = set()

        for sub in substances:
            # Add drug node
            if sub.name not in seen_nodes:
                nodes.append({"id": sub.name, "type": "drug"})
                seen_nodes.add(sub.name)

            # Add mechanism nodes and edges
            mech_nodes = MechanismNode.query.filter_by(substance_id=sub.id).all()
            for mn in mech_nodes:
                if mn.node_name not in seen_nodes:
                    nodes.append({"id": mn.node_name, "type": mn.node_type})
                    seen_nodes.add(mn.node_name)

                edges.append({
                    "source": sub.name,
                    "target": mn.node_name,
                    "label": mn.effect
                })

        return {"nodes": nodes, "edges": edges}
