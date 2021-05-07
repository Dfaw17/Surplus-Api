import requests
from env import stagging
from pprint import pprint
from assertpy import assert_that


class TestCustomerOrdersDetailOrder:

    global setting_env,url_login,url_list_order,url_detail_order,email,kata_sandi,wrong_token

    setting_env = stagging
    url_login = f"{setting_env}/api/v2/customer/auth/login/email"
    url_list_order = f"{setting_env}/api/v2/customer/orders"
    url_detail_order = f"{setting_env}/api/v2/customer/orders/"
    email = "kopiruangvirtual@gmail.com"
    kata_sandi = '12345678'
    wrong_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvc3RhZ2luZy5hZG1pbnN1cnBsdXMubmV0XC9hcGlcL3YyXC9jdXN0b21lclwvYXV0aFwvbG9naW5cL2VtYWlsIiwiaWF0IjoxNjE2ODA1NzI2LCJleHAiOjE2MTkzOTc3MjYsIm5iZiI6MTYxNjgwNTcyNiwianRpIjoib05ESmxFRE5hSzNrN2RtVyIsInN1YiI6NDEyNiwicHJ2IjoiMjc0MTA1ZGE2ZTk1YmVmMjgwNzc4NmRkODczODg2N2NmOWMwMmFhYiJ9.fj51xIfQrqleRvdSJUbWcdrvsxQPUn8HpccnOmTgPDI'

    def test_order_detail_normal(self):
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
            'status_order': 'done'
        }
        detail_order = requests.get(url_detail_order + 'S210406121863', headers=headers2)

        validate_status = detail_order.json().get('success')
        validate_message = detail_order.json().get('message')
        validate_data = detail_order.json().get('data')

        assert detail_order.status_code == 200
        assert validate_status == bool(True)
        assert 'berhasil ditemukan.' in validate_message
        assert_that(validate_data).is_not_none()
        assert validate_data['registrasi_order_number'] == 'S210406121863'


    def test_order_detail_token_empty_value(self):
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
            'status_order': 'done'
        }
        detail_order = requests.get(url_detail_order + 'S210406121863', headers=headers2)

        validate_status = detail_order.json().get('success')
        validate_message = detail_order.json().get('message')

        assert detail_order.status_code == 401
        assert validate_status == bool(False)
        assert 'Unauthorized' in validate_message

    def test_order_detail_token_wrong_value(self):
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
            'status_order': 'done'
        }
        detail_order = requests.get(url_detail_order + 'S210406121863', headers=headers2)

        validate_status = detail_order.json().get('success')
        validate_message = detail_order.json().get('message')

        assert detail_order.status_code == 401
        assert validate_status == bool(False)
        assert 'Unauthorized' in validate_message

    def test_order_detail_id_transaksi_wrong_format_value(self):
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
            'status_order': 'done'
        }
        detail_order = requests.get(url_detail_order + '081386356616', headers=headers2)

        validate_status = detail_order.json().get('success')
        validate_message = detail_order.json().get('message')

        assert detail_order.status_code == 404
        assert validate_status == bool(False)
        assert 'Data pesanan tidak ditemukan' in validate_message

    def test_order_detail_id_transaksi_not_found(self):
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
            'status_order': 'done'
        }
        detail_order = requests.get(url_detail_order + 'S666666667777', headers=headers2)

        validate_status = detail_order.json().get('success')
        validate_message = detail_order.json().get('message')

        assert detail_order.status_code == 404
        assert validate_status == bool(False)
        assert 'Data pesanan tidak ditemukan' in validate_message

    def test_order_detail_id_transaksi_empty_value(self):
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
            'status_order': 'done'
        }
        detail_order = requests.get(url_detail_order, headers=headers2)

        validate_status = detail_order.json().get('success')
        validate_message = detail_order.json().get('message')['status_order']

        assert detail_order.status_code == 422
        assert validate_status == bool(False)
        assert 'Status pesanan tidak boleh kosong.' in validate_message
