import requests
from env import stagging
from assertpy import assert_that

class TestShowMerchantMenu :

    global setting_env, url_show_merchant_menu, url_login, email, kata_sandi, wrong_token

    setting_env = stagging
    url_show_merchant_menu = f"{setting_env}/api/v2/merchant/menus/"
    url_login = f"{setting_env}/api/v2/merchant/auth/login"
    email = "vd1@gmail.com"
    kata_sandi = "12345678"
    wrong_token = "yJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvc3RhZ2luZy5hZG1pbnN1cnBsdXMubmV0XC9hcGlcL3YyXC9tZXJjaGFudFwvYXV0aFwvbG9naW4iLCJpYXQiOjE2MTU2MTY0OTAsImV4cCI6MTYxODIwODQ5MCwibmJmIjoxNjE1NjE2NDkwLCJqdGkiOiJ5YjE4ZVlVY1JOVThVWWZ4Iiwic3ViIjo0MDc3LCJwcnYiOiIyNzQxMDVkYTZlOTViZWYyODA3Nzg2ZGQ4NzM4ODY3Y2Y5YzAyYWFiIn0.g1fCXWhLb_t7fll879LngGO03e1fy6B8mTdX4hrBrHM"

    def test_show_merchant_menu_normal(self):
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
        get_all_merchant_menu = requests.get(url_show_merchant_menu, headers=headers)
        data_menu = str(get_all_merchant_menu.json().get("data")[0]["id"])
        data_merchat_id = str(get_all_merchant_menu.json().get("data")[0]["merchant_id"])

        response = requests.get(url_show_merchant_menu + data_menu, headers=headers)
        data = response.json()

        validate_status = data.get("success")
        validate_message = data.get("message")
        validate_data_id = str(data.get("data")["id"])
        validate_merchant_id = str(data.get("data")["merchant_id"])
        validate_nama_makanan = data.get("data")["nama_menu_makanan"]

        assert validate_status == bool(True)
        assert response.status_code == 200
        assert validate_message == "Data menu ditemukan."
        assert validate_data_id == data_menu
        assert_that(validate_merchant_id).is_not_none()
        assert_that(validate_nama_makanan).is_not_empty()
        assert data_merchat_id == validate_merchant_id

    def test_show_merchant_menu_empty_token(self):
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
        get_all_merchant_menu = requests.get(url_show_merchant_menu, headers=headers)
        data_menu = str(get_all_merchant_menu.json().get("data")[0]["id"])
        data_merchat_id = str(get_all_merchant_menu.json().get("data")[0]["merchant_id"])

        response = requests.get(url_show_merchant_menu + data_menu, headers="")
        data = response.text

        assert response.status_code == 401
        assert "Unauthorized" in data

    def test_show_merchant_menu_wrong_token(self):
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
        get_all_merchant_menu = requests.get(url_show_merchant_menu, headers=headers)
        data_menu = str(get_all_merchant_menu.json().get("data")[0]["id"])
        data_merchat_id = str(get_all_merchant_menu.json().get("data")[0]["merchant_id"])

        response = requests.get(url_show_merchant_menu + data_menu, headers={"Authorization": wrong_token})
        data = response.text

        assert response.status_code == 401
        assert "Unauthorized" in data

    def test_show_merchant_menu_wrong_id(self):
        param = {
            "email": email,
            "password": kata_sandi
        }
        login = requests.post(url_login, data=param,
                              headers={'Accept': 'application/json'})
        token = login.json().get("token")
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json"
        }
        get_all_merchant_menu = requests.get(url_show_merchant_menu, headers=headers)
        data_menu = str(0000)

        response = requests.get(url_show_merchant_menu + data_menu, headers=headers)
        data = response.json()

        validate_status = data.get("success")
        validate_message = data.get("message")

        assert validate_status == bool(False)
        assert response.status_code == 404
        assert validate_message == "Data menu tidak ditemukan."

