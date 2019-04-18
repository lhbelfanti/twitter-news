import unittest
from unittest.mock import MagicMock

from data import DefaultDataManager


class DataManagerTest(unittest.TestCase):
    def setUp(self):
        self._data_manager = DefaultDataManager()

    def test_should_storage_and_give_trending_topics_data(self):
        trending_topics = MagicMock()
        trending_topics.data = {"test", "mock_data"}
        self._data_manager.set_trending_topics(trending_topics)
        saved_data = self._data_manager.get_trending_topics()
        self.assertEqual(trending_topics, saved_data)

    def tearDown(self):
        self._data_manager = None
