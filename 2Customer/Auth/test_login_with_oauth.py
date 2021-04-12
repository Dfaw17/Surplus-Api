import requests
from env import stagging
from pprint import pprint
from assertpy import assert_that

class TestCustomerLoginOauth:

    global setting_env,register_oauth,login_oauth,delete_oauth,email,origin,id_origin

    setting_env = stagging
    register_oauth = f"{setting_env}/api/v2/customer/auth/register/oauth"
    login_oauth = f"{setting_env}/api/v2/customer/auth/login/oauth"
    delete_oauth = f"{setting_env}/api/v2/customer/profiles"
    email = "daffafawwazmaulana170901@gmail.com"
    origin = "facebook"
    id_origin = "2840811776172986"

    def test_login_with_oauth_normal(self):
        param = {
            'email': email,
            'origin': origin,
            'id_from_origin': id_origin
        }
        headers = {
            "Accept": "application/json"
        }

        register = requests.post(register_oauth, params=param, headers=headers)
        login = requests.post(login_oauth, params=param, headers=headers)
        delete = requests.delete(delete_oauth, headers={"Authorization": f"Bearer {login.json().get('token')}"})

        validate_status = login.json().get('success')
        validate_message = login.json().get('message')
        validate_token = login.json().get('token')

        assert login.status_code == 200
        assert validate_status == bool(True)
        assert 'Login customer menggunakan facebook berhasil.' in validate_message
        assert_that(validate_token).is_not_empty()

    def test_login_with_oauth_hasnt_registered(self):
        param = {
            'email': email,
            'origin': origin,
            'id_from_origin': id_origin
        }
        headers = {
            "Accept": "application/json"
        }

        login = requests.post(login_oauth, params=param, headers=headers)

        validate_status = login.json().get('success')
        validate_message = login.json().get('message')

        assert login.status_code == 404
        assert validate_status == bool(False)
        assert 'Anda belum terdaftar' in validate_message

    def test_login_with_oauth_wrong_id_origin(self):
        param = {
            'email': email,
            'origin': origin,
            'id_from_origin': id_origin
        }
        headers = {
            "Accept": "application/json"
        }
        param_failed = {
            'email': email,
            'origin': origin,
            'id_from_origin': '2840811776172786'
        }

        register = requests.post(register_oauth, params=param, headers=headers)
        loginfailed = requests.post(login_oauth, params=param_failed, headers=headers)
        login = requests.post(login_oauth, params=param, headers=headers)
        delete = requests.delete(delete_oauth, headers={"Authorization": f"Bearer {login.json().get('token')}"})

        validate_status = loginfailed.json().get('success')
        validate_message = loginfailed.json().get('message')
        #
        #
        assert loginfailed.status_code == 404
        assert validate_status == bool(False)
        assert 'Invalid Oauth Attempt' in validate_message

    def test_login_with_oauth_without_param_email(self):
        param = {
            'origin': origin,
            'id_from_origin': id_origin
        }
        headers = {
            "Accept": "application/json"
        }

        login = requests.post(login_oauth, params=param, headers=headers)

        validate_status = login.json().get('success')
        validate_message = login.json().get('message')['email']

        assert login.status_code == 422
        assert validate_status == bool(False)
        assert 'email tidak boleh kosong.' in validate_message

    def test_login_with_oauth_email_empty_value(self):
        param = {
            'email': '',
            'origin': origin,
            'id_from_origin': id_origin
        }
        headers = {
            "Accept": "application/json"
        }

        login = requests.post(login_oauth, params=param, headers=headers)

        validate_status = login.json().get('success')
        validate_message = login.json().get('message')['email']

        assert login.status_code == 422
        assert validate_status == bool(False)
        assert 'email tidak boleh kosong.' in validate_message

    def test_login_with_oauth_email_without_at(self):
        param = {
            'email': 'daffafawwazmaulana170901gmail.com',
            'origin': origin,
            'id_from_origin': id_origin
        }
        headers = {
            "Accept": "application/json"
        }

        login = requests.post(login_oauth, params=param, headers=headers)

        validate_status = login.json().get('success')
        validate_message = login.json().get('message')['email']

        assert login.status_code == 422
        assert validate_status == bool(False)
        assert 'email harus merupakan alamat email yang valid.' in validate_message

    def test_login_with_oauth_email_with_space(self):
        param = {
            'email': 'daffafawwazmaulana170901 @gmail.com',
            'origin': origin,
            'id_from_origin': id_origin
        }
        headers = {
            "Accept": "application/json"
        }

        login = requests.post(login_oauth, params=param, headers=headers)

        validate_status = login.json().get('success')
        validate_message = login.json().get('message')

        assert login.status_code == 404
        assert validate_status == bool(False)
        assert 'Anda belum terdaftar' in validate_message

    def test_login_with_oauth_wrong_value(self):
        param = {
            'email': email,
            'origin': 'facebookk',
            'id_from_origin': id_origin
        }
        headers = {
            "Accept": "application/json"
        }

        login = requests.post(login_oauth, params=param, headers=headers)

        validate_status = login.json().get('success')
        validate_message = login.json().get('message')['origin']

        assert login.status_code == 422
        assert validate_status == bool(False)
        assert 'Sosial media hanya boleh Google atau Facebook' in validate_message

    def test_login_with_oauth_without_param_origin(self):
        param = {
            'email': email,
            'id_from_origin': id_origin
        }
        headers = {
            "Accept": "application/json"
        }

        login = requests.post(login_oauth, params=param, headers=headers)

        validate_status = login.json().get('success')
        validate_message = login.json().get('message')['origin']

        assert login.status_code == 422
        assert validate_status == bool(False)
        assert 'Sosial media tidak boleh kosong.' in validate_message

    def test_login_with_oauth_origin_empty_value(self):
        param = {
            'email': email,
            'origin': '',
            'id_from_origin': id_origin
        }
        headers = {
            "Accept": "application/json"
        }

        login = requests.post(login_oauth, params=param, headers=headers)

        validate_status = login.json().get('success')
        validate_message = login.json().get('message')['origin']

        assert login.status_code == 422
        assert validate_status == bool(False)
        assert 'Sosial media tidak boleh kosong.' in validate_message

    def test_login_with_oauth_id_origin_empty_value(self):
        param = {
            'email': email,
            'origin': origin,
            'id_from_origin': ''
        }
        headers = {
            "Accept": "application/json"
        }

        login = requests.post(login_oauth, params=param, headers=headers)

        validate_status = login.json().get('success')
        validate_message = login.json().get('message')['id_from_origin']

        assert login.status_code == 422
        assert validate_status == bool(False)
        assert 'id from origin tidak boleh kosong.' in validate_message

    def test_login_with_oauth_without_param_id_origin(self):
        param = {
            'email': email,
            'origin': origin
        }
        headers = {
            "Accept": "application/json"
        }

        login = requests.post(login_oauth, params=param, headers=headers)

        validate_status = login.json().get('success')
        validate_message = login.json().get('message')['id_from_origin']

        assert login.status_code == 422
        assert validate_status == bool(False)
        assert 'id from origin tidak boleh kosong.' in validate_message


