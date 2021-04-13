import requests
from env import stagging
from pprint import pprint
from assertpy import assert_that


class TestCustomerOrdersSelfPickup:

    global setting_env,url_login,url_discover,url_self_pickup,email,kata_sandi,wrong_token

    setting_env = stagging
    url_login = f"{setting_env}/api/v2/customer/auth/login/email"
    url_discover = f"{setting_env}/api/v2/customer/discover"
    url_self_pickup = f"{setting_env}/api/v2/customer/orders/self-pickup"
    email = "kopiruangvirtual@gmail.com"
    kata_sandi = '12345678'
    wrong_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvc3RhZ2luZy5hZG1pbnN1cnBsdXMubmV0XC9hcGlcL3YyXC9jdXN0b21lclwvYXV0aFwvbG9naW5cL2VtYWlsIiwiaWF0IjoxNjE2ODA1NzI2LCJleHAiOjE2MTkzOTc3MjYsIm5iZiI6MTYxNjgwNTcyNiwianRpIjoib05ESmxFRE5hSzNrN2RtVyIsInN1YiI6NDEyNiwicHJ2IjoiMjc0MTA1ZGE2ZTk1YmVmMjgwNzc4NmRkODczODg2N2NmOWMwMmFhYiJ9.fj51xIfQrqleRvdSJUbWcdrvsxQPUn8HpccnOmTgPDI'

    def test_sp_normal(self):
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
            'payment_method_id': '1',
            'phone_number': '081386356616',
            'is_lunchbox': '0',
            'donation_price': '2500',
            'voucher_id': '62',
            'order_items[0][stock_id]': discover.json().get('data')['nearby_menu'][0]['stock_id'],
            'order_items[0][qty]': '1',
            'order_items[0][note]': 'Note Menu',
            'address': 'Megaregency',
            'note': 'Note QA'
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        self_pickup = requests.post(url_self_pickup, data=param3, headers=headers3)

        validate_status = self_pickup.json().get('success')
        validate_message = self_pickup.json().get('message')
        validate_data = self_pickup.json().get('data')
        validate_data_transaksi = self_pickup.json().get('data')['transaksi']

        assert self_pickup.status_code == 201
        assert validate_status == bool(True)
        assert 'Order Self Pickup berhasil dibuat' in validate_message
        assert_that(validate_data).is_not_none()
        assert_that(validate_data_transaksi).is_not_none()
        assert_that(validate_data).contains_only('id', 'registrasi_order_number', 'alamat', 'status_order_id',
                                                 'canceled_by',
                                                 'created_at', 'keterangan', 'ulasan', 'rating', 'transaksi')
        assert_that(validate_data_transaksi).contains_only('id', 'metode_pembayaran_id', 'order_id', 'invoice_id',
                                                           'invoice_url', 'invoice_expired', 'phone_number', 'subtotal',
                                                           'grand_total', 'grand_total_harga_asli', 'potongan_surplus',
                                                           'potongan_voucher', 'potongan_kotak_makan', 'hemat',
                                                           'komisi_merchant', 'komisi_surplus', 'kode', 'jenis_kode',
                                                           'is_tempat_makanan', 'image_lunchbox', 'is_dikirim',
                                                           'status_transaksi_id', 'status_pickup_id', 'step_progress',
                                                           'pickup_by_system', 'created_at', 'updated_at', 'voucher_id',
                                                           'shipment_price')

    def test_sp_wrong_token(self):
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
            'payment_method_id': '1',
            'phone_number': '081386356616',
            'is_lunchbox': '0',
            'donation_price': '2500',
            'voucher_id': '62',
            'order_items[0][stock_id]': discover.json().get('data')['nearby_menu'][0]['stock_id'],
            'order_items[0][qty]': '1',
            'order_items[0][note]': 'Note Menu',
            'address': 'Megaregency',
            'note': 'Note QA'
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": wrong_token
        }
        self_pickup = requests.post(url_self_pickup, data=param3, headers=headers3)

        validate_status = self_pickup.json().get('success')
        validate_message = self_pickup.json().get('message')

        assert self_pickup.status_code == 401
        assert validate_status == bool(False)
        assert 'Unauthorized' in validate_message

    def test_sp_token_empty_value(self):
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
            'payment_method_id': '1',
            'phone_number': '081386356616',
            'is_lunchbox': '0',
            'donation_price': '2500',
            'voucher_id': '62',
            'order_items[0][stock_id]': discover.json().get('data')['nearby_menu'][0]['stock_id'],
            'order_items[0][qty]': '1',
            'order_items[0][note]': 'Note Menu',
            'address': 'Megaregency',
            'note': 'Note QA'
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": ''
        }
        self_pickup = requests.post(url_self_pickup, data=param3, headers=headers3)

        validate_status = self_pickup.json().get('success')
        validate_message = self_pickup.json().get('message')

        assert self_pickup.status_code == 401
        assert validate_status == bool(False)
        assert 'Unauthorized' in validate_message

    def test_sp_payment_methode_empty_value(self):
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
            'payment_method_id': '',
            'phone_number': '081386356616',
            'is_lunchbox': '0',
            'donation_price': '2500',
            'voucher_id': '62',
            'order_items[0][stock_id]': discover.json().get('data')['nearby_menu'][0]['stock_id'],
            'order_items[0][qty]': '1',
            'order_items[0][note]': 'Note Menu',
            'address': 'Megaregency',
            'note': 'Note QA'
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        self_pickup = requests.post(url_self_pickup, data=param3, headers=headers3)

        validate_status = self_pickup.json().get('success')
        validate_message = self_pickup.json().get('message')['payment_method_id']

        assert self_pickup.status_code == 422
        assert validate_status == bool(False)
        assert 'Metode Pembayaran tidak boleh kosong.' in validate_message

    def test_sp_without_param_payment_methode(self):
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
            # 'payment_method_id': '',
            'phone_number': '081386356616',
            'is_lunchbox': '0',
            'donation_price': '2500',
            'voucher_id': '62',
            'order_items[0][stock_id]': discover.json().get('data')['nearby_menu'][0]['stock_id'],
            'order_items[0][qty]': '1',
            'order_items[0][note]': 'Note Menu',
            'address': 'Megaregency',
            'note': 'Note QA'
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        self_pickup = requests.post(url_self_pickup, data=param3, headers=headers3)

        validate_status = self_pickup.json().get('success')
        validate_message = self_pickup.json().get('message')['payment_method_id']

        assert self_pickup.status_code == 422
        assert validate_status == bool(False)
        assert 'Metode Pembayaran tidak boleh kosong.' in validate_message

    def test_sp_payment_methode_wrong_value(self):
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
            'payment_method_id': '66',
            'phone_number': '081386356616',
            'is_lunchbox': '0',
            'donation_price': '2500',
            'voucher_id': '62',
            'order_items[0][stock_id]': discover.json().get('data')['nearby_menu'][0]['stock_id'],
            'order_items[0][qty]': '1',
            'order_items[0][note]': 'Note Menu',
            'address': 'Megaregency',
            'note': 'Note QA'
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        self_pickup = requests.post(url_self_pickup, data=param3, headers=headers3)

        validate_status = self_pickup.json().get('success')
        validate_message = self_pickup.json().get('message')['payment_method_id']

        assert self_pickup.status_code == 422
        assert validate_status == bool(False)
        assert 'Metode Pembayaran yang dipilih tidak tersedia.' in validate_message

    def test_sp_payment_methode_text_value(self):
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
            'payment_method_id': 'aaa',
            'phone_number': '081386356616',
            'is_lunchbox': '0',
            'donation_price': '2500',
            'voucher_id': '62',
            'order_items[0][stock_id]': discover.json().get('data')['nearby_menu'][0]['stock_id'],
            'order_items[0][qty]': '1',
            'order_items[0][note]': 'Note Menu',
            'address': 'Megaregency',
            'note': 'Note QA'
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        self_pickup = requests.post(url_self_pickup, data=param3, headers=headers3)

        validate_status = self_pickup.json().get('success')
        validate_message = self_pickup.json().get('message')['payment_method_id']

        assert self_pickup.status_code == 422
        assert validate_status == bool(False)
        assert 'Metode Pembayaran yang dipilih tidak tersedia.' in validate_message

    def test_sp_phone_empty_value(self):
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
            'payment_method_id': '1',
            'phone_number': '',
            'is_lunchbox': '0',
            'donation_price': '2500',
            'voucher_id': '62',
            'order_items[0][stock_id]': discover.json().get('data')['nearby_menu'][0]['stock_id'],
            'order_items[0][qty]': '1',
            'order_items[0][note]': 'Note Menu',
            'address': 'Megaregency',
            'note': 'Note QA'
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        self_pickup = requests.post(url_self_pickup, data=param3, headers=headers3)

        validate_status = self_pickup.json().get('success')
        validate_message = self_pickup.json().get('message')['phone_number']

        assert self_pickup.status_code == 422
        assert validate_status == bool(False)
        assert 'No. HP tidak boleh kosong ketika Metode Pembayaran adalah 1.' in validate_message

    def test_sp_without_param_phone(self):
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
            'payment_method_id': '1',
            'phone_number': '',
            'is_lunchbox': '0',
            'donation_price': '2500',
            'voucher_id': '62',
            'order_items[0][stock_id]': discover.json().get('data')['nearby_menu'][0]['stock_id'],
            'order_items[0][qty]': '1',
            'order_items[0][note]': 'Note Menu',
            'address': 'Megaregency',
            'note': 'Note QA'
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        self_pickup = requests.post(url_self_pickup, data=param3, headers=headers3)

        validate_status = self_pickup.json().get('success')
        validate_message = self_pickup.json().get('message')['phone_number']

        assert self_pickup.status_code == 422
        assert validate_status == bool(False)
        assert 'No. HP tidak boleh kosong ketika Metode Pembayaran adalah 1.' in validate_message

    def test_sp_phone_text_value(self):
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
            'payment_method_id': '1',
            'phone_number': 'aaaaa',
            'is_lunchbox': '0',
            'donation_price': '2500',
            'voucher_id': '62',
            'order_items[0][stock_id]': discover.json().get('data')['nearby_menu'][0]['stock_id'],
            'order_items[0][qty]': '1',
            'order_items[0][note]': 'Note Menu',
            'address': 'Megaregency',
            'note': 'Note QA'
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        self_pickup = requests.post(url_self_pickup, data=param3, headers=headers3)

        validate_status = self_pickup.json().get('success')
        validate_message = self_pickup.json().get('message')

        assert self_pickup.status_code == 404
        assert validate_status == bool(False)
        assert 'Undefined index: message' in validate_message

    def test_sp_phone_wrong_format_value(self):
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
            'payment_method_id': '1',
            'phone_number': '09:00',
            'is_lunchbox': '0',
            'donation_price': '2500',
            'voucher_id': '62',
            'order_items[0][stock_id]': discover.json().get('data')['nearby_menu'][0]['stock_id'],
            'order_items[0][qty]': '1',
            'order_items[0][note]': 'Note Menu',
            'address': 'Megaregency',
            'note': 'Note QA'
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        self_pickup = requests.post(url_self_pickup, data=param3, headers=headers3)

        validate_status = self_pickup.json().get('success')
        validate_message = self_pickup.json().get('message')

        assert self_pickup.status_code == 404
        assert validate_status == bool(False)
        assert 'Undefined index: message' in validate_message

    def test_sp_lunchbox_empty_value(self):
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
            'payment_method_id': '1',
            'phone_number': '081386356616',
            'is_lunchbox': '',
            'donation_price': '2500',
            'voucher_id': '62',
            'order_items[0][stock_id]': discover.json().get('data')['nearby_menu'][0]['stock_id'],
            'order_items[0][qty]': '1',
            'order_items[0][note]': 'Note Menu',
            'address': 'Megaregency',
            'note': 'Note QA'
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        self_pickup = requests.post(url_self_pickup, data=param3, headers=headers3)

        validate_status = self_pickup.json().get('success')
        validate_message = self_pickup.json().get('message')['is_lunchbox']

        assert self_pickup.status_code == 422
        assert validate_status == bool(False)
        assert 'Kotak makan tidak boleh kosong.' in validate_message

    def test_sp_without_param_lunchbox(self):
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
            'payment_method_id': '1',
            'phone_number': '081386356616',
            # 'is_lunchbox': '',
            'donation_price': '2500',
            'voucher_id': '62',
            'order_items[0][stock_id]': discover.json().get('data')['nearby_menu'][0]['stock_id'],
            'order_items[0][qty]': '1',
            'order_items[0][note]': 'Note Menu',
            'address': 'Megaregency',
            'note': 'Note QA'
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        self_pickup = requests.post(url_self_pickup, data=param3, headers=headers3)

        validate_status = self_pickup.json().get('success')
        validate_message = self_pickup.json().get('message')['is_lunchbox']

        assert self_pickup.status_code == 422
        assert validate_status == bool(False)
        assert 'Kotak makan tidak boleh kosong.' in validate_message

    def test_sp_lunchbox_text_value(self):
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
            'payment_method_id': '1',
            'phone_number': '081386356616',
            'is_lunchbox': 'aaa',
            'donation_price': '2500',
            'voucher_id': '62',
            'order_items[0][stock_id]': discover.json().get('data')['nearby_menu'][0]['stock_id'],
            'order_items[0][qty]': '1',
            'order_items[0][note]': 'Note Menu',
            'address': 'Megaregency',
            'note': 'Note QA'
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        self_pickup = requests.post(url_self_pickup, data=param3, headers=headers3)

        validate_status = self_pickup.json().get('success')
        validate_message = self_pickup.json().get('message')['is_lunchbox']

        assert self_pickup.status_code == 422
        assert validate_status == bool(False)
        assert 'Kotak makan harus bernilai true atau false.' in validate_message

    def test_sp_lunchbox_not_bool_value(self):
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
            'payment_method_id': '1',
            'phone_number': '081386356616',
            'is_lunchbox': '10',
            'donation_price': '2500',
            'voucher_id': '62',
            'order_items[0][stock_id]': discover.json().get('data')['nearby_menu'][0]['stock_id'],
            'order_items[0][qty]': '1',
            'order_items[0][note]': 'Note Menu',
            'address': 'Megaregency',
            'note': 'Note QA'
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        self_pickup = requests.post(url_self_pickup, data=param3, headers=headers3)

        validate_status = self_pickup.json().get('success')
        validate_message = self_pickup.json().get('message')['is_lunchbox']

        assert self_pickup.status_code == 422
        assert validate_status == bool(False)
        assert 'Kotak makan harus bernilai true atau false.' in validate_message

    def test_sp_donation_empty_value(self):
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
            'payment_method_id': '1',
            'phone_number': '081386356616',
            'is_lunchbox': '0',
            'donation_price': '',
            'voucher_id': '62',
            'order_items[0][stock_id]': discover.json().get('data')['nearby_menu'][0]['stock_id'],
            'order_items[0][qty]': '1',
            'order_items[0][note]': 'Note Menu',
            'address': 'Megaregency',
            'note': 'Note QA'
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        self_pickup = requests.post(url_self_pickup, data=param3, headers=headers3)

        validate_status = self_pickup.json().get('success')
        validate_message = self_pickup.json().get('message')['donation_price']

        assert self_pickup.status_code == 422
        assert validate_status == bool(False)
        assert 'Jumlah donasi harus berupa angka.' in validate_message

    def test_sp_without_param_donation(self):
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
            'payment_method_id': '1',
            'phone_number': '081386356616',
            'is_lunchbox': '0',
            # 'donation_price': '',
            'voucher_id': '62',
            'order_items[0][stock_id]': discover.json().get('data')['nearby_menu'][0]['stock_id'],
            'order_items[0][qty]': '1',
            'order_items[0][note]': 'Note Menu',
            'address': 'Megaregency',
            'note': 'Note QA'
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        self_pickup = requests.post(url_self_pickup, data=param3, headers=headers3)

        validate_status = self_pickup.json().get('success')
        validate_message = self_pickup.json().get('message')
        validate_data = self_pickup.json().get('data')
        validate_data_transaksi = self_pickup.json().get('data')['transaksi']

        assert self_pickup.status_code == 201
        assert validate_status == bool(True)
        assert 'Order Self Pickup berhasil dibuat' in validate_message
        assert_that(validate_data).is_not_none()
        assert_that(validate_data_transaksi).is_not_none()
        assert_that(validate_data).contains_only('id', 'registrasi_order_number', 'alamat', 'status_order_id',
                                                 'canceled_by',
                                                 'created_at', 'keterangan', 'ulasan', 'rating', 'transaksi')
        assert_that(validate_data_transaksi).contains_only('id', 'metode_pembayaran_id', 'order_id', 'invoice_id',
                                                           'invoice_url', 'invoice_expired', 'phone_number', 'subtotal',
                                                           'grand_total', 'grand_total_harga_asli', 'potongan_surplus',
                                                           'potongan_voucher', 'potongan_kotak_makan', 'hemat',
                                                           'komisi_merchant', 'komisi_surplus', 'kode', 'jenis_kode',
                                                           'is_tempat_makanan', 'image_lunchbox', 'is_dikirim',
                                                           'status_transaksi_id', 'status_pickup_id', 'step_progress',
                                                           'pickup_by_system', 'created_at', 'updated_at', 'voucher_id',
                                                           'shipment_price')

    def test_sp_donation_text_value(self):
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
            'payment_method_id': '1',
            'phone_number': '081386356616',
            'is_lunchbox': '0',
            'donation_price': 'aaa',
            'voucher_id': '62',
            'order_items[0][stock_id]': discover.json().get('data')['nearby_menu'][0]['stock_id'],
            'order_items[0][qty]': '1',
            'order_items[0][note]': 'Note Menu',
            'address': 'Megaregency',
            'note': 'Note QA'
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        self_pickup = requests.post(url_self_pickup, data=param3, headers=headers3)

        validate_status = self_pickup.json().get('success')
        validate_message = self_pickup.json().get('message')['donation_price']
        assert self_pickup.status_code == 422
        assert validate_status == bool(False)
        assert 'Jumlah donasi harus berupa angka.' in validate_message

    def test_sp_donation_value_kurang_2500(self):
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
            'payment_method_id': '1',
            'phone_number': '081386356616',
            'is_lunchbox': '0',
            'donation_price': '1',
            'voucher_id': '62',
            'order_items[0][stock_id]': discover.json().get('data')['nearby_menu'][0]['stock_id'],
            'order_items[0][qty]': '1',
            'order_items[0][note]': 'Note Menu',
            'address': 'Megaregency',
            'note': 'Note QA'
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        self_pickup = requests.post(url_self_pickup, data=param3, headers=headers3)

        validate_status = self_pickup.json().get('success')
        validate_message = self_pickup.json().get('message')['donation_price']
        assert self_pickup.status_code == 422
        assert validate_status == bool(False)
        assert 'Jumlah donasi harus diantara 2500 dan 30000' in validate_message

    def test_sp_voucher_empty_value(self):
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
            'payment_method_id': '1',
            'phone_number': '081386356616',
            'is_lunchbox': '0',
            'donation_price': '2500',
            'voucher_id': '',
            'order_items[0][stock_id]': discover.json().get('data')['nearby_menu'][0]['stock_id'],
            'order_items[0][qty]': '1',
            'order_items[0][note]': 'Note Menu',
            'address': 'Megaregency',
            'note': 'Note QA'
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        self_pickup = requests.post(url_self_pickup, data=param3, headers=headers3)

        validate_status = self_pickup.json().get('success')
        validate_message = self_pickup.json().get('message')['voucher_id']

        assert self_pickup.status_code == 422
        assert validate_status == bool(False)
        assert 'Voucher harus berupa angka.' in validate_message

    def test_sp_without_param_voucher(self):
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
            'payment_method_id': '1',
            'phone_number': '081386356616',
            'is_lunchbox': '0',
            'donation_price': '2500',
            # 'voucher_id': '',
            'order_items[0][stock_id]': discover.json().get('data')['nearby_menu'][0]['stock_id'],
            'order_items[0][qty]': '1',
            'order_items[0][note]': 'Note Menu',
            'address': 'Megaregency',
            'note': 'Note QA'
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        self_pickup = requests.post(url_self_pickup, data=param3, headers=headers3)

        validate_status = self_pickup.json().get('success')
        validate_message = self_pickup.json().get('message')
        validate_data = self_pickup.json().get('data')
        validate_data_transaksi = self_pickup.json().get('data')['transaksi']

        assert self_pickup.status_code == 201
        assert validate_status == bool(True)
        assert 'Order Self Pickup berhasil dibuat' in validate_message
        assert_that(validate_data).is_not_none()
        assert_that(validate_data_transaksi).is_not_none()
        assert_that(validate_data).contains_only('id', 'registrasi_order_number', 'alamat', 'status_order_id',
                                                 'canceled_by',
                                                 'created_at', 'keterangan', 'ulasan', 'rating', 'transaksi')
        assert_that(validate_data_transaksi).contains_only('id', 'metode_pembayaran_id', 'order_id', 'invoice_id',
                                                           'invoice_url', 'invoice_expired', 'phone_number', 'subtotal',
                                                           'grand_total', 'grand_total_harga_asli', 'potongan_surplus',
                                                           'potongan_voucher', 'potongan_kotak_makan', 'hemat',
                                                           'komisi_merchant', 'komisi_surplus', 'kode', 'jenis_kode',
                                                           'is_tempat_makanan', 'image_lunchbox', 'is_dikirim',
                                                           'status_transaksi_id', 'status_pickup_id', 'step_progress',
                                                           'pickup_by_system', 'created_at', 'updated_at', 'voucher_id',
                                                           'shipment_price')

    def test_sp_voucher_not_found(self):
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
            'payment_method_id': '1',
            'phone_number': '081386356616',
            'is_lunchbox': '0',
            'donation_price': '2500',
            'voucher_id': '666',
            'order_items[0][stock_id]': discover.json().get('data')['nearby_menu'][0]['stock_id'],
            'order_items[0][qty]': '1',
            'order_items[0][note]': 'Note Menu',
            'address': 'Megaregency',
            'note': 'Note QA'
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        self_pickup = requests.post(url_self_pickup, data=param3, headers=headers3)

        validate_status = self_pickup.json().get('success')
        validate_message = self_pickup.json().get('message')

        assert self_pickup.status_code == 400
        assert validate_status == bool(False)
        assert 'Voucher tidak ditemukan' in validate_message

    def test_sp_voucher_text_value(self):
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
            'payment_method_id': '1',
            'phone_number': '081386356616',
            'is_lunchbox': '0',
            'donation_price': '2500',
            'voucher_id': 'aaa',
            'order_items[0][stock_id]': discover.json().get('data')['nearby_menu'][0]['stock_id'],
            'order_items[0][qty]': '1',
            'order_items[0][note]': 'Note Menu',
            'address': 'Megaregency',
            'note': 'Note QA'
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        self_pickup = requests.post(url_self_pickup, data=param3, headers=headers3)

        validate_status = self_pickup.json().get('success')
        validate_message = self_pickup.json().get('message')['voucher_id']

        assert self_pickup.status_code == 422
        assert validate_status == bool(False)
        assert 'Voucher harus berupa angka.' in validate_message

    def test_sp_stock_id_empty_value(self):
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
            'payment_method_id': '1',
            'phone_number': '081386356616',
            'is_lunchbox': '0',
            'donation_price': '2500',
            'voucher_id': '62',
            'order_items[0][stock_id]': '',
            'order_items[0][qty]': '1',
            'order_items[0][note]': 'Note Menu',
            'address': 'Megaregency',
            'note': 'Note QA'
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        self_pickup = requests.post(url_self_pickup, data=param3, headers=headers3)

        validate_status = self_pickup.json().get('success')
        validate_message = self_pickup.json().get('message')['order_items.0.stock_id']

        assert self_pickup.status_code == 422
        assert validate_status == bool(False)
        assert 'order_items.0.stock_id tidak boleh kosong.' in validate_message

    def test_sp_without_param_stock_id(self):
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
            'payment_method_id': '1',
            'phone_number': '081386356616',
            'is_lunchbox': '0',
            'donation_price': '2500',
            'voucher_id': '62',
            # 'order_items[0][stock_id]': '',
            'order_items[0][qty]': '1',
            'order_items[0][note]': 'Note Menu',
            'address': 'Megaregency',
            'note': 'Note QA'
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        self_pickup = requests.post(url_self_pickup, data=param3, headers=headers3)

        validate_status = self_pickup.json().get('success')
        validate_message = self_pickup.json().get('message')['order_items.0.stock_id']

        assert self_pickup.status_code == 422
        assert validate_status == bool(False)
        assert 'order_items.0.stock_id tidak boleh kosong.' in validate_message

    def test_sp_stock_id_text_value(self):
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
            'payment_method_id': '1',
            'phone_number': '081386356616',
            'is_lunchbox': '0',
            'donation_price': '2500',
            'voucher_id': '62',
            'order_items[0][stock_id]': 'aaa',
            'order_items[0][qty]': '1',
            'order_items[0][note]': 'Note Menu',
            'address': 'Megaregency',
            'note': 'Note QA'
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        self_pickup = requests.post(url_self_pickup, data=param3, headers=headers3)

        validate_status = self_pickup.json().get('success')
        validate_message = self_pickup.json().get('message')['order_items.0.stock_id']

        assert self_pickup.status_code == 422
        assert validate_status == bool(False)
        assert 'order_items.0.stock_id harus berupa angka.' in validate_message

    def test_sp_stock_id_not_found(self):
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
            'payment_method_id': '1',
            'phone_number': '081386356616',
            'is_lunchbox': '0',
            'donation_price': '2500',
            'voucher_id': '62',
            'order_items[0][stock_id]': '66666',
            'order_items[0][qty]': '1',
            'order_items[0][note]': 'Note Menu',
            'address': 'Megaregency',
            'note': 'Note QA'
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        self_pickup = requests.post(url_self_pickup, data=param3, headers=headers3)

        validate_status = self_pickup.json().get('success')
        validate_message = self_pickup.json().get('message')[0]['message']

        assert self_pickup.status_code == 422
        assert validate_status == bool(False)
        assert 'Menu tidak ditemukan' in validate_message

    def test_sp_qty_empty_value(self):
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
            'payment_method_id': '1',
            'phone_number': '081386356616',
            'is_lunchbox': '0',
            'donation_price': '2500',
            'voucher_id': '62',
            'order_items[0][stock_id]': discover.json().get('data')['nearby_menu'][0]['stock_id'],
            'order_items[0][qty]': '',
            'order_items[0][note]': 'Note Menu',
            'address': 'Megaregency',
            'note': 'Note QA'
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        self_pickup = requests.post(url_self_pickup, data=param3, headers=headers3)

        validate_status = self_pickup.json().get('success')
        validate_message = self_pickup.json().get('message')['order_items.0.qty']

        assert self_pickup.status_code == 422
        assert validate_status == bool(False)
        assert 'order_items.0.qty tidak boleh kosong.' in validate_message

    def test_sp_without_param_qty(self):
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
            'payment_method_id': '1',
            'phone_number': '081386356616',
            'is_lunchbox': '0',
            'donation_price': '2500',
            'voucher_id': '62',
            'order_items[0][stock_id]': discover.json().get('data')['nearby_menu'][0]['stock_id'],
            # 'order_items[0][qty]': '',
            'order_items[0][note]': 'Note Menu',
            'address': 'Megaregency',
            'note': 'Note QA'
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        self_pickup = requests.post(url_self_pickup, data=param3, headers=headers3)

        validate_status = self_pickup.json().get('success')
        validate_message = self_pickup.json().get('message')['order_items.0.qty']

        assert self_pickup.status_code == 422
        assert validate_status == bool(False)
        assert 'order_items.0.qty tidak boleh kosong.' in validate_message

    def test_sp_qty_value_text(self):
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
            'payment_method_id': '1',
            'phone_number': '081386356616',
            'is_lunchbox': '0',
            'donation_price': '2500',
            'voucher_id': '62',
            'order_items[0][stock_id]': discover.json().get('data')['nearby_menu'][0]['stock_id'],
            'order_items[0][qty]': 'aaa',
            'order_items[0][note]': 'Note Menu',
            'address': 'Megaregency',
            'note': 'Note QA'
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        self_pickup = requests.post(url_self_pickup, data=param3, headers=headers3)

        validate_status = self_pickup.json().get('success')
        validate_message = self_pickup.json().get('message')['order_items.0.qty']

        assert self_pickup.status_code == 422
        assert validate_status == bool(False)
        assert 'order_items.0.qty harus berupa angka.' in validate_message

    def test_sp_qty_minus_value(self):
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
            'payment_method_id': '1',
            'phone_number': '081386356616',
            'is_lunchbox': '0',
            'donation_price': '2500',
            'voucher_id': '62',
            'order_items[0][stock_id]': discover.json().get('data')['nearby_menu'][0]['stock_id'],
            'order_items[0][qty]': '-20',
            'order_items[0][note]': 'Note Menu',
            'address': 'Megaregency',
            'note': 'Note QA'
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        self_pickup = requests.post(url_self_pickup, data=param3, headers=headers3)

        validate_status = self_pickup.json().get('success')
        validate_message = self_pickup.json().get('message')['order_items.0.qty']

        assert self_pickup.status_code == 422
        assert validate_status == bool(False)
        assert 'order_items.0.qty harus diantara 1 dan 999' in validate_message

    def test_sp_qty_melebihi_stock(self):
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
            'payment_method_id': '1',
            'phone_number': '081386356616',
            'is_lunchbox': '0',
            'donation_price': '2500',
            'voucher_id': '62',
            'order_items[0][stock_id]': discover.json().get('data')['nearby_menu'][0]['stock_id'],
            'order_items[0][qty]': '990',
            'order_items[0][note]': 'Note Menu',
            'address': 'Megaregency',
            'note': 'Note QA'
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        self_pickup = requests.post(url_self_pickup, data=param3, headers=headers3)

        validate_status = self_pickup.json().get('success')
        validate_message = self_pickup.json().get('message')[0]['message']

        assert self_pickup.status_code == 422
        assert validate_status == bool(False)
        assert 'tidak tersedia' in validate_message

    def test_sp_without_param_note(self):
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
            'payment_method_id': '1',
            'phone_number': '081386356616',
            'is_lunchbox': '0',
            'donation_price': '2500',
            'voucher_id': '62',
            'order_items[0][stock_id]': discover.json().get('data')['nearby_menu'][0]['stock_id'],
            'order_items[0][qty]': '1',
            # 'order_items[0][note]': 'Note Menu',
            'address': 'Megaregency',
            'note': 'Note QA'
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        self_pickup = requests.post(url_self_pickup, data=param3, headers=headers3)

        validate_status = self_pickup.json().get('success')
        validate_message = self_pickup.json().get('message')

        assert self_pickup.status_code == 201
        assert validate_status == bool(True)
        assert 'Order Self Pickup berhasil dibuat' in validate_message

    def test_sp_note_empty_value(self):
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
            'payment_method_id': '1',
            'phone_number': '081386356616',
            'is_lunchbox': '0',
            'donation_price': '2500',
            'voucher_id': '62',
            'order_items[0][stock_id]': discover.json().get('data')['nearby_menu'][0]['stock_id'],
            'order_items[0][qty]': '1',
            'order_items[0][note]': '',
            'address': 'Megaregency',
            'note': 'Note QA'
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        self_pickup = requests.post(url_self_pickup, data=param3, headers=headers3)

        validate_status = self_pickup.json().get('success')
        validate_message = self_pickup.json().get('message')

        assert self_pickup.status_code == 201
        assert validate_status == bool(True)
        assert 'Order Self Pickup berhasil dibuat' in validate_message

    def test_sp_without_param_address(self):
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
            'payment_method_id': '1',
            'phone_number': '081386356616',
            'is_lunchbox': '0',
            'donation_price': '2500',
            'voucher_id': '62',
            'order_items[0][stock_id]': discover.json().get('data')['nearby_menu'][0]['stock_id'],
            'order_items[0][qty]': '1',
            'order_items[0][note]': 'Note Menu',
            # 'address': 'Megaregency',
            'note': 'Note QA'
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        self_pickup = requests.post(url_self_pickup, data=param3, headers=headers3)

        validate_status = self_pickup.json().get('success')
        validate_message = self_pickup.json().get('message')['address']

        assert self_pickup.status_code == 422
        assert validate_status == bool(False)
        assert 'Alamat tidak boleh kosong.' in validate_message

    def test_sp_address_empty_value(self):
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
            'payment_method_id': '1',
            'phone_number': '081386356616',
            'is_lunchbox': '0',
            'donation_price': '2500',
            'voucher_id': '62',
            'order_items[0][stock_id]': discover.json().get('data')['nearby_menu'][0]['stock_id'],
            'order_items[0][qty]': '1',
            'order_items[0][note]': 'Note Menu',
            'address': '',
            'note': 'Note QA'
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        self_pickup = requests.post(url_self_pickup, data=param3, headers=headers3)

        validate_status = self_pickup.json().get('success')
        validate_message = self_pickup.json().get('message')['address']

        assert self_pickup.status_code == 422
        assert validate_status == bool(False)
        assert 'Alamat tidak boleh kosong.' in validate_message

    def test_sp_without_param_note_u(self):
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
            'payment_method_id': '1',
            'phone_number': '081386356616',
            'is_lunchbox': '0',
            'donation_price': '2500',
            'voucher_id': '62',
            'order_items[0][stock_id]': '160',
            'order_items[0][qty]': '1',
            'order_items[0][note]': 'Note Menu',
            'address': 'Megaregency',
            # 'note': 'Note QA'
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        self_pickup = requests.post(url_self_pickup, data=param3, headers=headers3)

        validate_status = self_pickup.json().get('success')
        validate_message = self_pickup.json().get('message')

        assert self_pickup.status_code == 500
        assert validate_status == bool(False)
        assert 'Aduh!' in validate_message

    def test_sp_note_empty_value_u(self):
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
            'payment_method_id': '1',
            'phone_number': '081386356616',
            'is_lunchbox': '0',
            'donation_price': '2500',
            'voucher_id': '62',
            'order_items[0][stock_id]': '160',
            'order_items[0][qty]': '1',
            'order_items[0][note]': 'Note Menu',
            'address': 'Megaregency',
            'note': ''
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        self_pickup = requests.post(url_self_pickup, data=param3, headers=headers3)

        validate_status = self_pickup.json().get('success')
        validate_message = self_pickup.json().get('message')

        assert self_pickup.status_code == 201
        assert validate_status == bool(True)
        assert 'Order Self Pickup berhasil dibuat' in validate_message
