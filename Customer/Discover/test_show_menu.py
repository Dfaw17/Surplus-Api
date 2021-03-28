import requests
from env import stagging
from pprint import pprint
from assertpy import assert_that


class TestCustomerShowMenu:
    global setting_env, url_login, url_discover, url_show_menu, email, kata_sandi, wrong_token

    setting_env = stagging
    url_login = f"{setting_env}/api/v2/customer/auth/login/email"
    url_discover = f"{setting_env}/api/v2/customer/discover"
    url_show_menu = f"{setting_env}/api/v2/customer/menus/"
    email = "kopiruangvirtual@gmail.com"
    kata_sandi = '12345678'
    wrong_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvc3RhZ2luZy5hZG1pbnN1cnBsdXMubmV0XC9hcGlcL3YyXC9jdXN0b21lclwvYXV0aFwvbG9naW5cL2VtYWlsIiwiaWF0IjoxNjE2ODA1NzI2LCJleHAiOjE2MTkzOTc3MjYsIm5iZiI6MTYxNjgwNTcyNiwianRpIjoib05ESmxFRE5hSzNrN2RtVyIsInN1YiI6NDEyNiwicHJ2IjoiMjc0MTA1ZGE2ZTk1YmVmMjgwNzc4NmRkODczODg2N2NmOWMwMmFhYiJ9.fj51xIfQrqleRvdSJUbWcdrvsxQPUn8HpccnOmTgPDI'

    def test_show_menu_normal(self):
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
        show_menu = requests.get(url_show_menu + str(discover.json().get('data')['nearby_menu'][0]['id']),
                                 params=param2, headers=headers2)

        validate_status = show_menu.json().get('success')
        validate_message = show_menu.json().get('message')
        validate_data_menu = show_menu.json().get('data')['id']
        validate_merchant_id = show_menu.json().get('data')['merchant_id']
        validate_nama_menu_makanan = show_menu.json().get('data')['nama_menu_makanan']
        validate_merchant_kategori_makanan_id = show_menu.json().get('data')['merchant_kategori_makanan_id']

        assert validate_status == bool(True)
        assert 'Data menu berhasil ditemukan.' in validate_message
        assert show_menu.status_code == 200
        assert_that([validate_data_menu, validate_nama_menu_makanan, validate_merchant_kategori_makanan_id,
                     validate_merchant_id]).is_not_empty()

    def test_show_menu_without_token(self):
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
        show_menu = requests.get(url_show_menu + str(discover.json().get('data')['nearby_menu'][0]['id']),
                                 params=param3, headers=headers3)

        validate_status = show_menu.json().get('success')
        validate_message = show_menu.json().get('message')
        assert validate_status == bool(False)
        assert 'Unauthorized' in validate_message
        assert show_menu.status_code == 401

    def test_show_menu_wrong_token(self):
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
        show_menu = requests.get(url_show_menu + str(discover.json().get('data')['nearby_menu'][0]['id']),
                                 params=param3, headers=headers3)

        validate_status = show_menu.json().get('success')
        validate_message = show_menu.json().get('message')
        assert validate_status == bool(False)
        assert 'Unauthorized' in validate_message
        assert show_menu.status_code == 401

    def test_show_menu_latitude_empty_value(self):
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
        show_menu = requests.get(url_show_menu + str(discover.json().get('data')['nearby_menu'][0]['id']),
                                 params=param3, headers=headers3)

        validate_status = show_menu.json().get('success')
        validate_message = show_menu.json().get('message')['latitude']
        assert validate_status == bool(False)
        assert 'latitude tidak boleh kosong.' in validate_message
        assert show_menu.status_code == 422

    def test_show_menu_latitude_text_value(self):
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
        show_menu = requests.get(url_show_menu + str(discover.json().get('data')['nearby_menu'][0]['id']),
                                 params=param3, headers=headers3)

        validate_status = show_menu.json().get('success')
        validate_message = show_menu.json().get('message')
        assert validate_status == bool(False)
        assert 'Aduh! Ada yang salah di sistem kami. Kita sedang memperbaikinya secepat mungkin. Kamu mungkin ingin mencoba sekali lagi' in validate_message
        assert show_menu.status_code == 500

    def test_show_menu_without_param_latitude(self):
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
        show_menu = requests.get(url_show_menu + str(discover.json().get('data')['nearby_menu'][0]['id']),
                                 params=param3, headers=headers3)

        validate_status = show_menu.json().get('success')
        validate_message = show_menu.json().get('message')['latitude']

        assert validate_status == bool(False)
        assert 'latitude tidak boleh kosong.' in validate_message
        assert show_menu.status_code == 422

    def test_show_menu_longitude_empty_value(self):
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
        show_menu = requests.get(url_show_menu + str(discover.json().get('data')['nearby_menu'][0]['id']),
                                 params=param3, headers=headers3)

        validate_status = show_menu.json().get('success')
        validate_message = show_menu.json().get('message')['longitude']
        assert validate_status == bool(False)
        assert 'longitude tidak boleh kosong.' in validate_message
        assert show_menu.status_code == 422

    def test_show_menu_longitude_text_value(self):
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
        show_menu = requests.get(url_show_menu + str(discover.json().get('data')['nearby_menu'][0]['id']),
                                 params=param3, headers=headers3)

        validate_status = show_menu.json().get('success')
        validate_message = show_menu.json().get('message')
        assert validate_status == bool(False)
        assert 'Aduh! Ada yang salah di sistem kami. Kita sedang memperbaikinya secepat mungkin. Kamu mungkin ingin mencoba sekali lagi' in validate_message
        assert show_menu.status_code == 500

    def test_show_menu_without_param_longitude(self):
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
        show_menu = requests.get(url_show_menu + str(discover.json().get('data')['nearby_menu'][0]['id']),
                                 params=param3, headers=headers3)

        validate_status = show_menu.json().get('success')
        validate_message = show_menu.json().get('message')['longitude']

        assert validate_status == bool(False)
        assert 'longitude tidak boleh kosong.' in validate_message
        assert show_menu.status_code == 422

    def test_show_menu_id_menu_not_found(self):
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
        show_menu = requests.get(url_show_menu + '99999', params=param3, headers=headers3)

        validate_status = show_menu.json().get('success')
        validate_message = show_menu.json().get('message')

        assert show_menu.status_code == 404
        assert validate_status == bool(False)
        assert 'Data menu tidak ditemukan' in validate_message

    def test_show_menu_without_id_menu(self):
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
        show_menu = requests.get(url_show_menu, params=param3, headers=headers3)

        validate_status = show_menu.json().get('success')
        validate_message = show_menu.json().get('message')['type']

        assert show_menu.status_code == 422
        assert validate_status == bool(False)
        assert 'type tidak boleh kosong.' in validate_message

    def test_show_menu_id_menu_text_value(self):
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
        show_menu = requests.get(url_show_menu + 'aaa', params=param3, headers=headers3)

        validate_status = show_menu.json().get('success')
        validate_message = show_menu.json().get('message')

        assert show_menu.status_code == 404
        assert validate_status == bool(False)
        assert 'Data menu tidak ditemukan' in validate_message