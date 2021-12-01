import unittest
import json
from unittest.mock import patch
import redis

from store import RedisStore, param_store, param_cache


data = {'uid:0': json.dumps(3).encode("utf-8"),
        'uid:1': json.dumps(["pets", "tv"]).encode("utf-8")}


def key_get(key):
    return data.get(key)


class TestGeneralConnectionSuite(unittest.TestCase):

    def setUp(self):
        self.general = RedisStore.from_args(param_store, 'general')
        self.general.connect()

    @patch('redis.StrictRedis.ping')
    def test_ping_connect(self, mock_ping):
        mock_ping.return_value = True
        res = self.general.try_command()
        self.assertEqual(res, True)

    @patch('redis.StrictRedis.ping')
    def test_ping_unconnected(self, mock_ping):
        mock_ping.side_effect = redis.ConnectionError
        res = self.general.try_command()
        self.assertEqual(res, False)

    @patch('redis.StrictRedis.ping')
    @patch('redis.StrictRedis.get')
    def test_get_correct_key(self, mock_get, mock_ping):
        mock_ping.return_value = True
        mock_get.side_effect = key_get
        res = self.general.get('uid:0')
        self.assertTrue(res is not None and isinstance(res, str))

    @patch('redis.StrictRedis.ping')
    @patch('redis.StrictRedis.get')
    def test_get_incorrect_key(self, mock_get, mock_ping):
        mock_ping.return_value = True
        mock_get.side_effect = key_get
        res = self.general.get('uid:2')
        self.assertTrue(res is None)


class TestStoreSuite(unittest.TestCase):

    def setUp(self):
        self.store = RedisStore.from_args(param_store, 'store')
        self.store.connect()

    @patch('redis.StrictRedis.ping')
    @patch('redis.StrictRedis.get')
    def test_set_unconnected(self, mock_get, mock_ping):
        mock_ping.return_value = True
        mock_get.side_effect = redis.exceptions.ConnectionError
        with self.assertRaises(ConnectionError):
            self.store.get('uid:2')

    @patch('redis.StrictRedis.ping')
    @patch('redis.StrictRedis.get')
    def test_set_unconnected(self, mock_get, mock_ping):
        mock_ping.return_value = False
        mock_get.side_effect = redis.ConnectionError
        with self.assertRaises(ConnectionError):
            self.store.get('uid:2')


class TestCacheSuite(unittest.TestCase):

    def setUp(self):
        self.cache = RedisStore.from_args(param_cache, 'cache')
        self.cache.connect()

    @patch('redis.StrictRedis.ping')
    @patch('redis.StrictRedis.get')
    def test_set_unconnected(self, mock_get, mock_ping):
        mock_ping.return_value = True
        mock_get.side_effect = redis.exceptions.ConnectionError
        self.assertIsNone(self.cache.get('uid:2'))

    @patch('redis.StrictRedis.ping')
    @patch('redis.StrictRedis.get')
    def test_store_incorrect_key(self, mock_get, mock_ping):
        mock_ping.return_value = False
        mock_get.side_effect = redis.exceptions.ConnectionError
        self.assertIsNone(self.cache.get('uid:2'))


if __name__ == "__main__":
    unittest.main()
