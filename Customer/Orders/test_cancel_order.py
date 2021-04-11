import requests
from env import stagging
from pprint import pprint
from assertpy import assert_that


class TestCustomerOrdersCancelOrder:

    global setting_env,url_login,url_discover,url_delivery_order,url_cancel_order,email,kata_sandi,longitude,latitude,wrong_token

    setting_env = stagging
    url_login = f"{setting_env}/api/v2/customer/auth/login/email"
    url_discover = f"{setting_env}/api/v2/customer/discover"
    url_delivery_order = f"{setting_env}/api/v2/customer/orders/delivery"
    url_cancel_order = f"{setting_env}/api/v2/customer/orders/"
    email = "kopiruangvirtual@gmail.com"
    kata_sandi = '12345678'
    longitude = '107.1162607'
    latitude = '-6.3823317'
    wrong_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvc3RhZ2luZy5hZG1pbnN1cnBsdXMubmV0XC9hcGlcL3YyXC9jdXN0b21lclwvYXV0aFwvbG9naW5cL2VtYWlsIiwiaWF0IjoxNjE2ODA1NzI2LCJleHAiOjE2MTkzOTc3MjYsIm5iZiI6MTYxNjgwNTcyNiwianRpIjoib05ESmxFRE5hSzNrN2RtVyIsInN1YiI6NDEyNiwicHJ2IjoiMjc0MTA1ZGE2ZTk1YmVmMjgwNzc4NmRkODczODg2N2NmOWMwMmFhYiJ9.fj51xIfQrqleRvdSJUbWcdrvsxQPUn8HpccnOmTgPDI'

    def test_order_cancel_normal(self):
        param = {
            'email': email,
            'password': kata_sandi
        }
        headers = {
            "Accept": "application/json"
        }
        login = requests.post(url_login, params=param, headers=headers)
        param2 = {
            'latitude': latitude,
            'longitude': longitude
        }
        headers2 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        discover = requests.get(url_discover, params=param2, headers=headers2)
        param3 = {
            'payment_method_id': '1',
            'is_lunchbox': '0',
            'order_items[0][qty]': '2',
            'order_items[0][stock_id]': discover.json().get('data')['nearby_menu'][0]['stock_id'],
            'address': 'Megaregency',
            'note': 'Test Notes',
            'delivery_price': '20000',
            'delivery_method': 'Instant',
            'origin_contact_name': 'Fawwaz 1',
            'origin_contact_phone': '081386356616',
            'origin_address': 'Perumahan Megaregency 1',
            'origin_lat_long': '-6.3823027,107.1162164',
            'destination_contact_name': 'Fawwaz 2',
            'destination_contact_phone': '0857108194',
            'destination_address': 'Perumahan Megaregency 2',
            'destination_lat_long': '-6.3772882,107.1062917',
            'phone_number': '085710819443'
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        delivery_order = requests.post(url_delivery_order, data=param3, headers=headers2)
        param4 = {
            'payment_phone_number': '081386356616',
            'reason': 'faw reason'
        }
        headers4 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        cancel_order = requests.patch(
            url_cancel_order + delivery_order.json().get('data')['registrasi_order_number'] + '/cancel', data=param4,
            headers=headers4)

        validation_status = cancel_order.json().get('success')
        validation_message = cancel_order.json().get('message')

        assert cancel_order.status_code == 200
        assert validation_status == bool(True)
        assert 'Order berhasil dibatalkan dan refund anda sedang diproses' in validation_message

    def test_order_cancel_wrong_token(self):
        param = {
            'email': email,
            'password': kata_sandi
        }
        headers = {
            "Accept": "application/json"
        }
        login = requests.post(url_login, params=param, headers=headers)
        param2 = {
            'latitude': latitude,
            'longitude': longitude
        }
        headers2 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        discover = requests.get(url_discover, params=param2, headers=headers2)
        param3 = {
            'payment_method_id': '1',
            'is_lunchbox': '0',
            'order_items[0][qty]': '2',
            'order_items[0][stock_id]': discover.json().get('data')['nearby_menu'][0]['stock_id'],
            'address': 'Megaregency',
            'note': 'Test Notes',
            'delivery_price': '20000',
            'delivery_method': 'Instant',
            'origin_contact_name': 'Fawwaz 1',
            'origin_contact_phone': '081386356616',
            'origin_address': 'Perumahan Megaregency 1',
            'origin_lat_long': '-6.3823027,107.1162164',
            'destination_contact_name': 'Fawwaz 2',
            'destination_contact_phone': '0857108194',
            'destination_address': 'Perumahan Megaregency 2',
            'destination_lat_long': '-6.3772882,107.1062917',
            'phone_number': '085710819443'
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        delivery_order = requests.post(url_delivery_order, data=param3, headers=headers2)
        param4 = {
            'payment_phone_number': '081386356616',
            'reason': 'faw reason'
        }
        headers4 = {
            "Accept": "application/json",
            "Authorization": wrong_token
        }
        cancel_order = requests.patch(
            url_cancel_order + delivery_order.json().get('data')['registrasi_order_number'] + '/cancel', data=param4,
            headers=headers4)

        validation_status = cancel_order.json().get('success')
        validation_message = cancel_order.json().get('message')

        assert cancel_order.status_code == 401
        assert validation_status == bool(False)
        assert 'Unauthorized' in validation_message

    def test_order_cancel_token_empty_value(self):
        param = {
            'email': email,
            'password': kata_sandi
        }
        headers = {
            "Accept": "application/json"
        }
        login = requests.post(url_login, params=param, headers=headers)
        param2 = {
            'latitude': latitude,
            'longitude': longitude
        }
        headers2 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        discover = requests.get(url_discover, params=param2, headers=headers2)
        param3 = {
            'payment_method_id': '1',
            'is_lunchbox': '0',
            'order_items[0][qty]': '2',
            'order_items[0][stock_id]': discover.json().get('data')['nearby_menu'][0]['stock_id'],
            'address': 'Megaregency',
            'note': 'Test Notes',
            'delivery_price': '20000',
            'delivery_method': 'Instant',
            'origin_contact_name': 'Fawwaz 1',
            'origin_contact_phone': '081386356616',
            'origin_address': 'Perumahan Megaregency 1',
            'origin_lat_long': '-6.3823027,107.1162164',
            'destination_contact_name': 'Fawwaz 2',
            'destination_contact_phone': '0857108194',
            'destination_address': 'Perumahan Megaregency 2',
            'destination_lat_long': '-6.3772882,107.1062917',
            'phone_number': '085710819443'
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        delivery_order = requests.post(url_delivery_order, data=param3, headers=headers2)
        param4 = {
            'payment_phone_number': '081386356616',
            'reason': 'faw reason'
        }
        headers4 = {
            "Accept": "application/json",
            "Authorization": ''
        }
        cancel_order = requests.patch(
            url_cancel_order + delivery_order.json().get('data')['registrasi_order_number'] + '/cancel', data=param4,
            headers=headers4)

        validation_status = cancel_order.json().get('success')
        validation_message = cancel_order.json().get('message')

        assert cancel_order.status_code == 401
        assert validation_status == bool(False)
        assert 'Unauthorized' in validation_message

    def test_order_cancel_trx_id_not_found(self):
        param = {
            'email': email,
            'password': kata_sandi
        }
        headers = {
            "Accept": "application/json"
        }
        login = requests.post(url_login, params=param, headers=headers)
        param2 = {
            'latitude': latitude,
            'longitude': longitude
        }
        headers2 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        discover = requests.get(url_discover, params=param2, headers=headers2)
        param3 = {
            'payment_method_id': '1',
            'is_lunchbox': '0',
            'order_items[0][qty]': '2',
            'order_items[0][stock_id]': discover.json().get('data')['nearby_menu'][0]['stock_id'],
            'address': 'Megaregency',
            'note': 'Test Notes',
            'delivery_price': '20000',
            'delivery_method': 'Instant',
            'origin_contact_name': 'Fawwaz 1',
            'origin_contact_phone': '081386356616',
            'origin_address': 'Perumahan Megaregency 1',
            'origin_lat_long': '-6.3823027,107.1162164',
            'destination_contact_name': 'Fawwaz 2',
            'destination_contact_phone': '0857108194',
            'destination_address': 'Perumahan Megaregency 2',
            'destination_lat_long': '-6.3772882,107.1062917',
            'phone_number': '085710819443'
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        delivery_order = requests.post(url_delivery_order, data=param3, headers=headers2)
        param4 = {
            'payment_phone_number': '081386356616',
            'reason': 'faw reason'
        }
        headers4 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        cancel_order = requests.patch(url_cancel_order + 'S1234567252906' + '/cancel', data=param4, headers=headers4)

        validation_status = cancel_order.json().get('success')
        validation_message = cancel_order.json().get('message')

        assert cancel_order.status_code == 400
        assert validation_status == bool(False)
        assert 'tidak ditemukan' in validation_message

    def test_order_cancel_trx_id_empty_value(self):
        param = {
            'email': email,
            'password': kata_sandi
        }
        headers = {
            "Accept": "application/json"
        }
        login = requests.post(url_login, params=param, headers=headers)
        param2 = {
            'latitude': latitude,
            'longitude': longitude
        }
        headers2 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        discover = requests.get(url_discover, params=param2, headers=headers2)
        param3 = {
            'payment_method_id': '1',
            'is_lunchbox': '0',
            'order_items[0][qty]': '2',
            'order_items[0][stock_id]': discover.json().get('data')['nearby_menu'][0]['stock_id'],
            'address': 'Megaregency',
            'note': 'Test Notes',
            'delivery_price': '20000',
            'delivery_method': 'Instant',
            'origin_contact_name': 'Fawwaz 1',
            'origin_contact_phone': '081386356616',
            'origin_address': 'Perumahan Megaregency 1',
            'origin_lat_long': '-6.3823027,107.1162164',
            'destination_contact_name': 'Fawwaz 2',
            'destination_contact_phone': '0857108194',
            'destination_address': 'Perumahan Megaregency 2',
            'destination_lat_long': '-6.3772882,107.1062917',
            'phone_number': '085710819443'
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        delivery_order = requests.post(url_delivery_order, data=param3, headers=headers2)
        param4 = {
            'payment_phone_number': '081386356616',
            'reason': 'faw reason'
        }
        headers4 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        cancel_order = requests.patch(url_cancel_order + '' + 'cancel', data=param4, headers=headers4)

        validation_status = cancel_order.json().get('success')
        validation_message = cancel_order.json().get('message')

        assert cancel_order.status_code == 405
        assert validation_status == bool(False)
        assert 'Method Not Allowed' in validation_message

    def test_Order_cancel_trx_id_wrong_format(self):
        param = {
            'email': email,
            'password': kata_sandi
        }
        headers = {
            "Accept": "application/json"
        }
        login = requests.post(url_login, params=param, headers=headers)
        param2 = {
            'latitude': latitude,
            'longitude': longitude
        }
        headers2 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        discover = requests.get(url_discover, params=param2, headers=headers2)
        param3 = {
            'payment_method_id': '1',
            'is_lunchbox': '0',
            'order_items[0][qty]': '2',
            'order_items[0][stock_id]': discover.json().get('data')['nearby_menu'][0]['stock_id'],
            'address': 'Megaregency',
            'note': 'Test Notes',
            'delivery_price': '20000',
            'delivery_method': 'Instant',
            'origin_contact_name': 'Fawwaz 1',
            'origin_contact_phone': '081386356616',
            'origin_address': 'Perumahan Megaregency 1',
            'origin_lat_long': '-6.3823027,107.1162164',
            'destination_contact_name': 'Fawwaz 2',
            'destination_contact_phone': '0857108194',
            'destination_address': 'Perumahan Megaregency 2',
            'destination_lat_long': '-6.3772882,107.1062917',
            'phone_number': '085710819443'
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        delivery_order = requests.post(url_delivery_order, data=param3, headers=headers2)
        param4 = {
            'payment_phone_number': '081386356616',
            'reason': 'faw reason'
        }
        headers4 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        cancel_order = requests.patch(url_cancel_order + 'K123456789765' + '/cancel', data=param4, headers=headers4)

        validation_status = cancel_order.json().get('success')
        validation_message = cancel_order.json().get('message')

        assert cancel_order.status_code == 400
        assert validation_status == bool(False)
        assert 'tidak ditemukan' in validation_message

    def test_order_cancel_reason_empty_value(self):
        param = {
            'email': email,
            'password': kata_sandi
        }
        headers = {
            "Accept": "application/json"
        }
        login = requests.post(url_login, params=param, headers=headers)
        param2 = {
            'latitude': latitude,
            'longitude': longitude
        }
        headers2 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        discover = requests.get(url_discover, params=param2, headers=headers2)
        param3 = {
            'payment_method_id': '1',
            'is_lunchbox': '0',
            'order_items[0][qty]': '2',
            'order_items[0][stock_id]': discover.json().get('data')['nearby_menu'][0]['stock_id'],
            'address': 'Megaregency',
            'note': 'Test Notes',
            'delivery_price': '20000',
            'delivery_method': 'Instant',
            'origin_contact_name': 'Fawwaz 1',
            'origin_contact_phone': '081386356616',
            'origin_address': 'Perumahan Megaregency 1',
            'origin_lat_long': '-6.3823027,107.1162164',
            'destination_contact_name': 'Fawwaz 2',
            'destination_contact_phone': '0857108194',
            'destination_address': 'Perumahan Megaregency 2',
            'destination_lat_long': '-6.3772882,107.1062917',
            'phone_number': '085710819443'
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        delivery_order = requests.post(url_delivery_order, data=param3, headers=headers2)
        param4 = {
            'payment_phone_number': '081386356616',
            'reason': ''
        }
        headers4 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        cancel_order = requests.patch(
            url_cancel_order + delivery_order.json().get('data')['registrasi_order_number'] + '/cancel', data=param4,
            headers=headers4)

        validation_status = cancel_order.json().get('success')
        validation_message = cancel_order.json().get('message')['reason']

        assert cancel_order.status_code == 422
        assert validation_status == bool(False)
        assert 'reason tidak boleh kosong.' in validation_message

    def test_order_cancel_without_param_reason(self):
        param = {
            'email': email,
            'password': kata_sandi
        }
        headers = {
            "Accept": "application/json"
        }
        login = requests.post(url_login, params=param, headers=headers)
        param2 = {
            'latitude': latitude,
            'longitude': longitude
        }
        headers2 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        discover = requests.get(url_discover, params=param2, headers=headers2)
        param3 = {
            'payment_method_id': '1',
            'is_lunchbox': '0',
            'order_items[0][qty]': '2',
            'order_items[0][stock_id]': discover.json().get('data')['nearby_menu'][0]['stock_id'],
            'address': 'Megaregency',
            'note': 'Test Notes',
            'delivery_price': '20000',
            'delivery_method': 'Instant',
            'origin_contact_name': 'Fawwaz 1',
            'origin_contact_phone': '081386356616',
            'origin_address': 'Perumahan Megaregency 1',
            'origin_lat_long': '-6.3823027,107.1162164',
            'destination_contact_name': 'Fawwaz 2',
            'destination_contact_phone': '0857108194',
            'destination_address': 'Perumahan Megaregency 2',
            'destination_lat_long': '-6.3772882,107.1062917',
            'phone_number': '085710819443'
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        delivery_order = requests.post(url_delivery_order, data=param3, headers=headers2)
        param4 = {
            'payment_phone_number': '081386356616'
            # 'reason': ''
        }
        headers4 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        cancel_order = requests.patch(
            url_cancel_order + delivery_order.json().get('data')['registrasi_order_number'] + '/cancel', data=param4,
            headers=headers4)

        validation_status = cancel_order.json().get('success')
        validation_message = cancel_order.json().get('message')['reason']

        assert cancel_order.status_code == 422
        assert validation_status == bool(False)
        assert 'reason tidak boleh kosong.' in validation_message

    def test_order_cancel_payment_phone_empty_value(self):
        param = {
            'email': email,
            'password': kata_sandi
        }
        headers = {
            "Accept": "application/json"
        }
        login = requests.post(url_login, params=param, headers=headers)
        param2 = {
            'latitude': latitude,
            'longitude': longitude
        }
        headers2 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        discover = requests.get(url_discover, params=param2, headers=headers2)
        param3 = {
            'payment_method_id': '1',
            'is_lunchbox': '0',
            'order_items[0][qty]': '2',
            'order_items[0][stock_id]': discover.json().get('data')['nearby_menu'][0]['stock_id'],
            'address': 'Megaregency',
            'note': 'Test Notes',
            'delivery_price': '20000',
            'delivery_method': 'Instant',
            'origin_contact_name': 'Fawwaz 1',
            'origin_contact_phone': '081386356616',
            'origin_address': 'Perumahan Megaregency 1',
            'origin_lat_long': '-6.3823027,107.1162164',
            'destination_contact_name': 'Fawwaz 2',
            'destination_contact_phone': '0857108194',
            'destination_address': 'Perumahan Megaregency 2',
            'destination_lat_long': '-6.3772882,107.1062917',
            'phone_number': '085710819443'
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        delivery_order = requests.post(url_delivery_order, data=param3, headers=headers2)
        param4 = {
            'payment_phone_number': '',
            'reason': 'sasasa'
        }
        headers4 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        cancel_order = requests.patch(
            url_cancel_order + delivery_order.json().get('data')['registrasi_order_number'] + '/cancel', data=param4,
            headers=headers4)

        validation_status = cancel_order.json().get('success')
        validation_message = cancel_order.json().get('message')['payment_phone_number']

        assert cancel_order.status_code == 422
        assert validation_status == bool(False)
        assert 'No. HP pembayaran tidak boleh kosong.' in validation_message

    def test_order_cancel_without_param_payment_phone(self):
        param = {
            'email': email,
            'password': kata_sandi
        }
        headers = {
            "Accept": "application/json"
        }
        login = requests.post(url_login, params=param, headers=headers)
        param2 = {
            'latitude': latitude,
            'longitude': longitude
        }
        headers2 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        discover = requests.get(url_discover, params=param2, headers=headers2)
        param3 = {
            'payment_method_id': '1',
            'is_lunchbox': '0',
            'order_items[0][qty]': '2',
            'order_items[0][stock_id]': discover.json().get('data')['nearby_menu'][0]['stock_id'],
            'address': 'Megaregency',
            'note': 'Test Notes',
            'delivery_price': '20000',
            'delivery_method': 'Instant',
            'origin_contact_name': 'Fawwaz 1',
            'origin_contact_phone': '081386356616',
            'origin_address': 'Perumahan Megaregency 1',
            'origin_lat_long': '-6.3823027,107.1162164',
            'destination_contact_name': 'Fawwaz 2',
            'destination_contact_phone': '0857108194',
            'destination_address': 'Perumahan Megaregency 2',
            'destination_lat_long': '-6.3772882,107.1062917',
            'phone_number': '085710819443'
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        delivery_order = requests.post(url_delivery_order, data=param3, headers=headers2)
        param4 = {
            # 'payment_phone_number': '',
            'reason': 'sasasa'
        }
        headers4 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        cancel_order = requests.patch(
            url_cancel_order + delivery_order.json().get('data')['registrasi_order_number'] + '/cancel', data=param4,
            headers=headers4)

        validation_status = cancel_order.json().get('success')
        validation_message = cancel_order.json().get('message')['payment_phone_number']

        assert cancel_order.status_code == 422
        assert validation_status == bool(False)
        assert 'No. HP pembayaran tidak boleh kosong.' in validation_message

    def test_order_cancel_payment_phone_text_value(self):
        param = {
            'email': email,
            'password': kata_sandi
        }
        headers = {
            "Accept": "application/json"
        }
        login = requests.post(url_login, params=param, headers=headers)
        param2 = {
            'latitude': latitude,
            'longitude': longitude
        }
        headers2 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        discover = requests.get(url_discover, params=param2, headers=headers2)
        param3 = {
            'payment_method_id': '1',
            'is_lunchbox': '0',
            'order_items[0][qty]': '2',
            'order_items[0][stock_id]': discover.json().get('data')['nearby_menu'][0]['stock_id'],
            'address': 'Megaregency',
            'note': 'Test Notes',
            'delivery_price': '20000',
            'delivery_method': 'Instant',
            'origin_contact_name': 'Fawwaz 1',
            'origin_contact_phone': '081386356616',
            'origin_address': 'Perumahan Megaregency 1',
            'origin_lat_long': '-6.3823027,107.1162164',
            'destination_contact_name': 'Fawwaz 2',
            'destination_contact_phone': '0857108194',
            'destination_address': 'Perumahan Megaregency 2',
            'destination_lat_long': '-6.3772882,107.1062917',
            'phone_number': '085710819443'
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        delivery_order = requests.post(url_delivery_order, data=param3, headers=headers2)
        param4 = {
            'payment_phone_number': 'aaaaa',
            'reason': 'sasasa'
        }
        headers4 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        cancel_order = requests.patch(
            url_cancel_order + delivery_order.json().get('data')['registrasi_order_number'] + '/cancel', data=param4,
            headers=headers4)

        validation_status = cancel_order.json().get('success')
        validation_message = cancel_order.json().get('message')

        assert cancel_order.status_code == 200
        assert validation_status == bool(True)
        assert 'Order berhasil dibatalkan dan refund anda sedang diproses' in validation_message

