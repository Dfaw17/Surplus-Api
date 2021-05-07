import requests
from env import stagging
from pprint import pprint
from assertpy import assert_that

class TestCustomerGetCommentForum:

    global setting_env,url_login,get_comment,email,kata_sandi,wrong_token

    setting_env = stagging
    url_login = f"{setting_env}/api/v2/customer/auth/login/email"
    get_comment = f"{setting_env}/api/v2/customer/comments/"
    email = "kopiruangvirtual@gmail.com"
    kata_sandi = '12345678'
    wrong_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvc3RhZ2luZy5hZG1pbnN1cnBsdXMubmV0XC9hcGlcL3YyXC9jdXN0b21lclwvYXV0aFwvbG9naW5cL2VtYWlsIiwiaWF0IjoxNjE2ODA1NzI2LCJleHAiOjE2MTkzOTc3MjYsIm5iZiI6MTYxNjgwNTcyNiwianRpIjoib05ESmxFRE5hSzNrN2RtVyIsInN1YiI6NDEyNiwicHJ2IjoiMjc0MTA1ZGE2ZTk1YmVmMjgwNzc4NmRkODczODg2N2NmOWMwMmFhYiJ9.fj51xIfQrqleRvdSJUbWcdrvsxQPUn8HpccnOmTgPDI'

    def test_get_comment_normal(self):
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
        param2 = {
            'forum_id': '350'
        }
        get_commnet = requests.get(get_comment, params=param2, headers=headers2)

        validate_status = get_commnet.json().get('success')
        validate_message = get_commnet.json().get('message')
        validate_data = get_commnet.json().get('data')

        assert get_commnet.status_code == 200
        assert validate_status == bool(True)
        assert "Komentar ditemukan" in validate_message

    def test_get_commnet_none_commnet(self):
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
        param2 = {
            'forum_id': '349'
        }
        get_commnet = requests.get(get_comment, params=param2, headers=headers2)

        validate_status = get_commnet.json().get('success')
        validate_message = get_commnet.json().get('message')

        assert get_commnet.status_code == 200
        assert validate_status == bool(True)
        assert "Komentar ditemukan" in validate_message

    def test_get_commnet_token_empty_value(self):
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
        param2 = {
            'forum_id': '349'
        }
        get_commnet = requests.get(get_comment, params=param2, headers=headers2)

        validate_status = get_commnet.json().get('success')
        validate_message = get_commnet.json().get('message')

        assert get_commnet.status_code == 401
        assert validate_status == bool(False)
        assert "Unauthorized" in validate_message

    def test_get_comment_wrong_param_token(self):
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
        param2 = {
            'forum_id': '349'
        }
        get_commnet = requests.get(get_comment, params=param2, headers=headers2)

        validate_status = get_commnet.json().get('success')
        validate_message = get_commnet.json().get('message')

        assert get_commnet.status_code == 401
        assert validate_status == bool(False)
        assert "Unauthorized" in validate_message

    def test_get_commnet_id_not_found(self):
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
        param2 = {
            'forum_id': '34999'
        }
        get_commnet = requests.get(get_comment, params=param2, headers=headers2)

        validate_status = get_commnet.json().get('success')
        validate_message = get_commnet.json().get('message')

        assert get_commnet.status_code == 200
        assert validate_status == bool(True)
        assert "Komentar ditemukan" in validate_message

    def test_get_commnet_id_text_value(self):
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
        param2 = {
            'forum_id': 'aaa'
        }
        get_commnet = requests.get(get_comment, params=param2, headers=headers2)

        validate_status = get_commnet.json().get('success')
        validate_message = get_commnet.json().get('message')['forum_id']

        assert get_commnet.status_code == 422
        assert validate_status == bool(False)
        assert "Forum harus berupa angka." in validate_message

    def test_get_commnet_id_empty_value(self):
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
        param2 = {
            'forum_id': ''
        }
        get_commnet = requests.get(get_comment, params=param2, headers=headers2)

        validate_status = get_commnet.json().get('success')
        validate_message = get_commnet.json().get('message')['forum_id']

        assert get_commnet.status_code == 422
        assert validate_status == bool(False)
        assert "Forum tidak boleh kosong." in validate_message
