import requests
from env import stagging
from pprint import pprint
from assertpy import assert_that


class TestCustomerOrdersDelivery:

    global setting_env, url_login, url_discover, url_delivery, email, kata_sandi, wrong_token

    setting_env = stagging
    url_login = f"{setting_env}/api/v2/customer/auth/login/email"
    url_discover = f"{setting_env}/api/v2/customer/discover"
    url_delivery = f"{setting_env}/api/v2/customer/orders/delivery"
    email = "kopiruangvirtual@gmail.com"
    kata_sandi = '12345678'
    wrong_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvc3RhZ2luZy5hZG1pbnN1cnBsdXMubmV0XC9hcGlcL3YyXC9jdXN0b21lclwvYXV0aFwvbG9naW5cL2VtYWlsIiwiaWF0IjoxNjE2ODA1NzI2LCJleHAiOjE2MTkzOTc3MjYsIm5iZiI6MTYxNjgwNTcyNiwianRpIjoib05ESmxFRE5hSzNrN2RtVyIsInN1YiI6NDEyNiwicHJ2IjoiMjc0MTA1ZGE2ZTk1YmVmMjgwNzc4NmRkODczODg2N2NmOWMwMmFhYiJ9.fj51xIfQrqleRvdSJUbWcdrvsxQPUn8HpccnOmTgPDI'

    def test_OD_normal(self):
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
            "payment_method_id": "1",
            "is_lunchbox": "0",
            "donation_price": "2500",
            "voucher_id": "62",
            "order_items[0][qty]": "2",
            "order_items[0][stock_id]": discover.json().get('data')['nearby_menu'][0]['stock_id'],
            "address": "Megaregency",
            "note": "Test Notes",
            "delivery_price": "20000",
            "delivery_method": "Instant",
            "origin_contact_name": "Fawwaz 1",
            "origin_contact_phone": "081386356616",
            "origin_address": "Perumahan Megaregency 1",
            "origin_lat_long": "-6.3823027,107.1162164",
            "destination_contact_name": "Fawwaz 2",
            "destination_contact_phone": "0857108194",
            "destination_address": "Perumahan Megaregency 2",
            "destination_lat_long": "-6.3772882,107.1062917",
            "phone_number": "085710819443"
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        delivery = requests.post(url_delivery, data=param3, headers=headers3)

        verify_status = delivery.json().get('success')
        verify_message = delivery.json().get('message')
        verify_data = delivery.json().get('data')
        verify_data_merchant = delivery.json().get('data')['merchant']
        verify_data_transaksi = delivery.json().get('data')['transaksi']

        assert delivery.status_code == 201
        assert verify_status == bool(True)
        assert "Order Delivery berhasil dibuat" in verify_message
        assert_that(verify_data).is_not_none()
        assert_that(verify_data).contains_only('id', 'registrasi_order_number', 'alamat', 'status_order_id',
                                               'canceled_by',
                                               'created_at', 'keterangan', 'ulasan', 'rating', 'merchant', 'transaksi')
        assert_that(verify_data_merchant).contains_only('id', 'name', 'email', 'no_ponsel', 'alamat', 'auth_origin',
                                                        'referal_code', 'onesignal_loc', 'latitude', 'longitude')
        assert_that(verify_data_transaksi).contains_only('id', 'metode_pembayaran_id', 'order_id', 'invoice_id',
                                                         'invoice_url',
                                                         'invoice_expired', 'phone_number', 'subtotal', 'grand_total',
                                                         'grand_total_harga_asli', 'potongan_surplus',
                                                         'potongan_voucher',
                                                         'potongan_kotak_makan', 'hemat', 'komisi_merchant',
                                                         'komisi_surplus',
                                                         'kode', 'jenis_kode', 'is_tempat_makanan', 'image_lunchbox',
                                                         'is_dikirim', 'status_transaksi_id', 'status_pickup_id',
                                                         'step_progress', 'pickup_by_system', 'created_at',
                                                         'updated_at',
                                                         'voucher_id', 'shipment_price')

    def test_OD_wrong_Token(self):
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
            "payment_method_id": "1",
            "is_lunchbox": "0",
            "donation_price": "2500",
            "voucher_id": "62",
            "order_items[0][qty]": "2",
            "order_items[0][stock_id]": discover.json().get('data')['nearby_menu'][0]['stock_id'],
            "address": "Megaregency",
            "note": "Test Notes",
            "delivery_price": "20000",
            "delivery_method": "Instant",
            "origin_contact_name": "Fawwaz 1",
            "origin_contact_phone": "081386356616",
            "origin_address": "Perumahan Megaregency 1",
            "origin_lat_long": "-6.3823027,107.1162164",
            "destination_contact_name": "Fawwaz 2",
            "destination_contact_phone": "0857108194",
            "destination_address": "Perumahan Megaregency 2",
            "destination_lat_long": "-6.3772882,107.1062917",
            "phone_number": "085710819443"
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": wrong_token
        }
        delivery = requests.post(url_delivery, data=param3, headers=headers3)

        verify_status = delivery.json().get('success')
        verify_message = delivery.json().get('message')

        assert delivery.status_code == 401
        assert verify_status == bool(False)
        assert "Unauthorized" in verify_message

    def test_OD_without_param_token(self):
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
            "payment_method_id": "1",
            "is_lunchbox": "0",
            "donation_price": "2500",
            "voucher_id": "62",
            "order_items[0][qty]": "2",
            "order_items[0][stock_id]": discover.json().get('data')['nearby_menu'][0]['stock_id'],
            "address": "Megaregency",
            "note": "Test Notes",
            "delivery_price": "20000",
            "delivery_method": "Instant",
            "origin_contact_name": "Fawwaz 1",
            "origin_contact_phone": "081386356616",
            "origin_address": "Perumahan Megaregency 1",
            "origin_lat_long": "-6.3823027,107.1162164",
            "destination_contact_name": "Fawwaz 2",
            "destination_contact_phone": "0857108194",
            "destination_address": "Perumahan Megaregency 2",
            "destination_lat_long": "-6.3772882,107.1062917",
            "phone_number": "085710819443"
        }
        headers3 = {
            "Accept": "application/json",
            # "Authorization": wrong_token
        }
        delivery = requests.post(url_delivery, data=param3, headers=headers3)

        verify_status = delivery.json().get('success')
        verify_message = delivery.json().get('message')

        assert delivery.status_code == 401
        assert verify_status == bool(False)
        assert "Unauthorized" in verify_message

    def test_OD_without_param_metode_pembayaran(self):
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
            # "payment_method_id": "1",
            "is_lunchbox": "0",
            "donation_price": "2500",
            "voucher_id": "62",
            "order_items[0][qty]": "2",
            "order_items[0][stock_id]": discover.json().get('data')['nearby_menu'][0]['stock_id'],
            "address": "Megaregency",
            "note": "Test Notes",
            "delivery_price": "20000",
            "delivery_method": "Instant",
            "origin_contact_name": "Fawwaz 1",
            "origin_contact_phone": "081386356616",
            "origin_address": "Perumahan Megaregency 1",
            "origin_lat_long": "-6.3823027,107.1162164",
            "destination_contact_name": "Fawwaz 2",
            "destination_contact_phone": "0857108194",
            "destination_address": "Perumahan Megaregency 2",
            "destination_lat_long": "-6.3772882,107.1062917",
            "phone_number": "085710819443"
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        delivery = requests.post(url_delivery, data=param3, headers=headers3)

        verify_status = delivery.json().get('success')
        verify_message = delivery.json().get('message')['payment_method_id'][0]

        assert delivery.status_code == 422
        assert verify_status == bool(False)
        assert "Metode Pembayaran tidak boleh kosong" in verify_message

    def test_OD_metode_pembayaran_empty_value(self):
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
            "payment_method_id": "",
            "is_lunchbox": "0",
            "donation_price": "2500",
            "voucher_id": "62",
            "order_items[0][qty]": "2",
            "order_items[0][stock_id]": discover.json().get('data')['nearby_menu'][0]['stock_id'],
            "address": "Megaregency",
            "note": "Test Notes",
            "delivery_price": "20000",
            "delivery_method": "Instant",
            "origin_contact_name": "Fawwaz 1",
            "origin_contact_phone": "081386356616",
            "origin_address": "Perumahan Megaregency 1",
            "origin_lat_long": "-6.3823027,107.1162164",
            "destination_contact_name": "Fawwaz 2",
            "destination_contact_phone": "0857108194",
            "destination_address": "Perumahan Megaregency 2",
            "destination_lat_long": "-6.3772882,107.1062917",
            "phone_number": "085710819443"
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        delivery = requests.post(url_delivery, data=param3, headers=headers3)

        verify_status = delivery.json().get('success')
        verify_message = delivery.json().get('message')['payment_method_id'][0]

        assert delivery.status_code == 422
        assert verify_status == bool(False)
        assert "Metode Pembayaran tidak boleh kosong" in verify_message

    def test_OD_metode_pembayaran_text_value(self):
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
            "payment_method_id": "a",
            "is_lunchbox": "0",
            "donation_price": "2500",
            "voucher_id": "62",
            "order_items[0][qty]": "2",
            "order_items[0][stock_id]": discover.json().get('data')['nearby_menu'][0]['stock_id'],
            "address": "Megaregency",
            "note": "Test Notes",
            "delivery_price": "20000",
            "delivery_method": "Instant",
            "origin_contact_name": "Fawwaz 1",
            "origin_contact_phone": "081386356616",
            "origin_address": "Perumahan Megaregency 1",
            "origin_lat_long": "-6.3823027,107.1162164",
            "destination_contact_name": "Fawwaz 2",
            "destination_contact_phone": "0857108194",
            "destination_address": "Perumahan Megaregency 2",
            "destination_lat_long": "-6.3772882,107.1062917",
            "phone_number": "085710819443"
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        delivery = requests.post(url_delivery, data=param3, headers=headers3)

        verify_status = delivery.json().get('success')
        verify_message = delivery.json().get('message')['payment_method_id'][0]

        assert delivery.status_code == 422
        assert verify_status == bool(False)
        assert "Metode Pembayaran yang dipilih tidak tersedia." in verify_message

    def test_OD_metode_pembayaran_wrong_value(self):
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
            "payment_method_id": "10",
            "is_lunchbox": "0",
            "donation_price": "2500",
            "voucher_id": "62",
            "order_items[0][qty]": "2",
            "order_items[0][stock_id]": discover.json().get('data')['nearby_menu'][0]['stock_id'],
            "address": "Megaregency",
            "note": "Test Notes",
            "delivery_price": "20000",
            "delivery_method": "Instant",
            "origin_contact_name": "Fawwaz 1",
            "origin_contact_phone": "081386356616",
            "origin_address": "Perumahan Megaregency 1",
            "origin_lat_long": "-6.3823027,107.1162164",
            "destination_contact_name": "Fawwaz 2",
            "destination_contact_phone": "0857108194",
            "destination_address": "Perumahan Megaregency 2",
            "destination_lat_long": "-6.3772882,107.1062917",
            "phone_number": "085710819443"
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        delivery = requests.post(url_delivery, data=param3, headers=headers3)

        verify_status = delivery.json().get('success')
        verify_message = delivery.json().get('message')['payment_method_id'][0]

        assert delivery.status_code == 422
        assert verify_status == bool(False)
        assert "Metode Pembayaran yang dipilih tidak tersedia." in verify_message

    def test_OD_lunchbox_empty_value(self):
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
            "payment_method_id": "1",
            "is_lunchbox": "",
            "donation_price": "2500",
            "voucher_id": "62",
            "order_items[0][qty]": "2",
            "order_items[0][stock_id]": discover.json().get('data')['nearby_menu'][0]['stock_id'],
            "address": "Megaregency",
            "note": "Test Notes",
            "delivery_price": "20000",
            "delivery_method": "Instant",
            "origin_contact_name": "Fawwaz 1",
            "origin_contact_phone": "081386356616",
            "origin_address": "Perumahan Megaregency 1",
            "origin_lat_long": "-6.3823027,107.1162164",
            "destination_contact_name": "Fawwaz 2",
            "destination_contact_phone": "0857108194",
            "destination_address": "Perumahan Megaregency 2",
            "destination_lat_long": "-6.3772882,107.1062917",
            "phone_number": "085710819443"
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        delivery = requests.post(url_delivery, data=param3, headers=headers3)

        verify_status = delivery.json().get('success')
        verify_message = delivery.json().get('message')['is_lunchbox'][0]

        assert delivery.status_code == 422
        assert verify_status == bool(False)
        assert "Kotak makan tidak boleh kosong." in verify_message

    def test_OD_without_param_lunchbox(self):
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
            "payment_method_id": "1",
            # "is_lunchbox": "",
            "donation_price": "2500",
            "voucher_id": "62",
            "order_items[0][qty]": "2",
            "order_items[0][stock_id]": discover.json().get('data')['nearby_menu'][0]['stock_id'],
            "address": "Megaregency",
            "note": "Test Notes",
            "delivery_price": "20000",
            "delivery_method": "Instant",
            "origin_contact_name": "Fawwaz 1",
            "origin_contact_phone": "081386356616",
            "origin_address": "Perumahan Megaregency 1",
            "origin_lat_long": "-6.3823027,107.1162164",
            "destination_contact_name": "Fawwaz 2",
            "destination_contact_phone": "0857108194",
            "destination_address": "Perumahan Megaregency 2",
            "destination_lat_long": "-6.3772882,107.1062917",
            "phone_number": "085710819443"
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        delivery = requests.post(url_delivery, data=param3, headers=headers3)

        verify_status = delivery.json().get('success')
        verify_message = delivery.json().get('message')['is_lunchbox'][0]

        assert delivery.status_code == 422
        assert verify_status == bool(False)
        assert "Kotak makan tidak boleh kosong." in verify_message

    def test_OD_lunchbox_text_value(self):
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
            "payment_method_id": "1",
            "is_lunchbox": "a",
            "donation_price": "2500",
            "voucher_id": "62",
            "order_items[0][qty]": "2",
            "order_items[0][stock_id]": discover.json().get('data')['nearby_menu'][0]['stock_id'],
            "address": "Megaregency",
            "note": "Test Notes",
            "delivery_price": "20000",
            "delivery_method": "Instant",
            "origin_contact_name": "Fawwaz 1",
            "origin_contact_phone": "081386356616",
            "origin_address": "Perumahan Megaregency 1",
            "origin_lat_long": "-6.3823027,107.1162164",
            "destination_contact_name": "Fawwaz 2",
            "destination_contact_phone": "0857108194",
            "destination_address": "Perumahan Megaregency 2",
            "destination_lat_long": "-6.3772882,107.1062917",
            "phone_number": "085710819443"
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        delivery = requests.post(url_delivery, data=param3, headers=headers3)

        verify_status = delivery.json().get('success')
        verify_message = delivery.json().get('message')['is_lunchbox'][0]

        assert delivery.status_code == 422
        assert verify_status == bool(False)
        assert "Kotak makan harus bernilai true atau false." in verify_message

    def test_OD_lunchbox_not_bool_value(self):
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
            "payment_method_id": "1",
            "is_lunchbox": "10",
            "donation_price": "2500",
            "voucher_id": "62",
            "order_items[0][qty]": "2",
            "order_items[0][stock_id]": discover.json().get('data')['nearby_menu'][0]['stock_id'],
            "address": "Megaregency",
            "note": "Test Notes",
            "delivery_price": "20000",
            "delivery_method": "Instant",
            "origin_contact_name": "Fawwaz 1",
            "origin_contact_phone": "081386356616",
            "origin_address": "Perumahan Megaregency 1",
            "origin_lat_long": "-6.3823027,107.1162164",
            "destination_contact_name": "Fawwaz 2",
            "destination_contact_phone": "0857108194",
            "destination_address": "Perumahan Megaregency 2",
            "destination_lat_long": "-6.3772882,107.1062917",
            "phone_number": "085710819443"
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        delivery = requests.post(url_delivery, data=param3, headers=headers3)

        verify_status = delivery.json().get('success')
        verify_message = delivery.json().get('message')['is_lunchbox'][0]

        assert delivery.status_code == 422
        assert verify_status == bool(False)
        assert "Kotak makan harus bernilai true atau false." in verify_message

    def test_OD_donation_empty_value(self):
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
            "payment_method_id": "1",
            "is_lunchbox": "0",
            "donation_price": "",
            "voucher_id": "62",
            "order_items[0][qty]": "2",
            "order_items[0][stock_id]": discover.json().get('data')['nearby_menu'][0]['stock_id'],
            "address": "Megaregency",
            "note": "Test Notes",
            "delivery_price": "20000",
            "delivery_method": "Instant",
            "origin_contact_name": "Fawwaz 1",
            "origin_contact_phone": "081386356616",
            "origin_address": "Perumahan Megaregency 1",
            "origin_lat_long": "-6.3823027,107.1162164",
            "destination_contact_name": "Fawwaz 2",
            "destination_contact_phone": "0857108194",
            "destination_address": "Perumahan Megaregency 2",
            "destination_lat_long": "-6.3772882,107.1062917",
            "phone_number": "085710819443"
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        delivery = requests.post(url_delivery, data=param3, headers=headers3)

        verify_status = delivery.json().get('success')
        verify_message = delivery.json().get('message')['donation_price'][0]

        assert delivery.status_code == 422
        assert verify_status == bool(False)
        assert "Jumlah donasi harus berupa angka." in verify_message

    def test_OD_without_param_donation(self):
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
            "payment_method_id": "1",
            "is_lunchbox": "0",
            # "donation_price": "",
            "voucher_id": "62",
            "order_items[0][qty]": "2",
            "order_items[0][stock_id]": discover.json().get('data')['nearby_menu'][0]['stock_id'],
            "address": "Megaregency",
            "note": "Test Notes",
            "delivery_price": "20000",
            "delivery_method": "Instant",
            "origin_contact_name": "Fawwaz 1",
            "origin_contact_phone": "081386356616",
            "origin_address": "Perumahan Megaregency 1",
            "origin_lat_long": "-6.3823027,107.1162164",
            "destination_contact_name": "Fawwaz 2",
            "destination_contact_phone": "0857108194",
            "destination_address": "Perumahan Megaregency 2",
            "destination_lat_long": "-6.3772882,107.1062917",
            "phone_number": "085710819443"
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        delivery = requests.post(url_delivery, data=param3, headers=headers3)

        verify_status = delivery.json().get('success')
        verify_message = delivery.json().get('message')

        assert delivery.status_code == 201
        assert verify_status == bool(True)
        assert "Order Delivery berhasil dibuat" in verify_message

    def test_OD_donation_text_value(self):
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
            "payment_method_id": "1",
            "is_lunchbox": "0",
            "donation_price": "a",
            "voucher_id": "62",
            "order_items[0][qty]": "2",
            "order_items[0][stock_id]": discover.json().get('data')['nearby_menu'][0]['stock_id'],
            "address": "Megaregency",
            "note": "Test Notes",
            "delivery_price": "20000",
            "delivery_method": "Instant",
            "origin_contact_name": "Fawwaz 1",
            "origin_contact_phone": "081386356616",
            "origin_address": "Perumahan Megaregency 1",
            "origin_lat_long": "-6.3823027,107.1162164",
            "destination_contact_name": "Fawwaz 2",
            "destination_contact_phone": "0857108194",
            "destination_address": "Perumahan Megaregency 2",
            "destination_lat_long": "-6.3772882,107.1062917",
            "phone_number": "085710819443"
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        delivery = requests.post(url_delivery, data=param3, headers=headers3)

        verify_status = delivery.json().get('success')
        verify_message = delivery.json().get('message')['donation_price']

        assert delivery.status_code == 422
        assert verify_status == bool(False)
        assert "Jumlah donasi harus berupa angka." in verify_message

    def test_OD_donation_value_kurang_2500(self):
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
            "payment_method_id": "1",
            "is_lunchbox": "0",
            "donation_price": "1",
            "voucher_id": "62",
            "order_items[0][qty]": "2",
            "order_items[0][stock_id]": discover.json().get('data')['nearby_menu'][0]['stock_id'],
            "address": "Megaregency",
            "note": "Test Notes",
            "delivery_price": "20000",
            "delivery_method": "Instant",
            "origin_contact_name": "Fawwaz 1",
            "origin_contact_phone": "081386356616",
            "origin_address": "Perumahan Megaregency 1",
            "origin_lat_long": "-6.3823027,107.1162164",
            "destination_contact_name": "Fawwaz 2",
            "destination_contact_phone": "0857108194",
            "destination_address": "Perumahan Megaregency 2",
            "destination_lat_long": "-6.3772882,107.1062917",
            "phone_number": "085710819443"
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        delivery = requests.post(url_delivery, data=param3, headers=headers3)

        verify_status = delivery.json().get('success')
        verify_message = delivery.json().get('message')['donation_price']

        assert delivery.status_code == 422
        assert verify_status == bool(False)
        assert "Jumlah donasi harus diantara 2500 dan 30000" in verify_message

    def test_OD_voucher_empty_value(self):
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
            "payment_method_id": "1",
            "is_lunchbox": "0",
            "donation_price": "2500",
            "voucher_id": "",
            "order_items[0][qty]": "2",
            "order_items[0][stock_id]": discover.json().get('data')['nearby_menu'][0]['stock_id'],
            "address": "Megaregency",
            "note": "Test Notes",
            "delivery_price": "20000",
            "delivery_method": "Instant",
            "origin_contact_name": "Fawwaz 1",
            "origin_contact_phone": "081386356616",
            "origin_address": "Perumahan Megaregency 1",
            "origin_lat_long": "-6.3823027,107.1162164",
            "destination_contact_name": "Fawwaz 2",
            "destination_contact_phone": "0857108194",
            "destination_address": "Perumahan Megaregency 2",
            "destination_lat_long": "-6.3772882,107.1062917",
            "phone_number": "085710819443"
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        delivery = requests.post(url_delivery, data=param3, headers=headers3)

        verify_status = delivery.json().get('success')
        verify_message = delivery.json().get('message')['voucher_id']

        assert delivery.status_code == 422
        assert verify_status == bool(False)
        assert "Voucher harus berupa angka." in verify_message

    def test_OD_without_param_voucher(self):
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
            "payment_method_id": "1",
            "is_lunchbox": "0",
            "donation_price": "2500",
            # "voucher_id": "",
            "order_items[0][qty]": "2",
            "order_items[0][stock_id]": discover.json().get('data')['nearby_menu'][0]['stock_id'],
            "address": "Megaregency",
            "note": "Test Notes",
            "delivery_price": "20000",
            "delivery_method": "Instant",
            "origin_contact_name": "Fawwaz 1",
            "origin_contact_phone": "081386356616",
            "origin_address": "Perumahan Megaregency 1",
            "origin_lat_long": "-6.3823027,107.1162164",
            "destination_contact_name": "Fawwaz 2",
            "destination_contact_phone": "0857108194",
            "destination_address": "Perumahan Megaregency 2",
            "destination_lat_long": "-6.3772882,107.1062917",
            "phone_number": "085710819443"
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        delivery = requests.post(url_delivery, data=param3, headers=headers3)

        verify_status = delivery.json().get('success')
        verify_message = delivery.json().get('message')

        assert delivery.status_code == 201
        assert verify_status == bool(True)
        assert "Order Delivery berhasil dibuat" in verify_message

    def test_OD_voucher_not_found(self):
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
            "payment_method_id": "1",
            "is_lunchbox": "0",
            "donation_price": "2500",
            "voucher_id": "66666",
            "order_items[0][qty]": "2",
            "order_items[0][stock_id]": discover.json().get('data')['nearby_menu'][0]['stock_id'],
            "address": "Megaregency",
            "note": "Test Notes",
            "delivery_price": "20000",
            "delivery_method": "Instant",
            "origin_contact_name": "Fawwaz 1",
            "origin_contact_phone": "081386356616",
            "origin_address": "Perumahan Megaregency 1",
            "origin_lat_long": "-6.3823027,107.1162164",
            "destination_contact_name": "Fawwaz 2",
            "destination_contact_phone": "0857108194",
            "destination_address": "Perumahan Megaregency 2",
            "destination_lat_long": "-6.3772882,107.1062917",
            "phone_number": "085710819443"
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        delivery = requests.post(url_delivery, data=param3, headers=headers3)

        verify_status = delivery.json().get('success')
        verify_message = delivery.json().get('message')

        assert delivery.status_code == 400
        assert verify_status == bool(False)
        assert "Voucher tidak ditemukan" in verify_message

    def test_OD_voucher_text_value(self):
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
            "payment_method_id": "1",
            "is_lunchbox": "0",
            "donation_price": "2500",
            "voucher_id": "aa",
            "order_items[0][qty]": "2",
            "order_items[0][stock_id]": discover.json().get('data')['nearby_menu'][0]['stock_id'],
            "address": "Megaregency",
            "note": "Test Notes",
            "delivery_price": "20000",
            "delivery_method": "Instant",
            "origin_contact_name": "Fawwaz 1",
            "origin_contact_phone": "081386356616",
            "origin_address": "Perumahan Megaregency 1",
            "origin_lat_long": "-6.3823027,107.1162164",
            "destination_contact_name": "Fawwaz 2",
            "destination_contact_phone": "0857108194",
            "destination_address": "Perumahan Megaregency 2",
            "destination_lat_long": "-6.3772882,107.1062917",
            "phone_number": "085710819443"
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        delivery = requests.post(url_delivery, data=param3, headers=headers3)

        verify_status = delivery.json().get('success')
        verify_message = delivery.json().get('message')['voucher_id']

        assert delivery.status_code == 422
        assert verify_status == bool(False)
        assert "Voucher harus berupa angka." in verify_message

    def test_OD_stock_id_empty_value(self):
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
            "payment_method_id": "1",
            "is_lunchbox": "0",
            "donation_price": "2500",
            "voucher_id": "62",
            "order_items[0][qty]": "2",
            "order_items[0][stock_id]": '',
            "address": "Megaregency",
            "note": "Test Notes",
            "delivery_price": "20000",
            "delivery_method": "Instant",
            "origin_contact_name": "Fawwaz 1",
            "origin_contact_phone": "081386356616",
            "origin_address": "Perumahan Megaregency 1",
            "origin_lat_long": "-6.3823027,107.1162164",
            "destination_contact_name": "Fawwaz 2",
            "destination_contact_phone": "0857108194",
            "destination_address": "Perumahan Megaregency 2",
            "destination_lat_long": "-6.3772882,107.1062917",
            "phone_number": "085710819443"
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        delivery = requests.post(url_delivery, data=param3, headers=headers3)

        verify_status = delivery.json().get('success')
        verify_message = delivery.json().get('message')['order_items.0.stock_id']

        assert delivery.status_code == 422
        assert verify_status == bool(False)
        assert "order_items.0.stock_id tidak boleh kosong." in verify_message

    def test_OD_OD_without_param_stock_id(self):
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
            "payment_method_id": "1",
            "is_lunchbox": "0",
            "donation_price": "2500",
            "voucher_id": "62",
            "order_items[0][qty]": "2",
            # "order_items[0][stock_id]": '',
            "address": "Megaregency",
            "note": "Test Notes",
            "delivery_price": "20000",
            "delivery_method": "Instant",
            "origin_contact_name": "Fawwaz 1",
            "origin_contact_phone": "081386356616",
            "origin_address": "Perumahan Megaregency 1",
            "origin_lat_long": "-6.3823027,107.1162164",
            "destination_contact_name": "Fawwaz 2",
            "destination_contact_phone": "0857108194",
            "destination_address": "Perumahan Megaregency 2",
            "destination_lat_long": "-6.3772882,107.1062917",
            "phone_number": "085710819443"
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        delivery = requests.post(url_delivery, data=param3, headers=headers3)

        verify_status = delivery.json().get('success')
        verify_message = delivery.json().get('message')['order_items.0.stock_id']

        assert delivery.status_code == 422
        assert verify_status == bool(False)
        assert "order_items.0.stock_id tidak boleh kosong." in verify_message

    def test_OD_stock_id_text_value(self):
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
            "payment_method_id": "1",
            "is_lunchbox": "0",
            "donation_price": "2500",
            "voucher_id": "62",
            "order_items[0][qty]": "2",
            "order_items[0][stock_id]": 'aa',
            "address": "Megaregency",
            "note": "Test Notes",
            "delivery_price": "20000",
            "delivery_method": "Instant",
            "origin_contact_name": "Fawwaz 1",
            "origin_contact_phone": "081386356616",
            "origin_address": "Perumahan Megaregency 1",
            "origin_lat_long": "-6.3823027,107.1162164",
            "destination_contact_name": "Fawwaz 2",
            "destination_contact_phone": "0857108194",
            "destination_address": "Perumahan Megaregency 2",
            "destination_lat_long": "-6.3772882,107.1062917",
            "phone_number": "085710819443"
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        delivery = requests.post(url_delivery, data=param3, headers=headers3)

        verify_status = delivery.json().get('success')
        verify_message = delivery.json().get('message')['order_items.0.stock_id']

        assert delivery.status_code == 422
        assert verify_status == bool(False)

    def test_OD_stock_id_not_found(self):
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
            "payment_method_id": "1",
            "is_lunchbox": "0",
            "donation_price": "2500",
            "voucher_id": "62",
            "order_items[0][qty]": "2",
            "order_items[0][stock_id]": '66666',
            "address": "Megaregency",
            "note": "Test Notes",
            "delivery_price": "20000",
            "delivery_method": "Instant",
            "origin_contact_name": "Fawwaz 1",
            "origin_contact_phone": "081386356616",
            "origin_address": "Perumahan Megaregency 1",
            "origin_lat_long": "-6.3823027,107.1162164",
            "destination_contact_name": "Fawwaz 2",
            "destination_contact_phone": "0857108194",
            "destination_address": "Perumahan Megaregency 2",
            "destination_lat_long": "-6.3772882,107.1062917",
            "phone_number": "085710819443"
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        delivery = requests.post(url_delivery, data=param3, headers=headers3)

        verify_status = delivery.json().get('success')
        verify_message = delivery.json().get('message')[0]['message']

        assert delivery.status_code == 422
        assert verify_status == bool(False)
        assert "Menu tidak ditemukan" in verify_message

    def test_OD_qty_empty_value(self):
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
            "payment_method_id": "1",
            "is_lunchbox": "0",
            "donation_price": "2500",
            "voucher_id": "62",
            "order_items[0][qty]": "",
            "order_items[0][stock_id]": discover.json().get('data')['nearby_menu'][0]['stock_id'],
            "address": "Megaregency",
            "note": "Test Notes",
            "delivery_price": "20000",
            "delivery_method": "Instant",
            "origin_contact_name": "Fawwaz 1",
            "origin_contact_phone": "081386356616",
            "origin_address": "Perumahan Megaregency 1",
            "origin_lat_long": "-6.3823027,107.1162164",
            "destination_contact_name": "Fawwaz 2",
            "destination_contact_phone": "0857108194",
            "destination_address": "Perumahan Megaregency 2",
            "destination_lat_long": "-6.3772882,107.1062917",
            "phone_number": "085710819443"
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        delivery = requests.post(url_delivery, data=param3, headers=headers3)

        verify_status = delivery.json().get('success')
        verify_message = delivery.json().get('message')['order_items.0.qty']

        assert delivery.status_code == 422
        assert verify_status == bool(False)
        assert "order_items.0.qty tidak boleh kosong." in verify_message

    def test_OD_without_param_qty(self):
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
            "payment_method_id": "1",
            "is_lunchbox": "0",
            "donation_price": "2500",
            "voucher_id": "62",
            # "order_items[0][qty]": "",
            "order_items[0][stock_id]": discover.json().get('data')['nearby_menu'][0]['stock_id'],
            "address": "Megaregency",
            "note": "Test Notes",
            "delivery_price": "20000",
            "delivery_method": "Instant",
            "origin_contact_name": "Fawwaz 1",
            "origin_contact_phone": "081386356616",
            "origin_address": "Perumahan Megaregency 1",
            "origin_lat_long": "-6.3823027,107.1162164",
            "destination_contact_name": "Fawwaz 2",
            "destination_contact_phone": "0857108194",
            "destination_address": "Perumahan Megaregency 2",
            "destination_lat_long": "-6.3772882,107.1062917",
            "phone_number": "085710819443"
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        delivery = requests.post(url_delivery, data=param3, headers=headers3)

        verify_status = delivery.json().get('success')
        verify_message = delivery.json().get('message')['order_items.0.qty']

        assert delivery.status_code == 422
        assert verify_status == bool(False)
        assert "order_items.0.qty tidak boleh kosong." in verify_message

    def test_OD_qty_value_text(self):
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
            "payment_method_id": "1",
            "is_lunchbox": "0",
            "donation_price": "2500",
            "voucher_id": "62",
            "order_items[0][qty]": "a",
            "order_items[0][stock_id]": discover.json().get('data')['nearby_menu'][0]['stock_id'],
            "address": "Megaregency",
            "note": "Test Notes",
            "delivery_price": "20000",
            "delivery_method": "Instant",
            "origin_contact_name": "Fawwaz 1",
            "origin_contact_phone": "081386356616",
            "origin_address": "Perumahan Megaregency 1",
            "origin_lat_long": "-6.3823027,107.1162164",
            "destination_contact_name": "Fawwaz 2",
            "destination_contact_phone": "0857108194",
            "destination_address": "Perumahan Megaregency 2",
            "destination_lat_long": "-6.3772882,107.1062917",
            "phone_number": "085710819443"
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        delivery = requests.post(url_delivery, data=param3, headers=headers3)

        verify_status = delivery.json().get('success')
        verify_message = delivery.json().get('message')['order_items.0.qty']

        assert delivery.status_code == 422
        assert verify_status == bool(False)
        assert "order_items.0.qty harus berupa angka." in verify_message

    def test_OD_qty_minus_value(self):
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
            "payment_method_id": "1",
            "is_lunchbox": "0",
            "donation_price": "2500",
            "voucher_id": "62",
            "order_items[0][qty]": "-5",
            "order_items[0][stock_id]": discover.json().get('data')['nearby_menu'][0]['stock_id'],
            "address": "Megaregency",
            "note": "Test Notes",
            "delivery_price": "20000",
            "delivery_method": "Instant",
            "origin_contact_name": "Fawwaz 1",
            "origin_contact_phone": "081386356616",
            "origin_address": "Perumahan Megaregency 1",
            "origin_lat_long": "-6.3823027,107.1162164",
            "destination_contact_name": "Fawwaz 2",
            "destination_contact_phone": "0857108194",
            "destination_address": "Perumahan Megaregency 2",
            "destination_lat_long": "-6.3772882,107.1062917",
            "phone_number": "085710819443"
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        delivery = requests.post(url_delivery, data=param3, headers=headers3)

        verify_status = delivery.json().get('success')
        verify_message = delivery.json().get('message')['order_items.0.qty']

        assert delivery.status_code == 422
        assert verify_status == bool(False)
        assert "order_items.0.qty harus diantara 1 dan 999" in verify_message

    def test_OD_qty_kurang_stock(self):
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
            "payment_method_id": "1",
            "is_lunchbox": "0",
            "donation_price": "2500",
            "voucher_id": "62",
            "order_items[0][qty]": "999",
            "order_items[0][stock_id]": discover.json().get('data')['nearby_menu'][0]['stock_id'],
            "address": "Megaregency",
            "note": "Test Notes",
            "delivery_price": "20000",
            "delivery_method": "Instant",
            "origin_contact_name": "Fawwaz 1",
            "origin_contact_phone": "081386356616",
            "origin_address": "Perumahan Megaregency 1",
            "origin_lat_long": "-6.3823027,107.1162164",
            "destination_contact_name": "Fawwaz 2",
            "destination_contact_phone": "0857108194",
            "destination_address": "Perumahan Megaregency 2",
            "destination_lat_long": "-6.3772882,107.1062917",
            "phone_number": "085710819443"
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        delivery = requests.post(url_delivery, data=param3, headers=headers3)

        verify_status = delivery.json().get('success')
        verify_message = delivery.json().get('message')[0]['message']

        assert delivery.status_code == 422
        assert verify_status == bool(False)
        assert "tidak tersedia" in verify_message

    def test_OD_without_param_note(self):
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
            "payment_method_id": "1",
            "is_lunchbox": "0",
            "donation_price": "2500",
            "voucher_id": "62",
            "order_items[0][qty]": "1",
            "order_items[0][stock_id]": discover.json().get('data')['nearby_menu'][0]['stock_id'],
            "address": "Megaregency",
            # "note": "Test Notes",
            "delivery_price": "20000",
            "delivery_method": "Instant",
            "origin_contact_name": "Fawwaz 1",
            "origin_contact_phone": "081386356616",
            "origin_address": "Perumahan Megaregency 1",
            "origin_lat_long": "-6.3823027,107.1162164",
            "destination_contact_name": "Fawwaz 2",
            "destination_contact_phone": "0857108194",
            "destination_address": "Perumahan Megaregency 2",
            "destination_lat_long": "-6.3772882,107.1062917",
            "phone_number": "085710819443"
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        delivery = requests.post(url_delivery, data=param3, headers=headers3)

        verify_status = delivery.json().get('success')
        verify_message = delivery.json().get('message')

        assert delivery.status_code == 500
        assert verify_status == bool(False)
        assert "Aduh!" in verify_message

    def test_OD_note_empty_value(self):
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
            "payment_method_id": "1",
            "is_lunchbox": "0",
            "donation_price": "2500",
            "voucher_id": "62",
            "order_items[0][qty]": "1",
            "order_items[0][stock_id]": discover.json().get('data')['nearby_menu'][0]['stock_id'],
            "address": "Megaregency",
            "note": "",
            "delivery_price": "20000",
            "delivery_method": "Instant",
            "origin_contact_name": "Fawwaz 1",
            "origin_contact_phone": "081386356616",
            "origin_address": "Perumahan Megaregency 1",
            "origin_lat_long": "-6.3823027,107.1162164",
            "destination_contact_name": "Fawwaz 2",
            "destination_contact_phone": "0857108194",
            "destination_address": "Perumahan Megaregency 2",
            "destination_lat_long": "-6.3772882,107.1062917",
            "phone_number": "085710819443"
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        delivery = requests.post(url_delivery, data=param3, headers=headers3)

        verify_status = delivery.json().get('success')
        verify_message = delivery.json().get('message')

        assert delivery.status_code == 201
        assert verify_status == bool(True)
        assert "Order Delivery berhasil dibuat" in verify_message

    def test_OD_address_empty_value(self):
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
            "payment_method_id": "1",
            "is_lunchbox": "0",
            "donation_price": "2500",
            "voucher_id": "62",
            "order_items[0][qty]": "1",
            "order_items[0][stock_id]": discover.json().get('data')['nearby_menu'][0]['stock_id'],
            "address": "",
            "note": "hai",
            "delivery_price": "20000",
            "delivery_method": "Instant",
            "origin_contact_name": "Fawwaz 1",
            "origin_contact_phone": "081386356616",
            "origin_address": "Perumahan Megaregency 1",
            "origin_lat_long": "-6.3823027,107.1162164",
            "destination_contact_name": "Fawwaz 2",
            "destination_contact_phone": "0857108194",
            "destination_address": "Perumahan Megaregency 2",
            "destination_lat_long": "-6.3772882,107.1062917",
            "phone_number": "085710819443"
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        delivery = requests.post(url_delivery, data=param3, headers=headers3)

        verify_status = delivery.json().get('success')
        verify_message = delivery.json().get('message')['address']

        assert delivery.status_code == 422
        assert verify_status == bool(False)
        assert "Alamat tidak boleh kosong." in verify_message

    def test_OD_without_param_address(self):
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
            "payment_method_id": "1",
            "is_lunchbox": "0",
            "donation_price": "2500",
            "voucher_id": "62",
            "order_items[0][qty]": "1",
            "order_items[0][stock_id]": discover.json().get('data')['nearby_menu'][0]['stock_id'],
            # "address": "",
            "note": "hai",
            "delivery_price": "20000",
            "delivery_method": "Instant",
            "origin_contact_name": "Fawwaz 1",
            "origin_contact_phone": "081386356616",
            "origin_address": "Perumahan Megaregency 1",
            "origin_lat_long": "-6.3823027,107.1162164",
            "destination_contact_name": "Fawwaz 2",
            "destination_contact_phone": "0857108194",
            "destination_address": "Perumahan Megaregency 2",
            "destination_lat_long": "-6.3772882,107.1062917",
            "phone_number": "085710819443"
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        delivery = requests.post(url_delivery, data=param3, headers=headers3)

        verify_status = delivery.json().get('success')
        verify_message = delivery.json().get('message')['address']

        assert delivery.status_code == 422
        assert verify_status == bool(False)
        assert "Alamat tidak boleh kosong." in verify_message

    def test_OD_price_empty_value(self):
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
            "payment_method_id": "1",
            "is_lunchbox": "0",
            "donation_price": "2500",
            "voucher_id": "62",
            "order_items[0][qty]": "1",
            "order_items[0][stock_id]": discover.json().get('data')['nearby_menu'][0]['stock_id'],
            "address": "Megaregency",
            "note": "hai",
            "delivery_price": "",
            "delivery_method": "Instant",
            "origin_contact_name": "Fawwaz 1",
            "origin_contact_phone": "081386356616",
            "origin_address": "Perumahan Megaregency 1",
            "origin_lat_long": "-6.3823027,107.1162164",
            "destination_contact_name": "Fawwaz 2",
            "destination_contact_phone": "0857108194",
            "destination_address": "Perumahan Megaregency 2",
            "destination_lat_long": "-6.3772882,107.1062917",
            "phone_number": "085710819443"
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        delivery = requests.post(url_delivery, data=param3, headers=headers3)

        verify_status = delivery.json().get('success')
        verify_message = delivery.json().get('message')['delivery_price']

        assert delivery.status_code == 422
        assert verify_status == bool(False)
        assert "Ongkos kirim tidak boleh kosong." in verify_message

        print(delivery.json())

    def test_OD_without_param_price(self):
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
            "payment_method_id": "1",
            "is_lunchbox": "0",
            "donation_price": "2500",
            "voucher_id": "62",
            "order_items[0][qty]": "1",
            "order_items[0][stock_id]": discover.json().get('data')['nearby_menu'][0]['stock_id'],
            "address": "Megaregency",
            "note": "hai",
            # "delivery_price": "",
            "delivery_method": "Instant",
            "origin_contact_name": "Fawwaz 1",
            "origin_contact_phone": "081386356616",
            "origin_address": "Perumahan Megaregency 1",
            "origin_lat_long": "-6.3823027,107.1162164",
            "destination_contact_name": "Fawwaz 2",
            "destination_contact_phone": "0857108194",
            "destination_address": "Perumahan Megaregency 2",
            "destination_lat_long": "-6.3772882,107.1062917",
            "phone_number": "085710819443"
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        delivery = requests.post(url_delivery, data=param3, headers=headers3)

        verify_status = delivery.json().get('success')
        verify_message = delivery.json().get('message')['delivery_price']

        assert delivery.status_code == 422
        assert verify_status == bool(False)
        assert "Ongkos kirim tidak boleh kosong." in verify_message

        print(delivery.json())

    def test_OD_price_text_value(self):
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
            "payment_method_id": "1",
            "is_lunchbox": "0",
            "donation_price": "2500",
            "voucher_id": "62",
            "order_items[0][qty]": "1",
            "order_items[0][stock_id]": discover.json().get('data')['nearby_menu'][0]['stock_id'],
            "address": "Megaregency",
            "note": "hai",
            "delivery_price": "aaa",
            "delivery_method": "Instant",
            "origin_contact_name": "Fawwaz 1",
            "origin_contact_phone": "081386356616",
            "origin_address": "Perumahan Megaregency 1",
            "origin_lat_long": "-6.3823027,107.1162164",
            "destination_contact_name": "Fawwaz 2",
            "destination_contact_phone": "0857108194",
            "destination_address": "Perumahan Megaregency 2",
            "destination_lat_long": "-6.3772882,107.1062917",
            "phone_number": "085710819443"
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        delivery = requests.post(url_delivery, data=param3, headers=headers3)

        verify_status = delivery.json().get('success')
        verify_message = delivery.json().get('message')['delivery_price']

        assert delivery.status_code == 422
        assert verify_status == bool(False)
        assert "Ongkos kirim harus berupa angka." in verify_message

    def test_OD_price_wrong_format(self):
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
            "payment_method_id": "1",
            "is_lunchbox": "0",
            "donation_price": "2500",
            "voucher_id": "62",
            "order_items[0][qty]": "1",
            "order_items[0][stock_id]": discover.json().get('data')['nearby_menu'][0]['stock_id'],
            "address": "Megaregency",
            "note": "hai",
            "delivery_price": "19:00",
            "delivery_method": "Instant",
            "origin_contact_name": "Fawwaz 1",
            "origin_contact_phone": "081386356616",
            "origin_address": "Perumahan Megaregency 1",
            "origin_lat_long": "-6.3823027,107.1162164",
            "destination_contact_name": "Fawwaz 2",
            "destination_contact_phone": "0857108194",
            "destination_address": "Perumahan Megaregency 2",
            "destination_lat_long": "-6.3772882,107.1062917",
            "phone_number": "085710819443"
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        delivery = requests.post(url_delivery, data=param3, headers=headers3)

        verify_status = delivery.json().get('success')
        verify_message = delivery.json().get('message')['delivery_price']

        assert delivery.status_code == 422
        assert verify_status == bool(False)
        assert "Ongkos kirim harus berupa angka." in verify_message

    def test_price_minus_value(self):
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
            "payment_method_id": "1",
            "is_lunchbox": "0",
            "donation_price": "2500",
            "voucher_id": "62",
            "order_items[0][qty]": "1",
            "order_items[0][stock_id]": discover.json().get('data')['nearby_menu'][0]['stock_id'],
            "address": "Megaregency",
            "note": "hai",
            "delivery_price": "-20000",
            "delivery_method": "Instant",
            "origin_contact_name": "Fawwaz 1",
            "origin_contact_phone": "081386356616",
            "origin_address": "Perumahan Megaregency 1",
            "origin_lat_long": "-6.3823027,107.1162164",
            "destination_contact_name": "Fawwaz 2",
            "destination_contact_phone": "0857108194",
            "destination_address": "Perumahan Megaregency 2",
            "destination_lat_long": "-6.3772882,107.1062917",
            "phone_number": "085710819443"
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        delivery = requests.post(url_delivery, data=param3, headers=headers3)

        verify_status = delivery.json().get('success')
        verify_message = delivery.json().get('message')

        assert delivery.status_code == 500
        assert verify_status == bool(False)
        assert "Aduh!" in verify_message

    def test_OD_methode_empty_value(self):
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
            "payment_method_id": "1",
            "is_lunchbox": "0",
            "donation_price": "2500",
            "voucher_id": "62",
            "order_items[0][qty]": "1",
            "order_items[0][stock_id]": discover.json().get('data')['nearby_menu'][0]['stock_id'],
            "address": "Megaregency",
            "note": "hai",
            "delivery_price": "20000",
            "delivery_method": "",
            "origin_contact_name": "Fawwaz 1",
            "origin_contact_phone": "081386356616",
            "origin_address": "Perumahan Megaregency 1",
            "origin_lat_long": "-6.3823027,107.1162164",
            "destination_contact_name": "Fawwaz 2",
            "destination_contact_phone": "0857108194",
            "destination_address": "Perumahan Megaregency 2",
            "destination_lat_long": "-6.3772882,107.1062917",
            "phone_number": "085710819443"
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        delivery = requests.post(url_delivery, data=param3, headers=headers3)

        verify_status = delivery.json().get('success')
        verify_message = delivery.json().get('message')['delivery_method']

        assert delivery.status_code == 422
        assert verify_status == bool(False)
        assert "Metode pengiriman tidak boleh kosong." in verify_message

    def test_OD_without_param_methode(self):
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
            "payment_method_id": "1",
            "is_lunchbox": "0",
            "donation_price": "2500",
            "voucher_id": "62",
            "order_items[0][qty]": "1",
            "order_items[0][stock_id]": discover.json().get('data')['nearby_menu'][0]['stock_id'],
            "address": "Megaregency",
            "note": "hai",
            "delivery_price": "20000",
            # "delivery_method": "",
            "origin_contact_name": "Fawwaz 1",
            "origin_contact_phone": "081386356616",
            "origin_address": "Perumahan Megaregency 1",
            "origin_lat_long": "-6.3823027,107.1162164",
            "destination_contact_name": "Fawwaz 2",
            "destination_contact_phone": "0857108194",
            "destination_address": "Perumahan Megaregency 2",
            "destination_lat_long": "-6.3772882,107.1062917",
            "phone_number": "085710819443"
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        delivery = requests.post(url_delivery, data=param3, headers=headers3)

        verify_status = delivery.json().get('success')
        verify_message = delivery.json().get('message')['delivery_method']

        assert delivery.status_code == 422
        assert verify_status == bool(False)
        assert "Metode pengiriman tidak boleh kosong." in verify_message

    def test_OD_methode_not_found(self):
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
            "payment_method_id": "1",
            "is_lunchbox": "0",
            "donation_price": "2500",
            "voucher_id": "62",
            "order_items[0][qty]": "1",
            "order_items[0][stock_id]": discover.json().get('data')['nearby_menu'][0]['stock_id'],
            "address": "Megaregency",
            "note": "hai",
            "delivery_price": "20000",
            "delivery_method": "AOI",
            "origin_contact_name": "Fawwaz 1",
            "origin_contact_phone": "081386356616",
            "origin_address": "Perumahan Megaregency 1",
            "origin_lat_long": "-6.3823027,107.1162164",
            "destination_contact_name": "Fawwaz 2",
            "destination_contact_phone": "0857108194",
            "destination_address": "Perumahan Megaregency 2",
            "destination_lat_long": "-6.3772882,107.1062917",
            "phone_number": "085710819443"
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        delivery = requests.post(url_delivery, data=param3, headers=headers3)

        verify_status = delivery.json().get('success')
        verify_message = delivery.json().get('message')['delivery_method']

        assert delivery.status_code == 422
        assert verify_status == bool(False)
        assert "Metode pengiriman yang dipilih tidak tersedia." in verify_message

    def test_OD_origin_contact_name_empty_value(self):
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
            "payment_method_id": "1",
            "is_lunchbox": "0",
            "donation_price": "2500",
            "voucher_id": "62",
            "order_items[0][qty]": "1",
            "order_items[0][stock_id]": discover.json().get('data')['nearby_menu'][0]['stock_id'],
            "address": "Megaregency",
            "note": "hai",
            "delivery_price": "20000",
            "delivery_method": "Instant",
            "origin_contact_name": "",
            "origin_contact_phone": "081386356616",
            "origin_address": "Perumahan Megaregency 1",
            "origin_lat_long": "-6.3823027,107.1162164",
            "destination_contact_name": "Fawwaz 2",
            "destination_contact_phone": "0857108194",
            "destination_address": "Perumahan Megaregency 2",
            "destination_lat_long": "-6.3772882,107.1062917",
            "phone_number": "085710819443"
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        delivery = requests.post(url_delivery, data=param3, headers=headers3)

        verify_status = delivery.json().get('success')
        verify_message = delivery.json().get('message')['origin_contact_name']

        assert delivery.status_code == 422
        assert verify_status == bool(False)
        assert "Nama toko tidak boleh kosong." in verify_message

    def test_OD_without_param_origin_contact_name(self):
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
            "payment_method_id": "1",
            "is_lunchbox": "0",
            "donation_price": "2500",
            "voucher_id": "62",
            "order_items[0][qty]": "1",
            "order_items[0][stock_id]": discover.json().get('data')['nearby_menu'][0]['stock_id'],
            "address": "Megaregency",
            "note": "hai",
            "delivery_price": "20000",
            # "delivery_method": "Instant",
            "origin_contact_name": "",
            "origin_contact_phone": "081386356616",
            "origin_address": "Perumahan Megaregency 1",
            "origin_lat_long": "-6.3823027,107.1162164",
            "destination_contact_name": "Fawwaz 2",
            "destination_contact_phone": "0857108194",
            "destination_address": "Perumahan Megaregency 2",
            "destination_lat_long": "-6.3772882,107.1062917",
            "phone_number": "085710819443"
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        delivery = requests.post(url_delivery, data=param3, headers=headers3)

        verify_status = delivery.json().get('success')
        verify_message = delivery.json().get('message')['origin_contact_name']

        assert delivery.status_code == 422
        assert verify_status == bool(False)
        assert "Nama toko tidak boleh kosong." in verify_message

    def test_OD_origin_contact_phone_empty_value(self):
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
            "payment_method_id": "1",
            "is_lunchbox": "0",
            "donation_price": "2500",
            "voucher_id": "62",
            "order_items[0][qty]": "1",
            "order_items[0][stock_id]": discover.json().get('data')['nearby_menu'][0]['stock_id'],
            "address": "Megaregency",
            "note": "hai",
            "delivery_price": "20000",
            "delivery_method": "Instant",
            "origin_contact_name": "Fawwa 1",
            "origin_contact_phone": "",
            "origin_address": "Perumahan Megaregency 1",
            "origin_lat_long": "-6.3823027,107.1162164",
            "destination_contact_name": "Fawwaz 2",
            "destination_contact_phone": "0857108194",
            "destination_address": "Perumahan Megaregency 2",
            "destination_lat_long": "-6.3772882,107.1062917",
            "phone_number": "085710819443"
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        delivery = requests.post(url_delivery, data=param3, headers=headers3)

        verify_status = delivery.json().get('success')
        verify_message = delivery.json().get('message')['origin_contact_phone']

        assert delivery.status_code == 422
        assert verify_status == bool(False)
        assert "No. HP toko tidak boleh kosong." in verify_message

    def test_OD_without_param_origin_contact_phone (self):
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
            "payment_method_id": "1",
            "is_lunchbox": "0",
            "donation_price": "2500",
            "voucher_id": "62",
            "order_items[0][qty]": "1",
            "order_items[0][stock_id]": discover.json().get('data')['nearby_menu'][0]['stock_id'],
            "address": "Megaregency",
            "note": "hai",
            "delivery_price": "20000",
            "delivery_method": "Instant",
            "origin_contact_name": "Fawwa 1",
            # "origin_contact_phone": "",
            "origin_address": "Perumahan Megaregency 1",
            "origin_lat_long": "-6.3823027,107.1162164",
            "destination_contact_name": "Fawwaz 2",
            "destination_contact_phone": "0857108194",
            "destination_address": "Perumahan Megaregency 2",
            "destination_lat_long": "-6.3772882,107.1062917",
            "phone_number": "085710819443"
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        delivery = requests.post(url_delivery, data=param3, headers=headers3)

        verify_status = delivery.json().get('success')
        verify_message = delivery.json().get('message')['origin_contact_phone']

        assert delivery.status_code == 422
        assert verify_status == bool(False)
        assert "No. HP toko tidak boleh kosong." in verify_message

    def test_OD_origin_contact_phone_text_value(self):
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
            "payment_method_id": "1",
            "is_lunchbox": "0",
            "donation_price": "2500",
            "voucher_id": "62",
            "order_items[0][qty]": "1",
            "order_items[0][stock_id]": discover.json().get('data')['nearby_menu'][0]['stock_id'],
            "address": "Megaregency",
            "note": "hai",
            "delivery_price": "20000",
            "delivery_method": "Instant",
            "origin_contact_name": "Fawwa 1",
            "origin_contact_phone": "aaa",
            "origin_address": "Perumahan Megaregency 1",
            "origin_lat_long": "-6.3823027,107.1162164",
            "destination_contact_name": "Fawwaz 2",
            "destination_contact_phone": "0857108194",
            "destination_address": "Perumahan Megaregency 2",
            "destination_lat_long": "-6.3772882,107.1062917",
            "phone_number": "085710819443"
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        delivery = requests.post(url_delivery, data=param3, headers=headers3)

        verify_status = delivery.json().get('success')
        verify_message = delivery.json().get('message')['origin_contact_phone']

        assert delivery.status_code == 422
        assert verify_status == bool(False)
        assert "The No. HP toko format wrong." in verify_message

    def test_OD_origin_address_empty_value(self):
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
            "payment_method_id": "1",
            "is_lunchbox": "0",
            "donation_price": "2500",
            "voucher_id": "62",
            "order_items[0][qty]": "1",
            "order_items[0][stock_id]": discover.json().get('data')['nearby_menu'][0]['stock_id'],
            "address": "Megaregency",
            "note": "hai",
            "delivery_price": "20000",
            "delivery_method": "Instant",
            "origin_contact_name": "Fawwa 1",
            "origin_contact_phone": "081386356616",
            "origin_address": "",
            "origin_lat_long": "-6.3823027,107.1162164",
            "destination_contact_name": "Fawwaz 2",
            "destination_contact_phone": "0857108194",
            "destination_address": "Perumahan Megaregency 2",
            "destination_lat_long": "-6.3772882,107.1062917",
            "phone_number": "085710819443"
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        delivery = requests.post(url_delivery, data=param3, headers=headers3)

        verify_status = delivery.json().get('success')
        verify_message = delivery.json().get('message')['origin_address']

        assert delivery.status_code == 422
        assert verify_status == bool(False)
        assert "Alamat toko tidak boleh kosong." in verify_message

    def test_OD_without_param_origin_address(self):
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
            "payment_method_id": "1",
            "is_lunchbox": "0",
            "donation_price": "2500",
            "voucher_id": "62",
            "order_items[0][qty]": "1",
            "order_items[0][stock_id]": discover.json().get('data')['nearby_menu'][0]['stock_id'],
            "address": "Megaregency",
            "note": "hai",
            "delivery_price": "20000",
            "delivery_method": "Instant",
            "origin_contact_name": "Fawwa 1",
            "origin_contact_phone": "081386356616",
            # "origin_address": "",
            "origin_lat_long": "-6.3823027,107.1162164",
            "destination_contact_name": "Fawwaz 2",
            "destination_contact_phone": "0857108194",
            "destination_address": "Perumahan Megaregency 2",
            "destination_lat_long": "-6.3772882,107.1062917",
            "phone_number": "085710819443"
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        delivery = requests.post(url_delivery, data=param3, headers=headers3)

        verify_status = delivery.json().get('success')
        verify_message = delivery.json().get('message')['origin_address']

        assert delivery.status_code == 422
        assert verify_status == bool(False)
        assert "Alamat toko tidak boleh kosong." in verify_message

    def test_OD_origin_address_value_kurang_10(self):
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
            "payment_method_id": "1",
            "is_lunchbox": "0",
            "donation_price": "2500",
            "voucher_id": "62",
            "order_items[0][qty]": "1",
            "order_items[0][stock_id]": discover.json().get('data')['nearby_menu'][0]['stock_id'],
            "address": "Megaregency",
            "note": "hai",
            "delivery_price": "20000",
            "delivery_method": "Instant",
            "origin_contact_name": "Fawwa 1",
            "origin_contact_phone": "081386356616",
            "origin_address": "a",
            "origin_lat_long": "-6.3823027,107.1162164",
            "destination_contact_name": "Fawwaz 2",
            "destination_contact_phone": "0857108194",
            "destination_address": "Perumahan Megaregency 2",
            "destination_lat_long": "-6.3772882,107.1062917",
            "phone_number": "085710819443"
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        delivery = requests.post(url_delivery, data=param3, headers=headers3)

        verify_status = delivery.json().get('success')
        verify_message = delivery.json().get('message')['origin_address']

        assert delivery.status_code == 422
        assert verify_status == bool(False)
        assert "Alamat toko setidaknya harus 10 karakter." in verify_message

    def test_OD_origin_latlong_empty_value(self):
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
            "payment_method_id": "1",
            "is_lunchbox": "0",
            "donation_price": "2500",
            "voucher_id": "62",
            "order_items[0][qty]": "1",
            "order_items[0][stock_id]": discover.json().get('data')['nearby_menu'][0]['stock_id'],
            "address": "Megaregency",
            "note": "hai",
            "delivery_price": "20000",
            "delivery_method": "Instant",
            "origin_contact_name": "Fawwa 1",
            "origin_contact_phone": "081386356616",
            "origin_address": "Perumahan Megaregency 1",
            "origin_lat_long": "",
            "destination_contact_name": "Fawwaz 2",
            "destination_contact_phone": "0857108194",
            "destination_address": "Perumahan Megaregency 2",
            "destination_lat_long": "-6.3772882,107.1062917",
            "phone_number": "085710819443"
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        delivery = requests.post(url_delivery, data=param3, headers=headers3)

        verify_status = delivery.json().get('success')
        verify_message = delivery.json().get('message')['origin_lat_long']

        assert delivery.status_code == 422
        assert verify_status == bool(False)
        assert "Titik lokasi toko tidak boleh kosong." in verify_message

    def test_OD_without_param_origin_lat_long(self):
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
            "payment_method_id": "1",
            "is_lunchbox": "0",
            "donation_price": "2500",
            "voucher_id": "62",
            "order_items[0][qty]": "1",
            "order_items[0][stock_id]": discover.json().get('data')['nearby_menu'][0]['stock_id'],
            "address": "Megaregency",
            "note": "hai",
            "delivery_price": "20000",
            "delivery_method": "Instant",
            "origin_contact_name": "Fawwa 1",
            "origin_contact_phone": "081386356616",
            "origin_address": "Perumahan Megaregency 1",
            # "origin_lat_long": "",
            "destination_contact_name": "Fawwaz 2",
            "destination_contact_phone": "0857108194",
            "destination_address": "Perumahan Megaregency 2",
            "destination_lat_long": "-6.3772882,107.1062917",
            "phone_number": "085710819443"
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        delivery = requests.post(url_delivery, data=param3, headers=headers3)

        verify_status = delivery.json().get('success')
        verify_message = delivery.json().get('message')['origin_lat_long']

        assert delivery.status_code == 422
        assert verify_status == bool(False)
        assert "Titik lokasi toko tidak boleh kosong." in verify_message

    def test_OD_origin_latlong_text_value(self):
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
            "payment_method_id": "1",
            "is_lunchbox": "0",
            "donation_price": "2500",
            "voucher_id": "62",
            "order_items[0][qty]": "1",
            "order_items[0][stock_id]": discover.json().get('data')['nearby_menu'][0]['stock_id'],
            "address": "Megaregency",
            "note": "hai",
            "delivery_price": "20000",
            "delivery_method": "Instant",
            "origin_contact_name": "Fawwa 1",
            "origin_contact_phone": "081386356616",
            "origin_address": "Perumahan Megaregency 1",
            "origin_lat_long": "aaa",
            "destination_contact_name": "Fawwaz 2",
            "destination_contact_phone": "0857108194",
            "destination_address": "Perumahan Megaregency 2",
            "destination_lat_long": "-6.3772882,107.1062917",
            "phone_number": "085710819443"
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        delivery = requests.post(url_delivery, data=param3, headers=headers3)

        verify_status = delivery.json().get('success')
        verify_message = delivery.json().get('message')['origin_lat_long']

        assert delivery.status_code == 422
        assert verify_status == bool(False)
        assert "The Titik lokasi toko must be latitude and longitude." in verify_message

    def test_OD_origin_latlong_wrong_format_value(self):
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
            "payment_method_id": "1",
            "is_lunchbox": "0",
            "donation_price": "2500",
            "voucher_id": "62",
            "order_items[0][qty]": "1",
            "order_items[0][stock_id]": discover.json().get('data')['nearby_menu'][0]['stock_id'],
            "address": "Megaregency",
            "note": "hai",
            "delivery_price": "20000",
            "delivery_method": "Instant",
            "origin_contact_name": "Fawwa 1",
            "origin_contact_phone": "081386356616",
            "origin_address": "Perumahan Megaregency 1",
            "origin_lat_long": "19:00",
            "destination_contact_name": "Fawwaz 2",
            "destination_contact_phone": "0857108194",
            "destination_address": "Perumahan Megaregency 2",
            "destination_lat_long": "-6.3772882,107.1062917",
            "phone_number": "085710819443"
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        delivery = requests.post(url_delivery, data=param3, headers=headers3)

        verify_status = delivery.json().get('success')
        verify_message = delivery.json().get('message')['origin_lat_long']

        assert delivery.status_code == 422
        assert verify_status == bool(False)
        assert "The Titik lokasi toko must be latitude and longitude." in verify_message

    def test_OD_destination_contact_name_empty_value(self):
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
            "payment_method_id": "1",
            "is_lunchbox": "0",
            "donation_price": "2500",
            "voucher_id": "62",
            "order_items[0][qty]": "1",
            "order_items[0][stock_id]": discover.json().get('data')['nearby_menu'][0]['stock_id'],
            "address": "Megaregency",
            "note": "hai",
            "delivery_price": "20000",
            "delivery_method": "Instant",
            "origin_contact_name": "Fawwa 1",
            "origin_contact_phone": "081386356616",
            "origin_address": "Perumahan Megaregency 1",
            "origin_lat_long": "-6.3772882,107.1062917",
            "destination_contact_name": "",
            "destination_contact_phone": "0857108194",
            "destination_address": "Perumahan Megaregency 2",
            "destination_lat_long": "-6.3772882,107.1062917",
            "phone_number": "085710819443"
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        delivery = requests.post(url_delivery, data=param3, headers=headers3)

        verify_status = delivery.json().get('success')
        verify_message = delivery.json().get('message')['destination_contact_name']

        assert delivery.status_code == 422
        assert verify_status == bool(False)
        assert "Nama penerima tidak boleh kosong." in verify_message

    def test_OD_without_param_destination_contact_name(self):
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
            "payment_method_id": "1",
            "is_lunchbox": "0",
            "donation_price": "2500",
            "voucher_id": "62",
            "order_items[0][qty]": "1",
            "order_items[0][stock_id]": discover.json().get('data')['nearby_menu'][0]['stock_id'],
            "address": "Megaregency",
            "note": "hai",
            "delivery_price": "20000",
            "delivery_method": "Instant",
            "origin_contact_name": "Fawwa 1",
            "origin_contact_phone": "081386356616",
            "origin_address": "Perumahan Megaregency 1",
            "origin_lat_long": "-6.3772882,107.1062917",
            # "destination_contact_name": "Fawwaz 2",
            "destination_contact_phone": "0857108194",
            "destination_address": "Perumahan Megaregency 2",
            "destination_lat_long": "-6.3772882,107.1062917",
            "phone_number": "085710819443"
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        delivery = requests.post(url_delivery, data=param3, headers=headers3)

        verify_status = delivery.json().get('success')
        verify_message = delivery.json().get('message')['destination_contact_name']

        assert delivery.status_code == 422
        assert verify_status == bool(False)
        assert "Nama penerima tidak boleh kosong." in verify_message

    def test_OD_destination_contact_phone_empty_value(self):
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
            "payment_method_id": "1",
            "is_lunchbox": "0",
            "donation_price": "2500",
            "voucher_id": "62",
            "order_items[0][qty]": "1",
            "order_items[0][stock_id]": discover.json().get('data')['nearby_menu'][0]['stock_id'],
            "address": "Megaregency",
            "note": "hai",
            "delivery_price": "20000",
            "delivery_method": "Instant",
            "origin_contact_name": "Fawwa 1",
            "origin_contact_phone": "081386356616",
            "origin_address": "Perumahan Megaregency 1",
            "origin_lat_long": "-6.3772882,107.1062917",
            "destination_contact_name": "Fawwaz 2",
            "destination_contact_phone": "",
            "destination_address": "Perumahan Megaregency 2",
            "destination_lat_long": "-6.3772882,107.1062917",
            "phone_number": "085710819443"
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        delivery = requests.post(url_delivery, data=param3, headers=headers3)

        verify_status = delivery.json().get('success')
        verify_message = delivery.json().get('message')['destination_contact_phone']

        assert delivery.status_code == 422
        assert verify_status == bool(False)
        assert "No. HP penerima tidak boleh kosong." in verify_message

    def test_OD_without_param_destination_contact_phone (self):
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
            "payment_method_id": "1",
            "is_lunchbox": "0",
            "donation_price": "2500",
            "voucher_id": "62",
            "order_items[0][qty]": "1",
            "order_items[0][stock_id]": discover.json().get('data')['nearby_menu'][0]['stock_id'],
            "address": "Megaregency",
            "note": "hai",
            "delivery_price": "20000",
            "delivery_method": "Instant",
            "origin_contact_name": "Fawwa 1",
            "origin_contact_phone": "081386356616",
            "origin_address": "Perumahan Megaregency 1",
            "origin_lat_long": "-6.3772882,107.1062917",
            "destination_contact_name": "Fawwaz 2",
            # "destination_contact_phone": "",
            "destination_address": "Perumahan Megaregency 2",
            "destination_lat_long": "-6.3772882,107.1062917",
            "phone_number": "085710819443"
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        delivery = requests.post(url_delivery, data=param3, headers=headers3)

        verify_status = delivery.json().get('success')
        verify_message = delivery.json().get('message')['destination_contact_phone']

        assert delivery.status_code == 422
        assert verify_status == bool(False)
        assert "No. HP penerima tidak boleh kosong." in verify_message

    def test_OD_destination_contact_phone_text_value(self):
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
            "payment_method_id": "1",
            "is_lunchbox": "0",
            "donation_price": "2500",
            "voucher_id": "62",
            "order_items[0][qty]": "1",
            "order_items[0][stock_id]": discover.json().get('data')['nearby_menu'][0]['stock_id'],
            "address": "Megaregency",
            "note": "hai",
            "delivery_price": "20000",
            "delivery_method": "Instant",
            "origin_contact_name": "Fawwa 1",
            "origin_contact_phone": "081386356616",
            "origin_address": "Perumahan Megaregency 1",
            "origin_lat_long": "-6.3772882,107.1062917",
            "destination_contact_name": "Fawwaz 2",
            "destination_contact_phone": "aaa",
            "destination_address": "Perumahan Megaregency 2",
            "destination_lat_long": "-6.3772882,107.1062917",
            "phone_number": "085710819443"
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        delivery = requests.post(url_delivery, data=param3, headers=headers3)

        verify_status = delivery.json().get('success')
        verify_message = delivery.json().get('message')['destination_contact_phone']

        assert delivery.status_code == 422
        assert verify_status == bool(False)
        assert "The No. HP penerima format wrong." in verify_message

    def test_OD_destination_address_empty_value(self):
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
            "payment_method_id": "1",
            "is_lunchbox": "0",
            "donation_price": "2500",
            "voucher_id": "62",
            "order_items[0][qty]": "1",
            "order_items[0][stock_id]": discover.json().get('data')['nearby_menu'][0]['stock_id'],
            "address": "Megaregency",
            "note": "hai",
            "delivery_price": "20000",
            "delivery_method": "Instant",
            "origin_contact_name": "Fawwa 1",
            "origin_contact_phone": "081386356616",
            "origin_address": "Perumahan Megaregency 1",
            "origin_lat_long": "-6.3772882,107.1062917",
            "destination_contact_name": "Fawwaz 2",
            "destination_contact_phone": "085710819443",
            "destination_address": "",
            "destination_lat_long": "-6.3772882,107.1062917",
            "phone_number": "085710819443"
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        delivery = requests.post(url_delivery, data=param3, headers=headers3)

        verify_status = delivery.json().get('success')
        verify_message = delivery.json().get('message')['destination_address']

        assert delivery.status_code == 422
        assert verify_status == bool(False)
        assert "Alamat penerima tidak boleh kosong." in verify_message

    def test_OD_without_param_destination_address(self):
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
            "payment_method_id": "1",
            "is_lunchbox": "0",
            "donation_price": "2500",
            "voucher_id": "62",
            "order_items[0][qty]": "1",
            "order_items[0][stock_id]": discover.json().get('data')['nearby_menu'][0]['stock_id'],
            "address": "Megaregency",
            "note": "hai",
            "delivery_price": "20000",
            "delivery_method": "Instant",
            "origin_contact_name": "Fawwa 1",
            "origin_contact_phone": "081386356616",
            "origin_address": "Perumahan Megaregency 1",
            "origin_lat_long": "-6.3772882,107.1062917",
            "destination_contact_name": "Fawwaz 2",
            "destination_contact_phone": "085710819443",
            # "destination_address": "",
            "destination_lat_long": "-6.3772882,107.1062917",
            "phone_number": "085710819443"
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        delivery = requests.post(url_delivery, data=param3, headers=headers3)

        verify_status = delivery.json().get('success')
        verify_message = delivery.json().get('message')['destination_address']

        assert delivery.status_code == 422
        assert verify_status == bool(False)
        assert "Alamat penerima tidak boleh kosong." in verify_message

    def test_OD_destination_address_value_kurang_10(self):
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
            "payment_method_id": "1",
            "is_lunchbox": "0",
            "donation_price": "2500",
            "voucher_id": "62",
            "order_items[0][qty]": "1",
            "order_items[0][stock_id]": discover.json().get('data')['nearby_menu'][0]['stock_id'],
            "address": "Megaregency",
            "note": "hai",
            "delivery_price": "20000",
            "delivery_method": "Instant",
            "origin_contact_name": "Fawwa 1",
            "origin_contact_phone": "081386356616",
            "origin_address": "Perumahan Megaregency 1",
            "origin_lat_long": "-6.3772882,107.1062917",
            "destination_contact_name": "Fawwaz 2",
            "destination_contact_phone": "085710819443",
            "destination_address": "a",
            "destination_lat_long": "-6.3772882,107.1062917",
            "phone_number": "085710819443"
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        delivery = requests.post(url_delivery, data=param3, headers=headers3)

        verify_status = delivery.json().get('success')
        verify_message = delivery.json().get('message')['destination_address']

        assert delivery.status_code == 422
        assert verify_status == bool(False)
        assert "Alamat penerima setidaknya harus 10 karakter." in verify_message

    def test_OD_destination_latlong_empty_value(self):
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
            "payment_method_id": "1",
            "is_lunchbox": "0",
            "donation_price": "2500",
            "voucher_id": "62",
            "order_items[0][qty]": "1",
            "order_items[0][stock_id]": discover.json().get('data')['nearby_menu'][0]['stock_id'],
            "address": "Megaregency",
            "note": "hai",
            "delivery_price": "20000",
            "delivery_method": "Instant",
            "origin_contact_name": "Fawwa 1",
            "origin_contact_phone": "081386356616",
            "origin_address": "Perumahan Megaregency 1",
            "origin_lat_long": "-6.3772882,107.1062917",
            "destination_contact_name": "Fawwaz 2",
            "destination_contact_phone": "085710819443",
            "destination_address": "Perumahan Megaregency 2",
            "destination_lat_long": "",
            "phone_number": "085710819443"
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        delivery = requests.post(url_delivery, data=param3, headers=headers3)

        verify_status = delivery.json().get('success')
        verify_message = delivery.json().get('message')['destination_lat_long']

        assert delivery.status_code == 422
        assert verify_status == bool(False)
        assert "Titik lokasi penerime tidak boleh kosong." in verify_message

    def test_OD_without_param_destination_latlong(self):
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
            "payment_method_id": "1",
            "is_lunchbox": "0",
            "donation_price": "2500",
            "voucher_id": "62",
            "order_items[0][qty]": "1",
            "order_items[0][stock_id]": discover.json().get('data')['nearby_menu'][0]['stock_id'],
            "address": "Megaregency",
            "note": "hai",
            "delivery_price": "20000",
            "delivery_method": "Instant",
            "origin_contact_name": "Fawwa 1",
            "origin_contact_phone": "081386356616",
            "origin_address": "Perumahan Megaregency 1",
            "origin_lat_long": "-6.3772882,107.1062917",
            "destination_contact_name": "Fawwaz 2",
            "destination_contact_phone": "085710819443",
            "destination_address": "Perumahan Megaregency 2",
            # "destination_lat_long": "",
            "phone_number": "085710819443"
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        delivery = requests.post(url_delivery, data=param3, headers=headers3)

        verify_status = delivery.json().get('success')
        verify_message = delivery.json().get('message')['destination_lat_long']

        assert delivery.status_code == 422
        assert verify_status == bool(False)
        assert "Titik lokasi penerime tidak boleh kosong." in verify_message

    def test_OD_destination_latlong_text_value(self):
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
            "payment_method_id": "1",
            "is_lunchbox": "0",
            "donation_price": "2500",
            "voucher_id": "62",
            "order_items[0][qty]": "1",
            "order_items[0][stock_id]": discover.json().get('data')['nearby_menu'][0]['stock_id'],
            "address": "Megaregency",
            "note": "hai",
            "delivery_price": "20000",
            "delivery_method": "Instant",
            "origin_contact_name": "Fawwa 1",
            "origin_contact_phone": "081386356616",
            "origin_address": "Perumahan Megaregency 1",
            "origin_lat_long": "-6.3772882,107.1062917",
            "destination_contact_name": "Fawwaz 2",
            "destination_contact_phone": "085710819443",
            "destination_address": "Perumahan Megaregency 2",
            "destination_lat_long": "aaa",
            "phone_number": "085710819443"
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        delivery = requests.post(url_delivery, data=param3, headers=headers3)

        verify_status = delivery.json().get('success')
        verify_message = delivery.json().get('message')['destination_lat_long']

        assert delivery.status_code == 422
        assert verify_status == bool(False)
        assert "The Titik lokasi penerime must be latitude and longitude." in verify_message

    def test_OD_destination_latlong_wrong_format_value(self):
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
            "payment_method_id": "1",
            "is_lunchbox": "0",
            "donation_price": "2500",
            "voucher_id": "62",
            "order_items[0][qty]": "1",
            "order_items[0][stock_id]": discover.json().get('data')['nearby_menu'][0]['stock_id'],
            "address": "Megaregency",
            "note": "hai",
            "delivery_price": "20000",
            "delivery_method": "Instant",
            "origin_contact_name": "Fawwa 1",
            "origin_contact_phone": "081386356616",
            "origin_address": "Perumahan Megaregency 1",
            "origin_lat_long": "-6.3772882,107.1062917",
            "destination_contact_name": "Fawwaz 2",
            "destination_contact_phone": "085710819443",
            "destination_address": "Perumahan Megaregency 2",
            "destination_lat_long": "19:00",
            "phone_number": "085710819443"
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        delivery = requests.post(url_delivery, data=param3, headers=headers3)

        verify_status = delivery.json().get('success')
        verify_message = delivery.json().get('message')['destination_lat_long']

        assert delivery.status_code == 422
        assert verify_status == bool(False)
        assert "The Titik lokasi penerime must be latitude and longitude." in verify_message

    def test_OD_phone_empty_value(self):
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
            "payment_method_id": "1",
            "is_lunchbox": "0",
            "donation_price": "2500",
            "voucher_id": "62",
            "order_items[0][qty]": "1",
            "order_items[0][stock_id]": discover.json().get('data')['nearby_menu'][0]['stock_id'],
            "address": "Megaregency",
            "note": "hai",
            "delivery_price": "20000",
            "delivery_method": "Instant",
            "origin_contact_name": "Fawwa 1",
            "origin_contact_phone": "081386356616",
            "origin_address": "Perumahan Megaregency 1",
            "origin_lat_long": "-6.3772882,107.1062917",
            "destination_contact_name": "Fawwaz 2",
            "destination_contact_phone": "085710819443",
            "destination_address": "Perumahan Megaregency 2",
            "destination_lat_long": "-6.3823027,107.1162164",
            "phone_number": ""
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        delivery = requests.post(url_delivery, data=param3, headers=headers3)

        verify_status = delivery.json().get('success')
        verify_message = delivery.json().get('message')['phone_number']

        assert delivery.status_code == 422
        assert verify_status == bool(False)
        assert "No. HP tidak boleh kosong ketika Metode Pembayaran adalah 1." in verify_message

    def test_OD_without_param_phone(self):
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
            "payment_method_id": "1",
            "is_lunchbox": "0",
            "donation_price": "2500",
            "voucher_id": "62",
            "order_items[0][qty]": "1",
            "order_items[0][stock_id]": discover.json().get('data')['nearby_menu'][0]['stock_id'],
            "address": "Megaregency",
            "note": "hai",
            "delivery_price": "20000",
            "delivery_method": "Instant",
            "origin_contact_name": "Fawwa 1",
            "origin_contact_phone": "081386356616",
            "origin_address": "Perumahan Megaregency 1",
            "origin_lat_long": "-6.3772882,107.1062917",
            "destination_contact_name": "Fawwaz 2",
            "destination_contact_phone": "085710819443",
            "destination_address": "Perumahan Megaregency 2",
            "destination_lat_long": "-6.3823027,107.1162164",
            # "phone_number": ""
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        delivery = requests.post(url_delivery, data=param3, headers=headers3)

        verify_status = delivery.json().get('success')
        verify_message = delivery.json().get('message')['phone_number']

        assert delivery.status_code == 422
        assert verify_status == bool(False)
        assert "No. HP tidak boleh kosong ketika Metode Pembayaran adalah 1." in verify_message

    def test_OD_phone_text_value(self):
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
            "payment_method_id": "1",
            "is_lunchbox": "0",
            "donation_price": "2500",
            "voucher_id": "62",
            "order_items[0][qty]": "1",
            "order_items[0][stock_id]": discover.json().get('data')['nearby_menu'][0]['stock_id'],
            "address": "Megaregency",
            "note": "hai",
            "delivery_price": "20000",
            "delivery_method": "Instant",
            "origin_contact_name": "Fawwa 1",
            "origin_contact_phone": "081386356616",
            "origin_address": "Perumahan Megaregency 1",
            "origin_lat_long": "-6.3772882,107.1062917",
            "destination_contact_name": "Fawwaz 2",
            "destination_contact_phone": "085710819443",
            "destination_address": "Perumahan Megaregency 2",
            "destination_lat_long": "-6.3823027,107.1162164",
            "phone_number": "aaa"
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        delivery = requests.post(url_delivery, data=param3, headers=headers3)

        verify_status = delivery.json().get('success')
        verify_message = delivery.json().get('message')['phone_number']

        assert delivery.status_code == 422
        assert verify_status == bool(False)
        assert "The No. HP format wrong." in verify_message

    def test_OD_phone_wrong_format_value(self):
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
            "payment_method_id": "1",
            "is_lunchbox": "0",
            "donation_price": "2500",
            "voucher_id": "62",
            "order_items[0][qty]": "1",
            "order_items[0][stock_id]": discover.json().get('data')['nearby_menu'][0]['stock_id'],
            "address": "Megaregency",
            "note": "hai",
            "delivery_price": "20000",
            "delivery_method": "Instant",
            "origin_contact_name": "Fawwa 1",
            "origin_contact_phone": "081386356616",
            "origin_address": "Perumahan Megaregency 1",
            "origin_lat_long": "-6.3772882,107.1062917",
            "destination_contact_name": "Fawwaz 2",
            "destination_contact_phone": "085710819443",
            "destination_address": "Perumahan Megaregency 2",
            "destination_lat_long": "-6.3823027,107.1162164",
            "phone_number": "19:00"
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        delivery = requests.post(url_delivery, data=param3, headers=headers3)

        verify_status = delivery.json().get('success')
        verify_message = delivery.json().get('message')['phone_number']

        assert delivery.status_code == 422
        assert verify_status == bool(False)
        assert "The No. HP format wrong." in verify_message






