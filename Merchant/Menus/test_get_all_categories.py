import requests
from env import stagging

class TestGetAllCategories:

    global url_all_category, url_login, email, kata_sandi, wrong_token, setting_env

    setting_env = stagging
    url_all_category = f"{setting_env}/api/v2/merchant/categories"
    url_login = f"{setting_env}/api/v2/merchant/auth/login"
    email = "vd1@gmail.com"
    kata_sandi = "12345678"
    wrong_token = "yJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvc3RhZ2luZy5hZG1pbnN1cnBsdXMubmV0XC9hcGlcL3YyXC9tZXJjaGFudFwvYXV0aFwvbG9naW4iLCJpYXQiOjE2MTUzOTIzMDQsImV4cCI6MTYxNzk4NDMwNCwibmJmIjoxNjE1MzkyMzA0LCJqdGkiOiJOVGJ1Qk4xODE2VU5Fd2VKIiwic3ViIjo0MDc3LCJwcnYiOiIyNzQxMDVkYTZlOTViZWYyODA3Nzg2ZGQ4NzM4ODY3Y2Y5YzAyYWFiIn0.QQqZAjqTaM6aUJ-uZU8E53iIRySWB_A9mQTIt_tUXsQ"

    def test_get_all_categories_menu_normal (self):
        param = {
            "email": email,
            "password": kata_sandi
        }
        login = requests.post(url_login, data=param,
                              headers={'Accept': 'application/json'})
        token = login.json().get("token")
        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {token}"
        }
        response = requests.get(url_all_category, headers=headers)
        data = response.json()

        validate_status = data.get("success")
        validate_message = data.get("message")
        validate_data = len(data.get("data"))

        assert validate_status == bool(True)
        assert response.status_code == 200
        assert "Data menu ditemukan." in validate_message
        assert validate_data >= 1

    def test_get_all_categories_menu_wrong_token (self):
        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {wrong_token}"
        }
        response = requests.get(url_all_category, headers=headers)
        data = response.json()

        validate_status = data.get("success")
        validate_message = data.get("message")

        assert validate_status == bool(False)
        assert response.status_code == 401
        assert "Unauthorized" in validate_message

    def test_get_all_categories_menu_empty_token(self):
        headers = {
            "Accept": "application/json",
            "Authorization": ""
        }
        response = requests.get(url_all_category, headers=headers)
        data = response.json()

        validate_status = data.get("success")
        validate_message = data.get("message")

        assert validate_status == bool(False)
        assert response.status_code == 401
        assert "Unauthorized" in validate_message

    def test_get_all_categories_menu_no_auth(self):
        response = requests.get(url_all_category)
        data = response.text

        assert response.status_code == 401
        assert "Unauthorized" in data
