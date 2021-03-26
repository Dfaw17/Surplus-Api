import requests
from env import stagging
from pprint import pprint
from assertpy import assert_that

class TestCustomerCheckEmail:

    global setting_env,check_email,email_has_registered,email_hasnt_registered

    setting_env = stagging
    check_email = f"{setting_env}/api/v2/customer/auth/register/check-email"
    email_has_registered = "kopiruangvirtual@gmail.com"
    email_hasnt_registered = "abc@gmail.com"

    def test_check_email_belum_terdaftar(self):
        param = {
            'email': email_hasnt_registered
        }
        headers = {
            "Accept": "application/json"
        }

        response = requests.post(check_email, params=param, headers=headers)
        data = response.json()
        pprint(data)

        validate_status = data.get('success')
        validate_message = data.get('message')
        #
        assert response.status_code == 200
        assert validate_status == bool(True)
        assert 'tersedia.' in validate_message

    def test_check_email_sudah_terdaftar(self):
        param = {
            'email': email_has_registered
        }
        headers = {
            "Accept": "application/json"
        }

        response = requests.post(check_email, params=param, headers=headers)
        data = response.json()
        pprint(data)

        validate_status = data.get('success')
        validate_message = data.get('message')
        #
        assert response.status_code == 404
        assert validate_status == bool(False)
        assert 'sudah terdaftar' in validate_message

    def test_check_email_empty_value(self):
        param = {
            'email': ''
        }
        headers = {
            "Accept": "application/json"
        }

        response = requests.post(check_email, params=param, headers=headers)
        data = response.json()
        pprint(data)

        validate_status = data.get('success')
        validate_message = data.get('message')['email']

        assert response.status_code == 422
        assert validate_status == bool(False)
        assert 'email tidak boleh kosong.' in validate_message

    def test_check_email_without_para_email(self):
        param = {

        }
        headers = {
            "Accept": "application/json"
        }

        response = requests.post(check_email, params=param, headers=headers)
        data = response.json()
        pprint(data)

        validate_status = data.get('success')
        validate_message = data.get('message')['email']

        assert response.status_code == 422
        assert validate_status == bool(False)
        assert 'email tidak boleh kosong.' in validate_message

    def test_check_email_with_space(self):
        param = {
            'email': 'kopiruangvirtual gmail.com'
        }
        headers = {
            "Accept": "application/json"
        }

        response = requests.post(check_email, params=param, headers=headers)
        data = response.json()
        pprint(data)

        validate_status = data.get('success')
        validate_message = data.get('message')['email']

        assert response.status_code == 422
        assert validate_status == bool(False)
        assert 'email harus merupakan alamat email yang valid.' in validate_message

    def test_check_email_without(self):
        param = {
            'email': 'kopiruangvirtualgmail.com'
        }
        headers = {
            "Accept": "application/json"
        }

        response = requests.post(check_email, params=param, headers=headers)
        data = response.json()
        pprint(data)

        validate_status = data.get('success')
        validate_message = data.get('message')['email']

        assert response.status_code == 422
        assert validate_status == bool(False)
        assert 'email harus merupakan alamat email yang valid.' in validate_message