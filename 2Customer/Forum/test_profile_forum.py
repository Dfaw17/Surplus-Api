import requests
from env import *
from assertpy import assert_that


class TestCustomerGetCommentForum:
    global setting_env, url_login, url_profile_forum, email, kata_sandi, wrong_token

    setting_env = mock
    url_login = f"{setting_env}/api/v2/customer/auth/login/email"
    url_profile_forum = f"{setting_env}/api/v2/customer/profile-forums"
    email = "kopiruangvirtual@gmail.com"
    kata_sandi = '12345678'
    wrong_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvc3RhZ2luZy5hZG1pbnN1cnBsdXMubmV0XC9hcGlcL3YyXC9jdXN0b21lclwvYXV0aFwvbG9naW5cL2VtYWlsIiwiaWF0IjoxNjE2ODA1NzI2LCJleHAiOjE2MTkzOTc3MjYsIm5iZiI6MTYxNjgwNTcyNiwianRpIjoib05ESmxFRE5hSzNrN2RtVyIsInN1YiI6NDEyNiwicHJ2IjoiMjc0MTA1ZGE2ZTk1YmVmMjgwNzc4NmRkODczODg2N2NmOWMwMmFhYiJ9.fj51xIfQrqleRvdSJUbWcdrvsxQPUn8HpccnOmTgPDI'

    def test_get_profile_forum_normal(self):
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

        profile_forum = requests.get(url_profile_forum, headers=headers2)

        validate_status = profile_forum.json().get('success')
        validate_message = profile_forum.json().get('message')
        validate_owner = profile_forum.json().get('data')['post_owner_name']
        validate_badge_owner = profile_forum.json().get('data')['badge_owner']
        validate_total_post = profile_forum.json().get('data')['total_post']
        validate_total_like = profile_forum.json().get('data')['total_like']
        validate_total_saved = profile_forum.json().get('data')['total_saved']
        validate_forums = profile_forum.json().get('data')['newest_forums']
        validate_forums_saved = profile_forum.json().get('data')['saved_forums']
        validate_forums_liked = profile_forum.json().get('data')['liked_forums']
        calculate_like = sum([a['banyak_like'] for a in validate_forums])
        calculate_saved = sum([a['banyak_disimpan'] for a in validate_forums])

        assert profile_forum.status_code == 200
        assert validate_status == bool(True)
        assert 'Data profile forum ditemukan.' in validate_message
        assert_that(validate_owner).is_not_empty() and assert_that(validate_owner).is_not_none()
        assert_that(validate_badge_owner).is_not_none()
        assert_that(validate_total_post).is_not_none()
        assert_that(validate_total_like).is_not_none()
        assert_that(validate_total_saved).is_not_none()
        assert_that(validate_forums).is_type_of(list)
        assert_that(validate_forums_saved).is_type_of(list)
        assert_that(validate_forums_liked).is_type_of(list)
        assert_that(validate_forums).is_type_of(list)
        assert_that(validate_total_post).is_type_of(int)
        assert_that(validate_total_like).is_type_of(int)
        assert_that(validate_total_saved).is_type_of(int)
        assert_that(len(validate_forums)).is_equal_to(5)
        assert_that(len(validate_forums_saved)).is_equal_to(5)
        assert_that(len(validate_forums_liked)).is_equal_to(5)
        assert_that(profile_forum.json().get('data')).contains_only('post_owner_name', 'badge_owner', 'total_post', 'total_like',
                                                           'total_saved', 'newest_forums', 'saved_forums',
                                                           'liked_forums')