import requests
from env import stagging
from pprint import pprint
from assertpy import assert_that
import pytest

class TestMerchantBranchIndex:

    global setting_env,url_login,url_branch,email,kata_sandi,wrong_token

    setting_env = stagging
    url_login = f"{setting_env}/api/v2/merchant/auth/login"
    url_branch = f"{setting_env}/api/v2/merchant/branches"
    email = "vd@gmail.com"
    kata_sandi = '12345678'
    wrong_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvc3RhZ2luZy5hZG1pbnN1cnBsdXMubmV0XC9hcGlcL3YyXC9jdXN0b21lclwvYXV0aFwvbG9naW5cL2VtYWlsIiwiaWF0IjoxNjE2ODA1NzI2LCJleHAiOjE2MTkzOTc3MjYsIm5iZiI6MTYxNjgwNTcyNiwianRpIjoib05ESmxFRE5hSzNrN2RtVyIsInN1YiI6NDEyNiwicHJ2IjoiMjc0MTA1ZGE2ZTk1YmVmMjgwNzc4NmRkODczODg2N2NmOWMwMmFhYiJ9.fj51xIfQrqleRvdSJUbWcdrvsxQPUn8HpccnOmTgPDI'

    @pytest.mark.order(1)
    def test_index_branch_normal(self):
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

        branch = requests.get(url_branch, headers=headers2)

        validate_status = branch.json().get('success')
        validate_message = branch.json().get('message')
        validate_data = branch.json().get('data')

        assert branch.status_code == 200
        assert validate_status == bool(True)
        assert "Data cabang berhasil ditemukan." in validate_message
        assert_that(validate_data).is_not_none()
        assert_that(validate_data[0]).contains_only('id', 'name', 'email', 'status', 'area', 'merchant_logo')

    @pytest.mark.order(2)
    def test_index_branch_wrong_token(self):
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

        branch = requests.get(url_branch, headers=headers2)

        validate_status = branch.json().get('success')
        validate_message = branch.json().get('message')

        assert branch.status_code == 401
        assert validate_status == bool(False)
        assert "Unauthorized" in validate_message

    @pytest.mark.order(3)
    def test_index_branch_token_empty(self):
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

        branch = requests.get(url_branch, headers=headers2)

        validate_status = branch.json().get('success')
        validate_message = branch.json().get('message')

        assert branch.status_code == 401
        assert validate_status == bool(False)
        assert "Unauthorized" in validate_message
