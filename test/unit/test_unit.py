import unittest

import api
from test.help_testing import cases, set_valid_auth


class TestMethodRequestFields(unittest.TestCase):

    @cases([222, 222., [2], (2,), None])
    def test_char_field_invalid(self, value):
        class A:
            pass
        char_field = api.CharField(required=True)
        char_field.__set_name__(None, 'char_field')
        with self.assertRaises(api.ValidationError):
            char_field.__set__(A, value)

    @cases(['lol', ''])
    def test_char_field_valid(self, value):
        class A:
            pass
        char_field = api.CharField(required=True)
        char_field.__set_name__(None, 'char_field')
        char_field.__set__(A, value)
        self.assertEquals(A._char_field, value)

    @cases([None])
    def test_char_field_nonrequired(self, value):
        class A:
            pass

        char_field = api.CharField(required=False)
        char_field.__set_name__(None, 'char_field')
        char_field.__set__(A, value)
        self.assertEquals(A._char_field, value)

    @cases(['3', [3], (3,), 3., 3, None])
    def test_arg_field_invalid(self, value):
        class A:
            pass
        arg_field = api.ArgumentsField(required=True)
        arg_field.__set_name__(None, 'arg_field')
        with self.assertRaises(api.ValidationError):
            arg_field.__set__(A, value)

    @cases([{}, {'a': 1}])
    def test_arg_field_valid(self, value):
        class A:
            pass

        arg_field = api.ArgumentsField(required=True)
        arg_field.__set_name__(None, 'arg_field')
        arg_field.__set__(A, value)
        self.assertEquals(A._arg_field, value)


class TestOnlineScoreFields(unittest.TestCase):

    @cases(["devotus.ru", 43, 532.564, "dev@otusru", "dev@otus.ru333"])
    def test_email_field_invalid(self, value):
        class A:
            pass

        email_field = api.EmailField(required=True)
        email_field.__set_name__(None, 'email_field')
        with self.assertRaises(api.ValidationError):
            email_field.__set__(A, value)

    @cases([56, 79175002040.0, "a", "7917500d040", "791750020400", "+79175002040"])
    def test_phone_field_invalid(self, value):
        class A:
            pass

        phone_field = api.PhoneField(required=True)
        phone_field.__set_name__(None, 'phone_field')
        with self.assertRaises(api.ValidationError):
            phone_field.__set__(A, value)

    @cases([79175002040, '79175002040'])
    def test_phone_field_valid(self, value):
        class A:
            pass

        phone_field = api.PhoneField(required=True)
        phone_field.__set_name__(None, 'phone_field')
        phone_field.__set__(A, value)
        self.assertEquals(A._phone_field, value)

    @cases(["01.01.20", "01/01/2000", "01-01-2000", "01.01.1930", "05.30.2020", 30052020, 15.07])
    def test_birthday_field_invalid(self, value):
        class A:
            pass

        birth_field = api.BirthDayField(required=True)
        birth_field.__set_name__(None, 'birth_field')
        with self.assertRaises(api.ValidationError):
            birth_field.__set__(A, value)

    @cases([-1, "1", 1.0, 5])
    def test_gender_field_invalid(self, value):
        class A:
            pass

        gender_field = api.GenderField(required=True)
        gender_field.__set_name__(None, 'gender_field')
        with self.assertRaises(api.ValidationError):
            gender_field.__set__(A, value)


class TestClientsInterestsFields(unittest.TestCase):

    @cases(["01-01-2020", "01/01/2020", "01.01.20", "05.30.2020", 30052020, '2020-12-10'])
    def test_date_field_invalid(self, value):
        class A:
            pass

        date_field = api.DateField(required=True)
        date_field.__set_name__(None, 'date_field')
        with self.assertRaises(api.ValidationError):
            date_field.__set__(A, value)

    @cases([[], (1, ), 1, 1.4, ["a"], ["1"]])
    def test_client_field_invalid(self, value):
        class A:
            pass

        client_field = api.ClientIDsField(required=True)
        client_field.__set_name__(None, 'client_field')
        with self.assertRaises(api.ValidationError):
            client_field.__set__(A, value)


if __name__ == "__main__":
    unittest.main()
