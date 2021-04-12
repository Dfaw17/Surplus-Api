import requests
from env import stagging
from pprint import pprint
from assertpy import assert_that

class TestCustomerUpdatePassword:

    global setting_env,url_login,url_update_password,email,kata_sandi,wrong_token

    setting_env = stagging
    url_login = f"{setting_env}/api/v2/customer/auth/login/email"
    url_update_password = f"{setting_env}/api/v2/customer/profiles/password"
    email = "kopiruangvirtual@gmail.com"
    kata_sandi = '12345678'
    wrong_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvc3RhZ2luZy5hZG1pbnN1cnBsdXMubmV0XC9hcGlcL3YyXC9jdXN0b21lclwvYXV0aFwvbG9naW5cL2VtYWlsIiwiaWF0IjoxNjE2ODA1NzI2LCJleHAiOjE2MTkzOTc3MjYsIm5iZiI6MTYxNjgwNTcyNiwianRpIjoib05ESmxFRE5hSzNrN2RtVyIsInN1YiI6NDEyNiwicHJ2IjoiMjc0MTA1ZGE2ZTk1YmVmMjgwNzc4NmRkODczODg2N2NmOWMwMmFhYiJ9.fj51xIfQrqleRvdSJUbWcdrvsxQPUn8HpccnOmTgPDI'

    def test_update_password_normal(self):
        param = {
            'email': email,
            'password': kata_sandi
        }
        headers = {
            "Accept": "application/json"
        }
        login = requests.post(url_login, params=param, headers=headers)
        headers2 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        param2 = {
            'old_password': '12345678',
            'new_password': '12345678',
            're_new_password': '12345678'
        }
        update_passwrod = requests.patch(url_update_password, params=param2, headers=headers2)

        validate_status = update_passwrod.json().get('success')
        validate_message = update_passwrod.json().get('message')

        assert update_passwrod.status_code == 200
        assert validate_status == bool(True)
        assert 'Password berhasil diperbaharui' in validate_message

    def test_update_password_wrong_token(self):
        param = {
            'email': email,
            'password': kata_sandi
        }
        headers = {
            "Accept": "application/json"
        }
        login = requests.post(url_login, params=param, headers=headers)
        headers2 = {
            "Accept": "application/json",
            "Authorization": wrong_token
        }
        param2 = {
            'old_password': '12345678',
            'new_password': '12345678',
            're_new_password': '12345678'
        }
        update_passwrod = requests.patch(url_update_password, params=param2, headers=headers2)

        validate_status = update_passwrod.json().get('success')
        validate_message = update_passwrod.json().get('message')

        assert update_passwrod.status_code == 401
        assert validate_status == bool(False)
        assert 'Unauthorized' in validate_message

    def test_update_password_token_empty_value(self):
        param = {
            'email': email,
            'password': kata_sandi
        }
        headers = {
            "Accept": "application/json"
        }
        login = requests.post(url_login, params=param, headers=headers)
        headers2 = {
            "Accept": "application/json",
            "Authorization": ''
        }
        param2 = {
            'old_password': '12345678',
            'new_password': '12345678',
            're_new_password': '12345678'
        }
        update_passwrod = requests.patch(url_update_password, params=param2, headers=headers2)

        validate_status = update_passwrod.json().get('success')
        validate_message = update_passwrod.json().get('message')

        assert update_passwrod.status_code == 401
        assert validate_status == bool(False)
        assert 'Unauthorized' in validate_message

    def test_update_password_old_empty_value(self):
        param = {
            'email': email,
            'password': kata_sandi
        }
        headers = {
            "Accept": "application/json"
        }
        login = requests.post(url_login, params=param, headers=headers)
        headers2 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        param2 = {
            'old_password': '',
            'new_password': '12345678',
            're_new_password': '12345678'
        }
        update_passwrod = requests.patch(url_update_password, params=param2, headers=headers2)

        validate_status = update_passwrod.json().get('success')
        validate_message = update_passwrod.json().get('message')['old_password']

        assert update_passwrod.status_code == 422
        assert validate_status == bool(False)
        assert 'Kata sandi lama tidak boleh kosong.' in validate_message

    def test_update_password_without_param_old(self):
        param = {
            'email': email,
            'password': kata_sandi
        }
        headers = {
            "Accept": "application/json"
        }
        login = requests.post(url_login, params=param, headers=headers)
        headers2 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        param2 = {
            # 'old_password': '',
            'new_password': '12345678',
            're_new_password': '12345678'
        }
        update_passwrod = requests.patch(url_update_password, params=param2, headers=headers2)

        validate_status = update_passwrod.json().get('success')
        validate_message = update_passwrod.json().get('message')['old_password']

        assert update_passwrod.status_code == 422
        assert validate_status == bool(False)
        assert 'Kata sandi lama tidak boleh kosong.' in validate_message

    def test_update_password_old_wrong(self):
        param = {
            'email': email,
            'password': kata_sandi
        }
        headers = {
            "Accept": "application/json"
        }
        login = requests.post(url_login, params=param, headers=headers)
        headers2 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        param2 = {
            'old_password': 'aaaaaaaaa',
            'new_password': '12345678',
            're_new_password': '12345678'
        }
        update_passwrod = requests.patch(url_update_password, params=param2, headers=headers2)

        validate_status = update_passwrod.json().get('success')
        validate_message = update_passwrod.json().get('message')['old_password']

        assert update_passwrod.status_code == 422
        assert validate_status == bool(False)
        assert 'Kata sandi lama tidak sesuai atau salah' in validate_message

    def test_update_password_new_empty_value(self):
        param = {
            'email': email,
            'password': kata_sandi
        }
        headers = {
            "Accept": "application/json"
        }
        login = requests.post(url_login, params=param, headers=headers)
        headers2 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        param2 = {
            'old_password': '12345678',
            'new_password': '',
            're_new_password': '12345678'
        }
        update_passwrod = requests.patch(url_update_password, params=param2, headers=headers2)

        validate_status = update_passwrod.json().get('success')
        validate_message = update_passwrod.json().get('message')['new_password']

        assert update_passwrod.status_code == 422
        assert validate_status == bool(False)
        assert 'Kata sandi baru tidak boleh kosong.' in validate_message

    def test_update_password_without_param_new(self):
        param = {
            'email': email,
            'password': kata_sandi
        }
        headers = {
            "Accept": "application/json"
        }
        login = requests.post(url_login, params=param, headers=headers)
        headers2 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        param2 = {
            'old_password': '12345678',
            # 'new_password': '',
            're_new_password': '12345678'
        }
        update_passwrod = requests.patch(url_update_password, params=param2, headers=headers2)

        validate_status = update_passwrod.json().get('success')
        validate_message = update_passwrod.json().get('message')['new_password']

        assert update_passwrod.status_code == 422
        assert validate_status == bool(False)
        assert 'Kata sandi baru tidak boleh kosong.' in validate_message

    def test_update_password_new_value_kurang6(self):
        param = {
            'email': email,
            'password': kata_sandi
        }
        headers = {
            "Accept": "application/json"
        }
        login = requests.post(url_login, params=param, headers=headers)
        headers2 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        param2 = {
            'old_password': '12345678',
            'new_password': '123',
            're_new_password': '12345678'
        }
        update_passwrod = requests.patch(url_update_password, params=param2, headers=headers2)

        validate_status = update_passwrod.json().get('success')
        validate_message = update_passwrod.json().get('message')['new_password']

        assert update_passwrod.status_code == 422
        assert validate_status == bool(False)
        assert 'Kata sandi baru harus diantara 6 dan 20 karakter.' in validate_message

    def test_update_password_new_doesnt_match(self):
        param = {
            'email': email,
            'password': kata_sandi
        }
        headers = {
            "Accept": "application/json"
        }
        login = requests.post(url_login, params=param, headers=headers)
        headers2 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        param2 = {
            'old_password': '12345678',
            'new_password': '12345678',
            're_new_password': '12345679'
        }
        update_passwrod = requests.patch(url_update_password, params=param2, headers=headers2)

        validate_status = update_passwrod.json().get('success')
        validate_message = update_passwrod.json().get('message')['re_new_password']

        assert update_passwrod.status_code == 422
        assert validate_status == bool(False)
        assert 'Ulang kata sandi baru dan Kata sandi baru harus sama.' in validate_message

    def test_update_password_re_new_empty_value(self):
        param = {
            'email': email,
            'password': kata_sandi
        }
        headers = {
            "Accept": "application/json"
        }
        login = requests.post(url_login, params=param, headers=headers)
        headers2 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        param2 = {
            'old_password': '12345678',
            'new_password': '12345678',
            're_new_password': ''
        }
        update_passwrod = requests.patch(url_update_password, params=param2, headers=headers2)

        validate_status = update_passwrod.json().get('success')
        validate_message = update_passwrod.json().get('message')['re_new_password']

        assert update_passwrod.status_code == 422
        assert validate_status == bool(False)
        assert 'Ulang kata sandi baru tidak boleh kosong.' in validate_message

    def test_update_password_without_param_re_new(self):
        param = {
            'email': email,
            'password': kata_sandi
        }
        headers = {
            "Accept": "application/json"
        }
        login = requests.post(url_login, params=param, headers=headers)
        headers2 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        param2 = {
            'old_password': '12345678',
            'new_password': '12345678'
            # 're_new_password': ''
        }
        update_passwrod = requests.patch(url_update_password, params=param2, headers=headers2)

        validate_status = update_passwrod.json().get('success')
        validate_message = update_passwrod.json().get('message')['re_new_password']

        assert update_passwrod.status_code == 422
        assert validate_status == bool(False)
        assert 'Ulang kata sandi baru tidak boleh kosong.' in validate_message




