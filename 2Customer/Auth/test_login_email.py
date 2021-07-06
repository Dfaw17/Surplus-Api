import requests
from env import stagging
from pprint import pprint
from assertpy import assert_that


class TestCustomerLoginEmail:
    global setting_env, login_email, email, kata_sandi

    setting_env = stagging
    login_email = f"{setting_env}/api/v2/customer/auth/login/email"
    email = "kopiruangvirtual@gmail.com"
    kata_sandi = "12345678"

    def test_login_normal(self):
        param = {
            'email': email,
            'password': kata_sandi
        }
        headers = {
            "Accept": "application/json"
        }

        response = requests.post(login_email, data=param, headers=headers)
        data = response.json()
        pprint(data)
        validate_status = data.get('success')
        validate_message = data.get('message')
        validate_token = data.get('token')

        assert response.status_code == 200
        assert validate_status == bool(True)
        assert 'Login customer berhasil.' in validate_message
        assert_that(validate_token).is_not_empty()

    def test_login_hasnt_fulfill_additional_data(self):
        param = {
            'email': email,
            'password': kata_sandi
        }
        headers = {
            "Accept": "application/json"
        }

        response = requests.post(login_email, data=param, headers=headers)
        data = response.json()
        pprint(data)
        validate_status = data.get('success')
        validate_message = data.get('message')
        validate_token = data.get('token')

        assert response.status_code == 200
        assert validate_status == bool(True)
        assert 'Login customer berhasil.' in validate_message
        assert_that(validate_token).is_not_empty()

    def test_login_email_empty_value(self):
        param = {
            'email': "",
            'password': kata_sandi
        }
        headers = {
            "Accept": "application/json"
        }

        response = requests.post(login_email, data=param, headers=headers)
        data = response.json()
        pprint(data)
        validate_status = data.get('success')
        validate_message = data.get('message')['email']
        validate_token = data.get('token')

        assert response.status_code == 422
        assert validate_status == bool(False)
        assert 'email tidak boleh kosong.' in validate_message

    def test_login_without_param_email(self):
        param = {
            'email': "",
            'password': kata_sandi
        }
        headers = {
            "Accept": "application/json"
        }

        response = requests.post(login_email, data=param, headers=headers)
        data = response.json()
        pprint(data)
        validate_status = data.get('success')
        validate_message = data.get('message')['email']
        validate_token = data.get('token')

        assert response.status_code == 422
        assert validate_status == bool(False)
        assert 'email tidak boleh kosong.' in validate_message

    def test_login_password_empty_value(self):
        param = {
            'email': email,
            'password': ""
        }
        headers = {
            "Accept": "application/json"
        }

        response = requests.post(login_email, data=param, headers=headers)
        data = response.json()
        pprint(data)
        validate_status = data.get('success')
        validate_message = data.get('message')['password']

        assert response.status_code == 422
        assert validate_status == bool(False)
        assert 'Kata sandi tidak boleh kosong.' in validate_message

    def test_login_without_param_password(self):
        param = {
            'password': ""
        }
        headers = {
            "Accept": "application/json"
        }

        response = requests.post(login_email, data=param, headers=headers)
        data = response.json()
        pprint(data)
        validate_status = data.get('success')
        validate_message = data.get('message')['password']

        assert response.status_code == 422
        assert validate_status == bool(False)
        assert 'Kata sandi tidak boleh kosong.' in validate_message

    def test_login_wrong_password(self):
        param = {
            'email': email,
            'password': '123456789'
        }
        headers = {
            "Accept": "application/json"
        }

        response = requests.post(login_email, data=param, headers=headers)
        data = response.json()
        pprint(data)
        validate_status = data.get('success')
        validate_message = data.get('message')

        assert response.status_code == 404
        assert validate_status == bool(False)
        assert 'Email atau password salah.' in validate_message

    def test_login_email_with_space(self):
        param = {
            'email': 'kopiruangvirtual @gmail.com',
            'password': kata_sandi
        }
        headers = {
            "Accept": "application/json"
        }

        response = requests.post(login_email, data=param, headers=headers)
        data = response.json()
        pprint(data)
        validate_status = data.get('success')
        validate_message = data.get('message')

        assert response.status_code == 404
        assert validate_status == bool(False)
        assert 'Email atau password salah.' in validate_message

    def test_login_email_without_at(self):
        param = {
            'email': 'kopiruangvirtualgmail.com',
            'password': kata_sandi
        }
        headers = {
            "Accept": "application/json"
        }

        response = requests.post(login_email, data=param, headers=headers)
        data = response.json()
        pprint(data)
        validate_status = data.get('success')
        validate_message = data.get('message')['email']

        assert response.status_code == 422
        assert validate_status == bool(False)
        assert 'email harus merupakan alamat email yang valid.' in validate_message
