import requests
from env import stagging
from pprint import pprint
from assertpy import assert_that
import time

class TestCustomerLogout:

    global setting_env,url_login,url_logout,email,kata_sandi,wrong_token

    setting_env = stagging
    url_login = f"{setting_env}/api/v2/customer/auth/login/email"
    url_logout = f"{setting_env}/api/v2/customer/auth/logout"
    email = "kopiruangvirtual@gmail.com"
    kata_sandi = '12345678'
    wrong_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvc3RhZ2luZy5hZG1pbnN1cnBsdXMubmV0XC9hcGlcL3YyXC9jdXN0b21lclwvYXV0aFwvbG9naW5cL2VtYWlsIiwiaWF0IjoxNjE2ODA1NzI2LCJleHAiOjE2MTkzOTc3MjYsIm5iZiI6MTYxNjgwNTcyNiwianRpIjoib05ESmxFRE5hSzNrN2RtVyIsInN1YiI6NDEyNiwicHJ2IjoiMjc0MTA1ZGE2ZTk1YmVmMjgwNzc4NmRkODczODg2N2NmOWMwMmFhYiJ9.fj51xIfQrqleRvdSJUbWcdrvsxQPUn8HpccnOmTgPDI'

    def test_logout_normal(self):
        param = {
            'email': email,
            'password': kata_sandi
        }
        headers = {
            "Accept": "application/json"
        }
        login = requests.post(url_login, params=param, headers=headers)
        time.sleep(1)
        param2 = {
            'token': login.json().get('token')
        }
        logout = requests.post(url_logout, params=param2, headers=headers)

        validate_status = logout.json().get('success')
        validate_message = logout.json().get('message')

        assert logout.status_code == 200
        assert validate_status == bool(True)
        assert 'User logged out successfully' in validate_message

    def test_logout_wrong_token(self):
        param = {
            'email': email,
            'password': kata_sandi
        }
        headers = {
            "Accept": "application/json"
        }
        login = requests.post(url_login, params=param, headers=headers)
        param2 = {
            'token': wrong_token
        }
        logout = requests.post(url_logout, params=param2, headers=headers)

        validate_status = logout.json().get('success')
        validate_message = logout.json().get('message')

        assert logout.status_code == 401
        assert validate_status == bool(False)
        assert 'Unauthorized' in validate_message

    def test_logout_token_empty_value(self):
        param = {
            'email': email,
            'password': kata_sandi
        }
        headers = {
            "Accept": "application/json"
        }
        login = requests.post(url_login, params=param, headers=headers)
        param2 = {
            'token': ''
        }
        logout = requests.post(url_logout, params=param2, headers=headers)

        validate_status = logout.json().get('success')
        validate_message = logout.json().get('message')

        assert logout.status_code == 401
        assert validate_status == bool(False)
        assert 'Unauthorized' in validate_message

    def test_logout_without_param_token(self):
        param = {
            'email': email,
            'password': kata_sandi
        }
        headers = {
            "Accept": "application/json"
        }
        login = requests.post(url_login, params=param, headers=headers)
        param2 = {

        }
        logout = requests.post(url_logout, params=param2, headers=headers)

        validate_status = logout.json().get('success')
        validate_message = logout.json().get('message')

        assert logout.status_code == 401
        assert validate_status == bool(False)
        assert 'Unauthorized' in validate_message