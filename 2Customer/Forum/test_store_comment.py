import requests
from env import *
from pprint import pprint
from assertpy import assert_that


class TestCustomerStoreForum:
    global setting_env, url_login, url_forum, url_forum_store_comment, email, kata_sandi, wrong_token

    setting_env = mock
    url_login = f"{setting_env}/api/v2/customer/auth/login/email"
    url_forum = f"{setting_env}/api/v2/customer/forums"
    url_forum_store_comment = f"{setting_env}/api/v2/customer/comments"
    email = "kopiruangvirtual@gmail.com"
    kata_sandi = '12345678'
    wrong_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvc3RhZ2luZy5hZG1pbnN1cnBsdXMubmV0XC9hcGlcL3YyXC9jdXN0b21lclwvYXV0aFwvbG9naW5cL2VtYWlsIiwiaWF0IjoxNjE2ODA1NzI2LCJleHAiOjE2MTkzOTc3MjYsIm5iZiI6MTYxNjgwNTcyNiwianRpIjoib05ESmxFRE5hSzNrN2RtVyIsInN1YiI6NDEyNiwicHJ2IjoiMjc0MTA1ZGE2ZTk1YmVmMjgwNzc4NmRkODczODg2N2NmOWMwMmFhYiJ9.fj51xIfQrqleRvdSJUbWcdrvsxQPUn8HpccnOmTgPDI'

    def test_store_comment_normal(self):
        param = {
            'email': email,
            'password': kata_sandi
        }
        headers = {
            "Accept": "application/json"
        }
        login = requests.post(url_login, params=param, headers=headers)
        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }

        forum_id = "212"
        isi_comment = "Test komentar sendiri"

        param = {
            "forum_id": forum_id,
            "comment": isi_comment,
            "mentions[0]": "dfaw17@gmail.com",
            "mentions[1]": "raffi@gmail.com"
        }
        # url_store_comment = "https://5bb4e7db-1cd4-4003-ac9a-526e1696768c.mock.pstmn.io/api/v2/customer/comments"
        store_comment = requests.post(url_forum_store_comment, headers=headers, params=param)

        validate_status = store_comment.json().get('success')
        validate_message = store_comment.json().get('message')
        validate_data = store_comment.json().get('data')

        assert store_comment.status_code == 200
        assert validate_status == bool(True)
        assert 'Komentar berhasil diposting.' in validate_message
        assert_that(validate_data['forum_id']).is_equal_to(forum_id)
        assert_that(validate_data['komentar']).is_equal_to(isi_comment)
        assert_that(validate_data).contains_only('user_id', 'forum_id', 'komentar', 'updated_at', 'created_at', 'id',
                                                 'is_like', 'time_difference', 'is_report', 'is_post', 'commenter',
                                                 'commenter_badge')

    def test_store_commnet_token_empty_value(self):
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
        headers3 = {
            "Accept": "application/json",
            "Authorization": ""
        }
        param3 = {
            "forum_id": index_forum.json().get('data')['forums']['data'][0]['id'],
            "comment": "Test komentar sendiri"
        }
        store_comment = requests.post(url_forum_store_comment, params=param3, headers=headers3)

        validate_status = store_comment.json().get('success')
        validate_message = store_comment.json().get('message')

        assert store_comment.status_code == 401
        assert validate_status == bool(False)
        assert "Unauthorized" in validate_message

    def test_store_commnet_wrong_token(self):
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
        headers3 = {
            "Accept": "application/json",
            "Authorization": wrong_token
        }
        param3 = {
            "forum_id": index_forum.json().get('data')['forums']['data'][0]['id'],
            "comment": "Test komentar sendiri"
        }
        store_comment = requests.post(url_forum_store_comment, params=param3, headers=headers3)

        validate_status = store_comment.json().get('success')
        validate_message = store_comment.json().get('message')

        assert store_comment.status_code == 401
        assert validate_status == bool(False)
        assert "Unauthorized" in validate_message

    def test_store_comment_without_param_id(self):
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
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        param3 = {
            # "forum_id": index_forum.json().get('data')['forums']['data'][0]['id'],
            "comment": "Test komentar sendiri"
        }
        store_comment = requests.post(url_forum_store_comment, params=param3, headers=headers3)

        validate_status = store_comment.json().get('success')
        validate_message = store_comment.json().get('message')['forum_id']

        assert store_comment.status_code == 422
        assert validate_status == bool(False)
        assert "Forum tidak boleh kosong." in validate_message

    def test_store_comment_param_id_not_found(self):
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
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        param3 = {
            "forum_id": '666',
            "comment": "Test komentar sendiri"
        }
        store_comment = requests.post(url_forum_store_comment, params=param3, headers=headers3)

        validate_status = store_comment.json().get('success')
        validate_message = store_comment.json().get('message')

        assert store_comment.status_code == 500
        assert validate_status == bool(False)
        assert "Aduh!" in validate_message

    def test_store_comment_param_id_empty_value(self):
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
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        param3 = {
            "forum_id": '',
            "comment": "Test komentar sendiri"
        }
        store_comment = requests.post(url_forum_store_comment, params=param3, headers=headers3)

        validate_status = store_comment.json().get('success')
        validate_message = store_comment.json().get('message')['forum_id']

        assert store_comment.status_code == 422
        assert validate_status == bool(False)
        assert "Forum tidak boleh kosong." in validate_message

    def test_store_comment_param_id_text_value(self):
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
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        param3 = {
            "forum_id": 'aaa',
            "comment": "Test komentar sendiri"
        }
        store_comment = requests.post(url_forum_store_comment, params=param3, headers=headers3)

        validate_status = store_comment.json().get('success')
        validate_message = store_comment.json().get('message')['forum_id']

        assert store_comment.status_code == 422
        assert validate_status == bool(False)
        assert "Forum harus berupa angka." in validate_message

    def test_store_comment_without_param_comment(self):
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
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        param3 = {
            "forum_id": index_forum.json().get('data')['forums']['data'][0]['id'],
            # "comment": "Test komentar sendiri"
        }
        store_comment = requests.post(url_forum_store_comment, params=param3, headers=headers3)

        validate_status = store_comment.json().get('success')
        validate_message = store_comment.json().get('message')['comment']

        assert store_comment.status_code == 422
        assert validate_status == bool(False)
        assert "Komentar tidak boleh kosong." in validate_message

    def test_store_comment_param_comment_empty_value(self):
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
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        param3 = {
            "forum_id": index_forum.json().get('data')['forums']['data'][0]['id'],
            "comment": ""
        }
        store_comment = requests.post(url_forum_store_comment, params=param3, headers=headers3)

        validate_status = store_comment.json().get('success')
        validate_message = store_comment.json().get('message')['comment']

        assert store_comment.status_code == 422
        assert validate_status == bool(False)
        assert "Komentar tidak boleh kosong." in validate_message
