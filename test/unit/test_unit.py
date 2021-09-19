import unittest

import api
from test.help_testing import cases, set_valid_auth


class TestMethodRequestSuite(unittest.TestCase):

    @cases([
        {"account": 5555, "login": "h&f", "method": "online_score", "arguments": {}},
        {"account": 5555., "login": "h&f", "method": "online_score", "arguments": {}}
    ])
    def test_invalid_account(self, request):
        request_obj = api.MethodRequest(**request)
        with self.assertRaises(api.ValidationError):
            request_obj.validate_all()

    @cases([
        {"account": "horns&hoofs", "login": 222, "method": "online_score", "arguments": {}},
        {"account": "horns&hoofs", "login": 222.222, "method": "online_score", "arguments": {}},
        {"account": "horns&hoofs", "method": "online_score", "arguments": {}}
    ])
    def test_invalid_login(self, request):
        request_obj = api.MethodRequest(**request)
        with self.assertRaises(api.ValidationError):
            request_obj.validate_all()

    @cases([
        {"account": "horns&hoofs", "login": "h&f", "method": "online_score", "arguments": '3'},
        {"account": "horns&hoofs", "login": "h&f", "method": "online_score", "arguments": [3]},
        {"account": "horns&hoofs", "login": "h&f", "method": "online_score", "arguments": (3,)},
        {"account": "horns&hoofs", "login": "h&f", "method": "online_score", "arguments": 3.},
        {"account": "horns&hoofs", "login": "h&f", "method": "online_score", "arguments": 3},
        {"account": "horns&hoofs", "login": "h&f", "method": "online_score"},
    ])
    def test_invalid_arguments(self, request):
        request_obj = api.MethodRequest(**request)
        with self.assertRaises(api.ValidationError):
            request_obj.validate_all()

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
        request_obj = api.MethodRequest(**request)
        with self.assertRaises(api.ValidationError):
            request_obj.validate_all()


class TestOnlineScoreSuite(unittest.TestCase):

    @cases([
        {"phone": "79175002040", "email": "dev@otus.ru", "gender": 1, "birthday": "01.01.2000", "first_name": 1},
        {"phone": "79175002040", "email": "dev@otus.ru", "gender": 1, "birthday": "01.01.2000", "first_name": 1.34}
        ])
    def test_invalid_first_name(self, arguments):
        request_obj = api.OnlineScoreRequest(**arguments)
        with self.assertRaises(api.ValidationError):
            request_obj.validate_all()

    @cases([
        {"phone": "79175002040", "email": "dev@otus.ru", "gender": 1, "birthday": "01.01.2000", "last_name": 123},
        {"phone": "79175002040", "email": "dev@otus.ru", "gender": 1, "birthday": "01.01.2000", "last_name": 1.43}
    ])
    def test_invalid_last_name(self, arguments):
        request_obj = api.OnlineScoreRequest(**arguments)
        with self.assertRaises(api.ValidationError):
            request_obj.validate_all()

    @cases([
        {"phone": "7917500d040", "email": "devotus.ru", "gender": 1, "birthday": "01.01.2000", "last_name": "a"},
        {"phone": "7917500d040", "email": 43, "gender": 1, "birthday": "01.01.2000", "last_name": "a"},
        {"phone": "7917500d040", "email": 532.564, "gender": 1, "birthday": "01.01.2000", "last_name": "a"},
        {"phone": "7917500d040", "email": "dev@otusru", "gender": 1, "birthday": "01.01.2000", "last_name": "a"},
        {"phone": "79175002040", "email": "dev@otus.ru333", "gender": 1, "birthday": "01.01.2000", "last_name": "a"}
    ])
    def test_invalid_email(self, arguments):
        request_obj = api.OnlineScoreRequest(**arguments)
        with self.assertRaises(api.ValidationError):
            request_obj.validate_all()

    @cases([
        {"phone": 56, "email": "dev@otus.ru", "gender": 1, "birthday": "01.01.2000", "last_name": "a"},
        {"phone": 79175002040.0, "email": "dev@otus.ru", "gender": 1, "birthday": "01.01.2000", "last_name": "a"},
        {"phone": "a", "email": "dev@otus.ru", "gender": 1, "birthday": "01.01.2000", "last_name": "a"},
        {"phone": "7917500d040", "email": "dev@otus.ru", "gender": 1, "birthday": "01.01.2000", "last_name": "a"},
        {"phone": "791750020400", "email": "dev@otus.ru", "gender": 1, "birthday": "01.01.2000", "last_name": "a"},
        {"phone": "+79175002040", "email": "dev@otus.ru", "gender": 1, "birthday": "01.01.2000", "last_name": "a"}
    ])
    def test_invalid_phone(self, arguments):
        request_obj = api.OnlineScoreRequest(**arguments)
        with self.assertRaises(api.ValidationError):
            request_obj.validate_all()

    @cases([
        {"phone": "79175002040", "email": "dev@otus.ru", "gender": 1, "birthday": "01.01.20", "last_name": "a"},
        {"phone": "79175002040", "email": "dev@otus.ru", "gender": 1, "birthday": "01/01/2000", "last_name": "a"},
        {"phone": "79175002040", "email": "dev@otus.ru", "gender": 1, "birthday": "01-01-2000", "last_name": "a"},
        {"phone": "79175002040", "email": "dev@otus.ru", "gender": 1, "birthday": "01.01.1930", "last_name": "a"},
        {"phone": "79175002040", "email": "dev@otus.ru", "gender": 1, "birthday": "05.30.2020", "last_name": "a"},
        {"phone": "79175002040", "email": "dev@otus.ru", "gender": 1, "birthday": 30052020, "last_name": "a"}
    ])
    def test_invalid_birthday(self, arguments):
        request_obj = api.OnlineScoreRequest(**arguments)
        with self.assertRaises(api.ValidationError):
            request_obj.validate_all()

    @cases([
        {"phone": "79175002040", "email": "dev@otus.ru", "gender": -1, "birthday": "01.01.2020", "last_name": "a"},
        {"phone": "79175002040", "email": "dev@otus.ru", "gender": "1", "birthday": "01.01.2020", "last_name": "a"},
        {"phone": "79175002040", "email": "dev@otus.ru", "gender": 1.0, "birthday": "01.01.2020", "last_name": "a"}
    ])
    def test_invalid_gender(self, arguments):
        request_obj = api.OnlineScoreRequest(**arguments)
        with self.assertRaises(api.ValidationError):
            request_obj.validate_all()


class TestClientsInterestsSuite(unittest.TestCase):

    @cases([
        {"date": "01-01-2020", "client_ids": [1, 2]},
        {"date": "01/01/2020", "client_ids": [1, 2]},
        {"date": "01.01.20", "client_ids": [1, 2]},
        {"date": "05.30.2020", "client_ids": [1, 2]},
        {"date": 30052020, "client_ids": [1, 2]}
    ])
    def test_invalid_date(self, arguments):
        request_obj = api.ClientsInterestsRequest(**arguments)
        with self.assertRaises(api.ValidationError):
            request_obj.validate_all()

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
        request_obj = api.ClientsInterestsRequest(**arguments)
        with self.assertRaises(api.ValidationError):
            request_obj.validate_all()

    @cases([
        {},
        {"phone": "79175002040"},
        {"phone": "79175002040", "gender": 1},
        {"phone": "79175002040", "gender": 1, "first_name": "s"},
        {"email": "dev@otus.ru", "birthday": "01.01.2000", "first_name": "s"},
    ])
    def test_invalid_score_request(self, arguments):
        request_obj = api.ClientsInterestsRequest(**arguments)
        with self.assertRaises(api.ValidationError):
            request_obj.validate_all()


if __name__ == "__main__":
    unittest.main()
