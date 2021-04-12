import requests
from env import stagging
from pprint import pprint
from assertpy import assert_that


class TestCustomerOrdersCheckout:

    global setting_env, url_login, url_discover, url_checkout, email, kata_sandi, wrong_token

    setting_env = stagging
    url_login = f"{setting_env}/api/v2/customer/auth/login/email"
    url_discover = f"{setting_env}/api/v2/customer/discover"
    url_checkout = f"{setting_env}/api/v2/customer/orders/checkout"
    email = "kopiruangvirtual@gmail.com"
    kata_sandi = '12345678'
    wrong_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvc3RhZ2luZy5hZG1pbnN1cnBsdXMubmV0XC9hcGlcL3YyXC9jdXN0b21lclwvYXV0aFwvbG9naW5cL2VtYWlsIiwiaWF0IjoxNjE2ODA1NzI2LCJleHAiOjE2MTkzOTc3MjYsIm5iZiI6MTYxNjgwNTcyNiwianRpIjoib05ESmxFRE5hSzNrN2RtVyIsInN1YiI6NDEyNiwicHJ2IjoiMjc0MTA1ZGE2ZTk1YmVmMjgwNzc4NmRkODczODg2N2NmOWMwMmFhYiJ9.fj51xIfQrqleRvdSJUbWcdrvsxQPUn8HpccnOmTgPDI'

    def test_checkout_normal(self):
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
            'delivery_price': '20000',
            'is_lunchbox': '0',
            'donation_price': '2500',
            'voucher_id': '62',
            'order_items[0][stock_id]': discover.json().get('data')['nearby_menu'][0]['stock_id'],
            'order_items[0][qty]': '5'
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        checkout = requests.post(url_checkout, data=param3, headers=headers3)

        verify_status = checkout.json().get('success')
        verify_message = checkout.json().get('message')['menu']
        verify_data = checkout.json().get('data')
        verify_data_items = checkout.json().get('data')['order_items'][0]

        assert checkout.status_code == 200
        assert verify_status == bool(True)
        assert 'Data menu berhasil ditemukan.' in verify_message
        assert_that(verify_data).is_not_none()
        assert_that(verify_data).contains_only('errors', 'order_items', 'donation_price', 'delivery_price',
                                               'surplus_discount',
                                               'lunchbox_discount', 'voucher_discount', 'voucher_target_id',
                                               'grand_total',
                                               'subtotal', 'saving', 'merchant_fee', 'surplus_fee',
                                               'subtotal_after_discount',
                                               'pickup_time')
        assert_that(verify_data_items).contains_only('stock_id', 'merchant_id', 'name', 'total')

    def test_checkout_token_wrong(self):
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
            'delivery_price': '20000',
            'is_lunchbox': '0',
            'donation_price': '2500',
            'voucher_id': '62',
            'order_items[0][stock_id]': discover.json().get('data')['nearby_menu'][0]['stock_id'],
            'order_items[0][qty]': '5'
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": wrong_token
        }
        checkout = requests.post(url_checkout, data=param3, headers=headers3)

        verify_status = checkout.json().get('success')
        verify_message = checkout.json().get('message')

        assert checkout.status_code == 401
        assert verify_status == bool(False)
        assert 'Unauthorized' in verify_message

    def test_checkout_token_empty_value(self):
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
            'delivery_price': '20000',
            'is_lunchbox': '0',
            'donation_price': '2500',
            'voucher_id': '62',
            'order_items[0][stock_id]': discover.json().get('data')['nearby_menu'][0]['stock_id'],
            'order_items[0][qty]': '5'
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": ''
        }
        checkout = requests.post(url_checkout, data=param3, headers=headers3)

        verify_status = checkout.json().get('success')
        verify_message = checkout.json().get('message')

        assert checkout.status_code == 401
        assert verify_status == bool(False)
        assert 'Unauthorized' in verify_message

    def test_checkout_without_param_delivery_price(self):
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
            # 'delivery_price': '20000',
            'is_lunchbox': '0',
            'donation_price': '2500',
            'voucher_id': '62',
            'order_items[0][stock_id]': discover.json().get('data')['nearby_menu'][0]['stock_id'],
            'order_items[0][qty]': '5'
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        checkout = requests.post(url_checkout, data=param3, headers=headers3)

        verify_status = checkout.json().get('success')
        verify_message = checkout.json().get('message')['menu']
        verify_data = checkout.json().get('data')
        verify_data_items = checkout.json().get('data')['order_items'][0]

        assert checkout.status_code == 200
        assert verify_status == bool(True)
        assert 'Data menu berhasil ditemukan.' in verify_message
        assert_that(verify_data).is_not_none()
        assert_that(verify_data).contains_only('errors', 'order_items', 'donation_price', 'delivery_price',
                                               'surplus_discount',
                                               'lunchbox_discount', 'voucher_discount', 'voucher_target_id',
                                               'grand_total',
                                               'subtotal', 'saving', 'merchant_fee', 'surplus_fee',
                                               'subtotal_after_discount',
                                               'pickup_time')
        assert_that(verify_data_items).contains_only('stock_id', 'merchant_id', 'name', 'total')

    def test_checkout_delivery_price_empty_value(self):
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
            'delivery_price': '',
            'is_lunchbox': '0',
            'donation_price': '2500',
            'voucher_id': '62',
            'order_items[0][stock_id]': discover.json().get('data')['nearby_menu'][0]['stock_id'],
            'order_items[0][qty]': '5'
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        checkout = requests.post(url_checkout, data=param3, headers=headers3)

        verify_status = checkout.json().get('success')
        verify_message = checkout.json().get('message')['delivery_price']

        assert checkout.status_code == 422
        assert verify_status == bool(False)
        assert 'Ongkos kirim harus berupa angka.' in verify_message

    def test_checkout_delivery_price_text_value(self):
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
            'delivery_price': 'aaa',
            'is_lunchbox': '0',
            'donation_price': '2500',
            'voucher_id': '62',
            'order_items[0][stock_id]': discover.json().get('data')['nearby_menu'][0]['stock_id'],
            'order_items[0][qty]': '5'
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        checkout = requests.post(url_checkout, data=param3, headers=headers3)

        verify_status = checkout.json().get('success')
        verify_message = checkout.json().get('message')['delivery_price']

        assert checkout.status_code == 422
        assert verify_status == bool(False)
        assert 'Ongkos kirim harus berupa angka.' in verify_message

    def test_Cceckout_delivery_price_wrong_format_value(self):
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
            'delivery_price': '09:00',
            'is_lunchbox': '0',
            'donation_price': '2500',
            'voucher_id': '62',
            'order_items[0][stock_id]': discover.json().get('data')['nearby_menu'][0]['stock_id'],
            'order_items[0][qty]': '5'
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        checkout = requests.post(url_checkout, data=param3, headers=headers3)

        verify_status = checkout.json().get('success')
        verify_message = checkout.json().get('message')['delivery_price']

        assert checkout.status_code == 422
        assert verify_status == bool(False)
        assert 'Ongkos kirim harus berupa angka.' in verify_message

    def test_checkout_delivery_price_minus_value(self):
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
            'delivery_price': '-20000',
            'is_lunchbox': '0',
            'donation_price': '2500',
            'voucher_id': '62',
            'order_items[0][stock_id]': discover.json().get('data')['nearby_menu'][0]['stock_id'],
            'order_items[0][qty]': '5'
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        checkout = requests.post(url_checkout, data=param3, headers=headers3)

        verify_status = checkout.json().get('success')
        verify_message = checkout.json().get('message')['menu']
        verify_data = checkout.json().get('data')
        verify_data_items = checkout.json().get('data')['order_items'][0]

        assert checkout.status_code == 200
        assert verify_status == bool(True)
        assert 'Data menu berhasil ditemukan.' in verify_message
        assert_that(verify_data).is_not_none()
        assert_that(verify_data).contains_only('errors', 'order_items', 'donation_price', 'delivery_price',
                                               'surplus_discount',
                                               'lunchbox_discount', 'voucher_discount', 'voucher_target_id',
                                               'grand_total',
                                               'subtotal', 'saving', 'merchant_fee', 'surplus_fee',
                                               'subtotal_after_discount',
                                               'pickup_time')
        assert_that(verify_data_items).contains_only('stock_id', 'merchant_id', 'name', 'total')

    def test_checkout_without_param_launchbox(self):
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
            'delivery_price': '20000',
            # 'is_lunchbox': '0',
            'donation_price': '2500',
            'voucher_id': '62',
            'order_items[0][stock_id]': discover.json().get('data')['nearby_menu'][0]['stock_id'],
            'order_items[0][qty]': '5'
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        checkout = requests.post(url_checkout, data=param3, headers=headers3)

        verify_status = checkout.json().get('success')
        verify_message = checkout.json().get('message')['is_lunchbox']

        assert checkout.status_code == 422
        assert verify_status == bool(False)
        assert 'Kotak makan tidak boleh kosong.' in verify_message

    def test_checkout_launchbox_text_value(self):
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
            'delivery_price': '20000',
            'is_lunchbox': 'aaa',
            'donation_price': '2500',
            'voucher_id': '62',
            'order_items[0][stock_id]': discover.json().get('data')['nearby_menu'][0]['stock_id'],
            'order_items[0][qty]': '5'
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        checkout = requests.post(url_checkout, data=param3, headers=headers3)

        verify_status = checkout.json().get('success')
        verify_message = checkout.json().get('message')['is_lunchbox']

        assert checkout.status_code == 422
        assert verify_status == bool(False)
        assert 'Kotak makan harus bernilai true atau false.' in verify_message

    def test_checkout_launchbox_not_bool_value(self):
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
            'delivery_price': '20000',
            'is_lunchbox': '5',
            'donation_price': '2500',
            'voucher_id': '62',
            'order_items[0][stock_id]': discover.json().get('data')['nearby_menu'][0]['stock_id'],
            'order_items[0][qty]': '5'
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        checkout = requests.post(url_checkout, data=param3, headers=headers3)

        verify_status = checkout.json().get('success')
        verify_message = checkout.json().get('message')['is_lunchbox']

        assert checkout.status_code == 422
        assert verify_status == bool(False)
        assert 'Kotak makan harus bernilai true atau false.' in verify_message

    def test_checkout_launchbox_empty_value(self):
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
            'delivery_price': '20000',
            'is_lunchbox': '',
            'donation_price': '2500',
            'voucher_id': '62',
            'order_items[0][stock_id]': discover.json().get('data')['nearby_menu'][0]['stock_id'],
            'order_items[0][qty]': '5'
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        checkout = requests.post(url_checkout, data=param3, headers=headers3)

        verify_status = checkout.json().get('success')
        verify_message = checkout.json().get('message')['is_lunchbox']

        assert checkout.status_code == 422
        assert verify_status == bool(False)
        assert 'Kotak makan tidak boleh kosong.' in verify_message

    def test_checkout_donation_empty_value(self):
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
            'delivery_price': '20000',
            'is_lunchbox': '1',
            'donation_price': '',
            'voucher_id': '62',
            'order_items[0][stock_id]': discover.json().get('data')['nearby_menu'][0]['stock_id'],
            'order_items[0][qty]': '5'
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        checkout = requests.post(url_checkout, data=param3, headers=headers3)

        verify_status = checkout.json().get('success')
        verify_message = checkout.json().get('message')['donation_price']

        assert checkout.status_code == 422
        assert verify_status == bool(False)
        assert 'Jumlah donasi harus berupa angka.' in verify_message

    def test_checkout_without_param_donation(self):
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
            'delivery_price': '20000',
            'is_lunchbox': '0',
            # 'donation_price': '',
            'voucher_id': '62',
            'order_items[0][stock_id]': discover.json().get('data')['nearby_menu'][0]['stock_id'],
            'order_items[0][qty]': '5'
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        checkout = requests.post(url_checkout, data=param3, headers=headers3)

        verify_status = checkout.json().get('success')
        verify_message = checkout.json().get('message')['menu']
        verify_data = checkout.json().get('data')
        verify_data_items = checkout.json().get('data')['order_items'][0]

        assert checkout.status_code == 200
        assert verify_status == bool(True)
        assert 'Data menu berhasil ditemukan.' in verify_message
        assert_that(verify_data).is_not_none()
        assert_that(verify_data).contains_only('errors', 'order_items', 'donation_price', 'delivery_price',
                                               'surplus_discount',
                                               'lunchbox_discount', 'voucher_discount', 'voucher_target_id',
                                               'grand_total',
                                               'subtotal', 'saving', 'merchant_fee', 'surplus_fee',
                                               'subtotal_after_discount',
                                               'pickup_time')
        assert_that(verify_data_items).contains_only('stock_id', 'merchant_id', 'name', 'total')

    def test_checkout_donation_value_kurang_2500(self):
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
            'delivery_price': '20000',
            'is_lunchbox': '0',
            'donation_price': '100',
            'voucher_id': '62',
            'order_items[0][stock_id]': discover.json().get('data')['nearby_menu'][0]['stock_id'],
            'order_items[0][qty]': '5'
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        checkout = requests.post(url_checkout, data=param3, headers=headers3)

        verify_status = checkout.json().get('success')
        verify_message = checkout.json().get('message')['donation_price']

        assert checkout.status_code == 422
        assert verify_status == bool(False)
        assert 'Jumlah donasi harus diantara 2500 dan 30000' in verify_message

    def test_checkout_donation_text_value(self):
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
            'delivery_price': '20000',
            'is_lunchbox': '0',
            'donation_price': 'aaa',
            'voucher_id': '62',
            'order_items[0][stock_id]': discover.json().get('data')['nearby_menu'][0]['stock_id'],
            'order_items[0][qty]': '5'
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        checkout = requests.post(url_checkout, data=param3, headers=headers3)

        verify_status = checkout.json().get('success')
        verify_message = checkout.json().get('message')['donation_price']

        assert checkout.status_code == 422
        assert verify_status == bool(False)
        assert 'Jumlah donasi harus berupa angka.' in verify_message

    def test_checkout_without_param_voucher_id(self):
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
            'delivery_price': '20000',
            'is_lunchbox': '0',
            'donation_price': '2500',
            # 'voucher_id': '62',
            'order_items[0][stock_id]': discover.json().get('data')['nearby_menu'][0]['stock_id'],
            'order_items[0][qty]': '5'
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        checkout = requests.post(url_checkout, data=param3, headers=headers3)

        verify_status = checkout.json().get('success')
        verify_message = checkout.json().get('message')['menu']
        verify_data = checkout.json().get('data')
        verify_data_items = checkout.json().get('data')['order_items'][0]

        assert checkout.status_code == 200
        assert verify_status == bool(True)
        assert 'Data menu berhasil ditemukan.' in verify_message
        assert_that(verify_data).is_not_none()
        assert_that(verify_data).contains_only('errors', 'order_items', 'donation_price', 'delivery_price',
                                               'surplus_discount',
                                               'lunchbox_discount', 'voucher_discount', 'voucher_target_id',
                                               'grand_total',
                                               'subtotal', 'saving', 'merchant_fee', 'surplus_fee',
                                               'pickup_time')
        assert_that(verify_data_items).contains_only('stock_id', 'merchant_id', 'name', 'total')

    def test_checkout_voucher_id_empty_value(self):
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
            'delivery_price': '20000',
            'is_lunchbox': '0',
            'donation_price': '2500',
            'voucher_id': '',
            'order_items[0][stock_id]': discover.json().get('data')['nearby_menu'][0]['stock_id'],
            'order_items[0][qty]': '5'
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        checkout = requests.post(url_checkout, data=param3, headers=headers3)

        verify_status = checkout.json().get('success')
        verify_message = checkout.json().get('message')['voucher_id']

        assert checkout.status_code == 422
        assert verify_status == bool(False)
        assert 'Voucher harus berupa angka.' in verify_message

    def test_checkout_voucher_id_text_value(self):
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
            'delivery_price': '20000',
            'is_lunchbox': '0',
            'donation_price': '2500',
            'voucher_id': 'aaa',
            'order_items[0][stock_id]': discover.json().get('data')['nearby_menu'][0]['stock_id'],
            'order_items[0][qty]': '5'
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        checkout = requests.post(url_checkout, data=param3, headers=headers3)

        verify_status = checkout.json().get('success')
        verify_message = checkout.json().get('message')['voucher_id']

        assert checkout.status_code == 422
        assert verify_status == bool(False)
        assert 'Voucher harus berupa angka.' in verify_message

    def test_checkout_voucher_id_not_found(self):
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
            'delivery_price': '20000',
            'is_lunchbox': '0',
            'donation_price': '2500',
            'voucher_id': '6666666',
            'order_items[0][stock_id]': discover.json().get('data')['nearby_menu'][0]['stock_id'],
            'order_items[0][qty]': '5'
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        checkout = requests.post(url_checkout, data=param3, headers=headers3)

        verify_status = checkout.json().get('success')
        verify_message = checkout.json().get('message')['menu']
        verify_data = checkout.json().get('data')
        verify_data_items = checkout.json().get('data')['order_items'][0]

        assert checkout.status_code == 200
        assert verify_status == bool(True)
        assert 'Data menu berhasil ditemukan.' in verify_message
        assert_that(verify_data).is_not_none()
        assert_that(verify_data).contains_only('errors', 'order_items', 'donation_price', 'delivery_price',
                                               'surplus_discount',
                                               'lunchbox_discount', 'voucher_discount', 'voucher_target_id',
                                               'grand_total',
                                               'subtotal', 'saving', 'merchant_fee', 'surplus_fee',
                                               'pickup_time')
        assert_that(verify_data_items).contains_only('stock_id', 'merchant_id', 'name', 'total')

    def test_checkout_qty_item_empty_value(self):
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
            'delivery_price': '20000',
            'is_lunchbox': '0',
            'donation_price': '2500',
            'voucher_id': '62',
            'order_items[0][stock_id]': discover.json().get('data')['nearby_menu'][0]['stock_id'],
            'order_items[0][qty]': ''
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        checkout = requests.post(url_checkout, data=param3, headers=headers3)

        verify_status = checkout.json().get('success')
        verify_message = checkout.json().get('message')['order_items.0.qty']

        assert checkout.status_code == 422
        assert verify_status == bool(False)
        assert 'order_items.0.qty tidak boleh kosong.' in verify_message

    def test_checkout_without_param_qty_id(self):
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
            'delivery_price': '20000',
            'is_lunchbox': '0',
            'donation_price': '2500',
            'voucher_id': '62',
            'order_items[0][stock_id]': discover.json().get('data')['nearby_menu'][0]['stock_id'],
            # 'order_items[0][qty]': ''
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        checkout = requests.post(url_checkout, data=param3, headers=headers3)

        verify_status = checkout.json().get('success')
        verify_message = checkout.json().get('message')['order_items.0.qty']

        assert checkout.status_code == 422
        assert verify_status == bool(False)
        assert 'order_items.0.qty tidak boleh kosong.' in verify_message

    def test_checkout_qty_id_text_value(self):
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
            'delivery_price': '20000',
            'is_lunchbox': '0',
            'donation_price': '2500',
            'voucher_id': '62',
            'order_items[0][stock_id]': discover.json().get('data')['nearby_menu'][0]['stock_id'],
            'order_items[0][qty]': 'aaa'
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        checkout = requests.post(url_checkout, data=param3, headers=headers3)

        verify_status = checkout.json().get('success')
        verify_message = checkout.json().get('message')['order_items.0.qty']

        assert checkout.status_code == 422
        assert verify_status == bool(False)
        assert "order_items.0.qty harus berupa angka." in verify_message

    def test_checkout_qty_value_kurang_Stock(self):
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
            'delivery_price': '20000',
            'is_lunchbox': '0',
            'donation_price': '2500',
            'voucher_id': '62',
            'order_items[0][stock_id]': discover.json().get('data')['nearby_menu'][0]['stock_id'],
            'order_items[0][qty]': '999'
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        checkout = requests.post(url_checkout, data=param3, headers=headers3)

        verify_status = checkout.json().get('success')
        verify_message = checkout.json().get('message')['menu'][0]['message']
        verify_data = checkout.json().get('data')
        verify_data_items = checkout.json().get('data')['order_items'][0]

        assert checkout.status_code == 200
        assert verify_status == bool(True)
        assert 'tidak tersedia' in verify_message
        assert_that(verify_data).is_not_none()
        assert_that(verify_data).contains_only('errors', 'order_items', 'donation_price', 'delivery_price',
                                               'surplus_discount',
                                               'lunchbox_discount', 'voucher_discount', 'voucher_target_id',
                                               'grand_total',
                                               'subtotal', 'saving', 'merchant_fee', 'surplus_fee',
                                               'subtotal_after_discount',
                                               'pickup_time')
        assert_that(verify_data_items).contains_only('stock_id', 'merchant_id', 'name', 'total')

    def test_checkout_stock_id_empty_value(self):
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
            'delivery_price': '20000',
            'is_lunchbox': '0',
            'donation_price': '2500',
            'voucher_id': '62',
            'order_items[0][stock_id]': '',
            'order_items[0][qty]': '1'
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        checkout = requests.post(url_checkout, data=param3, headers=headers3)

        verify_status = checkout.json().get('success')
        verify_message = checkout.json().get('message')['order_items.0.stock_id'][0]

        assert checkout.status_code == 422
        assert verify_status == bool(False)
        assert 'order_items.0.stock_id tidak boleh kosong.' in verify_message

    def test_checkout_without_param_stock_id(self):
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
            'delivery_price': '20000',
            'is_lunchbox': '0',
            'donation_price': '2500',
            'voucher_id': '62',
            # 'order_items[0][stock_id]': '',
            'order_items[0][qty]': '1'
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        checkout = requests.post(url_checkout, data=param3, headers=headers3)

        verify_status = checkout.json().get('success')
        verify_message = checkout.json().get('message')['order_items.0.stock_id'][0]

        assert checkout.status_code == 422
        assert verify_status == bool(False)
        assert 'order_items.0.stock_id tidak boleh kosong.' in verify_message

    def test_checkout_stock_id_text_value(self):
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
            'delivery_price': '20000',
            'is_lunchbox': '0',
            'donation_price': '2500',
            'voucher_id': '62',
            'order_items[0][stock_id]': 'aaa',
            'order_items[0][qty]': '1'
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        checkout = requests.post(url_checkout, data=param3, headers=headers3)

        verify_status = checkout.json().get('success')
        verify_message = checkout.json().get('message')['order_items.0.stock_id'][0]

        assert checkout.status_code == 422
        assert verify_status == bool(False)
        assert 'order_items.0.stock_id harus berupa angka.' in verify_message

    def test_checkout_stock_id_not_found(self):
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
            'delivery_price': '20000',
            'is_lunchbox': '0',
            'donation_price': '2500',
            'voucher_id': '62',
            'order_items[0][stock_id]': '666666',
            'order_items[0][qty]': '1'
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        checkout = requests.post(url_checkout, data=param3, headers=headers3)

        verify_status = checkout.json().get('success')
        verify_message = checkout.json().get('message')

        assert checkout.status_code == 500
        assert verify_status == bool(False)
        assert 'Aduh! ' in verify_message