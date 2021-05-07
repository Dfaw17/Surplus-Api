import requests
from env import stagging

class TestLogin:

    global url_login, email, kata_sandi, email_not_registered, kata_sandi_not_registered\
            , wrong_email, wrong_pass, email_withot_at, kata_sandi_kurang_char, setting_env

    setting_env = stagging
    url_login = f"{setting_env}/api/v2/merchant/auth/login"
    email ="vd1@gmail.com"
    kata_sandi ="12345678"
    email_not_registered = "kopi.ruang.rehat@gmail.com"
    kata_sandi_not_registered = "12345678"
    wrong_email = "vd11@gmail.com"
    wrong_pass = "123456789"
    email_withot_at = "vd gmail.com"
    kata_sandi_kurang_char = "123"

    def test_login_normal(self):

        param = {
            "email": email,
            "password": kata_sandi
        }

        response =requests.post(url_login, data=param,
                                headers={'Accept': 'application/json'})
        data = response.json()
        validate_message = data.get("message")
        validate_status = data.get("success")

        assert validate_message == "Login merchant berhasil."
        assert validate_status == bool(True)
        assert response.status_code == 200

    def test_login_akun_belum_register(self):
        param = {
            "email": email_not_registered,
            "password": kata_sandi_not_registered
        }

        response = requests.post(url_login, data=param,
                                 headers={'Accept': 'application/json'})
        data = response.json()
        validate_message = data.get("message")
        validate_status = data.get("success")

        assert "tidak ada atau belum disetujui." in validate_message
        assert validate_status == bool(False)
        assert response.status_code == 404

    def test_login_salah_email(self):
        param = {
            "email": wrong_email,
            "password": kata_sandi
        }

        response = requests.post(url_login, data=param,
                                 headers={'Accept': 'application/json'})
        data = response.json()
        validate_message = data.get("message")
        validate_status = data.get("success")

        assert "tidak ada atau belum disetujui." in validate_message
        assert validate_status == bool(False)
        assert response.status_code == 404

    def test_login_salah_password(self):
        param = {
            "email": email,
            "password": wrong_pass
        }

        response = requests.post(url_login, data=param,
                                 headers={'Accept': 'application/json'})
        data = response.json()
        validate_message = data.get("message")
        validate_status = data.get("success")

        assert validate_message == "Email atau password salah."
        assert validate_status == bool(False)
        assert response.status_code == 404

    def test_login_empty_password(self):
        param = {
            "email": email,
            "password": ""
        }

        response = requests.post(url_login, data=param,
                                 headers={'Accept': 'application/json'})
        data = response.json()
        validate_message = data.get("message")["password"]
        validate_status = data.get("success")


        assert "Kata sandi tidak boleh kosong." in validate_message
        assert validate_status == bool(False)
        assert response.status_code == 422

    def test_login_empty_email(self):
        param = {
            "email": "",
            "password": kata_sandi
        }

        response = requests.post(url_login, data=param,
                                 headers={'Accept': 'application/json'})
        data = response.json()
        validate_message = data.get("message")["email"]
        validate_status = data.get("success")

        assert "email tidak boleh kosong." in validate_message
        assert validate_status == bool(False)
        assert response.status_code == 422

    def test_login_without_at(self):
        param = {
            "email": email_withot_at,
            "password": kata_sandi
        }

        response = requests.post(url_login, data=param,
                                 headers={'Accept': 'application/json'})
        data = response.json()
        validate_message = data.get("message")["email"]
        validate_status = data.get("success")

        assert "email harus merupakan alamat email yang valid." in validate_message
        assert validate_status == bool(False)
        assert response.status_code == 422

    def test_kata_sandi_kurang_char(self):
        param = {
            "email": email,
            "password": kata_sandi_kurang_char
        }

        response = requests.post(url_login, data=param,
                                 headers={'Accept': 'application/json'})
        data = response.json()
        validate_message = data.get("message")["password"]
        validate_status = data.get("success")

        assert "Kata sandi harus diantara 6 dan 20 karakter." in validate_message
        assert validate_status == bool(False)
        assert response.status_code == 422