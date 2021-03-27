import requests
from env import stagging
from pprint import pprint
from assertpy import assert_that

class TestCustomerDiscoverMenu:

    global setting_env,url_login,url_discover,email,kata_sandi,wrong_token

    setting_env = stagging
    url_login = f"{setting_env}/api/v2/customer/auth/login/email"
    url_discover = f"{setting_env}/api/v2/customer/discover"
    email = "kopiruangvirtual@gmail.com"
    kata_sandi = '12345678'
    wrong_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvc3RhZ2luZy5hZG1pbnN1cnBsdXMubmV0XC9hcGlcL3YyXC9jdXN0b21lclwvYXV0aFwvbG9naW5cL2VtYWlsIiwiaWF0IjoxNjE2ODA1NzI2LCJleHAiOjE2MTkzOTc3MjYsIm5iZiI6MTYxNjgwNTcyNiwianRpIjoib05ESmxFRE5hSzNrN2RtVyIsInN1YiI6NDEyNiwicHJ2IjoiMjc0MTA1ZGE2ZTk1YmVmMjgwNzc4NmRkODczODg2N2NmOWMwMmFhYiJ9.fj51xIfQrqleRvdSJUbWcdrvsxQPUn8HpccnOmTgPDI'

    def test_discovers_menu_normal(self):
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

        validate_status = discover.json().get('success')
        validate_message = discover.json().get('message')
        validate_menu_kategori = len(discover.json().get('data')['menu_categories'])
        validate_data = discover.json().get('data')
        #
        assert discover.status_code == 200
        assert validate_status == bool(True)
        assert 'Data discover berhasil ditemukan.' in validate_message
        assert validate_menu_kategori == 10
        assert_that(validate_data).contains_only('nearby_menu', 'available_voucher', 'menu_categories', 'missed_menu',
                                                 'newest_menu', 'bestseller_menu', 'nearby_merchant', 'menu_makanan',
                                                 'menu_roti', 'menu_vegan', 'menu_bahan_makanan', 'menu_kue',
                                                 'menu_buah', 'menu_non_halal', 'menu_lainnya')

    def test_discovers_latitude_empty_value(self):
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
        discover = requests.get(url_discover, params=param2, headers=headers2)

        validate_status = discover.json().get('success')
        validate_message = discover.json().get('message')['latitude']
        #
        assert discover.status_code == 422
        assert validate_status == bool(False)
        assert 'latitude tidak boleh kosong.' in validate_message

    def test_discovers_without_param_latitude(self):
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
        discover = requests.get(url_discover, params=param2, headers=headers2)

        validate_status = discover.json().get('success')
        validate_message = discover.json().get('message')['latitude']
        #
        assert discover.status_code == 422
        assert validate_status == bool(False)
        assert 'latitude tidak boleh kosong.' in validate_message

    def test_discovers_longitude_empty_value(self):
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
        discover = requests.get(url_discover, params=param2, headers=headers2)

        validate_status = discover.json().get('success')
        validate_message = discover.json().get('message')['longitude']
        #
        assert discover.status_code == 422
        assert validate_status == bool(False)
        assert 'longitude tidak boleh kosong.' in validate_message

    def test_discovers_without_param_longitude(self):
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
        discover = requests.get(url_discover, params=param2, headers=headers2)

        validate_status = discover.json().get('success')
        validate_message = discover.json().get('message')['longitude']
        #
        assert discover.status_code == 422
        assert validate_status == bool(False)
        assert 'longitude tidak boleh kosong.' in validate_message

    def test_discover_wrong_token(self):
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
        discover = requests.get(url_discover, params=param2, headers=headers2)

        validate_status = discover.json().get('success')
        validate_message = discover.json().get('message')
        #
        assert discover.status_code == 401
        assert validate_status == bool(False)
        assert 'Unauthorized' in validate_message

    def test_discover_empty_token(self):
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
        discover = requests.get(url_discover, params=param2, headers=headers2)

        validate_status = discover.json().get('success')
        validate_message = discover.json().get('message')
        #
        assert discover.status_code == 401
        assert validate_status == bool(False)
        assert 'Unauthorized' in validate_message

    def test_discover_without_param_token(self):
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
            "Accept": "application/json"
        }
        discover = requests.get(url_discover, params=param2, headers=headers2)

        validate_status = discover.json().get('success')
        validate_message = discover.json().get('message')
        #
        assert discover.status_code == 401
        assert validate_status == bool(False)
        assert 'Unauthorized' in validate_message



