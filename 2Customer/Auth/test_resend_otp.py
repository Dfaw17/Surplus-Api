import requests
from env import stagging
from pprint import pprint

class TestCustomerResendOtp:

    global setting_env,resend_otp,email

    setting_env = stagging
    resend_otp = f"{setting_env}/api/v2/customer/auth/register/otp/resend"
    email = "daffafawwazmaulana170901@gmail.com"

    def test_resend_OTP_normal(self):
        param = {
            'email': email
        }

        response = requests.post(resend_otp, data=param)
        data = response.json()
        pprint(data)
        validate_status = data.get('success')
        validate_message = data.get('message')
        #
        assert response.status_code == 201
        assert validate_status == bool(True)
        assert 'OTP berhasil dikirim ulang ke email' in validate_message

    def test_resend_OTP_email_empty_value(self):
        param = {
            'email': ""
        }
        headers = {
            "Accept": "application/json"
        }

        response = requests.post(resend_otp, data=param, headers=headers)
        data = response.json()
        pprint(data)
        validate_status = data.get('success')
        validate_message = data.get('message')['email']

        assert response.status_code == 422
        assert validate_status == bool(False)
        assert 'email tidak boleh kosong.' in validate_message

    def test_resend_OTP_without_param_email(self):
        param = {
        }
        headers = {
            "Accept": "application/json"
        }

        response = requests.post(resend_otp, data=param, headers=headers)
        data = response.json()
        pprint(data)
        validate_status = data.get('success')
        validate_message = data.get('message')['email']

        assert response.status_code == 422
        assert validate_status == bool(False)
        assert 'email tidak boleh kosong.' in validate_message

    def test_resend_OTP_email_using_space(self):
        param = {
            'email': "daffafawwazmaulana170901 @gmail.com"
        }
        headers = {
            "Accept": "application/json"
        }

        response = requests.post(resend_otp, data=param, headers=headers)
        data = response.json()
        pprint(data)
        validate_status = data.get('success')
        validate_message = data.get('message')

        assert response.status_code == 500
        assert validate_status == bool(False)
        assert 'Ada yang salah di sistem kami.' in validate_message

    def test_resend_OTP_email_without_at(self):
        param = {
            'email': "daffafawwazmaulana170901gmail.com"
        }
        headers = {
            "Accept": "application/json"
        }

        response = requests.post(resend_otp, data=param, headers=headers)
        data = response.json()
        pprint(data)
        validate_status = data.get('success')
        validate_message = data.get('message')['email']

        assert response.status_code == 422
        assert validate_status == bool(False)
        assert 'email harus merupakan alamat email yang valid.' in validate_message



