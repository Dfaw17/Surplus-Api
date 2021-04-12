import requests
from env import stagging
from pprint import pprint
from assertpy import assert_that

class TestCustomerDeleteAddress:

    global setting_env, url_login, url_index_address, url_delete_address, email, kata_sandi, wrong_token

    setting_env = stagging
    url_login = f"{setting_env}/api/v2/customer/auth/login/email"
    url_index_address = f"{setting_env}/api/v2/customer/address/"
    url_delete_address = f"{setting_env}/api/v2/customer/address/"
    email = "kopiruangvirtual@gmail.com"
    kata_sandi = '12345678'
    wrong_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvc3RhZ2luZy5hZG1pbnN1cnBsdXMubmV0XC9hcGlcL3YyXC9jdXN0b21lclwvYXV0aFwvbG9naW5cL2VtYWlsIiwiaWF0IjoxNjE2ODA1NzI2LCJleHAiOjE2MTkzOTc3MjYsIm5iZiI6MTYxNjgwNTcyNiwianRpIjoib05ESmxFRE5hSzNrN2RtVyIsInN1YiI6NDEyNiwicHJ2IjoiMjc0MTA1ZGE2ZTk1YmVmMjgwNzc4NmRkODczODg2N2NmOWMwMmFhYiJ9.fj51xIfQrqleRvdSJUbWcdrvsxQPUn8HpccnOmTgPDI'

    def test_delete_address_normal(self):
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
        delete = requests.delete(url_index_address + str(index.json().get('data')[0]['id']), headers=headers2)

        validate_status = delete.json().get('success')
        validate_message = delete.json().get('message')

        assert delete.status_code == 200
        assert validate_status == bool(True)
        assert 'Data alamat berhasil dihapus' in validate_message

    def test_delete_wrong_token(self):
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
            "Authorization": wrong_token
        }
        delete = requests.delete(url_index_address + str(index.json().get('data')[0]['id']), headers=headers3)

        validate_status = delete.json().get('success')
        validate_message = delete.json().get('message')

        assert delete.status_code == 401
        assert validate_status == bool(False)
        assert 'Unauthorized' in validate_message

    def test_delete_address_token_empty_value(self):
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
            "Authorization": ''
        }
        delete = requests.delete(url_index_address + str(index.json().get('data')[0]['id']), headers=headers3)

        validate_status = delete.json().get('success')
        validate_message = delete.json().get('message')

        assert delete.status_code == 401
        assert validate_status == bool(False)
        assert 'Unauthorized' in validate_message

    def test_delete_address_id_empty_value(self):
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
        delete = requests.delete(url_index_address, headers=headers3)

        validate_status = delete.json().get('success')
        validate_message = delete.json().get('message')

        assert delete.status_code == 405
        assert validate_status == bool(False)
        assert 'Method Not Allowed' in validate_message

    def test_delete_address_id_text_value(self):
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
        delete = requests.delete(url_index_address+'aaaa', headers=headers3)

        validate_status = delete.json().get('success')
        validate_message = delete.json().get('message')

        assert delete.status_code == 404
        assert validate_status == bool(False)
        assert 'Alamat tidak ditemukan' in validate_message

    def test_delete_address_id_not_found(self):
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
        delete = requests.delete(url_index_address+'6666', headers=headers3)

        validate_status = delete.json().get('success')
        validate_message = delete.json().get('message')

        assert delete.status_code == 404
        assert validate_status == bool(False)
        assert 'Alamat tidak ditemukan' in validate_message
