import unittest
import json
from app import create_app, db
from app.core.ingestion.seed_loader import load_seed_data
import os

class CoreApiTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app({
            'TESTING': True,
            'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'
        })
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()
            # Manually load a small subset of seed data for testing if needed
            # or use the seed_loader with a test file
            seed_file = os.path.join(os.path.dirname(__file__), '..', 'app', 'core', 'ingestion', 'data', 'seed.json')
            # Adjust seed_loader to take app context or similar if necessary,
            # but here we just call the function which creates its own app context...
            # Actually, let's just use the real loader on the in-memory DB by passing the app
            self.load_test_data()

    def load_test_data(self):
        # Simplified loader for test context
        from app.core.models.substance import Substance
        from app.core.models.interaction import Interaction
        from app.core.models.symptom import Symptom
        from app.core.models.mapping import SymptomMapping

        s1 = Substance(name="Warfarin", half_life_hours=40, confidence=1.0, verified=True)
        s2 = Substance(name="Aspirin", half_life_hours=0.25, confidence=1.0, verified=True)
        db.session.add_all([s1, s2])
        db.session.commit()

        i = Interaction(substance_a_id=s1.id, substance_b_id=s2.id, severity="critical", confidence=1.0)
        db.session.add(i)

        sym = Symptom(name="Respiratory Depression")
        db.session.add(sym)
        db.session.commit()

        m = SymptomMapping(substance_id=s1.id, symptom_id=sym.id, relevance_score=0.9)
        db.session.add(m)
        db.session.commit()

    def test_health_check(self):
        response = self.client.get('/core/health')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'healthy', response.data)

    def test_interactions(self):
        response = self.client.post('/core/interactions',
                                    data=json.dumps({'substances': ['Warfarin', 'Aspirin']}),
                                    content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'success')
        self.assertTrue(len(data['data']) > 0)
        self.assertEqual(data['data'][0]['severity'], 'critical')

    def test_clinical(self):
        response = self.client.post('/core/clinical',
                                    data=json.dumps({'symptoms': ['Respiratory Depression']}),
                                    content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['data'][0]['substance'], 'Warfarin')

    def test_simulation(self):
        response = self.client.post('/core/simulation',
                                    data=json.dumps({'substances': [{'name': 'Warfarin', 'dose': 10, 'start_time': 0}]}),
                                    content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['data'][0]['name'], 'Warfarin')
        self.assertTrue(len(data['data'][0]['concentrations']) > 0)

if __name__ == '__main__':
    unittest.main()
