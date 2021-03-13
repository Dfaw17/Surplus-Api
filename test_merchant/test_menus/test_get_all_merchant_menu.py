import requests
from env import stagging

class TestGetAllMerchantMenu:

    global url_get_all_merchant_menu, url_login, email, kata_sandi, wrong_token, setting_env

    setting_env = stagging
    url_get_all_merchant_menu = f"{setting_env}/api/v2/merchant/menus/"
    url_login = f"{setting_env}/api/v2/merchant/auth/login"
    email = "kopiruangvirtual@gmail.com"
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

        assert response.status_code == 200
        assert validate_status == bool(True)
        assert "Data menu berhasil ditemukan." in validate_message

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