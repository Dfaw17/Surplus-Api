import requests
from env import *
from assertpy import *


class TestOrderHistoryIncome:
    global setting_env, url_history_income, url_login, email, kata_sandi, wrong_token

    setting_env = testing
    url_history_income = f"{setting_env}/api/v2/merchant/reports/income-history"
    url_login = f"{setting_env}/api/v2/merchant/auth/login"
    email = "sdet@gmail.com"
    kata_sandi = "12345678"
    wrong_token = "kyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvc3RhZ2luZy5hZG1pbnN1cnBsdXMubmV0XC9hcGlcL3YyXC9tZXJjaGFudFwvYXV0aFwvbG9naW4iLCJpYXQiOjE2MTU3MDExNDIsImV4cCI6MTYxODI5MzE0MiwibmJmIjoxNjE1NzAxMTQyLCJqdGkiOiJjOFluT3BlMzRqRVVIemZSIiwic3ViIjo0MDc3LCJwcnYiOiIyNzQxMDVkYTZlOTViZWYyODA3Nzg2ZGQ4NzM4ODY3Y2Y5YzAyYWFiIn0.xxI5o6tgIvb3Eds4CCfSnXM3ThFYiQwYcTCxKmrZozI"

    def test_history_income_normal(self):
        param = {
            "email": email,
            "password": kata_sandi
        }
        login = requests.post(url_login, data=param, headers={'Accept': 'application/json'})
        token = login.json().get("token")
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json"
        }
        param = {
            "start_date": "2020-04-01",
            "end_date": "2022-04-01"
        }
        response = requests.get(url_history_income, params=param, headers=headers)
        data = response.json()

        validate_status = data.get("success")
        validate_message = data.get("message")
        validate_data = data.get("data")
        validate_data_omset = data.get("data")['omset']
        validate_data_total_transaksi = data.get("data")['total_transaksi']

        assert response.status_code == 200
        assert validate_status == bool(True)
        assert "Data riwayat pemasukan berhasil ditemukan" in validate_message
        assert_that(validate_data).contains_only('omset', 'total_transaksi', 'date_range')
        assert_that(validate_data_omset).is_type_of(int)
        assert_that(validate_data_total_transaksi).is_type_of(int)

    def test_history_income_wrong_token(self):
        param = {
            "email": email,
            "password": kata_sandi
        }
        login = requests.post(url_login, data=param, headers={'Accept': 'application/json'})
        token = login.json().get("token")
        headers = {
            "Authorization": wrong_token,
            "Accept": "application/json"
        }
        param = {
            "start_date": "2020-04-01",
            "end_date": "2022-04-01"
        }
        response = requests.get(url_history_income, params=param, headers=headers)
        data = response.json()

        validate_status = data.get('success')
        validate_message = data.get('message')

        assert response.status_code == 401
        assert validate_status == bool(False)
        assert 'Unauthorized' in validate_message

    def test_history_income_token_empty_value(self):
        param = {
            "email": email,
            "password": kata_sandi
        }
        login = requests.post(url_login, data=param, headers={'Accept': 'application/json'})
        token = login.json().get("token")
        headers = {
            "Authorization": '',
            "Accept": "application/json"
        }
        param = {
            "start_date": "2020-04-01",
            "end_date": "2022-04-01"
        }
        response = requests.get(url_history_income, params=param, headers=headers)
        data = response.json()

        validate_status = data.get('success')
        validate_message = data.get('message')

        assert response.status_code == 401
        assert validate_status == bool(False)
        assert 'Unauthorized' in validate_message

    def test_history_income_start_date_empty_value(self):
        param = {
            "email": email,
            "password": kata_sandi
        }
        login = requests.post(url_login, data=param, headers={'Accept': 'application/json'})
        token = login.json().get("token")
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json"
        }
        param = {
            "start_date": "",
            "end_date": "2022-04-01"
        }
        response = requests.get(url_history_income, params=param, headers=headers)
        data = response.json()

        validate_status = data.get('success')
        validate_message = data.get('message')['start_date']

        assert response.status_code == 422
        assert validate_status == bool(False)
        assert 'Tanggal awal tidak boleh kosong.' in validate_message

    def test_history_income_without_param_start_sate(self):
        param = {
            "email": email,
            "password": kata_sandi
        }
        login = requests.post(url_login, data=param, headers={'Accept': 'application/json'})
        token = login.json().get("token")
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json"
        }
        param = {
            # "start_date": "2020-04-01",
            "end_date": "2022-04-01"
        }
        response = requests.get(url_history_income, params=param, headers=headers)
        data = response.json()

        validate_status = data.get('success')
        validate_message = data.get('message')['start_date']

        assert response.status_code == 422
        assert validate_status == bool(False)
        assert 'Tanggal awal tidak boleh kosong.' in validate_message

    def test_history_income_start_date_text_value(self):
        param = {
            "email": email,
            "password": kata_sandi
        }
        login = requests.post(url_login, data=param, headers={'Accept': 'application/json'})
        token = login.json().get("token")
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json"
        }
        param = {
            "start_date": "aaa",
            "end_date": "2022-04-01"
        }
        response = requests.get(url_history_income, params=param, headers=headers)
        data = response.json()

        validate_status = data.get('success')
        validate_message = data.get('message')['start_date']

        assert response.status_code == 422
        assert validate_status == bool(False)
        assert 'Tanggal awal tidak cocok dengan format Y-m-d.' in validate_message

    def test_history_income_start_date_Wrong_format_value(self):
        param = {

            "email": email,
            "password": kata_sandi
        }
        login = requests.post(url_login, data=param, headers={'Accept': 'application/json'})
        token = login.json().get("token")
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json"
        }
        param = {
            'start_date': '2021/01/01',
            'end_date': '2021-03-25'
        }

        response = requests.get(url_history_income, params=param, headers=headers)
        data = response.json()

        validate_status = data.get('success')
        validate_message = data.get('message')['start_date']

        assert response.status_code == 422
        assert validate_status == bool(False)
        assert 'Tanggal awal tidak cocok dengan format Y-m-d.' in validate_message

    def test_history_income_end_date_empty_value(self):
        param = {

            "email": email,
            "password": kata_sandi
        }
        login = requests.post(url_login, data=param, headers={'Accept': 'application/json'})
        token = login.json().get("token")
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json"
        }
        param = {
            'start_date': '2020-01-01',
            'end_date': ''
        }

        response = requests.get(url_history_income, params=param, headers=headers)
        data = response.json()

        validate_status = data.get('success')
        validate_message = data.get('message')['end_date']

        assert response.status_code == 422
        assert validate_status == bool(False)
        assert 'Tanggal akhir tidak boleh kosong.' in validate_message

    def test_history_income_without_param_end_date(self):
        param = {

            "email": email,
            "password": kata_sandi
        }
        login = requests.post(url_login, data=param, headers={'Accept': 'application/json'})
        token = login.json().get("token")
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json"
        }
        param = {
            'start_date': '2020-01-01'
        }

        response = requests.get(url_history_income, params=param, headers=headers)
        data = response.json()

        validate_status = data.get('success')
        validate_message = data.get('message')['end_date']

        assert response.status_code == 422
        assert validate_status == bool(False)
        assert 'Tanggal akhir tidak boleh kosong.' in validate_message

    def test_history_income_end_date_text_value(self):
        param = {

            "email": email,
            "password": kata_sandi
        }
        login = requests.post(url_login, data=param, headers={'Accept': 'application/json'})
        token = login.json().get("token")
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json"
        }
        param = {
            'start_date': '2020-01-01',
            'end_date': 'a'
        }

        response = requests.get(url_history_income, params=param, headers=headers)
        data = response.json()

        validate_status = data.get('success')
        validate_message = data.get('message')['end_date']

        assert response.status_code == 422
        assert validate_status == bool(False)
        assert 'Tanggal akhir tidak cocok dengan format Y-m-d.' in validate_message

    def test_history_income_end_date_wrong_format_value(self):
        param = {

            "email": email,
            "password": kata_sandi
        }
        login = requests.post(url_login, data=param, headers={'Accept': 'application/json'})
        token = login.json().get("token")
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json"
        }
        param = {
            'start_date': '2020-01-01',
            'end_date': '2021/01/01'
        }

        response = requests.get(url_history_income, params=param, headers=headers)
        data = response.json()

        print(data)

        validate_status = data.get('success')
        validate_message = data.get('message')['end_date']

        assert response.status_code == 422
        assert validate_status == bool(False)
        assert 'Tanggal akhir tidak cocok dengan format Y-m-d.' in validate_message
