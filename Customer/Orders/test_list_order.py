import requests
from env import stagging
from pprint import pprint
from assertpy import assert_that


class TestCustomerOrdersListOrder:

    global setting_env,url_login,url_list_order,email,kata_sandi,wrong_token

    setting_env = stagging
    url_login = f"{setting_env}/api/v2/customer/auth/login/email"
    url_list_order = f"{setting_env}/api/v2/customer/orders"
    email = "kopiruangvirtual@gmail.com"
    kata_sandi = '12345678'
    wrong_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvc3RhZ2luZy5hZG1pbnN1cnBsdXMubmV0XC9hcGlcL3YyXC9jdXN0b21lclwvYXV0aFwvbG9naW5cL2VtYWlsIiwiaWF0IjoxNjE2ODA1NzI2LCJleHAiOjE2MTkzOTc3MjYsIm5iZiI6MTYxNjgwNTcyNiwianRpIjoib05ESmxFRE5hSzNrN2RtVyIsInN1YiI6NDEyNiwicHJ2IjoiMjc0MTA1ZGE2ZTk1YmVmMjgwNzc4NmRkODczODg2N2NmOWMwMmFhYiJ9.fj51xIfQrqleRvdSJUbWcdrvsxQPUn8HpccnOmTgPDI'

    def test_order_list_normal(self):
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
        list_order = requests.get(url_list_order, params=param2, headers=headers2)

        validate_status = list_order.json().get('success')
        validate_message = list_order.json().get('message')
        validate_data = list_order.json().get('data')[0]

        assert list_order.status_code == 200
        assert validate_status == bool(True)
        assert 'Data order berhasil ditemukan.' in validate_message
        assert_that(validate_data).contains_only('id', 'registrasi_order_number', 'alamat', 'status_order_id',
                                                 'canceled_by',
                                                 'created_at', 'keterangan', 'ulasan', 'rating', 'merchant_name',
                                                 'merchant_logo', 'order_qty', 'order_date', 'grand_total',
                                                 'metode_pembayaran_id', 'invoice_url', 'is_tomorrow', 'shipment')

    def test_order_list_wrong_token(self):
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
        list_order = requests.get(url_list_order, params=param2, headers=headers2)

        validate_status = list_order.json().get('success')
        validate_message = list_order.json().get('message')

        assert list_order.status_code == 401
        assert validate_status == bool(False)
        assert 'Unauthorized' in validate_message

    def test_order_list_token_empty_value(self):
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
        list_order = requests.get(url_list_order, params=param2, headers=headers2)

        validate_status = list_order.json().get('success')
        validate_message = list_order.json().get('message')

        assert list_order.status_code == 401
        assert validate_status == bool(False)
        assert 'Unauthorized' in validate_message

    def test_order_list_status_order_wrong_value(self):
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
            'status_order': 'doneee'
        }
        list_order = requests.get(url_list_order, params=param2, headers=headers2)

        validate_status = list_order.json().get('success')
        validate_message = list_order.json().get('message')['status_order']

        assert list_order.status_code == 422
        assert validate_status == bool(False)
        assert 'Status pesanan yang dipilih tidak tersedia.' in validate_message

    def test_order_list_status_order_empty_value(self):
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
            'status_order': ''
        }
        list_order = requests.get(url_list_order, params=param2, headers=headers2)

        validate_status = list_order.json().get('success')
        validate_message = list_order.json().get('message')['status_order']

        assert list_order.status_code == 422
        assert validate_status == bool(False)
        assert 'Status pesanan tidak boleh kosong.' in validate_message

    def test_order_list_without_param_status_order(self):
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
            # 'status_order': ''
        }
        list_order = requests.get(url_list_order, params=param2, headers=headers2)

        validate_status = list_order.json().get('success')
        validate_message = list_order.json().get('message')['status_order']

        assert list_order.status_code == 422
        assert validate_status == bool(False)
        assert 'Status pesanan tidak boleh kosong.' in validate_message

