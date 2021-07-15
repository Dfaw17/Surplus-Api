import requests
from env import *
from assertpy import *


class TestGetAllMerchantMenu:
    global url_get_all_merchant_menu, url_login, email, kata_sandi, wrong_token, setting_env

    setting_env = testing
    url_get_all_merchant_menu = f"{setting_env}/api/v2/merchant/menus/"
    url_login = f"{setting_env}/api/v2/merchant/auth/login"
    email = "sdet@gmail.com"
    kata_sandi = "12345678"
    wrong_token = "yJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvc3RhZ2luZy5hZG1pbnN1cnBsdXMubmV0XC9hcGlcL3YyXC9tZXJjaGFudFwvYXV0aFwvbG9naW4iLCJpYXQiOjE2MTUzOTIzMDQsImV4cCI6MTYxNzk4NDMwNCwibmJmIjoxNjE1MzkyMzA0LCJqdGkiOiJOVGJ1Qk4xODE2VU5Fd2VKIiwic3ViIjo0MDc3LCJwcnYiOiIyNzQxMDVkYTZlOTViZWYyODA3Nzg2ZGQ4NzM4ODY3Y2Y5YzAyYWFiIn0.QQqZAjqTaM6aUJ-uZU8E53iIRySWB_A9mQTIt_tUXsQ"

    def test_get_all_merchant_menu_normal(self):
        param = {
            "email": email,
            "password": kata_sandi
        }
        login = requests.post(url_login, data=param,
                              headers={'Accept': 'application/json'})
        token = login.json().get("token")
        headers = {
            "Authorization": f"Bearer {token}"
        }
        response = requests.get(url_get_all_merchant_menu, headers=headers)
        data = response.json()
        validate_status = data.get("success")
        validate_message = data.get("message")
        validate_data = data.get("data")[0]

        assert response.status_code == 200
        assert validate_status == bool(True)
        assert "Data menu berhasil ditemukan." in validate_message
        assert_that(validate_data).contains_only('id', 'nama_menu_makanan', 'merchant_kategori_makanan_id',
                                                 'is_exclusive', 'deskripsi', 'harga_asli', 'harga_jual',
                                                 'is_non_halal', 'weight', 'weight_string', 'image_thumbnail',
                                                 'created_at', 'updated_at', 'stock_id', 'merchant_id',
                                                 'waktu_mulai_penjemputan', 'waktu_akhir_penjemputan', 'stock',
                                                 'in_catalog', 'is_active', 'is_missed', 'is_tomorrow', 'waktu_missed',
                                                 'total_terjual', 'max_active_date', 'expired_date', 'expired_time',
                                                 'max_storage_days', 'nama_kategori_makanan')

    def test_get_all_merchant_wrong_token(self):
        headers = {
            "Authorization": f"Bearer {wrong_token}"
        }
        response = requests.get(url_get_all_merchant_menu, headers=headers)
        data = response.text

        assert response.status_code == 401
        assert "Unauthorized" in data

    def test_get_all_merchant_empty_token(self):
        headers = {
            "Authorization": ""
        }
        response = requests.get(url_get_all_merchant_menu, headers=headers)
        data = response.text

        assert response.status_code == 401
        assert "Unauthorized" in data

    def test_get_all_merchant_noauth(self):
        response = requests.get(url_get_all_merchant_menu)
        data = response.text

        assert response.status_code == 401
        assert "Unauthorized" in data
