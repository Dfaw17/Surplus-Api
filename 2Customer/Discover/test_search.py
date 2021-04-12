import requests
from env import stagging
from pprint import pprint
from assertpy import assert_that

class TestCustomerSearchMenu:

    global setting_env,url_login,url_search,email,kata_sandi,wrong_token

    setting_env = stagging
    url_login = f"{setting_env}/api/v2/customer/auth/login/email"
    url_search = f"{setting_env}/api/v2/customer/search"
    email = "kopiruangvirtual@gmail.com"
    kata_sandi = '12345678'
    wrong_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvc3RhZ2luZy5hZG1pbnN1cnBsdXMubmV0XC9hcGlcL3YyXC9jdXN0b21lclwvYXV0aFwvbG9naW5cL2VtYWlsIiwiaWF0IjoxNjE2ODA1NzI2LCJleHAiOjE2MTkzOTc3MjYsIm5iZiI6MTYxNjgwNTcyNiwianRpIjoib05ESmxFRE5hSzNrN2RtVyIsInN1YiI6NDEyNiwicHJ2IjoiMjc0MTA1ZGE2ZTk1YmVmMjgwNzc4NmRkODczODg2N2NmOWMwMmFhYiJ9.fj51xIfQrqleRvdSJUbWcdrvsxQPUn8HpccnOmTgPDI'

    def test_search_normal(self):
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
            'longitude': '107.1162607',
            'missed': '0',
            'ready_stock': '1',
            'menu_categories[0]': '60',
            'max_price': '50000',
            'distance': '10000',
            'preorder': '0',
            'pickup_time_start': '01:00',
            'pickup_time_end': '23:00',
            'keyword': '',
            'order_by': 'nearby',
            'is_active': '1'
        }
        headers2 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        discover = requests.get(url_search, params=param2, headers=headers2)
        pprint(discover.json())
        validate_status = discover.json().get('success')
        validate_message = discover.json().get('message')
        validate_data = discover.json().get('data')
        # #
        assert discover.status_code == 200
        assert validate_status == bool(True)
        assert 'Data pencarian berhasil ditemukan.' in validate_message
        assert_that(validate_data).contains_only('menus', 'merchants')

    def test_search_token_empty_value(self):
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
            'longitude': '107.1162607',
            'missed': '0',
            'ready_stock': '1',
            'menu_categories[0]': '60',
            'max_price': '50000',
            'distance': '10000',
            'preorder': '0',
            'pickup_time_start': '01:00',
            'pickup_time_end': '23:00',
            'keyword': '',
            'order_by': 'nearby',
            'is_active': '1'
        }
        headers2 = {
            "Accept": "application/json",
            "Authorization": ""
        }
        discover = requests.get(url_search, params=param2, headers=headers2)

        validate_status = discover.json().get('success')
        validate_message = discover.json().get('message')

        assert discover.status_code == 401
        assert validate_status == bool(False)
        assert 'Unauthorized' in validate_message

    def test_wrong_token(self):
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
            'longitude': '107.1162607',
            'missed': '0',
            'ready_stock': '1',
            'menu_categories[0]': '60',
            'max_price': '50000',
            'distance': '10000',
            'preorder': '0',
            'pickup_time_start': '01:00',
            'pickup_time_end': '23:00',
            'keyword': '',
            'order_by': 'nearby',
            'is_active': '1'
        }
        headers2 = {
            "Accept": "application/json",
            "Authorization": wrong_token
        }
        discover = requests.get(url_search, params=param2, headers=headers2)

        validate_status = discover.json().get('success')
        validate_message = discover.json().get('message')

        assert discover.status_code == 401
        assert validate_status == bool(False)
        assert 'Unauthorized' in validate_message

    def test_search_latitude_empty_value(self):
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
            'longitude': '107.1162607',
            'missed': '0',
            'ready_stock': '1',
            'menu_categories[0]': '60',
            'max_price': '50000',
            'distance': '10000',
            'preorder': '0',
            'pickup_time_start': '01:00',
            'pickup_time_end': '23:00',
            'keyword': '',
            'order_by': 'nearby',
            'is_active': '1'
        }
        headers2 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        discover = requests.get(url_search, params=param2, headers=headers2)
        pprint(discover.json())
        validate_status = discover.json().get('success')
        validate_message = discover.json().get('message')['latitude']

        assert discover.status_code == 422
        assert validate_status == bool(False)
        assert 'latitude tidak boleh kosong.' in validate_message

    def test_search_without_param_latitude(self):
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
            'longitude': '107.1162607',
            'missed': '0',
            'ready_stock': '1',
            'menu_categories[0]': '60',
            'max_price': '50000',
            'distance': '10000',
            'preorder': '0',
            'pickup_time_start': '01:00',
            'pickup_time_end': '23:00',
            'keyword': '',
            'order_by': 'nearby',
            'is_active': '1'
        }
        headers2 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        discover = requests.get(url_search, params=param2, headers=headers2)
        pprint(discover.json())
        validate_status = discover.json().get('success')
        validate_message = discover.json().get('message')['latitude']

        assert discover.status_code == 422
        assert validate_status == bool(False)
        assert 'latitude tidak boleh kosong.' in validate_message

    def test_search_latitude_text_value(self):
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
            'longitude': '107.1162607',
            'missed': '0',
            'ready_stock': '1',
            'menu_categories[0]': '60',
            'max_price': '50000',
            'distance': '10000',
            'preorder': '0',
            'pickup_time_start': '01:00',
            'pickup_time_end': '23:00',
            'keyword': '',
            'order_by': 'nearby',
            'is_active': '1'
        }
        headers2 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        discover = requests.get(url_search, params=param2, headers=headers2)
        pprint(discover.json())
        validate_status = discover.json().get('success')
        validate_message = discover.json().get('message')

        assert discover.status_code == 500
        assert validate_status == bool(False)
        assert 'Aduh! Ada yang salah di sistem kami. Kita sedang memperbaikinya secepat mungkin. Kamu mungkin ingin mencoba sekali lagi' in validate_message

    def test_search_longitude_empty_value(self):
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
            'longitude': '',
            'missed': '0',
            'ready_stock': '1',
            'menu_categories[0]': '60',
            'max_price': '50000',
            'distance': '10000',
            'preorder': '0',
            'pickup_time_start': '01:00',
            'pickup_time_end': '23:00',
            'keyword': '',
            'order_by': 'nearby',
            'is_active': '1'
        }
        headers2 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        discover = requests.get(url_search, params=param2, headers=headers2)
        pprint(discover.json())
        validate_status = discover.json().get('success')
        validate_message = discover.json().get('message')['longitude']

        assert discover.status_code == 422
        assert validate_status == bool(False)
        assert 'longitude tidak boleh kosong.' in validate_message

    def test_search_longitude_text_value(self):
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
            'longitude': 'aaa',
            'missed': '0',
            'ready_stock': '1',
            'menu_categories[0]': '60',
            'max_price': '50000',
            'distance': '10000',
            'preorder': '0',
            'pickup_time_start': '01:00',
            'pickup_time_end': '23:00',
            'keyword': '',
            'order_by': 'nearby',
            'is_active': '1'
        }
        headers2 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        discover = requests.get(url_search, params=param2, headers=headers2)
        pprint(discover.json())
        validate_status = discover.json().get('success')
        validate_message = discover.json().get('message')
        # validate_data = discover.json().get('data')
        # #
        assert discover.status_code == 500
        assert validate_status == bool(False)
        assert 'Aduh! Ada yang salah di sistem kami. Kita sedang memperbaikinya secepat mungkin. Kamu mungkin ingin mencoba sekali lagi' in validate_message

    def test_search_without_param_longitude(self):
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
            'missed': '0',
            'ready_stock': '1',
            'menu_categories[0]': '60',
            'max_price': '50000',
            'distance': '10000',
            'preorder': '0',
            'pickup_time_start': '01:00',
            'pickup_time_end': '23:00',
            'keyword': '',
            'order_by': 'nearby',
            'is_active': '1'
        }
        headers2 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        discover = requests.get(url_search, params=param2, headers=headers2)
        pprint(discover.json())
        validate_status = discover.json().get('success')
        validate_message = discover.json().get('message')['longitude']

        assert discover.status_code == 422
        assert validate_status == bool(False)
        assert 'longitude tidak boleh kosong.' in validate_message

    def test_search_missed_empty_value(self):
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
            'longitude': '107.1162607',
            'missed': '',
            'ready_stock': '1',
            'menu_categories[0]': '60',
            'max_price': '50000',
            'distance': '10000',
            'preorder': '0',
            'pickup_time_start': '01:00',
            'pickup_time_end': '23:00',
            'keyword': '',
            'order_by': 'nearby',
            'is_active': '1'
        }
        headers2 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        discover = requests.get(url_search, params=param2, headers=headers2)
        pprint(discover.json())
        validate_status = discover.json().get('success')
        validate_message = discover.json().get('message')['missed']

        assert discover.status_code == 422
        assert validate_status == bool(False)
        assert 'Menu terlewat harus bernilai true atau false.' in validate_message

    def test_search_missed_text_value(self):
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
            'longitude': '107.1162607',
            'missed': 'aaa',
            'ready_stock': '1',
            'menu_categories[0]': '60',
            'max_price': '50000',
            'distance': '10000',
            'preorder': '0',
            'pickup_time_start': '01:00',
            'pickup_time_end': '23:00',
            'keyword': '',
            'order_by': 'nearby',
            'is_active': '1'
        }
        headers2 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        discover = requests.get(url_search, params=param2, headers=headers2)
        pprint(discover.json())
        validate_status = discover.json().get('success')
        validate_message = discover.json().get('message')['missed']

        assert discover.status_code == 422
        assert validate_status == bool(False)
        assert 'Menu terlewat harus bernilai true atau false.' in validate_message

    def test_search_missed_not_bool_value(self):
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
            'longitude': '107.1162607',
            'missed': '5',
            'ready_stock': '1',
            'menu_categories[0]': '60',
            'max_price': '50000',
            'distance': '10000',
            'preorder': '0',
            'pickup_time_start': '01:00',
            'pickup_time_end': '23:00',
            'keyword': '',
            'order_by': 'nearby',
            'is_active': '1'
        }
        headers2 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        discover = requests.get(url_search, params=param2, headers=headers2)
        pprint(discover.json())
        validate_status = discover.json().get('success')
        validate_message = discover.json().get('message')['missed']

        assert discover.status_code == 422
        assert validate_status == bool(False)
        assert 'Menu terlewat harus bernilai true atau false.' in validate_message

    def test_search_without_param_missed(self):
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
            'longitude': '107.1162607',
            'ready_stock': '1',
            'menu_categories[0]': '60',
            'max_price': '50000',
            'distance': '10000',
            'preorder': '0',
            'pickup_time_start': '01:00',
            'pickup_time_end': '23:00',
            'keyword': '',
            'order_by': 'nearby',
            'is_active': '1'
        }
        headers2 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        discover = requests.get(url_search, params=param2, headers=headers2)
        pprint(discover.json())
        validate_status = discover.json().get('success')
        validate_message = discover.json().get('message')
        validate_data = discover.json().get('data')
        # #
        assert discover.status_code == 200
        assert validate_status == bool(True)
        assert 'Data pencarian berhasil ditemukan.' in validate_message
        assert_that(validate_data).contains_only('menus', 'merchants')

    def test_search_menu_categories_empty_value(self):
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
            'longitude': '107.1162607',
            'missed': '0',
            'menu_categories[0]': '',
            'max_price': '50000',
            'distance': '10000',
            'preorder': '0',
            'pickup_time_start': '01:00',
            'pickup_time_end': '23:00',
            'keyword': '',
            'order_by': 'nearby',
            'is_active': '1'
        }
        headers2 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        discover = requests.get(url_search, params=param2, headers=headers2)
        pprint(discover.json())
        validate_status = discover.json().get('success')
        validate_message = discover.json().get('message')['menu_categories.0']
        # #
        assert discover.status_code == 422
        assert validate_status == bool(False)
        assert 'menu_categories.0 harus berupa angka.' in validate_message

    def test_search_menu_categories_text_value(self):
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
            'longitude': '107.1162607',
            'missed': '0',
            'menu_categories[0]': 'aaa',
            'max_price': '50000',
            'distance': '10000',
            'preorder': '0',
            'pickup_time_start': '01:00',
            'pickup_time_end': '23:00',
            'keyword': '',
            'order_by': 'nearby',
            'is_active': '1'
        }
        headers2 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        discover = requests.get(url_search, params=param2, headers=headers2)
        pprint(discover.json())
        validate_status = discover.json().get('success')
        validate_message = discover.json().get('message')['menu_categories.0']
        # #
        assert discover.status_code == 422
        assert validate_status == bool(False)
        assert 'menu_categories.0 harus berupa angka.' in validate_message

    def test_search_menu_categories_not_found_value(self):
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
            'longitude': '107.1162607',
            'missed': '0',
            'menu_categories[0]': '600',
            'max_price': '50000',
            'distance': '10000',
            'preorder': '0',
            'pickup_time_start': '01:00',
            'pickup_time_end': '23:00',
            'keyword': '',
            'order_by': 'nearby',
            'is_active': '1'
        }
        headers2 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        discover = requests.get(url_search, params=param2, headers=headers2)
        pprint(discover.json())
        validate_status = discover.json().get('success')
        validate_message = discover.json().get('message')
        validate_data = discover.json().get('data')
        # #
        assert discover.status_code == 200
        assert validate_status == bool(True)
        assert 'Data pencarian berhasil ditemukan.' in validate_message
        assert_that(validate_data).contains_only('menus', 'merchants')

    def test_search_menu_categories_without_index(self):
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
            'longitude': '107.1162607',
            'missed': '0',
            'menu_categories': '60',
            'max_price': '50000',
            'distance': '10000',
            'preorder': '0',
            'pickup_time_start': '01:00',
            'pickup_time_end': '23:00',
            'keyword': '',
            'order_by': 'nearby',
            'is_active': '1'
        }
        headers2 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        discover = requests.get(url_search, params=param2, headers=headers2)
        pprint(discover.json())
        validate_status = discover.json().get('success')
        validate_message = discover.json().get('message')['menu_categories']

        # #
        assert discover.status_code == 422
        assert validate_status == bool(False)
        assert 'Format Kategori Menu tidak benar.' in validate_message

    def test_search_without_param_menu_categories(self):
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
            'longitude': '107.1162607',
            'missed': '0',
            'max_price': '50000',
            'distance': '10000',
            'preorder': '0',
            'pickup_time_start': '01:00',
            'pickup_time_end': '23:00',
            'keyword': '',
            'order_by': 'nearby',
            'is_active': '1'
        }
        headers2 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        discover = requests.get(url_search, params=param2, headers=headers2)
        pprint(discover.json())
        validate_status = discover.json().get('success')
        validate_message = discover.json().get('message')
        validate_data = discover.json().get('data')

        # #
        assert discover.status_code == 200
        assert validate_status == bool(True)
        assert 'Data pencarian berhasil ditemukan' in validate_message
        assert_that(validate_data).contains_only('menus', 'merchants')

    def test_search_without_param_max_price(self):
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
            'longitude': '107.1162607',
            'missed': '0',
            'menu_categories[0]': '60',
            'max_price': '',
            'distance': '10000',
            'preorder': '0',
            'pickup_time_start': '01:00',
            'pickup_time_end': '23:00',
            'keyword': '',
            'order_by': 'nearby',
            'is_active': '1'
        }
        headers2 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        discover = requests.get(url_search, params=param2, headers=headers2)
        pprint(discover.json())
        validate_status = discover.json().get('success')
        validate_message = discover.json().get('message')
        validate_data = discover.json().get('data')

        assert discover.status_code == 200
        assert validate_status == bool(True)
        assert 'Data pencarian berhasil ditemukan' in validate_message
        assert_that(validate_data).contains_only('menus', 'merchants')

    def test_search_max_price_minus_value(self):
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
            'longitude': '107.1162607',
            'missed': '0',
            'menu_categories[0]': '60',
            'max_price': '-500000',
            'distance': '10000',
            'preorder': '0',
            'pickup_time_start': '01:00',
            'pickup_time_end': '23:00',
            'keyword': '',
            'order_by': 'nearby',
            'is_active': '1'
        }
        headers2 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        discover = requests.get(url_search, params=param2, headers=headers2)
        pprint(discover.json())
        validate_status = discover.json().get('success')
        validate_message = discover.json().get('message')
        validate_data = discover.json().get('data')

        assert discover.status_code == 200
        assert validate_status == bool(True)
        assert 'Data pencarian berhasil ditemukan' in validate_message
        assert_that(validate_data).contains_only('menus', 'merchants')

    def test_search_max_price_text_value(self):
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
            'longitude': '107.1162607',
            'missed': '0',
            'menu_categories[0]': '60',
            'max_price': 'aa',
            'distance': '10000',
            'preorder': '0',
            'pickup_time_start': '01:00',
            'pickup_time_end': '23:00',
            'keyword': '',
            'order_by': 'nearby',
            'is_active': '1'
        }
        headers2 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        discover = requests.get(url_search, params=param2, headers=headers2)
        pprint(discover.json())
        validate_status = discover.json().get('success')
        validate_message = discover.json().get('message')['max_price']

        assert discover.status_code == 422
        assert validate_status == bool(False)
        assert 'Harga Maksimal harus berupa angka.' in validate_message

    def test_search_without_param_max_price(self):
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
            'longitude': '107.1162607',
            'missed': '0',
            'menu_categories[0]': '60',
            'distance': '10000',
            'preorder': '0',
            'pickup_time_start': '01:00',
            'pickup_time_end': '23:00',
            'keyword': '',
            'order_by': 'nearby',
            'is_active': '1'
        }
        headers2 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        discover = requests.get(url_search, params=param2, headers=headers2)
        pprint(discover.json())
        validate_status = discover.json().get('success')
        validate_message = discover.json().get('message')
        validate_data = discover.json().get('data')

        assert discover.status_code == 200
        assert validate_status == bool(True)
        assert 'Data pencarian berhasil ditemukan.' in validate_message
        assert_that(validate_data).contains_only('menus', 'merchants')

    def test_search_without_param_distance(self):
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
            'longitude': '107.1162607',
            'missed': '0',
            'menu_categories[0]': '60',
            'max_price': '500000',
            'distance': '',
            'preorder': '0',
            'pickup_time_start': '01:00',
            'pickup_time_end': '23:00',
            'keyword': '',
            'order_by': 'nearby',
            'is_active': '1'
        }
        headers2 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        discover = requests.get(url_search, params=param2, headers=headers2)
        pprint(discover.json())
        validate_status = discover.json().get('success')
        validate_message = discover.json().get('message')
        validate_data = discover.json().get('data')

        assert discover.status_code == 200
        assert validate_status == bool(True)
        assert 'Data pencarian berhasil ditemukan.' in validate_message
        assert_that(validate_data).contains_only('menus', 'merchants')

    def test_search_distance_minus_value(self):
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
            'longitude': '107.1162607',
            'missed': '0',
            'menu_categories[0]': '60',
            'max_price': '500000',
            'distance': '-10000',
            'preorder': '0',
            'pickup_time_start': '01:00',
            'pickup_time_end': '23:00',
            'keyword': '',
            'order_by': 'nearby',
            'is_active': '1'
        }
        headers2 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        discover = requests.get(url_search, params=param2, headers=headers2)
        pprint(discover.json())
        validate_status = discover.json().get('success')
        validate_message = discover.json().get('message')['distance']

        assert discover.status_code == 422
        assert validate_status == bool(False)
        assert 'Jarak setidaknya harus 100.' in validate_message

    def test_search_distance_text_value(self):
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
            'longitude': '107.1162607',
            'missed': '0',
            'menu_categories[0]': '60',
            'max_price': '500000',
            'distance': 'aa',
            'preorder': '0',
            'pickup_time_start': '01:00',
            'pickup_time_end': '23:00',
            'keyword': '',
            'order_by': 'nearby',
            'is_active': '1'
        }
        headers2 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        discover = requests.get(url_search, params=param2, headers=headers2)
        pprint(discover.json())
        validate_status = discover.json().get('success')
        validate_message = discover.json().get('message')['distance']

        assert discover.status_code == 422
        assert validate_status == bool(False)
        assert 'Jarak harus berupa angka.' in validate_message

    def test_search_without_param_distance(self):
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
            'longitude': '107.1162607',
            'missed': '0',
            'menu_categories[0]': '60',
            'max_price': '500000',
            'preorder': '0',
            'pickup_time_start': '01:00',
            'pickup_time_end': '23:00',
            'keyword': '',
            'order_by': 'nearby',
            'is_active': '1'
        }
        headers2 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        discover = requests.get(url_search, params=param2, headers=headers2)
        pprint(discover.json())
        validate_status = discover.json().get('success')
        validate_message = discover.json().get('message')
        validate_data = discover.json().get('data')

        assert discover.status_code == 200
        assert validate_status == bool(True)
        assert 'Data pencarian berhasil ditemukan.' in validate_message
        assert_that(validate_data).contains_only('menus', 'merchants')

    def test_search_without_param_preorder(self):
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
            'longitude': '107.1162607',
            'missed': '0',
            'menu_categories[0]': '60',
            'max_price': '500000',
            'distance': '10000',
            'pickup_time_start': '01:00',
            'pickup_time_end': '23:00',
            'keyword': '',
            'order_by': 'nearby',
            'is_active': '1'
        }
        headers2 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        discover = requests.get(url_search, params=param2, headers=headers2)
        pprint(discover.json())
        validate_status = discover.json().get('success')
        validate_message = discover.json().get('message')
        validate_data = discover.json().get('data')

        assert discover.status_code == 200
        assert validate_status == bool(True)
        assert 'Data pencarian berhasil ditemukan.' in validate_message
        assert_that(validate_data).contains_only('menus', 'merchants')

    def test_search_preorder_empty_value(self):
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
            'longitude': '107.1162607',
            'missed': '0',
            'menu_categories[0]': '60',
            'max_price': '500000',
            'distance': '10000',
            'preorder': '',
            'pickup_time_start': '01:00',
            'pickup_time_end': '23:00',
            'keyword': '',
            'order_by': 'nearby',
            'is_active': '1'
        }
        headers2 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        discover = requests.get(url_search, params=param2, headers=headers2)
        pprint(discover.json())
        validate_status = discover.json().get('success')
        validate_message = discover.json().get('message')['preorder']
        validate_data = discover.json().get('data')

        assert discover.status_code == 422
        assert validate_status == bool(False)
        assert 'Menu Pre-order harus bernilai true atau false.' in validate_message

    def test_search_preorder_text_value(self):
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
            'longitude': '107.1162607',
            'missed': '0',
            'menu_categories[0]': '60',
            'max_price': '500000',
            'distance': '10000',
            'preorder': 'aaa',
            'pickup_time_start': '01:00',
            'pickup_time_end': '23:00',
            'keyword': '',
            'order_by': 'nearby',
            'is_active': '1'
        }
        headers2 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        discover = requests.get(url_search, params=param2, headers=headers2)
        pprint(discover.json())
        validate_status = discover.json().get('success')
        validate_message = discover.json().get('message')['preorder']
        validate_data = discover.json().get('data')

        assert discover.status_code == 422
        assert validate_status == bool(False)
        assert 'Menu Pre-order harus bernilai true atau false.' in validate_message

    def test_search_preorder_not_bool_value(self):
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
            'longitude': '107.1162607',
            'missed': '0',
            'menu_categories[0]': '60',
            'max_price': '500000',
            'distance': '10000',
            'preorder': '5',
            'pickup_time_start': '01:00',
            'pickup_time_end': '23:00',
            'keyword': '',
            'order_by': 'nearby',
            'is_active': '1'
        }
        headers2 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        discover = requests.get(url_search, params=param2, headers=headers2)
        pprint(discover.json())
        validate_status = discover.json().get('success')
        validate_message = discover.json().get('message')['preorder']
        validate_data = discover.json().get('data')

        assert discover.status_code == 422
        assert validate_status == bool(False)
        assert 'Menu Pre-order harus bernilai true atau false.' in validate_message

    def test_search_without_param_pickup_time_start(self):
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
            'longitude': '107.1162607',
            'missed': '0',
            'menu_categories[0]': '60',
            'max_price': '500000',
            'distance': '10000',
            'preorder': '0',
            # 'pickup_time_start': '01:00',
            'pickup_time_end': '23:00',
            'keyword': '',
            'order_by': 'nearby',
            'is_active': '1'
        }
        headers2 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        discover = requests.get(url_search, params=param2, headers=headers2)
        pprint(discover.json())
        validate_status = discover.json().get('success')
        validate_message = discover.json().get('message')
        validate_data = discover.json().get('data')
        #
        assert discover.status_code == 200
        assert validate_status == bool(True)
        assert 'Data pencarian berhasil ditemukan.' in validate_message
        assert_that(validate_data).contains_only('menus', 'merchants')

    def test_search_param_pickup_time_start_empty_value(self):
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
            'longitude': '107.1162607',
            'missed': '0',
            'menu_categories[0]': '60',
            'max_price': '500000',
            'distance': '10000',
            'preorder': '0',
            'pickup_time_start': '',
            'pickup_time_end': '23:00',
            'keyword': '',
            'order_by': 'nearby',
            'is_active': '1'
        }
        headers2 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        discover = requests.get(url_search, params=param2, headers=headers2)
        pprint(discover.json())
        validate_status = discover.json().get('success')
        validate_message = discover.json().get('message')['pickup_time_start']
        validate_data = discover.json().get('data')
        #
        assert discover.status_code == 422
        assert validate_status == bool(False)
        assert 'Waktu awal penjemputan tidak cocok dengan format H:i.' in validate_message

    def test_search_param_pickup_time_start_text_value(self):
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
            'longitude': '107.1162607',
            'missed': '0',
            'menu_categories[0]': '60',
            'max_price': '500000',
            'distance': '10000',
            'preorder': '0',
            'pickup_time_start': 'aaa',
            'pickup_time_end': '23:00',
            'keyword': '',
            'order_by': 'nearby',
            'is_active': '1'
        }
        headers2 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        discover = requests.get(url_search, params=param2, headers=headers2)
        pprint(discover.json())
        validate_status = discover.json().get('success')
        validate_message = discover.json().get('message')['pickup_time_start']
        validate_data = discover.json().get('data')
        #
        assert discover.status_code == 422
        assert validate_status == bool(False)
        assert 'Waktu awal penjemputan tidak cocok dengan format H:i.' in validate_message

    def test_search_param_pickup_time_start_not_time_value(self):
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
            'longitude': '107.1162607',
            'missed': '0',
            'menu_categories[0]': '60',
            'max_price': '500000',
            'distance': '10000',
            'preorder': '0',
            'pickup_time_start': '12345',
            'pickup_time_end': '23:00',
            'keyword': '',
            'order_by': 'nearby',
            'is_active': '1'
        }
        headers2 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        discover = requests.get(url_search, params=param2, headers=headers2)
        pprint(discover.json())
        validate_status = discover.json().get('success')
        validate_message = discover.json().get('message')['pickup_time_start']
        validate_data = discover.json().get('data')
        #
        assert discover.status_code == 422
        assert validate_status == bool(False)
        assert 'Waktu awal penjemputan tidak cocok dengan format H:i.' in validate_message

    def test_search_param_pickup_time_start_P_AM_value(self):
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
            'longitude': '107.1162607',
            'missed': '0',
            'menu_categories[0]': '60',
            'max_price': '500000',
            'distance': '10000',
            'preorder': '0',
            'pickup_time_start': '7 AM',
            'pickup_time_end': '23:00',
            'keyword': '',
            'order_by': 'nearby',
            'is_active': '1'
        }
        headers2 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        discover = requests.get(url_search, params=param2, headers=headers2)
        pprint(discover.json())
        validate_status = discover.json().get('success')
        validate_message = discover.json().get('message')['pickup_time_start']
        validate_data = discover.json().get('data')
        #
        assert discover.status_code == 422
        assert validate_status == bool(False)
        assert 'Waktu awal penjemputan tidak cocok dengan format H:i.' in validate_message

    def test_search_without_param_pickup_time_end(self):
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
            'longitude': '107.1162607',
            'missed': '0',
            'menu_categories[0]': '60',
            'max_price': '500000',
            'distance': '10000',
            'preorder': '0',
            'pickup_time_start': '02:00',
            # 'pickup_time_end': '23:00',
            'keyword': '',
            'order_by': 'nearby',
            'is_active': '1'
        }
        headers2 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        discover = requests.get(url_search, params=param2, headers=headers2)
        pprint(discover.json())
        validate_status = discover.json().get('success')
        validate_message = discover.json().get('message')
        validate_data = discover.json().get('data')
        #
        assert discover.status_code == 200
        assert validate_status == bool(True)
        assert 'Data pencarian berhasil ditemukan.' in validate_message
        assert_that(validate_data).contains_only('menus', 'merchants')

    def test_search_param_pickup_time_end_empty_value(self):
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
            'longitude': '107.1162607',
            'missed': '0',
            'menu_categories[0]': '60',
            'max_price': '500000',
            'distance': '10000',
            'preorder': '0',
            'pickup_time_start': '02:00',
            'pickup_time_end': '',
            'keyword': '',
            'order_by': 'nearby',
            'is_active': '1'
        }
        headers2 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        discover = requests.get(url_search, params=param2, headers=headers2)
        pprint(discover.json())
        validate_status = discover.json().get('success')
        validate_message = discover.json().get('message')['pickup_time_end']

        assert discover.status_code == 422
        assert validate_status == bool(False)
        assert 'Waktu akhir penjemputan tidak cocok dengan format H:i.' in validate_message

    def test_search_param_pickup_time_end_text_value(self):
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
            'longitude': '107.1162607',
            'missed': '0',
            'menu_categories[0]': '60',
            'max_price': '500000',
            'distance': '10000',
            'preorder': '0',
            'pickup_time_start': '02:00',
            'pickup_time_end': 'aaa',
            'keyword': '',
            'order_by': 'nearby',
            'is_active': '1'
        }
        headers2 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        discover = requests.get(url_search, params=param2, headers=headers2)
        pprint(discover.json())
        validate_status = discover.json().get('success')
        validate_message = discover.json().get('message')['pickup_time_end']

        assert discover.status_code == 422
        assert validate_status == bool(False)
        assert 'Waktu akhir penjemputan tidak cocok dengan format H:i.' in validate_message

    def test_search_param_pickup_time_end_not_time_value(self):
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
            'longitude': '107.1162607',
            'missed': '0',
            'menu_categories[0]': '60',
            'max_price': '500000',
            'distance': '10000',
            'preorder': '0',
            'pickup_time_start': '02:00',
            'pickup_time_end': '123',
            'keyword': '',
            'order_by': 'nearby',
            'is_active': '1'
        }
        headers2 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        discover = requests.get(url_search, params=param2, headers=headers2)
        pprint(discover.json())
        validate_status = discover.json().get('success')
        validate_message = discover.json().get('message')['pickup_time_end']

        assert discover.status_code == 422
        assert validate_status == bool(False)
        assert 'Waktu akhir penjemputan tidak cocok dengan format H:i.' in validate_message

    def test_search_param_pickup_time_end_P_AM_value(self):
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
            'longitude': '107.1162607',
            'missed': '0',
            'menu_categories[0]': '60',
            'max_price': '500000',
            'distance': '10000',
            'preorder': '0',
            'pickup_time_start': '02:00',
            'pickup_time_end': '5 PM',
            'keyword': '',
            'order_by': 'nearby',
            'is_active': '1'
        }
        headers2 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        discover = requests.get(url_search, params=param2, headers=headers2)
        pprint(discover.json())
        validate_status = discover.json().get('success')
        validate_message = discover.json().get('message')['pickup_time_end']

        assert discover.status_code == 422
        assert validate_status == bool(False)
        assert 'Waktu akhir penjemputan tidak cocok dengan format H:i.' in validate_message

    def test_search_without_param_keyword(self):
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
            'longitude': '107.1162607',
            'missed': '0',
            'menu_categories[0]': '60',
            'max_price': '500000',
            'distance': '10000',
            'preorder': '0',
            'pickup_time_start': '02:00',
            'pickup_time_end': '22:00',
            # 'keyword': '',
            'order_by': 'nearby',
            'is_active': '1'
        }
        headers2 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        discover = requests.get(url_search, params=param2, headers=headers2)
        pprint(discover.json())
        validate_status = discover.json().get('success')
        validate_message = discover.json().get('message')
        validate_data = discover.json().get('data')

        assert discover.status_code == 200
        assert validate_status == bool(True)
        assert 'Data pencarian berhasil ditemukan.' in validate_message
        assert_that(validate_data).contains_only('menus', 'merchants')

    def test_search_keyword_empty_value(self):
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
            'longitude': '107.1162607',
            'missed': '0',
            'menu_categories[0]': '60',
            'max_price': '500000',
            'distance': '10000',
            'preorder': '0',
            'pickup_time_start': '02:00',
            'pickup_time_end': '22:00',
            'keyword': '',
            'order_by': 'nearby',
            'is_active': '1'
        }
        headers2 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        discover = requests.get(url_search, params=param2, headers=headers2)
        pprint(discover.json())
        validate_status = discover.json().get('success')
        validate_message = discover.json().get('message')
        validate_data = discover.json().get('data')

        assert discover.status_code == 200
        assert validate_status == bool(True)
        assert 'Data pencarian berhasil ditemukan.' in validate_message
        assert_that(validate_data).contains_only('menus', 'merchants')

    def test_search_without_param_order_by(self):
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
            'longitude': '107.1162607',
            'missed': '0',
            'menu_categories[0]': '60',
            'max_price': '500000',
            'distance': '10000',
            'preorder': '0',
            'pickup_time_start': '02:00',
            'pickup_time_end': '22:00',
            'keyword': '',
            # 'order_by': 'nearby',
            'is_active': '1'
        }
        headers2 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        discover = requests.get(url_search, params=param2, headers=headers2)
        pprint(discover.json())
        validate_status = discover.json().get('success')
        validate_message = discover.json().get('message')
        validate_data = discover.json().get('data')

        assert discover.status_code == 200
        assert validate_status == bool(True)
        assert 'Data pencarian berhasil ditemukan.' in validate_message
        assert_that(validate_data).contains_only('menus', 'merchants')

    def test_search_order_by_empty_value(self):
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
            'longitude': '107.1162607',
            'missed': '0',
            'menu_categories[0]': '60',
            'max_price': '500000',
            'distance': '10000',
            'preorder': '0',
            'pickup_time_start': '02:00',
            'pickup_time_end': '22:00',
            'keyword': '',
            'order_by': '',
            'is_active': '1'
        }
        headers2 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        discover = requests.get(url_search, params=param2, headers=headers2)
        pprint(discover.json())
        validate_status = discover.json().get('success')
        validate_message = discover.json().get('message')['order_by']


        assert discover.status_code == 422
        assert validate_status == bool(False)
        assert 'Urutan yang dipilih tidak tersedia.' in validate_message

    def test_search_order_by_not_available_value(self):
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
            'longitude': '107.1162607',
            'missed': '0',
            'menu_categories[0]': '60',
            'max_price': '500000',
            'distance': '10000',
            'preorder': '0',
            'pickup_time_start': '02:00',
            'pickup_time_end': '22:00',
            'keyword': '',
            'order_by': 'nearbyy',
            'is_active': '1'
        }
        headers2 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        discover = requests.get(url_search, params=param2, headers=headers2)
        pprint(discover.json())
        validate_status = discover.json().get('success')
        validate_message = discover.json().get('message')['order_by']

        assert discover.status_code == 422
        assert validate_status == bool(False)
        assert 'Urutan yang dipilih tidak tersedia.' in validate_message


