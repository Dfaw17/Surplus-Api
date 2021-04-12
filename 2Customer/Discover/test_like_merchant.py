import requests
from env import stagging
from pprint import pprint
from assertpy import assert_that

class TestCustomerLikeMerchant:

    global setting_env,url_login,url_discover,url_like_merchant,email,kata_sandi,wrong_token

    setting_env = stagging
    url_login = f"{setting_env}/api/v2/customer/auth/login/email"
    url_discover = f"{setting_env}/api/v2/customer/discover"
    url_like_merchant = f"{setting_env}/api/v2/customer/merchants/"
    email = "kopiruangvirtual@gmail.com"
    kata_sandi = '12345678'
    wrong_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvc3RhZ2luZy5hZG1pbnN1cnBsdXMubmV0XC9hcGlcL3YyXC9jdXN0b21lclwvYXV0aFwvbG9naW5cL2VtYWlsIiwiaWF0IjoxNjE2ODA1NzI2LCJleHAiOjE2MTkzOTc3MjYsIm5iZiI6MTYxNjgwNTcyNiwianRpIjoib05ESmxFRE5hSzNrN2RtVyIsInN1YiI6NDEyNiwicHJ2IjoiMjc0MTA1ZGE2ZTk1YmVmMjgwNzc4NmRkODczODg2N2NmOWMwMmFhYiJ9.fj51xIfQrqleRvdSJUbWcdrvsxQPUn8HpccnOmTgPDI'

    def test_like_merchant_normal(self):
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
        discover = requests.get(url_discover, params=param2, headers=headers2)
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        like_merchants = requests.patch(
            url_like_merchant + str(discover.json()['data']['nearby_merchant'][0]['merchant_id']) + '/like',
            headers=headers3)

        validate_status = like_merchants.json().get('success')
        validate_message = like_merchants.json().get('message')
        # #
        assert like_merchants.status_code == 200
        assert validate_status == bool(True)
        assert 'disukai' in validate_message

    def test_unlike_merchant_normal(self):
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
        discover = requests.get(url_discover, params=param2, headers=headers2)
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        like_merchants = requests.patch(
            url_like_merchant + str(discover.json()['data']['nearby_merchant'][0]['merchant_id']) + '/like',
            headers=headers3)

        validate_status = like_merchants.json().get('success')
        validate_message = like_merchants.json().get('message')
        # #
        assert like_merchants.status_code == 200
        assert validate_status == bool(True)
        assert 'disukai' in validate_message

    def test_like_merchant_without_token(self):
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
        discover = requests.get(url_discover, params=param2, headers=headers2)
        headers3 = {
            "Accept": "application/json",
            "Authorization": ""
        }
        like_merchants = requests.patch(
            url_like_merchant + str(discover.json()['data']['nearby_merchant'][0]['merchant_id']) + '/like',
            headers=headers3)

        validate_status = like_merchants.json().get('success')
        validate_message = like_merchants.json().get('message')
        # #
        assert like_merchants.status_code == 401
        assert validate_status == bool(False)
        assert 'Unauthorized' in validate_message

    def test_like_merchant_wrong_token(self):
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
        discover = requests.get(url_discover, params=param2, headers=headers2)
        headers3 = {
            "Accept": "application/json",
            "Authorization": wrong_token
        }
        like_merchants = requests.patch(
            url_like_merchant + str(discover.json()['data']['nearby_merchant'][0]['merchant_id']) + '/like',
            headers=headers3)

        validate_status = like_merchants.json().get('success')
        validate_message = like_merchants.json().get('message')
        # #
        assert like_merchants.status_code == 401
        assert validate_status == bool(False)
        assert 'Unauthorized' in validate_message

    def test_like_merchant_id_not_found(self):
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
        discover = requests.get(url_discover, params=param2, headers=headers2)
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        like_merchants = requests.patch(url_like_merchant + '666666/like', headers=headers3)

        validate_status = like_merchants.json().get('success')
        validate_message = like_merchants.json().get('message')
        # #
        assert like_merchants.status_code == 200
        assert validate_status == bool(True)
        assert 'disukai' in validate_message

    def test_like_merchant_id_empty_value(self):
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
        discover = requests.get(url_discover, params=param2, headers=headers2)
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        like_merchants = requests.patch(url_like_merchant + '/like', headers=headers3)

        validate_status = like_merchants.json().get('success')
        validate_message = like_merchants.json().get('message')
        # #
        assert like_merchants.status_code == 404
        assert validate_status == bool(False)
        assert '' in validate_message

    def test_like_merchant_id_minus_value(self):
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
        discover = requests.get(url_discover, params=param2, headers=headers2)
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        like_merchants = requests.patch(url_like_merchant + '-666666/like', headers=headers3)

        validate_status = like_merchants.json().get('success')
        validate_message = like_merchants.json().get('message')
        # #
        assert like_merchants.status_code == 500
        assert validate_status == bool(False)
        assert 'Aduh!' in validate_message

    def test_like_merchant_id_text_value(self):
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
        discover = requests.get(url_discover, params=param2, headers=headers2)
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        like_merchants = requests.patch(url_like_merchant + 'aaa/like', headers=headers3)

        validate_status = like_merchants.json().get('success')
        validate_message = like_merchants.json().get('message')
        # #
        assert like_merchants.status_code == 500
        assert validate_status == bool(False)
        assert 'Aduh!' in validate_message

