import requests
from env import stagging
from pprint import pprint
from assertpy import assert_that

class TestCustomerRegisterProgress:

    global setting_env,register_progress,email,kata_sandi

    setting_env = stagging
    register_progress = f"{setting_env}/api/v2/customer/auth/register/progress"
    email = "kopiruangvirtual@gmail.com"
    kata_sandi = "12345678"

    def test_register_progress_normal(self):
        param = {
            'email': email
        }
        headers = {
            "Accept": "application/json"
        }

        response = requests.get(register_progress, params=param, headers=headers)
        data = response.json()
        # pprint(response.json())

        validate_status = data.get('success')
        validate_message = data.get('message')
        validate_email = data.get('data')['customer']
        validate_status_akun = data.get('data')['status']

        assert response.status_code == 200
        assert validate_status == bool(True)
        assert_that(validate_message).is_not_empty()
        validate_email == email
        assert_that(validate_status_akun).is_not_empty()

    def test_register_progress_without_param_email(self):
        param = {
            'email': ""
        }
        headers = {
            "Accept": "application/json"
        }

        response = requests.get(register_progress, params=param, headers=headers)
        data = response.json()
        # pprint(response.json())

        validate_status = data.get('success')
        validate_message = data.get('message')['email']

        assert response.status_code == 422
        assert validate_status == bool(False)
        assert 'email tidak boleh kosong.' in validate_message

    def test_register_progress_email_value_empty(self):
        param = {

        }
        headers = {
            "Accept": "application/json"
        }

        response = requests.get(register_progress, params=param, headers=headers)
        data = response.json()
        # pprint(response.json())

        validate_status = data.get('success')
        validate_message = data.get('message')['email']

        assert response.status_code == 422
        assert validate_status == bool(False)
        assert 'email tidak boleh kosong.' in validate_message

    def test_register_progress_email_without_at(self):
        param = {
            'email': "kopiruangvirtualgmail.com"
        }
        headers = {
            "Accept": "application/json"
        }

        response = requests.get(register_progress, params=param, headers=headers)
        data = response.json()
        # pprint(response.json())

        validate_status = data.get('success')
        validate_message = data.get('message')['email']

        assert response.status_code == 422
        assert validate_status == bool(False)
        assert 'email harus merupakan alamat email yang valid.' in validate_message