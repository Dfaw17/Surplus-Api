import requests
from env import *
from assertpy import assert_that


class TestSearchFilterForum:
    global setting_env, url_login, url_aearch_filter_forum, email, kata_sandi, wrong_token

    setting_env = mock
    url_login = f"{setting_env}/api/v2/customer/auth/login/email"
    url_aearch_filter_forum = f"{setting_env}/api/v2/customer/search-forums"
    email = "kopiruangvirtual@gmail.com"
    kata_sandi = '12345678'
    wrong_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvc3RhZ2luZy5hZG1pbnN1cnBsdXMubmV0XC9hcGlcL3YyXC9jdXN0b21lclwvYXV0aFwvbG9naW5cL2VtYWlsIiwiaWF0IjoxNjE2ODA1NzI2LCJleHAiOjE2MTkzOTc3MjYsIm5iZiI6MTYxNjgwNTcyNiwianRpIjoib05ESmxFRE5hSzNrN2RtVyIsInN1YiI6NDEyNiwicHJ2IjoiMjc0MTA1ZGE2ZTk1YmVmMjgwNzc4NmRkODczODg2N2NmOWMwMmFhYiJ9.fj51xIfQrqleRvdSJUbWcdrvsxQPUn8HpccnOmTgPDI'

    def test_search_forum_all_newest_filter_loc_img_link(self):
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

        page = 1
        per_page = 5
        forum_category_id = 2

        param = {
            "list_owner": "all",
            "event": "newest",
            "forum_category_id": forum_category_id,
            "per_page": per_page,
            "page": page,
            "long_posted_time": "7_days",
            "has_address": "1",
            "has_image": "1",
            "has_link": "1"
        }
        search_filter_comment = requests.get(url_aearch_filter_forum, headers=headers, params=param)

        validate_status = search_filter_comment.json().get('success')
        validate_message = search_filter_comment.json().get('message')
        validate_data = search_filter_comment.json().get('data')
        validate_data_page = search_filter_comment.json().get('data')['current_page']
        validate_per_page = search_filter_comment.json().get('data')['per_page']
        validate_post = search_filter_comment.json().get('data')['posts']
        post_address = [d['location'] for d in validate_post]
        post_link = [d['image'] for d in validate_post]
        post_image = [d['link'] for d in validate_post]
        post_forum_category_id = [d['forum_kategori_id'] for d in validate_post]

        assert search_filter_comment.status_code == 200
        assert validate_status == bool(True)
        assert 'Data forum berhasil ditemukan.' in validate_message
        assert_that(validate_data_page).is_equal_to(page)
        assert_that(validate_per_page).is_equal_to(per_page)
        assert_that(len(validate_data['posts'])).is_equal_to(per_page)
        assert_that(post_address).does_not_contain(None)
        assert_that(post_link).does_not_contain(None)
        assert_that(post_image).does_not_contain(None)
        assert_that(post_forum_category_id).contains_only(forum_category_id)

    def test_search_forum_all_newest_filter_img_link(self):
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

        page = 1
        per_page = 5
        forum_category_id = 2

        param = {
            "list_owner": "all",
            "event": "newest",
            "forum_category_id": forum_category_id,
            "per_page": per_page,
            "page": page,
            "long_posted_time": "7_days",
            "has_image": "1",
            "has_link": "1"
        }
        search_filter_comment = requests.get(url_aearch_filter_forum, headers=headers, params=param)

        validate_status = search_filter_comment.json().get('success')
        validate_message = search_filter_comment.json().get('message')
        validate_data = search_filter_comment.json().get('data')
        validate_data_page = search_filter_comment.json().get('data')['current_page']
        validate_per_page = search_filter_comment.json().get('data')['per_page']
        validate_post = search_filter_comment.json().get('data')['posts']
        post_address = [d['location'] for d in validate_post]
        post_link = [d['image'] for d in validate_post]
        post_image = [d['link'] for d in validate_post]
        post_forum_category_id = [d['forum_kategori_id'] for d in validate_post]

        assert search_filter_comment.status_code == 200
        assert validate_status == bool(True)
        assert 'Data forum berhasil ditemukan.' in validate_message
        assert_that(validate_data_page).is_equal_to(page)
        assert_that(validate_per_page).is_equal_to(per_page)
        assert_that(len(validate_data['posts'])).is_equal_to(per_page)
        assert_that(post_link).does_not_contain(None)
        assert_that(post_image).does_not_contain(None)
        assert_that(post_forum_category_id).contains_only(forum_category_id)

    def test_search_forum_all_newest_filter_link(self):
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

        page = 1
        per_page = 5
        forum_category_id = 2

        param = {
            "list_owner": "all",
            "event": "newest",
            "forum_category_id": forum_category_id,
            "per_page": per_page,
            "page": page,
            "long_posted_time": "7_days",
            "has_link": "1"
        }
        search_filter_comment = requests.get(url_aearch_filter_forum, headers=headers, params=param)

        validate_status = search_filter_comment.json().get('success')
        validate_message = search_filter_comment.json().get('message')
        validate_data = search_filter_comment.json().get('data')
        validate_data_page = search_filter_comment.json().get('data')['current_page']
        validate_per_page = search_filter_comment.json().get('data')['per_page']
        validate_post = search_filter_comment.json().get('data')['posts']
        post_address = [d['location'] for d in validate_post]
        post_link = [d['image'] for d in validate_post]
        post_image = [d['link'] for d in validate_post]
        post_forum_category_id = [d['forum_kategori_id'] for d in validate_post]

        assert search_filter_comment.status_code == 200
        assert validate_status == bool(True)
        assert 'Data forum berhasil ditemukan.' in validate_message
        assert_that(validate_data_page).is_equal_to(page)
        assert_that(validate_per_page).is_equal_to(per_page)
        assert_that(len(validate_data['posts'])).is_equal_to(per_page)
        assert_that(post_link).does_not_contain(None)
        assert_that(post_forum_category_id).contains_only(forum_category_id)
