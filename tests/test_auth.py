import unittest
from src import create_app
from src.config import TestingConfig
from src.database.DB import SessionManager
from src.auth.models import User


class AppTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.app = create_app(TestingConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client(use_cookies=True)
        user = User(username='user',
                    email='user@testmail.com',
                    password='test')
        with SessionManager() as session:
            session.add(user)

    def tearDown(self) -> None:
        self.app_context.pop()

    def test_register(self):
        res = self.client.post('/register', data={
            'username': 'user',
            'email': 'user@testmail.com',
            'password': 'test',
            'confirm_password': 'test'
        }, follow_redirects=True)
        self.assertEqual(res.status_code, 200)

    def test_register_authenticated(self):
        pass

    def test_login(self):
        res = self.client.post('/login', data={
            'email': 'user@testmail.com',
            'password': 'test'
        }, follow_redirects=True)
        self.assertEqual(res.status_code, 200)

    def test_logout(self):
        res = self.client.get('/logout', follow_redirects=True)
        self.assertEqual(res.status_code, 200)
