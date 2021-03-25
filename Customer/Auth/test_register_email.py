import requests
from env import stagging
from pprint import pprint
from assertpy import assert_that
from faker import Faker
fake = Faker()

class TestCustomerRegisterEmail:

    global setting_env,register_email,email,kata_sandi,email_has_registered

    setting_env = stagging
    register_email = f"{setting_env}/api/v2/customer/auth/register/email"
    email = fake.email()
    email_has_registered = 'kopiruangvirtual@gmail.com'
    kata_sandi = "12345678"

    def test_register_with_email_normal(self):
        headers = {
            "Accept": "application/json"
        }
        param = {

            "email": email,
            "password": kata_sandi,
            "re-password": kata_sandi
        }
        response = requests.post(register_email, data=param, headers=headers)
        data = response.json()

        validate_status = data.get('success')
        validate_message = data.get('message')
        validate_data = data.get('data')['id']
        validate_email = data.get('data')['email']

        assert response.status_code == 201
        assert validate_status == bool(True)
        assert 'Registrasi berhasil.' in validate_message
        assert_that(validate_data).is_type_of(int)
        assert validate_email == email
        pprint(response.json())

    def test_register_with_email_sudah_terdaftar(self):
        headers = {
            "Accept": "application/json"
        }
        param = {

            "email": email_has_registered,
            "password": kata_sandi,
            "re-password": kata_sandi
        }
        response = requests.post(register_email, data=param, headers=headers)
        data = response.json()

        validate_status = data.get('success')
        validate_message = data.get('message')

        assert response.status_code == 404
        assert validate_status == bool(False)
        assert 'sudah terdaftar' in validate_message

    def test_register_with_email_empty_value(self):
        headers = {
            "Accept": "application/json"
        }
        param = {

            "email": "",
            "password": kata_sandi,
            "re-password": kata_sandi
        }
        response = requests.post(register_email, data=param, headers=headers)
        data = response.json()

        validate_status = data.get('success')
        validate_message = data.get('message')['email']

        assert response.status_code == 422
        assert validate_status == bool(False)
        assert 'email tidak boleh kosong.' in validate_message

    def test_register_with_email_without_param_email(self):
        headers = {
            "Accept": "application/json"
        }
        param = {
            "password": kata_sandi,
            "re-password": kata_sandi
        }
        response = requests.post(register_email, data=param, headers=headers)
        data = response.json()

        validate_status = data.get('success')
        validate_message = data.get('message')['email']

        assert response.status_code == 422
        assert validate_status == bool(False)
        assert 'email tidak boleh kosong.' in validate_message

    def test_register_with_email_without_at(self):
        headers = {
            "Accept": "application/json"
        }
        param = {

            "email": "halo gmail.com",
            "password": kata_sandi,
            "re-password": kata_sandi
        }
        response = requests.post(register_email, data=param, headers=headers)
        data = response.json()

        validate_status = data.get('success')
        validate_message = data.get('message')['email']

        assert response.status_code == 422
        assert validate_status == bool(False)
        assert 'email harus merupakan alamat email yang valid.' in validate_message

    def test_register_with_email_using_space(self):
        headers = {
            "Accept": "application/json"
        }
        param = {

            "email": "halo @gmail.com",
            "password": kata_sandi,
            "re-password": kata_sandi
        }
        response = requests.post(register_email, data=param, headers=headers)
        data = response.json()

        validate_status = data.get('success')
        validate_message = data.get('message')

        assert response.status_code == 500
        assert validate_status == bool(False)
        assert 'Ada yang salah di sistem kami.' in validate_message

    def test_register_with_email_password_empty_value(self):
        headers = {
            "Accept": "application/json"
        }
        param = {

            "email": email,
            "password": "",
            "re-password": kata_sandi
        }
        response = requests.post(register_email, data=param, headers=headers)
        data = response.json()

        validate_status = data.get('success')
        validate_message = data.get('message')['password']

        assert response.status_code == 422
        assert validate_status == bool(False)
        assert 'Kata sandi tidak boleh kosong.' in validate_message

    def test_register_with_email_without_param_password(self):
        headers = {
            "Accept": "application/json"
        }
        param = {

            "email": email,
            "re-password": kata_sandi
        }
        response = requests.post(register_email, data=param, headers=headers)
        data = response.json()

        validate_status = data.get('success')
        validate_message = data.get('message')['password']

        assert response.status_code == 422
        assert validate_status == bool(False)
        assert 'Kata sandi tidak boleh kosong.' in validate_message

    def test_register_with_email_rePassword_empty_value(self):
        headers = {
            "Accept": "application/json"
        }
        param = {

            "email": email,
            'password': kata_sandi,
            "re-password": ""
        }
        response = requests.post(register_email, data=param, headers=headers)
        data = response.json()

        validate_status = data.get('success')
        validate_message = data.get('message')['re-password']

        assert response.status_code == 422
        assert validate_status == bool(False)
        assert 're-password tidak boleh kosong.' in validate_message

    def test_register_with_email_without_param_rePassword(self):
        headers = {
            "Accept": "application/json"
        }
        param = {

            "email": email,
            'password': kata_sandi
        }
        response = requests.post(register_email, data=param, headers=headers)
        data = response.json()

        validate_status = data.get('success')
        validate_message = data.get('message')['re-password']

        assert response.status_code == 422
        assert validate_status == bool(False)
        assert 're-password tidak boleh kosong.' in validate_message

    def test_register_with_email_pass_rePass_doesnt_match(self):
        headers = {
            "Accept": "application/json"
        }
        param = {

            "email": email,
            'password': 'kata_sandi',
            're-password': '12345678'
        }
        response = requests.post(register_email, data=param, headers=headers)
        data = response.json()

        validate_status = data.get('success')
        validate_message = data.get('message')['re-password']

        assert response.status_code == 422
        assert validate_status == bool(False)
        assert 're-password dan Kata sandi harus sama.' in validate_message



