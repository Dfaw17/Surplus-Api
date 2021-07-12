import requests
from env import *


class TestLogout:
    global url_login, url_logut, email, kata_sandi, token, setting_env

    setting_env = testing
    url_login = f"{setting_env}/api/v2/merchant/auth/login"
    url_logut = f"{setting_env}/api/v2/merchant/auth/logout"
    email = "sdet@gmail.com"
    kata_sandi = "12345678"

    def test_logout_normal(self):
        param = {
            "email": email,
            "password": kata_sandi
        }

        login = requests.post(url_login, data=param, headers={'Accept': 'application/json'})
        token = login.json().get("token")
        param2 = {
            "token": token
        }

        response = requests.post(url_logut, data=param2,
                                 headers={'Accept': 'application/json'})

        data = response.json()
        validate_status = data.get('success')
        validate_message = data.get('message')

        assert validate_status == bool(True)
        assert response.status_code == 200
        assert validate_message == "User logged out successfully"

    def test_logout_wrong_token(self):
        param2 = {
            "token": "WRONG TOKEN !!!"
        }

        response = requests.post(url_logut, data=param2,
                                 headers={'Accept': 'application/json'})

        data = response.json()
        validate_status = data.get('success')
        validate_message = data.get('message')

        assert validate_status == bool(False)
        assert response.status_code == 401
        assert validate_message == "Unauthorized"

    def test_logout_empty_token(self):
        param2 = {
            "token": "WRONG TOKEN !!!"
        }

        response = requests.post(url_logut, headers={'Accept': 'application/json'})

        data = response.json()
        validate_status = data.get('success')
        validate_message = data.get('message')

        assert validate_status == bool(False)
        assert response.status_code == 401
        assert validate_message == "Unauthorized"
