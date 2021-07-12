import requests
from env import *
from pprint import pprint
from assertpy import assert_that
from faker.providers.geo import Provider
fake = Provider()


class TestCustomerOrdersGosendEstimate:

    global setting_env,url_login,url_gosend_estimate,dari,ke,email,kata_sandi,wrong_token

    setting_env = sandbox
    url_login = f"{setting_env}/api/v2/customer/auth/login/email"
    url_gosend_estimate = f"{setting_env}/api/v2/customer/gosend/estimate"
    dari = '-6.3772882,107.1062917'
    ke = '-6.3823027,107.1162164'
    email = "kopiruangvirtual@gmail.com"
    kata_sandi = '12345678'
    wrong_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvc3RhZ2luZy5hZG1pbnN1cnBsdXMubmV0XC9hcGlcL3YyXC9jdXN0b21lclwvYXV0aFwvbG9naW5cL2VtYWlsIiwiaWF0IjoxNjE2ODA1NzI2LCJleHAiOjE2MTkzOTc3MjYsIm5iZiI6MTYxNjgwNTcyNiwianRpIjoib05ESmxFRE5hSzNrN2RtVyIsInN1YiI6NDEyNiwicHJ2IjoiMjc0MTA1ZGE2ZTk1YmVmMjgwNzc4NmRkODczODg2N2NmOWMwMmFhYiJ9.fj51xIfQrqleRvdSJUbWcdrvsxQPUn8HpccnOmTgPDI'

    def test_gosend_estimate_normal(self):
        param = {
            'email': email,
            'password': kata_sandi
        }
        headers = {
            "Accept": "application/json"
        }
        login = requests.post(url_login, params=param, headers=headers)

        origin = fake.local_latlng(country_code='ID', coords_only=True)
        dest = fake.local_latlng(country_code='ID', coords_only=True)

        print(origin)
        print(dest)

        param2 = {
            "origin": "-6.181663,106.805884",
            "destination": "-6.188844,106.847186",
            "id_stocks[0]": "54",
        }
        headers2 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        gosend_estimate = requests.get(url_gosend_estimate, params=param2, headers=headers2)

        param3 = {
            "origin": "-6.181663,106.805884",
            "destination": "-6.188844,106.847186",
            "paymentType": "3",
        }

        headers3 = {
            "Client-ID": "surplus-indonesia-engine",
            "Pass-Key": "de513a339c192d46a079f6f822b9e144fd50cb683df2dd374604e1add228ab58"
        }
        url3 = "https://integration-kilat-api.gojekapi.com/gokilat/v10/calculate/price"
        gosend_estimate_real = requests.get(url3, params=param3, headers=headers3)

        validate_status = gosend_estimate.json().get('success')
        validate_message = gosend_estimate.json().get('message')
        validate_price = gosend_estimate.json().get('data')['instant']['price']
        validate_price_real = gosend_estimate_real.json().get('Instant')['price']['total_price']

        assert gosend_estimate.status_code == 200
        assert validate_status == bool(True)
        assert 'Gosend tersedia' in validate_message
        assert_that(validate_price).is_equal_to(validate_price_real + float(1000))

    def test_gosend_estimate_wrong_token(self):
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
            'origin': dari,
            'destination': ke,
            'id_stocks[0]': '54'
        }
        gosend_estimate = requests.get(url_gosend_estimate, params=param2, headers=headers2)

        validate_status = gosend_estimate.json().get('success')
        validate_message = gosend_estimate.json().get('message')

        assert gosend_estimate.status_code == 401
        assert validate_status == bool(False)
        assert "Unauthorized" in validate_message

    def test_gosend_estimate_empty_value(self):
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
            "Authorization": ''
        }
        param2 = {
            'origin': dari,
            'destination': ke,
            'id_stocks[0]': '54'
        }
        gosend_estimate = requests.get(url_gosend_estimate, params=param2, headers=headers2)

        validate_status = gosend_estimate.json().get('success')
        validate_message = gosend_estimate.json().get('message')

        assert gosend_estimate.status_code == 401
        assert validate_status == bool(False)
        assert "Unauthorized" in validate_message

    def test_gosend_estimate_without_param_origin(self):
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
            # 'origin': dari,
            'destination': ke,
            'id_stocks[0]': '54'
        }
        gosend_estimate = requests.get(url_gosend_estimate, params=param2, headers=headers2)

        validate_status = gosend_estimate.json().get('success')
        validate_message = gosend_estimate.json().get('message')['origin']

        assert gosend_estimate.status_code == 422
        assert validate_status == bool(False)
        assert "Titik lokasi asal tidak boleh kosong." in validate_message

    def test_gosend_estimate_origin_empty_value(self):
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
            'origin': '',
            'destination': ke,
            'id_stocks[0]': '54'
        }
        gosend_estimate = requests.get(url_gosend_estimate, params=param2, headers=headers2)

        validate_status = gosend_estimate.json().get('success')
        validate_message = gosend_estimate.json().get('message')['origin']

        assert gosend_estimate.status_code == 422
        assert validate_status == bool(False)
        assert "Titik lokasi asal tidak boleh kosong." in validate_message

    def test_gosend_estimate_origin_text_value(self):
        setting_env = stagging
        url_login = f"{setting_env}/api/v2/customer/auth/login/email"
        url_gosend_estimate = f"{setting_env}/api/v2/customer/gosend/estimate"
        dari = '-6.3772882,107.1062917'
        ke = '-6.3823027,107.1162164'
        email = "kopiruangvirtual@gmail.com"
        kata_sandi = '12345678'
        wrong_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvc3RhZ2luZy5hZG1pbnN1cnBsdXMubmV0XC9hcGlcL3YyXC9jdXN0b21lclwvYXV0aFwvbG9naW5cL2VtYWlsIiwiaWF0IjoxNjE2ODA1NzI2LCJleHAiOjE2MTkzOTc3MjYsIm5iZiI6MTYxNjgwNTcyNiwianRpIjoib05ESmxFRE5hSzNrN2RtVyIsInN1YiI6NDEyNiwicHJ2IjoiMjc0MTA1ZGE2ZTk1YmVmMjgwNzc4NmRkODczODg2N2NmOWMwMmFhYiJ9.fj51xIfQrqleRvdSJUbWcdrvsxQPUn8HpccnOmTgPDI'

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
            'origin': 'aaaa',
            'destination': ke,
            'id_stocks[0]': '54'
        }
        gosend_estimate = requests.get(url_gosend_estimate, params=param2, headers=headers2)

        validate_status = gosend_estimate.json().get('success')
        validate_message = gosend_estimate.json().get('message')['origin']

        assert gosend_estimate.status_code == 422
        assert validate_status == bool(False)
        assert "The Titik lokasi asal must be latitude and longitude." in validate_message

    def test_gosend_estimate_origin_wrong_format_value(self):
        setting_env = stagging
        url_login = f"{setting_env}/api/v2/customer/auth/login/email"
        url_gosend_estimate = f"{setting_env}/api/v2/customer/gosend/estimate"
        dari = '-6.3772882,107.1062917'
        ke = '-6.3823027,107.1162164'
        email = "kopiruangvirtual@gmail.com"
        kata_sandi = '12345678'
        wrong_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvc3RhZ2luZy5hZG1pbnN1cnBsdXMubmV0XC9hcGlcL3YyXC9jdXN0b21lclwvYXV0aFwvbG9naW5cL2VtYWlsIiwiaWF0IjoxNjE2ODA1NzI2LCJleHAiOjE2MTkzOTc3MjYsIm5iZiI6MTYxNjgwNTcyNiwianRpIjoib05ESmxFRE5hSzNrN2RtVyIsInN1YiI6NDEyNiwicHJ2IjoiMjc0MTA1ZGE2ZTk1YmVmMjgwNzc4NmRkODczODg2N2NmOWMwMmFhYiJ9.fj51xIfQrqleRvdSJUbWcdrvsxQPUn8HpccnOmTgPDI'

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
            'origin': '081386356616',
            'destination': ke,
            'id_stocks[0]': '54'
        }
        gosend_estimate = requests.get(url_gosend_estimate, params=param2, headers=headers2)

        validate_status = gosend_estimate.json().get('success')
        validate_message = gosend_estimate.json().get('message')['origin']

        assert gosend_estimate.status_code == 422
        assert validate_status == bool(False)
        assert "The Titik lokasi asal must be latitude and longitude." in validate_message

    def test_gosend_estimate_without_param_destination(self):
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
            'origin': dari,
            # 'destination': ke,
            'id_stocks[0]': '54'
        }
        gosend_estimate = requests.get(url_gosend_estimate, params=param2, headers=headers2)

        validate_status = gosend_estimate.json().get('success')
        validate_message = gosend_estimate.json().get('message')['destination']

        assert gosend_estimate.status_code == 422
        assert validate_status == bool(False)
        assert "Titik lokasi tujuan tidak boleh kosong." in validate_message

    def test_gosend_estimate_destination_empty_value(self):
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
            'origin': dari,
            'destination': '',
            'id_stocks[0]': '54'
        }
        gosend_estimate = requests.get(url_gosend_estimate, params=param2, headers=headers2)

        validate_status = gosend_estimate.json().get('success')
        validate_message = gosend_estimate.json().get('message')['destination']

        assert gosend_estimate.status_code == 422
        assert validate_status == bool(False)
        assert "Titik lokasi tujuan tidak boleh kosong." in validate_message

    def test_gosend_estimate_destination_text_value(self):
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
            'origin': dari,
            'destination': 'aaa',
            'id_stocks[0]': '54'
        }
        gosend_estimate = requests.get(url_gosend_estimate, params=param2, headers=headers2)

        validate_status = gosend_estimate.json().get('success')
        validate_message = gosend_estimate.json().get('message')['destination']

        assert gosend_estimate.status_code == 422
        assert validate_status == bool(False)
        assert "The Titik lokasi tujuan must be latitude and longitude." in validate_message

    def test_gosend_estimate_destination_wrong_format_value(self):
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
            'origin': dari,
            'destination': '081386356616',
            'id_stocks[0]': '54'
        }
        gosend_estimate = requests.get(url_gosend_estimate, params=param2, headers=headers2)

        validate_status = gosend_estimate.json().get('success')
        validate_message = gosend_estimate.json().get('message')['destination']

        assert gosend_estimate.status_code == 422
        assert validate_status == bool(False)
        assert "The Titik lokasi tujuan must be latitude and longitude." in validate_message

    def test_gosend_estimate_id_menu_empty_value(self):
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
            'origin': dari,
            'destination': ke,
            'id_stocks[0]': ''
        }
        gosend_estimate = requests.get(url_gosend_estimate, params=param2, headers=headers2)

        validate_status = gosend_estimate.json().get('success')
        validate_message = gosend_estimate.json().get('message')

        assert gosend_estimate.status_code == 400
        assert validate_status == bool(False)
        assert "Menu tidak tersedia" in validate_message

    def test_gosend_estimate_without_param_id_menu(self):
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
            'origin': dari,
            'destination': ke
            # 'id_stocks[0]': ''
        }
        gosend_estimate = requests.get(url_gosend_estimate, params=param2, headers=headers2)

        validate_status = gosend_estimate.json().get('success')
        validate_message = gosend_estimate.json().get('message')['id_stocks']

        assert gosend_estimate.status_code == 422
        assert validate_status == bool(False)
        assert "id stocks tidak boleh kosong." in validate_message

    def test_gosend_estimate_id_menu_wrong_value(self):
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
            'origin': dari,
            'destination': ke,
            'id_stocks[0]': '666666'
        }
        gosend_estimate = requests.get(url_gosend_estimate, params=param2, headers=headers2)

        validate_status = gosend_estimate.json().get('success')
        validate_message = gosend_estimate.json().get('message')

        assert gosend_estimate.status_code == 400
        assert validate_status == bool(False)
        assert "Menu tidak tersedia" in validate_message

    def test_gosend_estimate_id_menu_text_value(self):
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
            'origin': dari,
            'destination': ke,
            'id_stocks[0]': 'aaaaa'
        }
        gosend_estimate = requests.get(url_gosend_estimate, params=param2, headers=headers2)

        validate_status = gosend_estimate.json().get('success')
        validate_message = gosend_estimate.json().get('message')

        assert gosend_estimate.status_code == 400
        assert validate_status == bool(False)
        assert "Menu tidak tersedia" in validate_message
