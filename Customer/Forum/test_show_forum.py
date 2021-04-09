import requests
from env import stagging
from pprint import pprint
from assertpy import assert_that

class TestCustomerShowForum:

    global setting_env, url_login, url_forum, url_forum_show, email, kata_sandi, wrong_token

    setting_env = stagging
    url_login = f"{setting_env}/api/v2/customer/auth/login/email"
    url_forum = f"{setting_env}/api/v2/customer/forums"
    url_forum_show = f"{setting_env}/api/v2/customer/forums/"
    email = "kopiruangvirtual@gmail.com"
    kata_sandi = '12345678'
    wrong_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvc3RhZ2luZy5hZG1pbnN1cnBsdXMubmV0XC9hcGlcL3YyXC9jdXN0b21lclwvYXV0aFwvbG9naW5cL2VtYWlsIiwiaWF0IjoxNjE2ODA1NzI2LCJleHAiOjE2MTkzOTc3MjYsIm5iZiI6MTYxNjgwNTcyNiwianRpIjoib05ESmxFRE5hSzNrN2RtVyIsInN1YiI6NDEyNiwicHJ2IjoiMjc0MTA1ZGE2ZTk1YmVmMjgwNzc4NmRkODczODg2N2NmOWMwMmFhYiJ9.fj51xIfQrqleRvdSJUbWcdrvsxQPUn8HpccnOmTgPDI'

    def test_show_forum_normal(self):
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
        show_forum = requests.get(url_forum_show + str(index_forum.json().get('data')['forums']['data'][0]['id']),
                                  headers=headers2)

        validate_status = show_forum.json().get('success')
        validate_message = show_forum.json().get('message')
        validate_data = show_forum.json().get('data')

        assert show_forum.status_code == 200
        assert validate_status == bool(True)
        assert "Data forum berhasil ditemukan." in validate_message
        assert_that(validate_data).is_not_none()
        assert_that(validate_data).contains_only('id', 'user_id', 'forum_kategori_id', 'judul', 'konten', 'link',
                                                 'image',
                                                 'banyak_komentar', 'banyak_like', 'location', 'post_owner_name',
                                                 'category_name', 'badge_owner', 'is_post', 'is_like', 'is_report',
                                                 'is_bookmark', 'time_difference', 'images')

    def test_show_forum_wrong_token(self):
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
        show_forum = requests.get(url_forum_show + str(index_forum.json().get('data')['forums']['data'][0]['id']),
                                  headers=headers3)

        validate_status = show_forum.json().get('success')
        validate_message = show_forum.json().get('message')

        assert show_forum.status_code == 401
        assert validate_status == bool(False)
        assert "Unauthorized" in validate_message

    def test_show_forum_token_empty_value(self):
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
            "Authorization": ''
        }
        show_forum = requests.get(url_forum_show + str(index_forum.json().get('data')['forums']['data'][0]['id']),
                                  headers=headers3)

        validate_status = show_forum.json().get('success')
        validate_message = show_forum.json().get('message')

        assert show_forum.status_code == 401
        assert validate_status == bool(False)
        assert "Unauthorized" in validate_message

    def test_show_forum_id_not_found(self):
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
        show_forum = requests.get(url_forum_show + '6666', headers=headers3)

        validate_status = show_forum.json().get('success')
        validate_message = show_forum.json().get('message')

        assert show_forum.status_code == 404
        assert validate_status == bool(False)
        assert "Data forum tidak ditemukan" in validate_message

    def test_show_forum_id_empty_value(self):
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
        show_forum = requests.get(url_forum_show, headers=headers3)

        validate_status = show_forum.json().get('success')
        validate_message_perPage = show_forum.json().get('message')['perPage']
        validate_message_page = show_forum.json().get('message')['page']

        assert show_forum.status_code == 422
        assert validate_status == bool(False)
        assert "per page tidak boleh kosong." in validate_message_perPage
        assert "page tidak boleh kosong." in validate_message_page

    def test_show_forum_id_text_value(self):
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
        show_forum = requests.get(url_forum_show + 'aaaa', headers=headers3)

        validate_status = show_forum.json().get('success')
        validate_message = show_forum.json().get('message')

        assert show_forum.status_code == 404
        assert validate_status == bool(False)
        assert "Data forum tidak ditemukan" in validate_message
