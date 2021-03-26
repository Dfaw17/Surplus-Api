import requests
from env import stagging
from pprint import pprint
from assertpy import assert_that

class TestCustomerRegisterOauth:

    global setting_env,register_oauth,login_auth,delete_account,email,origin_id,origin

    setting_env = stagging
    register_oauth = f"{setting_env}/api/v2/customer/auth/register/oauth"
    login_auth = f"{setting_env}/api/v2/customer/auth/login/oauth"
    delete_account = f"{setting_env}/api/v2/customer/profiles"
    email = "daffafawwazmaulana170901@gmail.com"
    origin_id = "2840811776172986"
    origin = "facebook"

    def test_register_with_oauth_normal(self):
        param = {

            "email": email,
            'origin': origin,
            'id_from_origin': origin_id
        }
        response = requests.post(register_oauth, data=param)
        data = response.json()

        validate_status = data.get('success')
        validate_message = data.get('message')
        validate_email = data.get('data')['email']
        validate_auth = data.get('data')['auth_origin']

        assert response.status_code == 201
        assert validate_status == bool(True)
        assert 'Registrasi berhasil.' in validate_message
        assert validate_email == email
        assert validate_auth == origin

        login_oauth = requests.post(login_auth, data=param)
        token = login_oauth.json().get('token')
        headers2 = {
            "Authorization": f"Bearer {token}"
        }
        delete_oauth = requests.delete(delete_account, headers=headers2)

    def test_register_with_oauth_email_empty_value(self):
        param = {

            "email": "",
            'origin': origin,
            'id_from_origin': origin_id
        }
        headers = {
            "Accept": "application/json"
        }
        response = requests.post(register_oauth, data=param, headers=headers)
        data = response.json()

        validate_status = data.get('success')
        validate_message = data.get('message')['email']

        assert response.status_code == 422
        assert validate_status == bool(False)
        assert 'email tidak boleh kosong.' in validate_message

    def test_register_with_oauth_without_param_email(self):
        param = {
            'origin': origin,
            'id_from_origin': origin_id
        }
        headers = {
            "Accept": "application/json"
        }
        response = requests.post(register_oauth, data=param, headers=headers)
        data = response.json()

        validate_status = data.get('success')
        validate_message = data.get('message')['email']

        assert response.status_code == 422
        assert validate_status == bool(False)
        assert 'email tidak boleh kosong.' in validate_message

    def test_register_with_oauth_origin_empty_value(self):
        param = {
            'email': email,
            'origin': '',
            'id_from_origin': origin_id
        }
        headers = {
            "Accept": "application/json"
        }
        response = requests.post(register_oauth, data=param, headers=headers)
        data = response.json()
        pprint(data)
        validate_status = data.get('success')
        validate_message = data.get('message')['origin']

        assert response.status_code == 422
        assert validate_status == bool(False)
        assert 'Sosial media tidak boleh kosong.' in validate_message

    def test_register_with_oauth_without_param_origin(self):
        param = {
            'email': email,
            'id_from_origin': origin_id
        }
        headers = {
            "Accept": "application/json"
        }
        response = requests.post(register_oauth, data=param, headers=headers)
        data = response.json()
        pprint(data)
        validate_status = data.get('success')
        validate_message = data.get('message')['origin']

        assert response.status_code == 422
        assert validate_status == bool(False)
        assert 'Sosial media tidak boleh kosong.' in validate_message

    def test_register_with_oauth_id_empty_value(self):
        param = {
            'email': email,
            'origin': origin,
            'id_from_origin': ''
        }
        headers = {
            "Accept": "application/json"
        }
        response = requests.post(register_oauth, data=param, headers=headers)
        data = response.json()
        pprint(data)
        validate_status = data.get('success')
        validate_message = data.get('message')['id_from_origin']

        assert response.status_code == 422
        assert validate_status == bool(False)
        assert 'id from origin tidak boleh kosong.' in validate_message

    def test_register_with_oauth_without_param_id(self):
        param = {
            'email': email,
            'origin': origin,
            'id_from_origin': ''
        }
        headers = {
            "Accept": "application/json"
        }
        response = requests.post(register_oauth, data=param, headers=headers)
        data = response.json()
        pprint(data)
        validate_status = data.get('success')
        validate_message = data.get('message')['id_from_origin']

        assert response.status_code == 422
        assert validate_status == bool(False)
        assert 'id from origin tidak boleh kosong.' in validate_message

    def test_register_with_oauth_email_without_at(self):
        param = {
            'email': 'halogmail.com',
            'origin': origin,
            'id_from_origin': origin_id
        }
        headers = {
            "Accept": "application/json"
        }
        response = requests.post(register_oauth, data=param, headers=headers)
        data = response.json()
        pprint(data)
        validate_status = data.get('success')
        validate_message = data.get('message')['email']

        assert response.status_code == 422
        assert validate_status == bool(False)
        assert 'email harus merupakan alamat email yang valid.' in validate_message

    def test_register_with_oauth_email_using_space(self):
        param = {
            'email': 'halo gmail.com',
            'origin': origin,
            'id_from_origin': origin_id
        }
        headers = {
            "Accept": "application/json"
        }
        response = requests.post(register_oauth, data=param, headers=headers)
        data = response.json()
        pprint(data)
        validate_status = data.get('success')
        validate_message = data.get('message')['email']

        assert response.status_code == 422
        assert validate_status == bool(False)
        assert 'email harus merupakan alamat email yang valid.' in validate_message

    def test_register_with_oauth_wrong_social_media(self):
        param = {
            'email': 'halogmail.com',
            'origin': 'facebookk',
            'id_from_origin': origin_id
        }
        headers = {
            "Accept": "application/json"
        }
        response = requests.post(register_oauth, data=param, headers=headers)
        data = response.json()
        pprint(data)
        validate_status = data.get('success')
        validate_message = data.get('message')['origin']

        assert response.status_code == 422
        assert validate_status == bool(False)
        assert 'Sosial media hanya boleh Google atau Facebook' in validate_message

