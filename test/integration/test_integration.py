import unittest
from datetime import datetime
import json
from unittest.mock import Mock
from unittest.mock import patch
import redis

import api
from store import RedisStore
from test.help_testing import cases, set_valid_auth, get_store_cache_key


def interest_find(key):
    data = {'i:0': json.dumps(["books", "hi-tech"]),
            'i:1': json.dumps(["pets", "tv"]),
            'i:2': json.dumps(["travel", "music"]),
            'i:3': json.dumps(['cinema', 'geek'])}
    return data[key]


attrs_mock = {'set.side_effect': None,
              'cache_get.return_value': None,
              'get.side_effect': interest_find}


class TestFunctionalSuite(unittest.TestCase):
    @patch("redis.StrictRedis")
    def setUp(self):
        with patch("redis.StrictRedis") as redis_mock:
            redis_mock.ping.return_value = None
            redis_mock.get.side_effect

        self.store = RedisStore(**attrs_mock)

    def test_cache_get_connected(self, key):