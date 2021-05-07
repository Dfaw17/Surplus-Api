import requests
from env import stagging
from pprint import pprint
from assertpy import assert_that


class TestCustomerListMerchant:
    global setting_env, url_login, url_list_merchant, email, kata_sandi, wrong_token

    setting_env = stagging
    url_login = f"{setting_env}/api/v2/customer/auth/login/email"
    url_list_merchant = f"{setting_env}/api/v2/customer/merchants"
    email = "kopiruangvirtual@gmail.com"
    kata_sandi = '12345678'
    wrong_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvc3RhZ2luZy5hZG1pbnN1cnBsdXMubmV0XC9hcGlcL3YyXC9jdXN0b21lclwvYXV0aFwvbG9naW5cL2VtYWlsIiwiaWF0IjoxNjE2ODA1NzI2LCJleHAiOjE2MTkzOTc3MjYsIm5iZiI6MTYxNjgwNTcyNiwianRpIjoib05ESmxFRE5hSzNrN2RtVyIsInN1YiI6NDEyNiwicHJ2IjoiMjc0MTA1ZGE2ZTk1YmVmMjgwNzc4NmRkODczODg2N2NmOWMwMmFhYiJ9.fj51xIfQrqleRvdSJUbWcdrvsxQPUn8HpccnOmTgPDI'

    def test_list_merchant_normal(self):
        param = {
            'email': email,
            'password': kata_sandi
        }
        headers = {
            "Accept": "application/json"
        }
        login = requests.post(url_login, params=param, headers=headers)
        param2 = {
            'latitude': '-6.3823317',
            'longitude': '107.1162607'
        }
        headers2 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        list_merchant = requests.get(url_list_merchant, params=param2, headers=headers2)

        validate_status = list_merchant.json().get('success')
        validate_message = list_merchant.json().get('message')
        validate_data = list_merchant.json().get('data')[0]
        validate_merchant_id = list_merchant.json().get('data')[0]['merchant_id']
        validate_nama_merchant = list_merchant.json().get('data')[0]['nama_merchant']
        # #
        assert list_merchant.status_code == 200
        assert validate_status == bool(True)
        assert 'Data merchant berhasil ditemukan.' in validate_message
        assert_that(validate_data).contains_only('merchant_id', 'nama_merchant', 'merchant_logo',
                                                 'merchant_branch_status', 'merchant_central_id', 'distance','merchant_verified')
        assert_that(validate_merchant_id).is_not_none()
        assert_that(validate_nama_merchant).is_not_none()

    def test_list_merchant_wrong_token(self):
        param = {
            'email': email,
            'password': kata_sandi
        }
        headers = {
            "Accept": "application/json"
        }
        login = requests.post(url_login, params=param, headers=headers)
        param2 = {
            'latitude': '-6.3823317',
            'longitude': '107.1162607'
        }
        headers2 = {
            "Accept": "application/json",
            "Authorization": wrong_token
        }
        list_merchant = requests.get(url_list_merchant, params=param2, headers=headers2)

        validate_status = list_merchant.json().get('success')
        validate_message = list_merchant.json().get('message')

        assert list_merchant.status_code == 401
        assert validate_status == bool(False)
        assert 'Unauthorized' in validate_message

    def test_list_merchant_token_empty_value(self):
        param = {
            'email': email,
            'password': kata_sandi
        }
        headers = {
            "Accept": "application/json"
        }
        login = requests.post(url_login, params=param, headers=headers)
        param2 = {
            'latitude': '-6.3823317',
            'longitude': '107.1162607'
        }
        headers2 = {
            "Accept": "application/json",
            "Authorization": ''
        }
        list_merchant = requests.get(url_list_merchant, params=param2, headers=headers2)

        validate_status = list_merchant.json().get('success')
        validate_message = list_merchant.json().get('message')

        assert list_merchant.status_code == 401
        assert validate_status == bool(False)
        assert 'Unauthorized' in validate_message

    def test_list_merchant_latitude_empty_value(self):
        param = {
            'email': email,
            'password': kata_sandi
        }
        headers = {
            "Accept": "application/json"
        }
        login = requests.post(url_login, params=param, headers=headers)
        param2 = {
            'latitude': '',
            'longitude': '107.1162607'
        }
        headers2 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        list_merchant = requests.get(url_list_merchant, params=param2, headers=headers2)

        validate_status = list_merchant.json().get('success')
        validate_message = list_merchant.json().get('message')['latitude']

        assert list_merchant.status_code == 422
        assert validate_status == bool(False)
        assert 'latitude tidak boleh kosong.' in validate_message

    def test_list_merchant_without_param_latitude(self):
        param = {
            'email': email,
            'password': kata_sandi
        }
        headers = {
            "Accept": "application/json"
        }
        login = requests.post(url_login, params=param, headers=headers)
        param2 = {
            'longitude': '107.1162607'
        }
        headers2 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        list_merchant = requests.get(url_list_merchant, params=param2, headers=headers2)

        validate_status = list_merchant.json().get('success')
        validate_message = list_merchant.json().get('message')['latitude']

        assert list_merchant.status_code == 422
        assert validate_status == bool(False)
        assert 'latitude tidak boleh kosong.' in validate_message

    def test_list_merchant_latitude_text_value(self):
        param = {
            'email': email,
            'password': kata_sandi
        }
        headers = {
            "Accept": "application/json"
        }
        login = requests.post(url_login, params=param, headers=headers)
        param2 = {
            'latitude': 'aaa',
            'longitude': '107.1162607'
        }
        headers2 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        list_merchant = requests.get(url_list_merchant, params=param2, headers=headers2)

        validate_status = list_merchant.json().get('success')
        validate_message = list_merchant.json().get('message')

        assert list_merchant.status_code == 500
        assert validate_status == bool(False)
        assert 'Aduh!' in validate_message

    def test_list_merchant_Longitude_empty_value(self):
        param = {
            'email': email,
            'password': kata_sandi
        }
        headers = {
            "Accept": "application/json"
        }
        login = requests.post(url_login, params=param, headers=headers)
        param2 = {
            'latitude': '-6.3823317',
            'longitude': ''
        }
        headers2 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        list_merchant = requests.get(url_list_merchant, params=param2, headers=headers2)

        validate_status = list_merchant.json().get('success')
        validate_message = list_merchant.json().get('message')['longitude']

        assert list_merchant.status_code == 422
        assert validate_status == bool(False)
        assert 'longitude tidak boleh kosong.' in validate_message

    def test_list_merchant_without_param_longitude(self):
        param = {
            'email': email,
            'password': kata_sandi
        }
        headers = {
            "Accept": "application/json"
        }
        login = requests.post(url_login, params=param, headers=headers)
        param2 = {
            'latitude': '-6.3823317'
        }
        headers2 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        list_merchant = requests.get(url_list_merchant, params=param2, headers=headers2)

        validate_status = list_merchant.json().get('success')
        validate_message = list_merchant.json().get('message')['longitude']

        assert list_merchant.status_code == 422
        assert validate_status == bool(False)
        assert 'longitude tidak boleh kosong.' in validate_message

    def test_list_merchant_longitude_text_value(self):
        param = {
            'email': email,
            'password': kata_sandi
        }
        headers = {
            "Accept": "application/json"
        }
        login = requests.post(url_login, params=param, headers=headers)
        param2 = {
            'latitude': '-6.3823317',
            'longitude': 'aaa'
        }
        headers2 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        list_merchant = requests.get(url_list_merchant, params=param2, headers=headers2)

        validate_status = list_merchant.json().get('success')
        validate_message = list_merchant.json().get('message')

        assert list_merchant.status_code == 500
        assert validate_status == bool(False)
        assert 'Aduh!' in validate_message
