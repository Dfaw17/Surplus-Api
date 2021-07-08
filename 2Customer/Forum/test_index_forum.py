import requests
from env import *
from assertpy import assert_that


class TestCustomerIndexForum:
    global setting_env, url_login, url_forum, email, kata_sandi, wrong_token

    setting_env = mock
    url_login = f"{setting_env}/api/v2/customer/auth/login/email"
    url_forum = f"{setting_env}/api/v2/customer/forums"
    email = "kopiruangvirtual@gmail.com"
    kata_sandi = '12345678'
    wrong_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvc3RhZ2luZy5hZG1pbnN1cnBsdXMubmV0XC9hcGlcL3YyXC9jdXN0b21lclwvYXV0aFwvbG9naW5cL2VtYWlsIiwiaWF0IjoxNjE2ODA1NzI2LCJleHAiOjE2MTkzOTc3MjYsIm5iZiI6MTYxNjgwNTcyNiwianRpIjoib05ESmxFRE5hSzNrN2RtVyIsInN1YiI6NDEyNiwicHJ2IjoiMjc0MTA1ZGE2ZTk1YmVmMjgwNzc4NmRkODczODg2N2NmOWMwMmFhYiJ9.fj51xIfQrqleRvdSJUbWcdrvsxQPUn8HpccnOmTgPDI'

    def test_index_forum_normal(self):
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
        index_forum = requests.get(url_forum)

        validate_status = index_forum.json().get('success')
        validate_message = index_forum.json().get('message')
        validate_data = index_forum.json().get('data')
        validate_data_donation_event = index_forum.json().get('data')['donation_event']
        validate_data_popular_posts = index_forum.json().get('data')['popular_posts']
        validate_data_saved_posts = index_forum.json().get('data')['saved_posts']
        validate_data_newest_posts = index_forum.json().get('data')['newest_posts']

        assert index_forum.status_code == 200
        assert validate_status == bool(True)
        assert 'Data forum berhasil ditemukan.' in validate_message
        assert_that(validate_data).contains_only('donation_event','popular_posts','liked_posts','saved_posts','newest_posts')
        assert_that(validate_data_donation_event).is_type_of(list)
        assert_that(validate_data_popular_posts).is_type_of(list)
        assert_that(validate_data_saved_posts).is_type_of(list)
        assert_that(validate_data_newest_posts).is_type_of(list)
        assert_that(len(validate_data_donation_event)).is_equal_to(5)
        assert_that(len(validate_data_popular_posts)).is_equal_to(5)
        assert_that(len(validate_data_saved_posts)).is_equal_to(5)
        assert_that(len(validate_data_newest_posts)).is_equal_to(5)
        assert_that(validate_data_donation_event[0]).contains_only('id','user_id','category_id','judul','konten','link','image','banyak_komentar','banyak_like','location','post_owner_name','category_name','badge_owner','is_post','is_like','is_report','is_bookmark','time_difference','images')
        assert_that(validate_data_popular_posts[0]).contains_only('id','user_id','category_id','judul','konten','link','image','banyak_komentar','banyak_like','location','post_owner_name','category_name','badge_owner','is_post','is_like','is_report','is_bookmark','time_difference','images')
        assert_that(validate_data_saved_posts[0]).contains_only('id','user_id','category_id','judul','konten','link','image','banyak_komentar','banyak_like','location','post_owner_name','category_name','badge_owner','is_post','is_like','is_report','is_bookmark','time_difference','images')
        assert_that(validate_data_newest_posts[0]).contains_only('id','user_id','category_id','judul','konten','link','image','banyak_komentar','banyak_like','location','post_owner_name','category_name','badge_owner','is_post','is_like','is_report','is_bookmark','time_difference','images')

    def test_index_forum_token_empty(self):
        param = {
            'email': email,
            'password': kata_sandi
        }
        headers = {
            "Accept": "application/json"
        }
        login = requests.post(url_login, params=param, headers=headers)
        headers2 = {
            "Accept": "application/json"
            # "Authorization": f"Bearer {login.json().get('token')}"
        }
        param2 = {
            'forum_category_id': '1',
            'perPage': '5',
            'page': '1'
        }
        update_passwrod = requests.get(url_forum, params=param2, headers=headers2)

        validate_status = update_passwrod.json().get('success')
        validate_message = update_passwrod.json().get('message')

        assert update_passwrod.status_code == 401
        assert validate_status == bool(False)
        assert 'Unauthorized' in validate_message

    def test_index_forum_wrong_token(self):
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
            'forum_category_id': '1',
            'perPage': '5',
            'page': '1'
        }
        update_passwrod = requests.get(url_forum, params=param2, headers=headers2)

        validate_status = update_passwrod.json().get('success')
        validate_message = update_passwrod.json().get('message')

        assert update_passwrod.status_code == 401
        assert validate_status == bool(False)
        assert 'Unauthorized' in validate_message

    def test_index_forum_category_id_not_found(self):
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
            'forum_category_id': '1000',
            'perPage': '5',
            'page': '1'
        }
        update_passwrod = requests.get(url_forum, params=param2, headers=headers2)

        validate_status = update_passwrod.json().get('success')
        validate_message = update_passwrod.json().get('message')

        assert update_passwrod.status_code == 200
        assert validate_status == bool(True)
        assert 'Data forum berhasil ditemukan.' in validate_message

    def test_index_forum_category_id_empty_value(self):
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
            'forum_category_id': '',
            'perPage': '5',
            'page': '1'
        }
        update_passwrod = requests.get(url_forum, params=param2, headers=headers2)

        validate_status = update_passwrod.json().get('success')
        validate_message = update_passwrod.json().get('message')['forum_category_id']

        assert update_passwrod.status_code == 422
        assert validate_status == bool(False)
        assert 'Kategori forum harus berupa angka.' in validate_message

    def test_index_forum_without_param_category_id(self):
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
            # 'forum_category_id': '',
            'perPage': '5',
            'page': '1'
        }
        update_passwrod = requests.get(url_forum, params=param2, headers=headers2)

        validate_status = update_passwrod.json().get('success')
        validate_message = update_passwrod.json().get('message')

        assert update_passwrod.status_code == 200
        assert validate_status == bool(True)
        assert 'Data forum berhasil ditemukan.' in validate_message

    def test_index_forum_category_id_text_value(self):
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
            'forum_category_id': 'aaaaa',
            'perPage': '5',
            'page': '1'
        }
        update_passwrod = requests.get(url_forum, params=param2, headers=headers2)

        validate_status = update_passwrod.json().get('success')
        validate_message = update_passwrod.json().get('message')['forum_category_id']

        assert update_passwrod.status_code == 422
        assert validate_status == bool(False)
        assert 'Kategori forum harus berupa angka.' in validate_message

    def test_index_forum_perPage_empty_value(self):
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
            'perPage': '',
            'page': '1'
        }
        update_passwrod = requests.get(url_forum, params=param2, headers=headers2)

        validate_status = update_passwrod.json().get('success')
        validate_message = update_passwrod.json().get('message')['perPage']

        assert update_passwrod.status_code == 422
        assert validate_status == bool(False)
        assert 'per page tidak boleh kosong.' in validate_message

    def test_index_forum_perPage_text_value(self):
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
            'perPage': 'aaa',
            'page': '1'
        }
        update_passwrod = requests.get(url_forum, params=param2, headers=headers2)

        validate_status = update_passwrod.json().get('success')
        validate_message = update_passwrod.json().get('message')['perPage']

        assert update_passwrod.status_code == 422
        assert validate_status == bool(False)
        assert 'per page harus berupa angka.' in validate_message

    def test_index_forum_without_param_perPage(self):
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
            # 'perPage': 'aaa',
            'page': '1'
        }
        update_passwrod = requests.get(url_forum, params=param2, headers=headers2)

        validate_status = update_passwrod.json().get('success')
        validate_message = update_passwrod.json().get('message')['perPage']

        assert update_passwrod.status_code == 422
        assert validate_status == bool(False)
        assert 'per page tidak boleh kosong.' in validate_message

    def test_index_forum_perPage_minus_value(self):
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
            'perPage': '-5',
            'page': '1'
        }
        update_passwrod = requests.get(url_forum, params=param2, headers=headers2)

        validate_status = update_passwrod.json().get('success')
        validate_message = update_passwrod.json().get('message')

        assert update_passwrod.status_code == 500
        assert validate_status == bool(False)
        assert 'Aduh!' in validate_message

    def test_index_forum_page_empty_value(self):
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
            'page': ''
        }
        update_passwrod = requests.get(url_forum, params=param2, headers=headers2)

        validate_status = update_passwrod.json().get('success')
        validate_message = update_passwrod.json().get('message')['page']

        assert update_passwrod.status_code == 422
        assert validate_status == bool(False)
        assert 'page tidak boleh kosong.' in validate_message

    def test_index_forum_page_text_value(self):
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
            'page': 'aaa'
        }
        update_passwrod = requests.get(url_forum, params=param2, headers=headers2)

        validate_status = update_passwrod.json().get('success')
        validate_message = update_passwrod.json().get('message')['page']

        assert update_passwrod.status_code == 422
        assert validate_status == bool(False)
        assert 'page harus berupa angka.' in validate_message

    def test_index_forum_without_param_page(self):
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
            'perPage': '5'
            # 'page': 'aaa'
        }
        update_passwrod = requests.get(url_forum, params=param2, headers=headers2)

        validate_status = update_passwrod.json().get('success')
        validate_message = update_passwrod.json().get('message')['page']

        assert update_passwrod.status_code == 422
        assert validate_status == bool(False)
        assert 'page tidak boleh kosong.' in validate_message

    def test_index_forum_page_minus_value(self):
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
            'page': '-1'
        }
        update_passwrod = requests.get(url_forum, params=param2, headers=headers2)

        validate_status = update_passwrod.json().get('success')
        validate_message = update_passwrod.json().get('message')

        assert update_passwrod.status_code == 200
        assert validate_status == bool(True)
        assert 'Data forum berhasil ditemukan.' in validate_message
