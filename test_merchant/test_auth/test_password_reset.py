import requests
from env import stagging

class TestPasswordReset :

    global url_reset_pass, email, wrong_email, email_without_at, email_with_space, setting_env

    setting_env = stagging
    url_reset_pass = f"{setting_env}/api/v2/merchant/auth/password-reset"
    email = "kopiruangvirtual@gmail.com"
    wrong_email = "kopiruangvirtual1@gmail.com"
    email_without_at = "kopiruangvirtual1gmail.com"
    email_with_space = "kopiruangvirtual @gmail.com"

    def test_reset_password_normal (self):
        param = {
            "email": email
        }

        response = requests.post(url_reset_pass, data=param,
                                 headers={'Accept': 'application/json'})

        data = response.json()
        validate_status = data.get("success")
        validate_message = data.get("message")
        assert validate_status == bool(True)
        assert response.status_code == 200
        assert "Kami mengirimkan link untuk reset password ke e-mail" in validate_message

    def test_reset_password_wrong_email (self):
        param = {
            "email": wrong_email
        }

        response = requests.post(url_reset_pass, data=param,
                                 headers={'Accept': 'application/json'})

        data = response.json()
        validate_status = data.get("success")
        validate_message = data.get("message")
        assert validate_status == bool(False)
        assert response.status_code == 404
        assert "Kami tidak menemukan merchant dengan e-mail " in validate_message

    def test_reset_password_email_without_at (self):
        param = {
            "email": email_without_at
        }

        response = requests.post(url_reset_pass, data=param,
                                 headers={'Accept': 'application/json'})

        data = response.json()
        validate_status = data.get("success")
        validate_message = data.get("message")["email"]
        assert validate_status == bool(False)
        assert response.status_code == 422
        assert "email harus merupakan alamat email yang valid." in validate_message

    def test_reset_password_email_with_space (self):
        param = {
            "email": email_with_space
        }

        response = requests.post(url_reset_pass, data=param,
                                 headers={'Accept': 'application/json'})

        data = response.json()
        validate_status = data.get("success")
        validate_message = data.get("message")
        assert validate_status == bool(False)
        assert response.status_code == 404
        assert "Kami tidak menemukan merchant dengan e-mail" in validate_message

    def test_reset_password_email_empty (self):
        param = {
            "email": ""
        }

        response = requests.post(url_reset_pass, data=param,
                                 headers={'Accept': 'application/json'})

        data = response.json()
        validate_status = data.get("success")
        validate_message = data.get("message")["email"]
        assert validate_status == bool(False)
        assert response.status_code == 422
        assert "email tidak boleh kosong." in validate_message
