import requests
from env import stagging
from pprint import pprint
from assertpy import assert_that

class TestCustomerShowAddress:

    global setting_env,url_login,url_index_address,url_show_address,email,kata_sandi,wrong_token

    setting_env = stagging
    url_login = f"{setting_env}/api/v2/customer/auth/login/email"
    url_index_address = f"{setting_env}/api/v2/customer/address/"
    url_show_address = f"{setting_env}/api/v2/customer/address/"
    email = "kopiruangvirtual@gmail.com"
    kata_sandi = '12345678'
    wrong_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvc3RhZ2luZy5hZG1pbnN1cnBsdXMubmV0XC9hcGlcL3YyXC9jdXN0b21lclwvYXV0aFwvbG9naW5cL2VtYWlsIiwiaWF0IjoxNjE2ODA1NzI2LCJleHAiOjE2MTkzOTc3MjYsIm5iZiI6MTYxNjgwNTcyNiwianRpIjoib05ESmxFRE5hSzNrN2RtVyIsInN1YiI6NDEyNiwicHJ2IjoiMjc0MTA1ZGE2ZTk1YmVmMjgwNzc4NmRkODczODg2N2NmOWMwMmFhYiJ9.fj51xIfQrqleRvdSJUbWcdrvsxQPUn8HpccnOmTgPDI'

    def test_show_address_normal(self):
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
        index = requests.get(url_index_address, headers=headers2)
        show = requests.get(url_show_address + str(index.json().get('data')[0]['id']), headers=headers2)

        verify_status = show.json().get('success')
        verify_message = show.json().get('message')
        verify_data = show.json().get('data')
        verify_data_id = show.json().get('data')['id']

        assert show.status_code == 200
        assert verify_status == bool(True)
        assert 'Data alamat berhasil ditemukan.' in verify_message
        assert_that(verify_data).contains_only('id', 'user_id', 'receiver', 'phone', 'address', 'kategori', 'title',
                                               'note',
                                               'created_at', 'updated_at', 'latitude', 'longitude')
        assert verify_data_id == index.json().get('data')[0]['id']

    def test_show_address_wrong_token(self):
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
        index = requests.get(url_index_address, headers=headers2)
        headers2 = {
            "Accept": "application/json",
            "Authorization": wrong_token
        }
        show = requests.get(url_show_address + str(index.json().get('data')[0]['id']), headers=headers2)

        verify_status = show.json().get('success')
        verify_message = show.json().get('message')

        assert show.status_code == 401
        assert verify_status == bool(False)
        assert 'Unauthorized' in verify_message

    def test_show_address_token_empty_value(self):
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
        index = requests.get(url_index_address, headers=headers2)
        headers2 = {
            "Accept": "application/json",
            "Authorization": ''
        }
        show = requests.get(url_show_address + str(index.json().get('data')[0]['id']), headers=headers2)

        verify_status = show.json().get('success')
        verify_message = show.json().get('message')

        assert show.status_code == 401
        assert verify_status == bool(False)
        assert 'Unauthorized' in verify_message

    def test_show_address_id_not_found(self):
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
        index = requests.get(url_index_address, headers=headers2)
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        show = requests.get(url_show_address + '6666', headers=headers3)

        verify_status = show.json().get('success')
        verify_message = show.json().get('message')

        assert show.status_code == 404
        assert verify_status == bool(False)
        assert 'Alamat tidak ditemukan' in verify_message

    def test_show_address_id_empty_value(self):
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
        index = requests.get(url_index_address, headers=headers2)
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        show = requests.get(url_show_address, headers=headers3)

        verify_status = show.json().get('success')
        verify_message = show.json().get('message')

        assert show.status_code == 200
        assert verify_status == bool(True)
        assert 'Data alamat berhasil ditemukan.' in verify_message

    def test_show_address_id_text_value(self):
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
        index = requests.get(url_index_address, headers=headers2)
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        show = requests.get(url_show_address + 'aaaa', headers=headers3)

        verify_status = show.json().get('success')
        verify_message = show.json().get('message')

        assert show.status_code == 404
        assert verify_status == bool(False)
        assert 'Alamat tidak ditemukan' in verify_message
