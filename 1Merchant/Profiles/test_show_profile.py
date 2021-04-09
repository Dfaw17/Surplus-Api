import requests
from assertpy import assert_that
from env import stagging

class TestShowProfile:

    global url_show_profile, url_login, email, kata_sandi, wrong_token, setting_env

    setting_env = stagging
    url_show_profile = f"{setting_env}/api/v2/merchant/profiles"
    url_login = f"{setting_env}/api/v2/merchant/auth/login"
    email = "vd1@gmail.com"
    kata_sandi = "12345678"
    wrong_token = "yJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvc3RhZ2luZy5hZG1pbnN1cnBsdXMubmV0XC9hcGlcL3YyXC9tZXJjaGFudFwvYXV0aFwvbG9naW4iLCJpYXQiOjE2MTUzOTIzMDQsImV4cCI6MTYxNzk4NDMwNCwibmJmIjoxNjE1MzkyMzA0LCJqdGkiOiJOVGJ1Qk4xODE2VU5Fd2VKIiwic3ViIjo0MDc3LCJwcnYiOiIyNzQxMDVkYTZlOTViZWYyODA3Nzg2ZGQ4NzM4ODY3Y2Y5YzAyYWFiIn0.QQqZAjqTaM6aUJ-uZU8E53iIRySWB_A9mQTIt_tUXsQ"

    def test_show_profile_normal(self):
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
        response = requests.get(url_show_profile, headers=headers)
        data = response.json()

        print(data)

        validate_status = data.get("success")
        validate_message = data.get("message")
        validate_data = data.get("data")["name"]
        validate_email = data.get("data")["email"]
        validate_outlet = data.get("data")["outlet"]
        validate_location = data.get("data")["location"]

        print(validate_outlet)

        assert validate_status == bool(True)
        assert response.status_code == 200
        assert "Data merchant ditemukan." in validate_message
        assert_that(validate_data).is_not_empty()
        assert_that(validate_outlet).is_not_empty()
        assert_that(validate_location).is_not_empty()
        assert validate_email == email

    def test_show_profile_wrong_token(self):
        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {wrong_token}"
        }
        response = requests.get(url_show_profile, headers=headers)
        data = response.json()
        validate_status = data.get("success")
        validate_message = data.get("message")

        assert validate_status == bool(False)
        assert "Unauthorized" in validate_message
        assert  response.status_code == 401

    def test_show_profile_empty_token(self):
        headers = {
            "Accept": "application/json",
            "Authorization": ""
        }
        response = requests.get(url_show_profile, headers=headers)
        data = response.json()
        validate_status = data.get("success")
        validate_message = data.get("message")

        assert validate_status == bool(False)
        assert "Unauthorized" in validate_message
        assert  response.status_code == 401

    def test_show_profile_no_auth(self):

        response = requests.get(url_show_profile)
        data = response.text

        assert "Unauthorized" in data
        assert  response.status_code == 401
