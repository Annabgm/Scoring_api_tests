import unittest
from unittest.mock import patch
import hashlib
import functools
import datetime

from store import MockStore, MockStoreConnection
import api

def cases(cases):
    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args):
            for c in cases:
                new_args = args + (c if isinstance(c, tuple) else (c,))
                try:
                    f(*new_args)
                except Exception as e:
                    msg = 'Case has failed with attributes:: ' + ', '.join('{}: {}'.format(k, v) for k, v in c.items())
                    print(msg)
                    raise e
        return wrapper
    return decorator


class TestIntergationConnectSuite(unittest.TestCase):
    def setUp(self):
        self.context = {}
        self.headers = {}
        self.store_connection = MockStoreConnection()
        self.store = MockStore(self.store_connection)

    def get_response(self, request):
        return api.method_handler({"body": request, "headers": self.headers}, self.context, self.store)

    def set_valid_auth(self, request):
        if request.get("login") == api.ADMIN_LOGIN:
            request["token"] = hashlib.sha512((datetime.datetime.now().strftime("%Y%m%d%H") +
                                               api.ADMIN_SALT).encode('utf-8')).hexdigest()
        else:
            msg = str(request.get("account", "")) + str(request.get("login", "")) + api.SALT
            request["token"] = hashlib.sha512(msg.encode('utf-8')).hexdigest()

    def get_store_cache_key(self, request):
        arg = request['arguments']
        key_parts = [
            arg.get('first_name', ""),
            arg.get('last_name', ""),
            str(arg.get('phone', "")),
            datetime.datetime.strptime(arg['birthday'], '%d.%m.%Y').strftime("%Y%m%d") if 'birthday' in arg.keys() else "",
        ]
        key = "uid:" + hashlib.md5("".join(key_parts).encode('utf-8')).hexdigest()
        return key


    @cases([
        {"phone": "79175002040", "email": "dev@otus.ru"},
        {"phone": 79175002040, "email": "dev@otus.ru"},
        {"gender": 1, "birthday": "01.01.2000", "first_name": "a", "last_name": "b"},
        {"gender": 0, "birthday": "01.01.2000"},
        {"gender": 2, "birthday": "01.01.2000"},
        {"first_name": "a", "last_name": "b"},
        {"phone": "79175002040", "email": "dev@otus.ru", "gender": 1, "birthday": "01.01.2000",
         "first_name": "a", "last_name": "b"},
    ])
    def test_ok_store_connection_score(self, arguments):
        request = {"account": "horns&hoofs", "login": "h&f", "method": "online_score", "arguments": arguments}
        self.set_valid_auth(request)
        response, code = self.get_response(request)
        self.assertEqual(api.OK, code, arguments)
        key = self.get_store_cache_key(request)
        self.assertTrue(key in self.store.store_cache, arguments)
        self.assertEqual(response.get("score"), self.store.store_cache[key][1], arguments)


class TestIntergationUnconnectSuite(unittest.TestCase):
    def setUp(self):
        self.context = {}
        self.headers = {}
        self.store_connection = MockStoreConnection(connected=False, probability=1)
        self.store = MockStore(self.store_connection)

    def get_response(self, request):
        return api.method_handler({"body": request, "headers": self.headers}, self.context, self.store)

    def set_valid_auth(self, request):
        if request.get("login") == api.ADMIN_LOGIN:
            request["token"] = hashlib.sha512((datetime.datetime.now().strftime("%Y%m%d%H") +
                                               api.ADMIN_SALT).encode('utf-8')).hexdigest()
        else:
            msg = str(request.get("account", "")) + str(request.get("login", "")) + api.SALT
            request["token"] = hashlib.sha512(msg.encode('utf-8')).hexdigest()

    def get_store_cache_key(self, request):
        arg = request['arguments']
        key_parts = [
            arg.get('first_name', ""),
            arg.get('last_name', ""),
            str(arg.get('phone', "")),
            datetime.datetime.strptime(arg['birthday'], '%d.%m.%Y').strftime("%Y%m%d") if 'birthday' in arg.keys() else "",
        ]
        key = "uid:" + hashlib.md5("".join(key_parts).encode('utf-8')).hexdigest()
        return key


    @cases([
        {"phone": "79175002040", "email": "dev@otus.ru"},
        {"first_name": "a", "last_name": "b"},
        {"phone": "79175002040", "email": "dev@otus.ru", "gender": 1, "birthday": "01.01.2000",
         "first_name": "a", "last_name": "b"},
    ])
    def test_no_store_connection_score(self, arguments):
        request = {"account": "horns&hoofs", "login": "h&f", "method": "online_score", "arguments": arguments}
        self.set_valid_auth(request)
        response, code = self.get_response(request)
        key = self.get_store_cache_key(request)
        self.assertTrue(key not in self.store.store_cache, arguments)
        self.assertEqual(api.OK, code, arguments)
        score = response.get("score")
        self.assertTrue(isinstance(score, (int, float)) and score >= 0, arguments)

    @cases([
        {"client_ids": [1, 2, 3], "date": datetime.datetime.today().strftime("%d.%m.%Y")},
        {"client_ids": [1, 2], "date": "19.07.2017"},
        {"client_ids": [0]},
    ])
    def test_no_store_connection_interests(self, arguments):
        request = {"account": "horns&hoofs", "login": "h&f", "method": "clients_interests", "arguments": arguments}
        self.set_valid_auth(request)
        response, code = self.get_response(request)
        self.assertEqual(api.INTERNAL_ERROR, code, arguments)


