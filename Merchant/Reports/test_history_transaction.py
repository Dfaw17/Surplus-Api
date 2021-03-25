import requests
from env import stagging

class TestOrderHistoryTransaction :

    global setting_env,history_trx,url_login,email,kata_sandi,wrong_token

    setting_env = stagging
    history_trx = f"{setting_env}/api/v2/merchant/reports/transaction-history"
    url_login = f"{setting_env}/api/v2/merchant/auth/login"
    email = "vd1@gmail.com"
    kata_sandi = "12345678"
    wrong_token = "yJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvc3RhZ2luZy5hZG1pbnN1cnBsdXMubmV0XC9hcGlcL3YyXC9tZXJjaGFudFwvYXV0aFwvbG9naW4iLCJpYXQiOjE2MTUzOTIzMDQsImV4cCI6MTYxNzk4NDMwNCwibmJmIjoxNjE1MzkyMzA0LCJqdGkiOiJOVGJ1Qk4xODE2VU5Fd2VKIiwic3ViIjo0MDc3LCJwcnYiOiIyNzQxMDVkYTZlOTViZWYyODA3Nzg2ZGQ4NzM4ODY3Y2Y5YzAyYWFiIn0.QQqZAjqTaM6aUJ-uZU8E53iIRySWB_A9mQTIt_tUXsQ"

    def test_history_transaction_normal(self):
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

        response = requests.get(history_trx, headers=headers)
        data = response.json()

        validate_status = data.get('success')
        validate_message = data.get('message')
        validate_data = len(data.get('data')['orders'])
        validate_data2 = data.get('data')['total_order']
        print(response.json())
        assert validate_status == bool(True)
        assert 'Data riwayat transaksi berhasil ditemukan' in validate_message
        assert validate_data == validate_data2
        assert response.status_code == 200

    def test_history_transaction_wrong_token(self):
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

        response = requests.get(history_trx, headers=headers)
        data = response.json()

        validate_status = data.get('success')
        validate_message = data.get('message')
        print(response.json())
        assert validate_status == bool(False)
        assert 'Unauthorized' in validate_message
        assert response.status_code == 401

    def test_history_transaction_token_empty(self):
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

        response = requests.get(history_trx, headers=headers)
        data = response.json()

        validate_status = data.get('success')
        validate_message = data.get('message')
        print(response.json())
        assert validate_status == bool(False)
        assert 'Unauthorized' in validate_message
        assert response.status_code == 401
