import requests
from env import stagging

class TestOrderIndex :

    global setting_env,order_index,url_login,email,kata_sandi,wrong_token

    setting_env = stagging
    order_index = f"{setting_env}/api/v2/merchant/orders"
    url_login = f"{setting_env}/api/v2/merchant/auth/login"
    email = "vd1@gmail.com"
    kata_sandi = "12345678"
    wrong_token = "yJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvc3RhZ2luZy5hZG1pbnN1cnBsdXMubmV0XC9hcGlcL3YyXC9tZXJjaGFudFwvYXV0aFwvbG9naW4iLCJpYXQiOjE2MTUzOTIzMDQsImV4cCI6MTYxNzk4NDMwNCwibmJmIjoxNjE1MzkyMzA0LCJqdGkiOiJOVGJ1Qk4xODE2VU5Fd2VKIiwic3ViIjo0MDc3LCJwcnYiOiIyNzQxMDVkYTZlOTViZWYyODA3Nzg2ZGQ4NzM4ODY3Y2Y5YzAyYWFiIn0.QQqZAjqTaM6aUJ-uZU8E53iIRySWB_A9mQTIt_tUXsQ"

    def test_order_index_normal(self):
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
        param2 = {

            "type": "finish"
        }

        response = requests.get(order_index, params=param2, headers=headers)
        data = response.json()

        validate_status = data.get('success')
        validate_message = data.get('message')
        validate_data = len(data.get('data'))
        print(validate_data)
        assert validate_status == bool(True)
        assert "Data pesanan ditemukan." in validate_message
        assert validate_data > 1

    def test_order_index_token_empty_value(self):
        param = {

            "email": email,
            "password": kata_sandi
        }
        login = requests.post(url_login, data=param, headers={'Accept': 'application/json'})
        token = login.json().get("token")
        headers = {
            "Authorization": "",
            "Accept": "application/json"
        }
        param2 = {

            "type": "finish"
        }

        response = requests.get(order_index, params=param2, headers=headers)
        data = response.json()

        validate_status = data.get('success')
        validate_message = data.get('message')

        assert response.status_code == 401
        assert validate_status == bool(False)
        assert "Unauthorized" in validate_message

    def test_order_index_token_wrong_value(self):
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
        param2 = {

            "type": "finish"
        }

        response = requests.get(order_index, params=param2, headers=headers)
        data = response.json()

        validate_status = data.get('success')
        validate_message = data.get('message')

        assert response.status_code == 401
        assert validate_status == bool(False)
        assert "Unauthorized" in validate_message

    def test_order_index_type_number_value(self):
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
        param2 = {

            "type": "1"
        }

        response = requests.get(order_index, params=param2, headers=headers)
        data = response.json()

        validate_status = data.get('success')
        validate_message = data.get('message')['type']
        print(data)
        assert response.status_code == 422
        assert validate_status == bool(False)
        assert "type yang dipilih tidak tersedia." in validate_message

    def test_order_index_type_empty_value(self):
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
        param2 = {

            "type": ""
        }

        response = requests.get(order_index, params=param2, headers=headers)
        data = response.json()

        validate_status = data.get('success')
        validate_message = data.get('message')['type']
        print(data)
        assert response.status_code == 422
        assert validate_status == bool(False)
        assert "type tidak boleh kosong." in validate_message

    def test_order_index_type_wrong_value(self):
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
        param2 = {

            "type": "new"
        }

        response = requests.get(order_index, params=param2, headers=headers)
        data = response.json()

        validate_status = data.get('success')
        validate_message = data.get('message')['type']
        print(data)
        assert response.status_code == 422
        assert validate_status == bool(False)
        assert "type yang dipilih tidak tersedia." in validate_message

