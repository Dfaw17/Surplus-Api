import requests
from env import stagging
from pprint import pprint
from assertpy import assert_that

class TestCustomerShowMerchant:

    global setting_env,url_login,url_discover,url_show_merchants,email,kata_sandi,wrong_token

    setting_env = stagging
    url_login = f"{setting_env}/api/v2/customer/auth/login/email"
    url_discover = f"{setting_env}/api/v2/customer/discover"
    url_show_merchants = f"{setting_env}/api/v2/customer/merchants/"
    email = "kopiruangvirtual@gmail.com"
    kata_sandi = '12345678'
    wrong_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvc3RhZ2luZy5hZG1pbnN1cnBsdXMubmV0XC9hcGlcL3YyXC9jdXN0b21lclwvYXV0aFwvbG9naW5cL2VtYWlsIiwiaWF0IjoxNjE2ODA1NzI2LCJleHAiOjE2MTkzOTc3MjYsIm5iZiI6MTYxNjgwNTcyNiwianRpIjoib05ESmxFRE5hSzNrN2RtVyIsInN1YiI6NDEyNiwicHJ2IjoiMjc0MTA1ZGE2ZTk1YmVmMjgwNzc4NmRkODczODg2N2NmOWMwMmFhYiJ9.fj51xIfQrqleRvdSJUbWcdrvsxQPUn8HpccnOmTgPDI'

    def test_show_merchant_normal(self):
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
        param3 = {
            'latitude': '-6.3823317',
            'longitude': '107.1162607'
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        show_merchants = requests.get(
            url_show_merchants + str(discover.json().get('data')['nearby_merchant'][0]['merchant_id']), params=param3,
            headers=headers3)

        validate_status = show_merchants.json().get('success')
        validate_message = show_merchants.json().get('message')
        validate_id_merchant = show_merchants.json().get('data')['merchant']['id']
        validate_data_merchant = show_merchants.json().get('data')['merchant']
        validate_data_menus = show_merchants.json().get('data')['menus']
        validate_data_merchant_name = show_merchants.json().get('data')['merchant']['name']
        validate_data_merchant_email = show_merchants.json().get('data')['merchant']['email']
        validate_data_merchant_phone = show_merchants.json().get('data')['merchant']['no_ponsel']
        validate_data_merchant_alamat = show_merchants.json().get('data')['merchant']['alamat']
        validate_data_merchant_merchant_latitude = show_merchants.json().get('data')['merchant']['merchant_latitude']
        validate_data_merchant_merchant_longitude = show_merchants.json().get('data')['merchant']['merchant_longitude']
        #
        assert show_merchants.status_code == 200
        assert validate_status == bool(True)
        assert 'Data merchant berhasil ditemukan.' in validate_message
        assert validate_id_merchant == discover.json().get('data')['nearby_merchant'][0]['merchant_id']
        assert_that(validate_data_merchant).contains_only('id', 'name', 'email', 'no_ponsel', 'alamat', 'rating',
                                                          'total_like',"total_review",
                                                          'logo_url', 'merchant_latitude', 'merchant_longitude',
                                                          'distance',"merchant_branch_status","merchant_central_id",
                                                          'isLike',"merchant_verified","merchant_category")
        assert_that(validate_data_menus).contains_only('ready_stock', 'preorder')
        assert_that([validate_data_merchant_name, validate_data_merchant_email, validate_data_merchant_phone,
                     validate_data_merchant_alamat, validate_data_merchant_merchant_latitude,
                     validate_data_merchant_merchant_longitude]).is_not_empty()

    def test_show_merchant_token_empty_value(self):
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
        param3 = {
            'latitude': '-6.3823317',
            'longitude': '107.1162607'
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": ""
        }
        show_merchants = requests.get(
            url_show_merchants + str(discover.json().get('data')['nearby_merchant'][0]['merchant_id']), params=param3,
            headers=headers3)

        validate_status = show_merchants.json().get('success')
        validate_message = show_merchants.json().get('message')
        #
        assert show_merchants.status_code == 401
        assert validate_status == bool(False)
        assert 'Unauthorized' in validate_message

    def test_show_merchant_wrong_token(self):
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
        param3 = {
            'latitude': '-6.3823317',
            'longitude': '107.1162607'
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": wrong_token
        }
        show_merchants = requests.get(
            url_show_merchants + str(discover.json().get('data')['nearby_merchant'][0]['merchant_id']), params=param3,
            headers=headers3)

        validate_status = show_merchants.json().get('success')
        validate_message = show_merchants.json().get('message')
        #
        assert show_merchants.status_code == 401
        assert validate_status == bool(False)
        assert 'Unauthorized' in validate_message

    def test_show_merchant_latitude_empty_value(self):
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
        param3 = {
            'latitude': '',
            'longitude': '107.1162607'
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        show_merchants = requests.get(
            url_show_merchants + str(discover.json().get('data')['nearby_merchant'][0]['merchant_id']), params=param3,
            headers=headers3)

        validate_status = show_merchants.json().get('success')
        validate_message = show_merchants.json().get('message')['latitude']
        #
        assert show_merchants.status_code == 422
        assert validate_status == bool(False)
        assert 'latitude tidak boleh kosong.' in validate_message

    def test_show_merchant_without_param_latitude(self):
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
        param3 = {
            'longitude': '107.1162607'
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        show_merchants = requests.get(
            url_show_merchants + str(discover.json().get('data')['nearby_merchant'][0]['merchant_id']), params=param3,
            headers=headers3)

        validate_status = show_merchants.json().get('success')
        validate_message = show_merchants.json().get('message')['latitude']
        #
        assert show_merchants.status_code == 422
        assert validate_status == bool(False)
        assert 'latitude tidak boleh kosong.' in validate_message

    def test_show_merchant_latitude_text_value(self):
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
        param3 = {
            'latitude': 'aaa',
            'longitude': '107.1162607'
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        show_merchants = requests.get(
            url_show_merchants + str(discover.json().get('data')['nearby_merchant'][0]['merchant_id']), params=param3,
            headers=headers3)

        validate_status = show_merchants.json().get('success')
        validate_message = show_merchants.json().get('message')

        assert show_merchants.status_code == 500
        assert validate_status == bool(False)
        assert 'Aduh! Ada yang salah di sistem kami. Kita sedang memperbaikinya secepat mungkin. Kamu mungkin ingin mencoba sekali lagi' in validate_message

    def test_show_merchant_without_param_longitude(self):
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
        param3 = {
            'latitude': '-6.3823317'
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        show_merchants = requests.get(
            url_show_merchants + str(discover.json().get('data')['nearby_merchant'][0]['merchant_id']), params=param3,
            headers=headers3)

        validate_status = show_merchants.json().get('success')
        validate_message = show_merchants.json().get('message')['longitude']
        #
        assert show_merchants.status_code == 422
        assert validate_status == bool(False)
        assert 'longitude tidak boleh kosong.' in validate_message

    def test_show_merchant_longitude_empty_value(self):
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
        param3 = {
            'latitude': '-6.3823317',
            'longitude': ''
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        show_merchants = requests.get(
            url_show_merchants + str(discover.json().get('data')['nearby_merchant'][0]['merchant_id']), params=param3,
            headers=headers3)

        validate_status = show_merchants.json().get('success')
        validate_message = show_merchants.json().get('message')['longitude']
        #
        assert show_merchants.status_code == 422
        assert validate_status == bool(False)
        assert 'longitude tidak boleh kosong.' in validate_message

    def test_show_merchant_longitude_text_value(self):
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
        param3 = {
            'latitude': '-6.3823317',
            'longitude': 'aaa'
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        show_merchants = requests.get(
            url_show_merchants + str(discover.json().get('data')['nearby_merchant'][0]['merchant_id']), params=param3,
            headers=headers3)

        validate_status = show_merchants.json().get('success')
        validate_message = show_merchants.json().get('message')
        #
        assert show_merchants.status_code == 500
        assert validate_status == bool(False)
        assert 'Aduh! Ada yang salah di sistem kami. Kita sedang memperbaikinya secepat mungkin. Kamu mungkin ingin mencoba sekali lagi' in validate_message

    def test_show_merchant_id_menu_not_found(self):
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
        param3 = {
            'latitude': '-6.3823317',
            'longitude': '107.1162607'
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        show_merchants = requests.get(
            url_show_merchants + '6666', params=param3,
            headers=headers3)

        validate_status = show_merchants.json().get('success')
        validate_message = show_merchants.json().get('message')
        #
        assert show_merchants.status_code == 404
        assert validate_status == bool(False)
        assert 'Merchant tidak ditemukan' in validate_message

    def test_show_merchant_without_id_menu(self):
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
        param3 = {
            'latitude': '-6.3823317',
            'longitude': '107.1162607'
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        show_merchants = requests.get(url_show_merchants, params=param3,headers=headers3)

        validate_status = show_merchants.json().get('success')
        validate_message = show_merchants.json().get('message')
        #
        assert show_merchants.status_code == 200
        assert validate_status == bool(True)
        assert 'Data merchant berhasil ditemukan.' in validate_message

    def test_show_merchant_id_menu_text_value(self):
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
        param3 = {
            'latitude': '-6.3823317',
            'longitude': '107.1162607'
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        show_merchants = requests.get(url_show_merchants + 'aaa', params=param3, headers=headers3)

        validate_status = show_merchants.json().get('success')
        validate_message = show_merchants.json().get('message')
        #
        assert show_merchants.status_code == 404
        assert validate_status == bool(False)
        assert 'Merchant tidak ditemukan' in validate_message


