import requests
from env import stagging
from pprint import pprint
from assertpy import assert_that

class TestCustomerLikeUnlikeForum:

    global setting_env, url_login, url_forum, url_like_unlike, email, kata_sandi, wrong_token

    setting_env = stagging
    url_login = f"{setting_env}/api/v2/customer/auth/login/email"
    url_forum = f"{setting_env}/api/v2/customer/forums"
    url_like_unlike = f"{setting_env}/api/v2/customer/likes"
    email = "kopiruangvirtual@gmail.com"
    kata_sandi = '12345678'
    wrong_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvc3RhZ2luZy5hZG1pbnN1cnBsdXMubmV0XC9hcGlcL3YyXC9jdXN0b21lclwvYXV0aFwvbG9naW5cL2VtYWlsIiwiaWF0IjoxNjE2ODA1NzI2LCJleHAiOjE2MTkzOTc3MjYsIm5iZiI6MTYxNjgwNTcyNiwianRpIjoib05ESmxFRE5hSzNrN2RtVyIsInN1YiI6NDEyNiwicHJ2IjoiMjc0MTA1ZGE2ZTk1YmVmMjgwNzc4NmRkODczODg2N2NmOWMwMmFhYiJ9.fj51xIfQrqleRvdSJUbWcdrvsxQPUn8HpccnOmTgPDI'

    def test_set_like_positive(self):
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
            'forum_category_id': '1',
            'perPage': '5',
            'page': '1'
        }
        index_forum = requests.get(url_forum, params=param2, headers=headers2)
        param3 = {
            'id': index_forum.json().get('data')['forums']['data'][0]['id'],
            'event': 'forum'
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        like_unlike = requests.post(url_like_unlike, params=param3, headers=headers3)

        validasi_status = like_unlike.json().get('success')
        validasi_message = like_unlike.json().get('message')

        assert like_unlike.status_code == 200
        assert validasi_status == bool(True)
        assert_that(validasi_message).is_not_none()

    def test_set_unlike_positive(self):
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
            'forum_category_id': '1',
            'perPage': '5',
            'page': '1'
        }
        index_forum = requests.get(url_forum, params=param2, headers=headers2)
        param3 = {
            'id': index_forum.json().get('data')['forums']['data'][0]['id'],
            'event': 'forum'
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        like_unlike = requests.post(url_like_unlike, params=param3, headers=headers3)

        validasi_status = like_unlike.json().get('success')
        validasi_message = like_unlike.json().get('message')

        assert like_unlike.status_code == 200
        assert validasi_status == bool(True)
        assert_that(validasi_message).is_not_none()

    def test_set_U_like_wrong_token(self):
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
            'forum_category_id': '1',
            'perPage': '5',
            'page': '1'
        }
        index_forum = requests.get(url_forum, params=param2, headers=headers2)
        param3 = {
            'id': index_forum.json().get('data')['forums']['data'][0]['id'],
            'event': 'forum'
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": wrong_token
        }
        like_unlike = requests.post(url_like_unlike, params=param3, headers=headers3)

        validasi_status = like_unlike.json().get('success')
        validasi_message = like_unlike.json().get('message')

        assert like_unlike.status_code == 401
        assert validasi_status == bool(False)
        assert "Unauthorized" in validasi_message

    def test_set_U_like_token_empty_value(self):
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
            'forum_category_id': '1',
            'perPage': '5',
            'page': '1'
        }
        index_forum = requests.get(url_forum, params=param2, headers=headers2)
        param3 = {
            'id': index_forum.json().get('data')['forums']['data'][0]['id'],
            'event': 'forum'
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": ''
        }
        like_unlike = requests.post(url_like_unlike, params=param3, headers=headers3)

        validasi_status = like_unlike.json().get('success')
        validasi_message = like_unlike.json().get('message')

        assert like_unlike.status_code == 401
        assert validasi_status == bool(False)
        assert "Unauthorized" in validasi_message

    def test_set_U_like_without_param_id(self):
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
            'forum_category_id': '1',
            'perPage': '5',
            'page': '1'
        }
        index_forum = requests.get(url_forum, params=param2, headers=headers2)
        param3 = {
            # 'id': index_forum.json().get('data')['forums']['data'][0]['id'],
            'event': 'forum'
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        like_unlike = requests.post(url_like_unlike, params=param3, headers=headers3)

        validasi_status = like_unlike.json().get('success')
        validasi_message = like_unlike.json().get('message')['id']

        assert like_unlike.status_code == 422
        assert validasi_status == bool(False)
        assert "id tidak boleh kosong." in validasi_message

    def test_set_u_like_param_id_not_found(self):
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
            'forum_category_id': '1',
            'perPage': '5',
            'page': '1'
        }
        index_forum = requests.get(url_forum, params=param2, headers=headers2)
        param3 = {
            'id': '666666',
            'event': 'forum'
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        like_unlike = requests.post(url_like_unlike, params=param3, headers=headers3)

        validasi_status = like_unlike.json().get('success')
        validasi_message = like_unlike.json().get('message')

        assert like_unlike.status_code == 404
        assert validasi_status == bool(False)
        assert "Forum tidak ditemukan" in validasi_message

    def test_set_U_like_param_id_empty_value(self):
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
            'forum_category_id': '1',
            'perPage': '5',
            'page': '1'
        }
        index_forum = requests.get(url_forum, params=param2, headers=headers2)
        param3 = {
            'id': "",
            'event': 'forum'
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        like_unlike = requests.post(url_like_unlike, params=param3, headers=headers3)

        validasi_status = like_unlike.json().get('success')
        validasi_message = like_unlike.json().get('message')['id']

        assert like_unlike.status_code == 422
        assert validasi_status == bool(False)
        assert "id tidak boleh kosong." in validasi_message

    def test_set_U_like_param_id_text_value(self):
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
            'forum_category_id': '1',
            'perPage': '5',
            'page': '1'
        }
        index_forum = requests.get(url_forum, params=param2, headers=headers2)
        param3 = {
            'id': "aaaa",
            'event': 'forum'
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        like_unlike = requests.post(url_like_unlike, params=param3, headers=headers3)

        validasi_status = like_unlike.json().get('success')
        validasi_message = like_unlike.json().get('message')['id']

        assert like_unlike.status_code == 422
        assert validasi_status == bool(False)
        assert "id harus berupa angka." in validasi_message

    def test_set_u_like_param_without_param_event(self):
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
            'forum_category_id': '1',
            'perPage': '5',
            'page': '1'
        }
        index_forum = requests.get(url_forum, params=param2, headers=headers2)
        param3 = {
            'id': index_forum.json().get('data')['forums']['data'][0]['id']
            # 'event': 'forum'
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        like_unlike = requests.post(url_like_unlike, params=param3, headers=headers3)

        validasi_status = like_unlike.json().get('success')
        validasi_message = like_unlike.json().get('message')['event']

        assert like_unlike.status_code == 422
        assert validasi_status == bool(False)
        assert "event tidak boleh kosong." in validasi_message

    def test_set_U_like_param_event_empty_value(self):
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
            'forum_category_id': '1',
            'perPage': '5',
            'page': '1'
        }
        index_forum = requests.get(url_forum, params=param2, headers=headers2)
        param3 = {
            'id': index_forum.json().get('data')['forums']['data'][0]['id'],
            'event': ''
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        like_unlike = requests.post(url_like_unlike, params=param3, headers=headers3)

        validasi_status = like_unlike.json().get('success')
        validasi_message = like_unlike.json().get('message')['event']

        assert like_unlike.status_code == 422
        assert validasi_status == bool(False)
        assert "event tidak boleh kosong." in validasi_message

    def test_set_U_like_param_event_not_forum_value(self):
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
            'forum_category_id': '1',
            'perPage': '5',
            'page': '1'
        }
        index_forum = requests.get(url_forum, params=param2, headers=headers2)
        param3 = {
            'id': index_forum.json().get('data')['forums']['data'][0]['id'],
            'event': 'forummm'
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        like_unlike = requests.post(url_like_unlike, params=param3, headers=headers3)

        validasi_status = like_unlike.json().get('success')
        validasi_message = like_unlike.json().get('message')['event']

        assert like_unlike.status_code == 422
        assert validasi_status == bool(False)
        assert "event yang dipilih tidak tersedia." in validasi_message

