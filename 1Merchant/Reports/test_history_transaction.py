import requests
from env import *
from assertpy import *


class TestOrderHistoryTransaction:
    global setting_env, url_history_trx, url_login, email, kata_sandi, wrong_token

    setting_env = testing
    url_history_trx = f"{setting_env}/api/v2/merchant/reports/transaction-history"
    url_login = f"{setting_env}/api/v2/merchant/auth/login"
    email = "sdet@gmail.com"
    kata_sandi = "12345678"
    wrong_token = "kyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvc3RhZ2luZy5hZG1pbnN1cnBsdXMubmV0XC9hcGlcL3YyXC9tZXJjaGFudFwvYXV0aFwvbG9naW4iLCJpYXQiOjE2MTU3MDExNDIsImV4cCI6MTYxODI5MzE0MiwibmJmIjoxNjE1NzAxMTQyLCJqdGkiOiJjOFluT3BlMzRqRVVIemZSIiwic3ViIjo0MDc3LCJwcnYiOiIyNzQxMDVkYTZlOTViZWYyODA3Nzg2ZGQ4NzM4ODY3Y2Y5YzAyYWFiIn0.xxI5o6tgIvb3Eds4CCfSnXM3ThFYiQwYcTCxKmrZozI"

    def test_history_transaction_normal(self):
        param = {
            "email": email,
            "password": kata_sandi
        }
        login = requests.post(url_login, data=param, headers={'Accept': 'application/json'})
        token = login.json().get("token")
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json"
        }
        response = requests.get(url_history_trx, headers=headers)
        data = response.json()

        validate_status = data.get("success")
        validate_message = data.get("message")
        validate_data = data.get("data")
        validate_data_orders = data.get("data")['orders']
        validate_data_total_order = data.get("data")['total_order']
        validate_data_order_item = data.get("data")['orders'][0]['order_item']

        assert response.status_code == 200
        assert validate_status == bool(True)
        assert "Data riwayat transaksi berhasil ditemukan" in validate_message
        assert_that(validate_data).contains_only('orders', 'total_order')
        assert_that(len(validate_data_orders)).is_equal_to(validate_data_total_order)
        assert_that(validate_data_orders[0]).contains_only('id', 'user_id', 'registrasi_order_number', 'created_at',
                                                           'shipment_detail_id', 'isDelivery', 'preorder', 'subtotal',
                                                           'grand_total', 'komisi_surplus', 'komisi_merchant',
                                                           'customer_name',
                                                           'order_date', 'cancel_status', 'is_tempat_makanan',
                                                           'total_jumlah_order', 'order_item')

        assert_that(validate_data_order_item[0]).contains_only('merchant_menu_id', 'stock_id', 'jumlah_order', 'note',
                                                               'nama_menu_makanan', 'deskripsi',
                                                               'waktu_mulai_penjemputan',
                                                               'waktu_akhir_penjemputan', 'harga_asli', 'harga_jual',
                                                               'is_non_halal', 'is_tomorrow', 'created_at',
                                                               'updated_at')

    def test_history_transaction_wrong_token(self):
        param = {
            "email": email,
            "password": kata_sandi
        }
        login = requests.post(url_login, data=param, headers={'Accept': 'application/json'})
        token = login.json().get("token")
        headers = {
            "Authorization": wrong_token,
            "Accept": "application/json"
        }
        response = requests.get(url_history_trx, headers=headers)
        data = response.json()

        validate_status = data.get("success")
        validate_message = data.get("message")

        assert validate_status == bool(False)
        assert 'Unauthorized' in validate_message
        assert response.status_code == 401

    def test_history_transaction_token_empty(self):
        param = {
            "email": email,
            "password": kata_sandi
        }
        login = requests.post(url_login, data=param, headers={'Accept': 'application/json'})
        token = login.json().get("token")
        headers = {
            "Authorization": '',
            "Accept": "application/json"
        }
        response = requests.get(url_history_trx, headers=headers)
        data = response.json()

        validate_status = data.get('success')
        validate_message = data.get('message')

        assert validate_status == bool(False)
        assert 'Unauthorized' in validate_message
        assert response.status_code == 401
