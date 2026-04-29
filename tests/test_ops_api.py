import unittest
import json
from app import create_app, db
from app.ops.models.store import Store
from app.ops.models.inventory import Inventory

class OpsApiTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app({
            'TESTING': True,
            'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'
        })
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()
            self.load_test_data()

    def load_test_data(self):
        s1 = Store(name="Store A", location_lat=12.9716, location_lng=77.5946, radius_km=5)
        s2 = Store(name="Store B", location_lat=12.9352, location_lng=77.6245, radius_km=5)
        db.session.add_all([s1, s2])
        db.session.commit()

        i1 = Inventory(store_id=s1.id, product_id=1, stock=50)
        i2 = Inventory(store_id=s2.id, product_id=1, stock=20)
        db.session.add_all([i1, i2])
        db.session.commit()

    def test_health_check(self):
        response = self.client.get('/ops/health')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'healthy', response.data)

    def test_assign_delivery_success(self):
        # User very close to Store A
        user_loc = {"lat": 12.9710, "lng": 77.5940}
        items = [{"product_id": 1, "quantity": 5}]
        response = self.client.post('/ops/delivery/assign',
                                    data=json.dumps({'user_location': user_loc, 'items': items}),
                                    content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['data']['store'], 'Store A')
        self.assertTrue(len(data['data']['reservations']) > 0)

    def test_assign_delivery_no_stock(self):
        user_loc = {"lat": 12.9710, "lng": 77.5940}
        items = [{"product_id": 1, "quantity": 100}]
        response = self.client.post('/ops/delivery/assign',
                                    data=json.dumps({'user_location': user_loc, 'items': items}),
                                    content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertIn('No store available', data['error'])

    def test_assign_delivery_out_of_radius(self):
        # User far away from both stores
        user_loc = {"lat": 13.5, "lng": 78.0}
        items = [{"product_id": 1, "quantity": 5}]
        response = self.client.post('/ops/delivery/assign',
                                    data=json.dumps({'user_location': user_loc, 'items': items}),
                                    content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
