import unittest
from flask import current_app
from src import create_app
from src.config import TestingConfig


class AppTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.app = create_app(TestingConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self) -> None:
        self.app_context.pop()

    def test_app(self):
        self.assertIsNotNone(current_app)

    def test_app_testing(self):
        self.assertTrue(current_app.config['TESTING'])