import unittest
from app import create_app, db
from app.auth.models.user import User
from app.auth.services import auth_service

class AuthTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app({
            'TESTING': True,
            'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
            'SECRET_KEY': 'test'
        })
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_register_user(self):
        user, error = auth_service.register_user("test@example.com", "password123", "Test User")
        self.assertIsNone(error)
        self.assertIsNotNone(user)
        self.assertEqual(user.email, "test@example.com")
        self.assertEqual(user.name, "Test User")

    def test_register_duplicate_email(self):
        auth_service.register_user("test@example.com", "password123", "Test User")
        user, error = auth_service.register_user("test@example.com", "password456", "Another User")
        self.assertEqual(error, "Email already exists")
        self.assertIsNone(user)

    def test_login_user(self):
        auth_service.register_user("test@example.com", "password123", "Test User")
        with self.app.test_request_context():
            user, error = auth_service.login_user("test@example.com", "password123")
            self.assertIsNone(error)
            self.assertIsNotNone(user)

    def test_api_login_logout_me(self):
        self.client.post('/auth/register', json={
            'email': 'api@test.com',
            'password': 'password123',
            'name': 'API User'
        })
        self.client.post('/auth/login', json={'email': 'api@test.com', 'password': 'password123'})
        response = self.client.get('/auth/me')
        self.assertEqual(response.status_code, 200)
        self.client.post('/auth/logout')
        response = self.client.get('/auth/me')
        self.assertEqual(response.status_code, 401)

if __name__ == '__main__':
    unittest.main()
