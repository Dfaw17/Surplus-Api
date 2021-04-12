import requests
from env import stagging
from pprint import pprint
from assertpy import assert_that

class TestCustomerOrdersIndexVoucher:

    global setting_env, url_login, url_index_voucher, email, kata_sandi, wrong_token

    setting_env = stagging
    url_login = f"{setting_env}/api/v2/customer/auth/login/email"
    url_index_voucher = f"{setting_env}/api/v2/customer/vouchers"
    email = "kopiruangvirtual@gmail.com"
    kata_sandi = '12345678'
    wrong_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvc3RhZ2luZy5hZG1pbnN1cnBsdXMubmV0XC9hcGlcL3YyXC9jdXN0b21lclwvYXV0aFwvbG9naW5cL2VtYWlsIiwiaWF0IjoxNjE2ODA1NzI2LCJleHAiOjE2MTkzOTc3MjYsIm5iZiI6MTYxNjgwNTcyNiwianRpIjoib05ESmxFRE5hSzNrN2RtVyIsInN1YiI6NDEyNiwicHJ2IjoiMjc0MTA1ZGE2ZTk1YmVmMjgwNzc4NmRkODczODg2N2NmOWMwMmFhYiJ9.fj51xIfQrqleRvdSJUbWcdrvsxQPUn8HpccnOmTgPDI'

    def test_index_voucher_normal(self):
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

        voucher = requests.get(url_index_voucher, headers=headers2)

        validate_status = voucher.json().get('success')
        validate_message = voucher.json().get('message')
        validate_data = voucher.json().get('data')

        assert voucher.status_code == 200
        assert validate_status == bool(True)
        assert "Voucher berhasil ditemukan" in validate_message
        assert_that(validate_data[0]).contains_only('id', 'title', 'description', 'code', 'percentage',
                                                    'fixed_discount',
                                                    'min_purchase', 'max_discount', 'max_usage', 'max_user',
                                                    'total_usage',
                                                    'total_user', 'is_specific_user', 'start_at', 'end_at', 'duration',
                                                    'custom_time', 'tos', 'guide', 'type_id', 'target_id', 'image',
                                                    'created_at', 'updated_at', 'deleted_at')

    def test_index_voucher_wrong_token(self):
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

        voucher = requests.get(url_index_voucher, headers=headers2)

        validate_status = voucher.json().get('success')
        validate_message = voucher.json().get('message')

        assert voucher.status_code == 401
        assert validate_status == bool(False)
        assert "Unauthorized" in validate_message

    def test_index_voucher_token_empty_value(self):
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
            "Authorization": ''
        }

        voucher = requests.get(url_index_voucher, headers=headers2)

        validate_status = voucher.json().get('success')
        validate_message = voucher.json().get('message')

        assert voucher.status_code == 401
        assert validate_status == bool(False)
        assert "Unauthorized" in validate_message
