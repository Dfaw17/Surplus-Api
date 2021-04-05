import requests
from env import stagging
from pprint import pprint
from assertpy import assert_that

class TestCustomerUpdatePrivateData:

    global setting_env,url_login,url_update_private_data,email,kata_sandi,wrong_token

    setting_env = stagging
    url_login = f"{setting_env}/api/v2/customer/auth/login/email"
    url_update_private_data = f"{setting_env}/api/v2/customer/profiles/private-data"
    email = "kopiruangvirtual@gmail.com"
    kata_sandi = '12345678'
    wrong_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvc3RhZ2luZy5hZG1pbnN1cnBsdXMubmV0XC9hcGlcL3YyXC9jdXN0b21lclwvYXV0aFwvbG9naW5cL2VtYWlsIiwiaWF0IjoxNjE2ODA1NzI2LCJleHAiOjE2MTkzOTc3MjYsIm5iZiI6MTYxNjgwNTcyNiwianRpIjoib05ESmxFRE5hSzNrN2RtVyIsInN1YiI6NDEyNiwicHJ2IjoiMjc0MTA1ZGE2ZTk1YmVmMjgwNzc4NmRkODczODg2N2NmOWMwMmFhYiJ9.fj51xIfQrqleRvdSJUbWcdrvsxQPUn8HpccnOmTgPDI'

    def test_update_private_data_normal(self):
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
            'name': 'maulana',
            'phone_number': '085710819443'
        }
        show_update_private_data = requests.patch(url_update_private_data, params=param2, headers=headers2)

        validate_status = show_update_private_data.json().get('success')
        validate_message = show_update_private_data.json().get('message')
        validate_data = show_update_private_data.json().get('data')
        validate_data_name = show_update_private_data.json().get('data')['name']
        validate_data_no_ponsel = show_update_private_data.json().get('data')['no_ponsel']

        assert show_update_private_data.status_code == 200
        assert validate_status == bool(True)
        assert 'Data customer berhasil diperbarui.' in validate_message
        assert_that(validate_data).contains_only('id', 'name', 'email', 'no_ponsel', 'alamat', 'auth_origin',
                                                 'referal_code',
                                                 'onesignal_loc', 'latitude', 'longitude')
        assert validate_data_name == 'maulana'
        assert validate_data_no_ponsel == '085710819443'

    def test_update_private_data_wrong_token(self):
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
            'name': 'maulana',
            'phone_number': '085710819443'
        }
        show_update_private_data = requests.patch(url_update_private_data, params=param2, headers=headers2)

        validate_status = show_update_private_data.json().get('success')
        validate_message = show_update_private_data.json().get('message')

        assert show_update_private_data.status_code == 401
        assert validate_status == bool(False)
        assert 'Unauthorized' in validate_message

    def test_update_private_data_empty_token(self):
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
            'name': 'maulana',
            'phone_number': '085710819443'
        }
        show_update_private_data = requests.patch(url_update_private_data, params=param2, headers=headers2)

        validate_status = show_update_private_data.json().get('success')
        validate_message = show_update_private_data.json().get('message')

        assert show_update_private_data.status_code == 401
        assert validate_status == bool(False)
        assert 'Unauthorized' in validate_message

    def test_update_private_data_without_param_nama(self):
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
            # 'name': 'maulana',
            'phone_number': '085710819443'
        }
        show_update_private_data = requests.patch(url_update_private_data, params=param2, headers=headers2)

        validate_status = show_update_private_data.json().get('success')
        validate_message = show_update_private_data.json().get('message')['name']

        assert show_update_private_data.status_code == 422
        assert validate_status == bool(False)
        assert 'Nama tidak boleh kosong.' in validate_message

    def test_update_private_data_nama_empty_value(self):
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
            'name': '',
            'phone_number': '085710819443'
        }
        show_update_private_data = requests.patch(url_update_private_data, params=param2, headers=headers2)

        validate_status = show_update_private_data.json().get('success')
        validate_message = show_update_private_data.json().get('message')['name']

        assert show_update_private_data.status_code == 422
        assert validate_status == bool(False)
        assert 'Nama tidak boleh kosong.' in validate_message

    def test_update_private_data_nama_value_kurang6(self):
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
            'name': 'a',
            'phone_number': '085710819443'
        }
        show_update_private_data = requests.patch(url_update_private_data, params=param2, headers=headers2)

        validate_status = show_update_private_data.json().get('success')
        validate_message = show_update_private_data.json().get('message')['name']

        assert show_update_private_data.status_code == 422
        assert validate_status == bool(False)
        assert 'Nama setidaknya harus 6 karakter.' in validate_message

    def test_update_private_data_without_param_phone(self):
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
            'name': 'maulana'
            # 'phone_number': '085710819443'
        }
        show_update_private_data = requests.patch(url_update_private_data, params=param2, headers=headers2)

        validate_status = show_update_private_data.json().get('success')
        validate_message = show_update_private_data.json().get('message')['phone_number']

        assert show_update_private_data.status_code == 422
        assert validate_status == bool(False)
        assert 'No. HP tidak boleh kosong.' in validate_message

    def test_update_private_data_phone_empty_value(self):
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
            'name': 'maulana',
            'phone_number': ''
        }
        show_update_private_data = requests.patch(url_update_private_data, params=param2, headers=headers2)

        validate_status = show_update_private_data.json().get('success')
        validate_message = show_update_private_data.json().get('message')['phone_number']

        assert show_update_private_data.status_code == 422
        assert validate_status == bool(False)
        assert 'No. HP tidak boleh kosong.' in validate_message

    def test_update_private_data_phone_text_value(self):
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
            'name': 'maulana',
            'phone_number': 'aaa'
        }
        show_update_private_data = requests.patch(url_update_private_data, params=param2, headers=headers2)

        validate_status = show_update_private_data.json().get('success')
        validate_message = show_update_private_data.json().get('message')

        assert show_update_private_data.status_code == 200
        assert validate_status == bool(True)
        assert 'Data customer berhasil diperbarui.' in validate_message

