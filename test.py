import unittest
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


class TestModuleSuite(unittest.TestCase):
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

    def test_empty_request(self):
        _, code = self.get_response({})
        self.assertEqual(api.INVALID_REQUEST, code)

    @cases([
        {"account": "horns&hoofs", "login": "h&f", "method": "online_score", "token": "", "arguments": {}},
        {"account": "horns&hoofs", "login": "h&f", "method": "online_score", "token": "sdd", "arguments": {}},
        {"account": "horns&hoofs", "login": "admin", "method": "online_score", "token": "", "arguments": {}},
    ])
    def test_bad_auth(self, request):
        _, code = self.get_response(request)
        self.assertEqual(api.FORBIDDEN, code)

    @cases([
        {"account": "horns&hoofs", "login": "h&f", "method": "online_score", "token": 11, "arguments": {}},
        {"account": "horns&hoofs", "login": "h&f", "method": "online_score", "token": 11., "arguments": {}},
        {"account": "horns&hoofs", "login": "admin", "method": "online_score", "arguments": {}}
    ])
    def test_invalid_token(self, request):
        _, code = self.get_response(request)
        self.assertEqual(api.INVALID_REQUEST, code)

    @cases([
        {"account": 5555, "login": "h&f", "method": "online_score", "arguments": {}},
        {"account": 5555., "login": "h&f", "method": "online_score", "arguments": {}}
    ])
    def test_invalid_account(self, request):
        self.set_valid_auth(request)
        response, code = self.get_response(request)
        self.assertEqual(api.INVALID_REQUEST, code)
        self.assertTrue(len(response))

    @cases([
        {"account": "horns&hoofs", "login": 222, "method": "online_score", "arguments": {}},
        {"account": "horns&hoofs", "login": 222.222, "method": "online_score", "arguments": {}},
        {"account": "horns&hoofs", "method": "online_score", "arguments": {}}
    ])
    def test_invalid_login(self, request):
        self.set_valid_auth(request)
        response, code = self.get_response(request)
        self.assertEqual(api.INVALID_REQUEST, code)
        self.assertTrue(len(response))

    @cases([
        {"account": "horns&hoofs", "login": "h&f", "method": "online_score", "arguments": '3'},
        {"account": "horns&hoofs", "login": "h&f", "method": "online_score", "arguments": [3]},
        {"account": "horns&hoofs", "login": "h&f", "method": "online_score", "arguments": (3,)},
        {"account": "horns&hoofs", "login": "h&f", "method": "online_score", "arguments": 3.},
        {"account": "horns&hoofs", "login": "h&f", "method": "online_score", "arguments": 3},
        {"account": "horns&hoofs", "login": "h&f", "method": "online_score"},
    ])
    def test_invalid_arguments(self, request):
        self.set_valid_auth(request)
        response, code = self.get_response(request)
        self.assertEqual(api.INVALID_REQUEST, code)
        self.assertTrue(len(response))

    @cases([
        {"account": "horns&hoofs", "login": "h&f", "arguments": {}},
        {"account": "horns&hoofs", "login": "h&f", "method": "online_request", "arguments": {}},
        {"account": "horns&hoofs", "login": "h&f", "method": "", "arguments": {}},
        {"account": "horns&hoofs", "login": "h&f", "method": 2, "arguments": {}},
        {"account": "horns&hoofs", "login": "h&f", "method": 2., "arguments": {}},
        {"account": "horns&hoofs", "login": "h&f", "method": [2], "arguments": {}},
        {"account": "horns&hoofs", "login": "h&f", "method": (2,), "arguments": {}}
    ])
    def test_invalid_method_request(self, request):
        self.set_valid_auth(request)
        response, code = self.get_response(request)
        self.assertEqual(api.INVALID_REQUEST, code)
        self.assertTrue(len(response))

    @cases([
        {"phone": "79175002040", "email": "dev@otus.ru", "gender": 1, "birthday": "01.01.2000", "first_name": 1},
        {"phone": "79175002040", "email": "dev@otus.ru", "gender": 1, "birthday": "01.01.2000", "first_name": 1.34}
        ])
    def test_invalid_first_name(self, arguments):
        request = {"account": "horns&hoofs", "login": "h&f", "method": "online_score", "arguments": arguments}
        self.set_valid_auth(request)
        response, code = self.get_response(request)
        self.assertEqual(api.INVALID_REQUEST, code, arguments)
        self.assertTrue(len(response))

    @cases([
        {"phone": "79175002040", "email": "dev@otus.ru", "gender": 1, "birthday": "01.01.2000", "last_name": 123},
        {"phone": "79175002040", "email": "dev@otus.ru", "gender": 1, "birthday": "01.01.2000", "last_name": 1.43}
    ])
    def test_invalid_last_name(self, arguments):
        request = {"account": "horns&hoofs", "login": "h&f", "method": "online_score", "arguments": arguments}
        self.set_valid_auth(request)
        response, code = self.get_response(request)
        self.assertEqual(api.INVALID_REQUEST, code, arguments)
        self.assertTrue(len(response))

    @cases([
        {"phone": "7917500d040", "email": "devotus.ru", "gender": 1, "birthday": "01.01.2000", "last_name": "a"},
        {"phone": "7917500d040", "email": 43, "gender": 1, "birthday": "01.01.2000", "last_name": "a"},
        {"phone": "7917500d040", "email": 532.564, "gender": 1, "birthday": "01.01.2000", "last_name": "a"},
        {"phone": "7917500d040", "email": "dev@otusru", "gender": 1, "birthday": "01.01.2000", "last_name": "a"},
        {"phone": "79175002040", "email": "dev@otus.ru333", "gender": 1, "birthday": "01.01.2000", "last_name": "a"}
    ])
    def test_invalid_email(self, arguments):
        request = {"account": "horns&hoofs", "login": "h&f", "method": "online_score", "arguments": arguments}
        self.set_valid_auth(request)
        response, code = self.get_response(request)
        self.assertEqual(api.INVALID_REQUEST, code, arguments)
        self.assertTrue(len(response))

    @cases([
        {"phone": 56, "email": "dev@otus.ru", "gender": 1, "birthday": "01.01.2000", "last_name": "a"},
        {"phone": 79175002040.0, "email": "dev@otus.ru", "gender": 1, "birthday": "01.01.2000", "last_name": "a"},
        {"phone": "a", "email": "dev@otus.ru", "gender": 1, "birthday": "01.01.2000", "last_name": "a"},
        {"phone": "7917500d040", "email": "dev@otus.ru", "gender": 1, "birthday": "01.01.2000", "last_name": "a"},
        {"phone": "791750020400", "email": "dev@otus.ru", "gender": 1, "birthday": "01.01.2000", "last_name": "a"},
        {"phone": "+79175002040", "email": "dev@otus.ru", "gender": 1, "birthday": "01.01.2000", "last_name": "a"}
    ])
    def test_invalid_phone(self, arguments):
        request = {"account": "horns&hoofs", "login": "h&f", "method": "online_score", "arguments": arguments}
        self.set_valid_auth(request)
        response, code = self.get_response(request)
        self.assertEqual(api.INVALID_REQUEST, code, arguments)
        self.assertTrue(len(response))

    @cases([
        {"phone": "79175002040", "email": "dev@otus.ru", "gender": 1, "birthday": "01.01.20", "last_name": "a"},
        {"phone": "79175002040", "email": "dev@otus.ru", "gender": 1, "birthday": "01/01/2000", "last_name": "a"},
        {"phone": "79175002040", "email": "dev@otus.ru", "gender": 1, "birthday": "01-01-2000", "last_name": "a"},
        {"phone": "79175002040", "email": "dev@otus.ru", "gender": 1, "birthday": "01.01.1930", "last_name": "a"},
        {"phone": "79175002040", "email": "dev@otus.ru", "gender": 1, "birthday": "05.30.2020", "last_name": "a"},
        {"phone": "79175002040", "email": "dev@otus.ru", "gender": 1, "birthday": 30052020, "last_name": "a"}
    ])
    def test_invalid_birthday(self, arguments):
        request = {"account": "horns&hoofs", "login": "h&f", "method": "online_score", "arguments": arguments}
        self.set_valid_auth(request)
        response, code = self.get_response(request)
        self.assertEqual(api.INVALID_REQUEST, code, arguments)
        self.assertTrue(len(response))

    @cases([
        {"phone": "79175002040", "email": "dev@otus.ru", "gender": -1, "birthday": "01.01.2020", "last_name": "a"},
        {"phone": "79175002040", "email": "dev@otus.ru", "gender": "1", "birthday": "01.01.2020", "last_name": "a"},
        {"phone": "79175002040", "email": "dev@otus.ru", "gender": 1.0, "birthday": "01.01.2020", "last_name": "a"}
    ])
    def test_invalid_gender(self, arguments):
        request = {"account": "horns&hoofs", "login": "h&f", "method": "online_score", "arguments": arguments}
        self.set_valid_auth(request)
        response, code = self.get_response(request)
        self.assertEqual(api.INVALID_REQUEST, code, arguments)
        self.assertTrue(len(response))

    @cases([
        {"date": "01-01-2020", "client_ids": [1, 2]},
        {"date": "01/01/2020", "client_ids": [1, 2]},
        {"date": "01.01.20", "client_ids": [1, 2]},
        {"date": "05.30.2020", "client_ids": [1, 2]},
        {"date": 30052020, "client_ids": [1, 2]}
    ])
    def test_invalid_date(self, arguments):
        request = {"account": "horns&hoofs", "login": "h&f", "method": "clients_interests", "arguments": arguments}
        self.set_valid_auth(request)
        response, code = self.get_response(request)
        self.assertEqual(api.INVALID_REQUEST, code, arguments)
        self.assertTrue(len(response))

    @cases([
        {"date": "01.01.2020"},
        {"date": "01.01.2020", "client_ids": []},
        {"date": "01.01.2020", "client_ids": (1, 2)},
        {"date": "01.01.2020", "client_ids": 1},
        {"date": "01.01.2020", "client_ids": 1.4},
        {"date": "01.01.2020", "client_ids": ["a"]},
        {"date": "01.01.2020", "client_ids": ["1"]}
    ])
    def test_invalid_client_ids(self, arguments):
        request = {"account": "horns&hoofs", "login": "h&f", "method": "clients_interests", "arguments": arguments}
        self.set_valid_auth(request)
        response, code = self.get_response(request)
        self.assertEqual(api.INVALID_REQUEST, code, arguments)
        self.assertTrue(len(response))

    @cases([
        {},
        {"phone": "79175002040"},
        {"phone": "79175002040", "gender": 1},
        {"phone": "79175002040", "gender": 1, "first_name": "s"},
        {"email": "dev@otus.ru", "birthday": "01.01.2000", "first_name": "s"},
    ])
    def test_invalid_score_request(self, arguments):
        request = {"account": "horns&hoofs", "login": "h&f", "method": "online_score", "arguments": arguments}
        self.set_valid_auth(request)
        response, code = self.get_response(request)
        self.assertEqual(api.INVALID_REQUEST, code, arguments)
        self.assertTrue(len(response))

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
    def test_ok_score_request(self, arguments):
        request = {"account": "horns&hoofs", "login": "h&f", "method": "online_score", "arguments": arguments}
        self.set_valid_auth(request)
        response, code = self.get_response(request)
        self.assertEqual(api.OK, code, arguments)
        score = response.get("score")
        self.assertTrue(isinstance(score, (int, float)) and score >= 0, arguments)
        self.assertEqual(sorted(self.context["has"]), sorted(arguments.keys()))

    def test_ok_score_admin_request(self):
        arguments = {"phone": "79175002040", "email": "dev@otus.ru"}
        request = {"account": "horns&hoofs", "login": "admin", "method": "online_score", "arguments": arguments}
        self.set_valid_auth(request)
        response, code = self.get_response(request)
        self.assertEqual(api.OK, code)
        score = response.get("score")
        self.assertEqual(score, 42)

    @cases([
        {"client_ids": [1, 2, 3], "date": datetime.datetime.today().strftime("%d.%m.%Y")},
        {"client_ids": [1, 2], "date": "19.07.2017"},
        {"client_ids": [0]},
    ])
    def test_ok_interests_request(self, arguments):
        request = {"account": "horns&hoofs", "login": "h&f", "method": "clients_interests", "arguments": arguments}
        self.set_valid_auth(request)
        response, code = self.get_response(request)
        self.assertEqual(api.OK, code, arguments)
        self.assertEqual(len(arguments["client_ids"]), len(response))
        self.assertTrue(all(v and isinstance(v, list) for v in response.values()))
        self.assertEqual(self.context.get("nclients"), len(arguments["client_ids"]))


if __name__ == "__main__":
    unittest.main()
