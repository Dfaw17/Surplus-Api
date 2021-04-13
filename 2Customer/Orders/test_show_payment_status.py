import requests
from env import stagging
from pprint import pprint
from assertpy import assert_that


class TestCustomerOrdersShowPaymentStatus:
    global setting_env, url_login, url_list_order, url_detail_order, url_show_payment_status, email, kata_sandi, wrong_token

    setting_env = stagging
    url_login = f"{setting_env}/api/v2/customer/auth/login/email"
    url_list_order = f"{setting_env}/api/v2/customer/orders"
    url_detail_order = f"{setting_env}/api/v2/customer/orders/"
    url_show_payment_status = f"{setting_env}/api/v2/customer/orders/"
    email = "kopiruangvirtual@gmail.com"
    kata_sandi = '12345678'
    wrong_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvc3RhZ2luZy5hZG1pbnN1cnBsdXMubmV0XC9hcGlcL3YyXC9jdXN0b21lclwvYXV0aFwvbG9naW5cL2VtYWlsIiwiaWF0IjoxNjE2ODA1NzI2LCJleHAiOjE2MTkzOTc3MjYsIm5iZiI6MTYxNjgwNTcyNiwianRpIjoib05ESmxFRE5hSzNrN2RtVyIsInN1YiI6NDEyNiwicHJ2IjoiMjc0MTA1ZGE2ZTk1YmVmMjgwNzc4NmRkODczODg2N2NmOWMwMmFhYiJ9.fj51xIfQrqleRvdSJUbWcdrvsxQPUn8HpccnOmTgPDI'

    def test_show_payement_status_normal(self):
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
        detail_order = requests.get(url_detail_order + list_order.json().get('data')[0]['registrasi_order_number'],
                                    headers=headers2)
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        param3 = {
            'payment_method': detail_order.json().get('data')['metode_pembayaran']
        }
        show_payment = requests.get(
            url_show_payment_status + list_order.json().get('data')[0]['registrasi_order_number'] + '/payment-status',
            params=param3, headers=headers3)

        validate_status = show_payment.json().get('success')
        validate_message = show_payment.json().get('message')

        assert show_payment.status_code == 200
        assert validate_status == bool(True)
        assert 'Status pembayaran berhasil ditemukan' in validate_message

    def test_show_payment_status_wrong_token(self):
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
        detail_order = requests.get(url_detail_order + list_order.json().get('data')[0]['registrasi_order_number'],
                                    headers=headers2)
        headers3 = {
            "Accept": "application/json",
            "Authorization": wrong_token
        }
        param3 = {
            'payment_method': detail_order.json().get('data')['metode_pembayaran']
        }
        show_payment = requests.get(
            url_show_payment_status + list_order.json().get('data')[0]['registrasi_order_number'] + '/payment-status',
            params=param3, headers=headers3)

        validate_status = show_payment.json().get('success')
        validate_message = show_payment.json().get('message')

        assert show_payment.status_code == 401
        assert validate_status == bool(False)
        assert 'Unauthorized' in validate_message

    def test_show_payment_status_token_empty_value(self):
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
        detail_order = requests.get(url_detail_order + list_order.json().get('data')[0]['registrasi_order_number'],
                                    headers=headers2)
        headers3 = {
            "Accept": "application/json",
            "Authorization": ''
        }
        param3 = {
            'payment_method': detail_order.json().get('data')['metode_pembayaran']
        }
        show_payment = requests.get(
            url_show_payment_status + list_order.json().get('data')[0]['registrasi_order_number'] + '/payment-status',
            params=param3, headers=headers3)

        validate_status = show_payment.json().get('success')
        validate_message = show_payment.json().get('message')

        assert show_payment.status_code == 401
        assert validate_status == bool(False)
        assert 'Unauthorized' in validate_message

    def test_show_payment_status_id_trx_not_found(self):
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
        detail_order = requests.get(url_detail_order + list_order.json().get('data')[0]['registrasi_order_number'],
                                    headers=headers2)
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        param3 = {
            'payment_method': detail_order.json().get('data')['metode_pembayaran']
        }
        show_payment = requests.get(url_show_payment_status + 'S12345678987654321' + '/payment-status', params=param3,
                                    headers=headers3)

        validate_status = show_payment.json().get('success')
        validate_message = show_payment.json().get('message')
        validate_data = show_payment.json().get('data')

        assert show_payment.status_code == 200
        assert validate_status == bool(True)
        assert 'Status pembayaran berhasil ditemukan' in validate_message
        assert 'Payment not found' in validate_data

    def test_show_payment_status_id_trx_empty_value(self):
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
        detail_order = requests.get(url_detail_order + list_order.json().get('data')[0]['registrasi_order_number'],
                                    headers=headers2)
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        param3 = {
            'payment_method': detail_order.json().get('data')['metode_pembayaran']
        }
        show_payment = requests.get(url_show_payment_status + 'payment-status', params=param3, headers=headers3)

        validate_status = show_payment.json().get('success')
        validate_message = show_payment.json().get('message')

        assert show_payment.status_code == 404
        assert validate_status == bool(False)
        assert 'Data pesanan tidak ditemukan' in validate_message

    def test_show_payment_status_id_trx_wrong_format(self):
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
        detail_order = requests.get(url_detail_order + list_order.json().get('data')[0]['registrasi_order_number'],
                                    headers=headers2)
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        param3 = {
            'payment_method': detail_order.json().get('data')['metode_pembayaran']
        }
        show_payment = requests.get(url_show_payment_status + '081386356616' + '/payment-status', params=param3,
                                    headers=headers3)

        validate_status = show_payment.json().get('success')
        validate_message = show_payment.json().get('message')
        validate_data = show_payment.json().get('data')

        assert show_payment.status_code == 200
        assert validate_status == bool(True)
        assert 'Status pembayaran berhasil ditemukan' in validate_message
        assert 'Payment not found' in validate_data

    def test_show_payment_status_without_param_payment_methode(self):
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
        detail_order = requests.get(url_detail_order + list_order.json().get('data')[0]['registrasi_order_number'],
                                    headers=headers2)
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        param3 = {
            # 'payment_method': detail_order.json().get('data')['metode_pembayaran']
        }
        show_payment = requests.get(url_show_payment_status + 'S2104080334264' + '/payment-status', params=param3,
                                    headers=headers3)

        validate_status = show_payment.json().get('success')
        validate_message = show_payment.json().get('message')['payment_method']

        assert show_payment.status_code == 422
        assert validate_status == bool(False)
        assert 'Metode Pembayaran tidak boleh kosong.' in validate_message

    def test_show_payment_status_payment_methode_empty(self):
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
        detail_order = requests.get(url_detail_order + list_order.json().get('data')[0]['registrasi_order_number'],
                                    headers=headers2)
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        param3 = {
            'payment_method': ''
        }
        show_payment = requests.get(url_show_payment_status + 'S2104080334264' + '/payment-status', params=param3,
                                    headers=headers3)

        validate_status = show_payment.json().get('success')
        validate_message = show_payment.json().get('message')['payment_method']

        assert show_payment.status_code == 422
        assert validate_status == bool(False)
        assert 'Metode Pembayaran tidak boleh kosong.' in validate_message

    def test_show_payment_status_payment_methode_wrong_value(self):
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
        detail_order = requests.get(url_detail_order + list_order.json().get('data')[0]['registrasi_order_number'],
                                    headers=headers2)
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        param3 = {
            'payment_method': 'OVOO'
        }
        show_payment = requests.get(url_show_payment_status + 'S2104080334264' + '/payment-status', params=param3,
                                    headers=headers3)

        validate_status = show_payment.json().get('success')
        validate_message = show_payment.json().get('message')['payment_method']

        assert show_payment.status_code == 422
        assert validate_status == bool(False)
        assert 'Metode Pembayaran yang dipilih tidak tersedia.' in validate_message

