import requests
from env import stagging
from pprint import pprint
from assertpy import assert_that

class TestCustomerShowProfiles:

    global setting_env,url_login,url_show_profiles,email,kata_sandi,wrong_token

    setting_env = stagging
    url_login = f"{setting_env}/api/v2/customer/auth/login/email"
    url_show_profiles = f"{setting_env}/api/v2/customer/profiles"
    email = "kopiruangvirtual@gmail.com"
    kata_sandi = '12345678'
    wrong_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvc3RhZ2luZy5hZG1pbnN1cnBsdXMubmV0XC9hcGlcL3YyXC9jdXN0b21lclwvYXV0aFwvbG9naW5cL2VtYWlsIiwiaWF0IjoxNjE2ODA1NzI2LCJleHAiOjE2MTkzOTc3MjYsIm5iZiI6MTYxNjgwNTcyNiwianRpIjoib05ESmxFRE5hSzNrN2RtVyIsInN1YiI6NDEyNiwicHJ2IjoiMjc0MTA1ZGE2ZTk1YmVmMjgwNzc4NmRkODczODg2N2NmOWMwMmFhYiJ9.fj51xIfQrqleRvdSJUbWcdrvsxQPUn8HpccnOmTgPDI'

    def test_show_profile_normal(self):
        param = {
            'email': email,
            'password': kata_sandi
        }
        headers = {
            "Accept": "application/json"
        }
        login = requests.post(url_login, params=param, headers=headers)
        headers2 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        show_profile = requests.get(url_show_profiles, headers=headers2)

        validate_status = show_profile.json().get('success')
        validate_message = show_profile.json().get('message')
        validate_data_email = show_profile.json().get('data')['email']
        validate_data_name = show_profile.json().get('data')['name']
        validate_data_no_ponsel = show_profile.json().get('data')['no_ponsel']

        assert show_profile.status_code == 200
        assert validate_status == bool(True)
        assert 'Data customer berhasil ditemukan.' in validate_message
        assert validate_data_email == email
        assert_that(validate_data_name).is_not_none()
        assert_that(validate_data_no_ponsel).is_not_none()

    def test_show_profile_wrong_token(self):
        param = {
            'email': email,
            'password': kata_sandi
        }
        headers = {
            "Accept": "application/json"
        }
        login = requests.post(url_login, params=param, headers=headers)
        headers2 = {
            "Accept": "application/json",
            "Authorization": wrong_token
        }
        show_profile = requests.get(url_show_profiles, headers=headers2)

        validate_status = show_profile.json().get('success')
        validate_message = show_profile.json().get('message')

        assert show_profile.status_code == 401
        assert validate_status == bool(False)
        assert 'Unauthorized' in validate_message

    def test_show_profile_token_empty_value(self):
        param = {
            'email': email,
            'password': kata_sandi
        }
        headers = {
            "Accept": "application/json"
        }
        login = requests.post(url_login, params=param, headers=headers)
        headers2 = {
            "Accept": "application/json",
            "Authorization": ""
        }
        show_profile = requests.get(url_show_profiles, headers=headers2)

        validate_status = show_profile.json().get('success')
        validate_message = show_profile.json().get('message')

        assert show_profile.status_code == 401
        assert validate_status == bool(False)
        assert 'Unauthorized' in validate_message
