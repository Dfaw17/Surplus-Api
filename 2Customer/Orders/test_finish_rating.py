import requests
from env import stagging
from pprint import pprint
from assertpy import assert_that


class TestCustomerOrdersFinishRating:

    global setting_env,url_login,url_order_list,url_finish_rating,email,kata_sandi,wrong_token

    setting_env = stagging
    url_login = f"{setting_env}/api/v2/customer/auth/login/email"
    url_order_list = f"{setting_env}/api/v2/customer/orders"
    url_finish_rating = f"{setting_env}/api/v2/customer/orders/"
    email = "kopiruangvirtual@gmail.com"
    kata_sandi = '12345678'
    wrong_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvc3RhZ2luZy5hZG1pbnN1cnBsdXMubmV0XC9hcGlcL3YyXC9jdXN0b21lclwvYXV0aFwvbG9naW5cL2VtYWlsIiwiaWF0IjoxNjE2ODA1NzI2LCJleHAiOjE2MTkzOTc3MjYsIm5iZiI6MTYxNjgwNTcyNiwianRpIjoib05ESmxFRE5hSzNrN2RtVyIsInN1YiI6NDEyNiwicHJ2IjoiMjc0MTA1ZGE2ZTk1YmVmMjgwNzc4NmRkODczODg2N2NmOWMwMmFhYiJ9.fj51xIfQrqleRvdSJUbWcdrvsxQPUn8HpccnOmTgPDI'

    def test_finish_rating_normal(self):
        param = {
            'email': email,
            'password': kata_sandi
        }
        headers = {
            "Accept": "application/json"
        }
        login = requests.post(url_login, params=param, headers=headers)
        param2 = {
            'status_order': 'done'
        }
        headers2 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        list_order = requests.get(url_order_list, params=param2, headers=headers2)
        param3 = {
            'ulasan': 'Mantap Faw',
            'rating': '5'
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        finish_rating = requests.patch(
            url_finish_rating + list_order.json().get('data')[0]['registrasi_order_number'] + '/rate', data=param3,
            headers=headers3)

        validate_status = finish_rating.json().get('success')
        validate_message = finish_rating.json().get('message')
        validate_data = finish_rating.json().get('data')
        validate_data_merchant = finish_rating.json().get('data')['merchant_name']

        assert finish_rating.status_code == 200
        assert validate_status == bool(True)
        assert 'Berhasil memberikan ulasan dan rating' in validate_message
        assert_that(validate_data).is_not_none()
        assert_that(validate_data_merchant).is_not_none()
        assert validate_data_merchant == list_order.json().get('data')[0]['merchant_name']

    def test_finish_rating_token_empty_value(self):
        param = {
            'email': email,
            'password': kata_sandi
        }
        headers = {
            "Accept": "application/json"
        }
        login = requests.post(url_login, params=param, headers=headers)
        param2 = {
            'status_order': 'done'
        }
        headers2 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        list_order = requests.get(url_order_list, params=param2, headers=headers2)
        param3 = {
            'ulasan': 'Mantap Faw',
            'rating': '5'
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": ''
        }
        finish_rating = requests.patch(
            url_finish_rating + list_order.json().get('data')[0]['registrasi_order_number'] + '/rate', data=param3,
            headers=headers3)

        validate_status = finish_rating.json().get('success')
        validate_message = finish_rating.json().get('message')

        assert finish_rating.status_code == 401
        assert validate_status == bool(False)
        assert 'Unauthorized' in validate_message

    def test_finish_rating_wrong_token(self):
        param = {
            'email': email,
            'password': kata_sandi
        }
        headers = {
            "Accept": "application/json"
        }
        login = requests.post(url_login, params=param, headers=headers)
        param2 = {
            'status_order': 'done'
        }
        headers2 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        list_order = requests.get(url_order_list, params=param2, headers=headers2)
        param3 = {
            'ulasan': 'Mantap Faw',
            'rating': '5'
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": wrong_token
        }
        finish_rating = requests.patch(
            url_finish_rating + list_order.json().get('data')[0]['registrasi_order_number'] + '/rate', data=param3,
            headers=headers3)

        validate_status = finish_rating.json().get('success')
        validate_message = finish_rating.json().get('message')

        assert finish_rating.status_code == 401
        assert validate_status == bool(False)
        assert 'Unauthorized' in validate_message

    def test_finish_rating_without_param_ulasan(self):
        param = {
            'email': email,
            'password': kata_sandi
        }
        headers = {
            "Accept": "application/json"
        }
        login = requests.post(url_login, params=param, headers=headers)
        param2 = {
            'status_order': 'done'
        }
        headers2 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        list_order = requests.get(url_order_list, params=param2, headers=headers2)
        param3 = {
            # 'ulasan':'Mantap Faw',
            'rating': '5'
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        finish_rating = requests.patch(
            url_finish_rating + list_order.json().get('data')[0]['registrasi_order_number'] + '/rate', data=param3,
            headers=headers3)

        validate_status = finish_rating.json().get('success')
        validate_message = finish_rating.json().get('message')
        validate_data = finish_rating.json().get('data')
        validate_data_merchant = finish_rating.json().get('data')['merchant_name']

        assert finish_rating.status_code == 200
        assert validate_status == bool(True)
        assert 'Berhasil memberikan ulasan dan rating' in validate_message
        assert_that(validate_data).is_not_none()
        assert_that(validate_data_merchant).is_not_none()
        assert validate_data_merchant == list_order.json().get('data')[0]['merchant_name']

    def test_finish_rating_ulasan_empty_value(self):
        param = {
            'email': email,
            'password': kata_sandi
        }
        headers = {
            "Accept": "application/json"
        }
        login = requests.post(url_login, params=param, headers=headers)
        param2 = {
            'status_order': 'done'
        }
        headers2 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        list_order = requests.get(url_order_list, params=param2, headers=headers2)
        param3 = {
            'ulasan':'',
            'rating': '5'
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        finish_rating = requests.patch(
            url_finish_rating + list_order.json().get('data')[0]['registrasi_order_number'] + '/rate', data=param3,
            headers=headers3)

        validate_status = finish_rating.json().get('success')
        validate_message = finish_rating.json().get('message')
        validate_data = finish_rating.json().get('data')
        validate_data_merchant = finish_rating.json().get('data')['merchant_name']

        assert finish_rating.status_code == 200
        assert validate_status == bool(True)
        assert 'Berhasil memberikan ulasan dan rating' in validate_message
        assert_that(validate_data).is_not_none()
        assert_that(validate_data_merchant).is_not_none()
        assert validate_data_merchant == list_order.json().get('data')[0]['merchant_name']

    def test_finish_rating_empty_value(self):
        param = {
            'email': email,
            'password': kata_sandi
        }
        headers = {
            "Accept": "application/json"
        }
        login = requests.post(url_login, params=param, headers=headers)
        param2 = {
            'status_order': 'done'
        }
        headers2 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        list_order = requests.get(url_order_list, params=param2, headers=headers2)
        param3 = {
            'ulasan': 'Mantap Faw',
            'rating': ''
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        finish_rating = requests.patch(
            url_finish_rating + list_order.json().get('data')[0]['registrasi_order_number'] + '/rate', data=param3,
            headers=headers3)

        validate_status = finish_rating.json().get('success')
        validate_message = finish_rating.json().get('message')['rating']

        assert finish_rating.status_code == 422
        assert validate_status == bool(False)
        assert 'rating tidak boleh kosong.' in validate_message

    def test_finish_rating_without_param_rating(self):
        param = {
            'email': email,
            'password': kata_sandi
        }
        headers = {
            "Accept": "application/json"
        }
        login = requests.post(url_login, params=param, headers=headers)
        param2 = {
            'status_order': 'done'
        }
        headers2 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        list_order = requests.get(url_order_list, params=param2, headers=headers2)
        param3 = {
            'ulasan': 'Mantap Faw'
            # 'rating': ''
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        finish_rating = requests.patch(
            url_finish_rating + list_order.json().get('data')[0]['registrasi_order_number'] + '/rate', data=param3,
            headers=headers3)

        validate_status = finish_rating.json().get('success')
        validate_message = finish_rating.json().get('message')['rating']

        assert finish_rating.status_code == 422
        assert validate_status == bool(False)
        assert 'rating tidak boleh kosong.' in validate_message

    def test_finish_rating_text_value(self):
        param = {
            'email': email,
            'password': kata_sandi
        }
        headers = {
            "Accept": "application/json"
        }
        login = requests.post(url_login, params=param, headers=headers)
        param2 = {
            'status_order': 'done'
        }
        headers2 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        list_order = requests.get(url_order_list, params=param2, headers=headers2)
        param3 = {
            'ulasan': 'Mantap Faw',
            'rating': 'aaaa'
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        finish_rating = requests.patch(
            url_finish_rating + list_order.json().get('data')[0]['registrasi_order_number'] + '/rate', data=param3,
            headers=headers3)

        validate_status = finish_rating.json().get('success')
        validate_message = finish_rating.json().get('message')

        assert finish_rating.status_code == 500
        assert validate_status == bool(False)
        assert 'Aduh!' in validate_message

    def test_finish_rating_value_more_5(self):
        param = {
            'email': email,
            'password': kata_sandi
        }
        headers = {
            "Accept": "application/json"
        }
        login = requests.post(url_login, params=param, headers=headers)
        param2 = {
            'status_order': 'done'
        }
        headers2 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        list_order = requests.get(url_order_list, params=param2, headers=headers2)
        param3 = {
            'ulasan': 'Mantap Faw',
            'rating': '200'
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        finish_rating = requests.patch(
            url_finish_rating + list_order.json().get('data')[0]['registrasi_order_number'] + '/rate', data=param3,
            headers=headers3)

        validate_status = finish_rating.json().get('success')
        validate_message = finish_rating.json().get('message')
        validate_data = finish_rating.json().get('data')
        validate_data_merchant = finish_rating.json().get('data')['merchant_name']

        assert finish_rating.status_code == 200
        assert validate_status == bool(True)
        assert 'Berhasil memberikan ulasan dan rating' in validate_message
        assert_that(validate_data).is_not_none()
        assert_that(validate_data_merchant).is_not_none()
        assert validate_data_merchant == list_order.json().get('data')[0]['merchant_name']

    def test_finish_rating_value_minus(self):
        param = {
            'email': email,
            'password': kata_sandi
        }
        headers = {
            "Accept": "application/json"
        }
        login = requests.post(url_login, params=param, headers=headers)
        param2 = {
            'status_order': 'done'
        }
        headers2 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        list_order = requests.get(url_order_list, params=param2, headers=headers2)
        param3 = {
            'ulasan': 'Mantap Faw',
            'rating': '-600'
        }
        headers3 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        finish_rating = requests.patch(
            url_finish_rating + list_order.json().get('data')[0]['registrasi_order_number'] + '/rate', data=param3,
            headers=headers3)

        validate_status = finish_rating.json().get('success')
        validate_message = finish_rating.json().get('message')
        validate_data = finish_rating.json().get('data')
        validate_data_merchant = finish_rating.json().get('data')['merchant_name']

        assert finish_rating.status_code == 200
        assert validate_status == bool(True)
        assert 'Berhasil memberikan ulasan dan rating' in validate_message
        assert_that(validate_data).is_not_none()
        assert_that(validate_data_merchant).is_not_none()
        assert validate_data_merchant == list_order.json().get('data')[0]['merchant_name']

