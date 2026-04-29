import json
import os
from app import create_app, db
from app.core.models.substance import Substance
from app.core.models.interaction import Interaction
from app.core.models.symptom import Symptom
from app.core.models.mapping import SymptomMapping
from app.core.models.mechanism import MechanismNode
from app.core.validators.validation import validate_substance, validate_interaction

def load_seed_data(filepath):
    with open(filepath, 'r') as f:
        data = json.load(f)

    app = create_app()
    with app.app_context():
        # Clear existing data
        db.session.query(MechanismNode).delete()
        db.session.query(SymptomMapping).delete()
        db.session.query(Interaction).delete()
        db.session.query(Symptom).delete()
        db.session.query(Substance).delete()
        db.session.commit()

        # Load Symptoms
        symptom_map = {}
        for s_data in data.get('symptoms', []):
            symptom = Symptom(name=s_data['name'], description=s_data.get('description'))
            db.session.add(symptom)
            db.session.flush()
            symptom_map[symptom.name] = symptom.id

        # Load Substances
        substance_map = {}
        for sub_data in data.get('substances', []):
            is_valid, error = validate_substance(sub_data)
            if not is_valid:
                print(f"Skipping substance {sub_data.get('name')}: {error}")
                continue

            substance = Substance(
                name=sub_data['name'],
                category=sub_data.get('category'),
                mechanism=sub_data.get('mechanism'),
                half_life_hours=sub_data.get('half_life_hours'),
                primary_organ=sub_data.get('primary_organ'),
                confidence=sub_data.get('confidence', 0.0),
                source=sub_data.get('source'),
                verified=sub_data.get('verified', False)
            )
            db.session.add(substance)
            db.session.flush()
            substance_map[substance.name] = substance.id

            # Load Mechanism Nodes
            for node_data in sub_data.get('mechanism_nodes', []):
                node = MechanismNode(
                    substance_id=substance.id,
                    node_name=node_data['node_name'],
                    node_type=node_data['node_type'],
                    effect=node_data['effect']
                )
                db.session.add(node)

            # Load Symptom Mappings
            for mapping_data in sub_data.get('symptom_mappings', []):
                symptom_id = symptom_map.get(mapping_data['symptom_name'])
                if symptom_id:
                    mapping = SymptomMapping(
                        substance_id=substance.id,
                        symptom_id=symptom_id,
                        relevance_score=mapping_data['relevance_score']
                    )
                    db.session.add(mapping)

        # Load Interactions
        for int_data in data.get('interactions', []):
            sub_a_id = substance_map.get(int_data['substance_a'])
            sub_b_id = substance_map.get(int_data['substance_b'])

            if sub_a_id and sub_b_id:
                interaction_data = int_data.copy()
                interaction_data['substance_a_id'] = sub_a_id
                interaction_data['substance_b_id'] = sub_b_id

                is_valid, error = validate_interaction(interaction_data)
                if not is_valid:
                    print(f"Skipping interaction {int_data['substance_a']} + {int_data['substance_b']}: {error}")
                    continue

                interaction = Interaction(
                    substance_a_id=sub_a_id,
                    substance_b_id=sub_b_id,
                    severity=int_data['severity'],
                    risk_score=int_data.get('risk_score'),
                    mechanism=int_data.get('mechanism'),
                    description=int_data.get('description'),
                    confidence=int_data.get('confidence', 0.0),
                    source=int_data.get('source'),
                    verified=int_data.get('verified', False)
                )
                db.session.add(interaction)

        db.session.commit()
        print("Seed data loaded successfully.")

if __name__ == "__main__":
    seed_file = os.path.join(os.path.dirname(__file__), 'data', 'seed.json')
    load_seed_data(seed_file)
