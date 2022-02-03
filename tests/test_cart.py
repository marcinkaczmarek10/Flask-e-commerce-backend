import unittest
from src import create_app
from src.config import TestingConfig


class AppTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.app = create_app(TestingConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()

    def tearDown(self) -> None:
        self.app_context.pop()

    def test_add_to_cart(self):
        res = self.client.post('/add-item/1')
        self.assertEqual(res.status_code, 200)
