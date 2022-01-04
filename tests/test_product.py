import unittest
from src import create_app
from src.config import TestingConfig


class AppTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.app = create_app(TestingConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self) -> None:
        self.app_context.pop()
