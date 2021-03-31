import requests
from env import stagging
from pprint import pprint
from assertpy import assert_that

class TestCustomerIndexMenu:

    global setting_env,url_login,url_index_menu,email,kata_sandi,wrong_token

    setting_env = stagging
    url_login = f"{setting_env}/api/v2/customer/auth/login/email"
    url_index_menu = f"{setting_env}/api/v2/customer/menus"
    email = "kopiruangvirtual@gmail.com"
    kata_sandi = '12345678'
    wrong_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvc3RhZ2luZy5hZG1pbnN1cnBsdXMubmV0XC9hcGlcL3YyXC9jdXN0b21lclwvYXV0aFwvbG9naW5cL2VtYWlsIiwiaWF0IjoxNjE2ODA1NzI2LCJleHAiOjE2MTkzOTc3MjYsIm5iZiI6MTYxNjgwNTcyNiwianRpIjoib05ESmxFRE5hSzNrN2RtVyIsInN1YiI6NDEyNiwicHJ2IjoiMjc0MTA1ZGE2ZTk1YmVmMjgwNzc4NmRkODczODg2N2NmOWMwMmFhYiJ9.fj51xIfQrqleRvdSJUbWcdrvsxQPUn8HpccnOmTgPDI'

    def test_index_menu_normal(self):
        param = {
            'email': email,
            'password': kata_sandi
        }
        headers = {
            "Accept": "application/json"
        }
        login = requests.post(url_login, params=param, headers=headers)
        param2 = {
            'type': 'nearby'
        }
        headers2 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        index_menu = requests.get(url_index_menu, params=param2, headers=headers2)

        validate_status = index_menu.json().get('success')
        validate_message = index_menu.json().get('message')
        validate_data = index_menu.json().get('data')[0]

        assert index_menu.status_code == 200
        assert validate_status == bool(True)
        assert 'Data menu terlewat berhasil ditemukan.' in validate_message
        assert_that(validate_data).contains_only('id', 'merchant_id', 'nama_menu_makanan',
                                                 'merchant_kategori_makanan_id',
                                                 'deskripsi', 'waktu_mulai_penjemputan', 'waktu_akhir_penjemputan',
                                                 'harga_asli', 'harga_jual', 'stock', 'is_non_halal', 'total_terjual',
                                                 'is_missed', 'is_active', 'waktu_missed', 'image_thumbnail',
                                                 'created_at',
                                                 'updated_at', 'is_tomorrow', 'menu_image', 'nama_merchant',
                                                 'alamat_merchant',
                                                 'merchant_logo', 'distance')

    def test_index_menu_wrong_token(self):
        param = {
            'email': email,
            'password': kata_sandi
        }
        headers = {
            "Accept": "application/json"
        }
        login = requests.post(url_login, params=param, headers=headers)
        param2 = {
            'type': 'nearby'
        }
        headers2 = {
            "Accept": "application/json",
            "Authorization": wrong_token
        }
        index_menu = requests.get(url_index_menu, params=param2, headers=headers2)

        validate_status = index_menu.json().get('success')
        validate_message = index_menu.json().get('message')

        assert index_menu.status_code == 401
        assert validate_status == bool(False)
        assert 'Unauthorized' in validate_message

    def test_index_menu_token_empty_value(self):
        param = {
            'email': email,
            'password': kata_sandi
        }
        headers = {
            "Accept": "application/json"
        }
        login = requests.post(url_login, params=param, headers=headers)
        param2 = {
            'type': 'nearby'
        }
        headers2 = {
            "Accept": "application/json",
            "Authorization": ""
        }
        index_menu = requests.get(url_index_menu, params=param2, headers=headers2)

        validate_status = index_menu.json().get('success')
        validate_message = index_menu.json().get('message')

        assert index_menu.status_code == 401
        assert validate_status == bool(False)
        assert 'Unauthorized' in validate_message

    def test_index_menu_type_empty_value(self):
        param = {
            'email': email,
            'password': kata_sandi
        }
        headers = {
            "Accept": "application/json"
        }
        login = requests.post(url_login, params=param, headers=headers)
        param2 = {
            'type': ''
        }
        headers2 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        index_menu = requests.get(url_index_menu, params=param2, headers=headers2)

        validate_status = index_menu.json().get('success')
        validate_message = index_menu.json().get('message')['type']

        assert index_menu.status_code == 422
        assert validate_status == bool(False)
        assert 'type tidak boleh kosong.' in validate_message

    def test_index_menu_type_not_available_value(self):
        param = {
            'email': email,
            'password': kata_sandi
        }
        headers = {
            "Accept": "application/json"
        }
        login = requests.post(url_login, params=param, headers=headers)
        param2 = {
            'type': 'qaqaqa'
        }
        headers2 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        index_menu = requests.get(url_index_menu, params=param2, headers=headers2)

        validate_status = index_menu.json().get('success')
        validate_message = index_menu.json().get('message')['type']

        assert index_menu.status_code == 422
        assert validate_status == bool(False)
        assert 'type yang dipilih tidak tersedia.' in validate_message

    def test_index_menu_without_param_type(self):
        param = {
            'email': email,
            'password': kata_sandi
        }
        headers = {
            "Accept": "application/json"
        }
        login = requests.post(url_login, params=param, headers=headers)
        param2 = {
        }
        headers2 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        index_menu = requests.get(url_index_menu, params=param2, headers=headers2)

        validate_status = index_menu.json().get('success')
        validate_message = index_menu.json().get('message')['type']

        assert index_menu.status_code == 422
        assert validate_status == bool(False)
        assert 'type tidak boleh kosong.' in validate_message


