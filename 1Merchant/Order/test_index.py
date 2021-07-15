import requests
from env import *
from assertpy import *


class TestOrderIndex:
    global setting_env, url_index_order, url_login, email, kata_sandi, wrong_token

    setting_env = testing
    url_index_order = f"{setting_env}/api/v2/merchant/orders?type=finish"
    url_login = f"{setting_env}/api/v2/merchant/auth/login"
    email = "sdet@gmail.com"
    kata_sandi = "12345678"
    wrong_token = "kyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvc3RhZ2luZy5hZG1pbnN1cnBsdXMubmV0XC9hcGlcL3YyXC9tZXJjaGFudFwvYXV0aFwvbG9naW4iLCJpYXQiOjE2MTU3MDExNDIsImV4cCI6MTYxODI5MzE0MiwibmJmIjoxNjE1NzAxMTQyLCJqdGkiOiJjOFluT3BlMzRqRVVIemZSIiwic3ViIjo0MDc3LCJwcnYiOiIyNzQxMDVkYTZlOTViZWYyODA3Nzg2ZGQ4NzM4ODY3Y2Y5YzAyYWFiIn0.xxI5o6tgIvb3Eds4CCfSnXM3ThFYiQwYcTCxKmrZozI"

    def test_order_index_normal(self):
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
        response = requests.get(url_index_order, headers=headers)
        data = response.json()

        validate_status = data.get("success")
        validate_message = data.get("message")
        validate_data = data.get("data")
        validate_order_items = data.get("data")[0]['order_item']

        assert response.status_code == 200
        assert validate_status == bool(True)
        assert "Data pesanan ditemukan." in validate_message
        assert_that(validate_data).is_type_of(list)
        assert_that(validate_data[0]).contains_only('id', 'user_id', 'registrasi_order_number', 'created_at',
                                                    'shipment_detail_id', 'isDelivery', 'preorder', 'subtotal',
                                                    'grand_total',
                                                    'komisi_surplus', 'komisi_merchant', 'customer_name', 'order_date',
                                                    'cancel_status', 'is_tempat_makanan', 'total_jumlah_order',
                                                    'order_item')
        assert_that(validate_order_items[0]).contains_only('merchant_menu_id', 'stock_id', 'jumlah_order', 'note',
                                                           'nama_menu_makanan', 'deskripsi', 'waktu_mulai_penjemputan',
                                                           'waktu_akhir_penjemputan', 'harga_asli', 'harga_jual',
                                                           'is_non_halal', 'is_tomorrow', 'created_at', 'updated_at')

    def test_order_index_token_empty_value(self):
        param = {
            "email": email,
            "password": kata_sandi
        }
        login = requests.post(url_login, data=param, headers={'Accept': 'application/json'})
        token = login.json().get("token")
        headers = {
            "Authorization": "",
            "Accept": "application/json"
        }
        response = requests.get(url_index_order, headers=headers)
        data = response.json()

        validate_status = data.get("success")
        validate_message = data.get("message")

        assert response.status_code == 401
        assert validate_status == bool(False)
        assert "Unauthorized" in validate_message

    def test_order_index_token_wrong_value(self):
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
        response = requests.get(url_index_order, headers=headers)
        data = response.json()

        validate_status = data.get("success")
        validate_message = data.get("message")

        assert response.status_code == 401
        assert validate_status == bool(False)
        assert "Unauthorized" in validate_message

    def test_order_index_type_number_value(self):
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
        response = requests.get(url_index_order + '123', headers=headers)
        data = response.json()

        validate_status = data.get("success")
        validate_message = data.get("message")['type']

        assert response.status_code == 422
        assert validate_status == bool(False)
        assert "type yang dipilih tidak tersedia." in validate_message

    def test_order_index_type_empty_value(self):
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
        response = requests.get(f"{setting_env}/api/v2/merchant/orders?type=", headers=headers)
        data = response.json()

        validate_status = data.get("success")
        validate_message = data.get("message")['type']

        assert response.status_code == 422
        assert validate_status == bool(False)
        assert "type tidak boleh kosong." in validate_message

    def test_order_index_type_wrong_value(self):
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
        response = requests.get(f"{setting_env}/api/v2/merchant/orders?type=done", headers=headers)
        data = response.json()

        validate_status = data.get("success")
        validate_message = data.get("message")['type']

        assert response.status_code == 422
        assert validate_status == bool(False)
        assert "type yang dipilih tidak tersedia." in validate_message
