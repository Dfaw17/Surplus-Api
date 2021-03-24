import requests
from env import stagging

class TestSetActiveMenu :

    global setting_env,set_active_menu,url_login,url_get_all_merchant_menu,email,kata_sandi,wrong_token

    setting_env = stagging
    set_active_menu = f"{setting_env}/api/v2/merchant/menus/"
    url_login = f"{setting_env}/api/v2/merchant/auth/login"
    url_get_all_merchant_menu = f"{setting_env}/api/v2/merchant/menus/"
    email = "vd1@gmail.com"
    kata_sandi = "12345678"
    wrong_token = "yJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvc3RhZ2luZy5hZG1pbnN1cnBsdXMubmV0XC9hcGlcL3YyXC9tZXJjaGFudFwvYXV0aFwvbG9naW4iLCJpYXQiOjE2MTUzOTIzMDQsImV4cCI6MTYxNzk4NDMwNCwibmJmIjoxNjE1MzkyMzA0LCJqdGkiOiJOVGJ1Qk4xODE2VU5Fd2VKIiwic3ViIjo0MDc3LCJwcnYiOiIyNzQxMDVkYTZlOTViZWYyODA3Nzg2ZGQ4NzM4ODY3Y2Y5YzAyYWFiIn0.QQqZAjqTaM6aUJ-uZU8E53iIRySWB_A9mQTIt_tUXsQ"

    def test_set_active_menu_normal(self):
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

        response = requests.get(url_get_all_merchant_menu, headers=headers)
        data_id = str(response.json().get("data")[0]["id"])

        param2 = {
            "is_tomorrow": "0",
            "stock": "100",
            "waktu_mulai_penjemputan": "01:00",
            "waktu_akhir_penjemputan": "23:00"
        }

        response2 = requests.patch(set_active_menu + data_id + "/active", data=param2, headers=headers)
        data = response2.json()
        validate_status = data.get('success')
        validate_message = data.get('message')
        validate_menu = str(data.get('data')['id'])
        validate_status_menu = data.get('data')['is_tomorrow']
        validate_menu_stock = data.get('data')['stock']
        validate_menu_start = data.get('data')['waktu_mulai_penjemputan']
        validate_menu_end = data.get('data')['waktu_akhir_penjemputan']

        assert response2.status_code == 200
        assert validate_status == bool(True)
        assert "berhasil diaktifkan" in validate_message
        assert validate_menu == data_id
        assert validate_status_menu == "0"
        assert validate_menu_stock == "100"
        assert validate_menu_start == "01:00"
        assert validate_menu_end == "23:00"

    def test_set_active_menu_wrong_id(self):
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

        response = requests.get(url_get_all_merchant_menu, headers=headers)
        data_id = str(response.json().get("data")[0]["id"])

        param2 = {
            "is_tomorrow": "0",
            "stock": "100",
            "waktu_mulai_penjemputan": "01:00",
            "waktu_akhir_penjemputan": "23:00"
        }

        response2 = requests.patch(set_active_menu + "666" + "/active", data=param2, headers=headers)
        data = response2.json()

        print(data)
        validate_status = data.get('success')
        validate_message = data.get('message')

        assert response2.status_code == 404
        assert validate_status == bool(False)
        assert "Data tidak ditemukan" in validate_message

    def test_set_active_menu_empty_id(self):
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

        response = requests.get(url_get_all_merchant_menu, headers=headers)
        data_id = str(response.json().get("data")[0]["id"])

        param2 = {
            "is_tomorrow": "0",
            "stock": "100",
            "waktu_mulai_penjemputan": "01:00",
            "waktu_akhir_penjemputan": "23:00"
        }

        response2 = requests.patch(set_active_menu + "/active", data=param2, headers=headers)
        data = response2.json()

        print(data)
        validate_status = data.get('success')

        assert response2.status_code == 404
        assert validate_status == bool(False)

    def test_set_active_menu_wrong_token(self):
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

        response = requests.get(url_get_all_merchant_menu, headers=headers)
        data_id = str(response.json().get("data")[0]["id"])

        param2 = {
            "is_tomorrow": "0",
            "stock": "100",
            "waktu_mulai_penjemputan": "01:00",
            "waktu_akhir_penjemputan": "23:00"
        }

        headers2 = {
            "Authorization": wrong_token,
            "Accept": "application/json"
        }

        response2 = requests.patch(set_active_menu + data_id + "/active", data=param2, headers=headers2)
        data = response2.json()

        print(data)
        validate_status = data.get('success')
        validate_message = data.get('message')

        assert response2.status_code == 401
        assert validate_status == bool(False)
        assert 'Unauthorized' in validate_message

    def test_set_active_menu_empty_token(self):
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

        response = requests.get(url_get_all_merchant_menu, headers=headers)
        data_id = str(response.json().get("data")[0]["id"])

        param2 = {
            "is_tomorrow": "0",
            "stock": "100",
            "waktu_mulai_penjemputan": "01:00",
            "waktu_akhir_penjemputan": "23:00"
        }

        headers2 = {
            "Authorization": "",
            "Accept": "application/json"
        }

        response2 = requests.patch(set_active_menu + data_id + "/active", data=param2, headers=headers2)
        data = response2.json()

        print(data)
        validate_status = data.get('success')
        validate_message = data.get('message')

        assert response2.status_code == 401
        assert validate_status == bool(False)
        assert 'Unauthorized' in validate_message

    def test_set_active_menu_is_tomorrow_set_not_bool(self):
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

        response = requests.get(url_get_all_merchant_menu, headers=headers)
        data_id = str(response.json().get("data")[0]["id"])

        param2 = {
            "is_tomorrow": "5",
            "stock": "100",
            "waktu_mulai_penjemputan": "01:00",
            "waktu_akhir_penjemputan": "23:00"
        }

        headers2 = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json"
        }

        response2 = requests.patch(set_active_menu + data_id + "/active", data=param2, headers=headers2)
        data = response2.json()

        print(data)
        validate_status = data.get('success')
        validate_message = data.get('message')['is_tomorrow']

        assert response2.status_code == 422
        assert validate_status == bool(False)
        assert 'Pre-order harus bernilai true atau false.' in validate_message

    def test_set_active_menu_is_tomorrow_empty_value(self):
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

        response = requests.get(url_get_all_merchant_menu, headers=headers)
        data_id = str(response.json().get("data")[0]["id"])

        param2 = {
            "is_tomorrow": "",
            "stock": "100",
            "waktu_mulai_penjemputan": "01:00",
            "waktu_akhir_penjemputan": "23:00"
        }

        headers2 = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json"
        }

        response2 = requests.patch(set_active_menu + data_id + "/active", data=param2, headers=headers2)
        data = response2.json()

        print(data)
        validate_status = data.get('success')
        validate_message = data.get('message')['is_tomorrow']

        assert response2.status_code == 422
        assert validate_status == bool(False)
        assert 'Pre-order tidak boleh kosong.' in validate_message

    def test_set_active_menu_stock_value_text(self):
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

        response = requests.get(url_get_all_merchant_menu, headers=headers)
        data_id = str(response.json().get("data")[0]["id"])

        param2 = {
            "is_tomorrow": "0",
            "stock": "aaa",
            "waktu_mulai_penjemputan": "01:00",
            "waktu_akhir_penjemputan": "23:00"
        }

        headers2 = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json"
        }

        response2 = requests.patch(set_active_menu + data_id + "/active", data=param2, headers=headers2)
        data = response2.json()

        print(data)
        validate_status = data.get('success')
        validate_message = data.get('message')['stock']

        assert response2.status_code == 422
        assert validate_status == bool(False)
        assert "stock harus berupa angka." in validate_message

    def test_set_active_menu_empty_stock_value(self):
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

        response = requests.get(url_get_all_merchant_menu, headers=headers)
        data_id = str(response.json().get("data")[0]["id"])

        param2 = {
            "is_tomorrow": "0",
            "stock": "",
            "waktu_mulai_penjemputan": "01:00",
            "waktu_akhir_penjemputan": "23:00"
        }

        headers2 = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json"
        }

        response2 = requests.patch(set_active_menu + data_id + "/active", data=param2, headers=headers2)
        data = response2.json()

        print(data)
        validate_status = data.get('success')
        validate_message = data.get('message')['stock']

        assert response2.status_code == 422
        assert validate_status == bool(False)
        assert "stock tidak boleh kosong." in validate_message

    def Set_active_menu_waktu_mulai_penjemputan_empty_value(self):
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

        response = requests.get(url_get_all_merchant_menu, headers=headers)
        data_id = str(response.json().get("data")[0]["id"])

        param2 = {
            "is_tomorrow": "0",
            "stock": "100",
            "waktu_mulai_penjemputan": "",
            "waktu_akhir_penjemputan": "23:00"
        }

        headers2 = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json"
        }

        response2 = requests.patch(set_active_menu + data_id + "/active", data=param2, headers=headers2)
        data = response2.json()

        print(data)
        validate_status = data.get('success')
        validate_message = data.get('message')['waktu_mulai_penjemputan']

        assert response2.status_code == 422
        assert validate_status == bool(False)
        assert "Waktu mulai penjemputan tidak boleh kosong." in validate_message

    def test_set_active_menu_waktu_mulai_penjemputan_text_value(self):
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

        response = requests.get(url_get_all_merchant_menu, headers=headers)
        data_id = str(response.json().get("data")[0]["id"])

        param2 = {
            "is_tomorrow": "0",
            "stock": "100",
            "waktu_mulai_penjemputan": "aa",
            "waktu_akhir_penjemputan": "23:00"
        }

        headers2 = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json"
        }

        response2 = requests.patch(set_active_menu + data_id + "/active", data=param2, headers=headers2)
        data = response2.json()

        print(data)
        validate_status = data.get('success')
        validate_message = data.get('message')['waktu_mulai_penjemputan']

        assert response2.status_code == 422
        assert validate_status == bool(False)
        assert "Waktu mulai penjemputan tidak cocok dengan format H:i." in validate_message

    def test_set_active_menu_waktu_mulai_penjemputan_lebih_kecil_waktu_akhir_penjemputan(self):
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

        response = requests.get(url_get_all_merchant_menu, headers=headers)
        data_id = str(response.json().get("data")[0]["id"])

        param2 = {
            "is_tomorrow": "0",
            "stock": "100",
            "waktu_mulai_penjemputan": "19:00",
            "waktu_akhir_penjemputan": "15:00"
        }

        headers2 = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json"
        }

        response2 = requests.patch(set_active_menu + data_id + "/active", data=param2, headers=headers2)
        data = response2.json()

        print(data)
        validate_status = data.get('success')
        validate_message = data.get('message')['waktu_akhir_penjemputan']

        assert response2.status_code == 422
        assert validate_status == bool(False)
        assert "Batas waktu penjemputan tidak benar" in validate_message

    def test_set_active_waktu_akhir_penjemputan_empty(self):
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

        response = requests.get(url_get_all_merchant_menu, headers=headers)
        data_id = str(response.json().get("data")[0]["id"])

        param2 = {
            "is_tomorrow": "0",
            "stock": "100",
            "waktu_mulai_penjemputan": "07:00",
            "waktu_akhir_penjemputan": ""
        }

        headers2 = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json"
        }

        response2 = requests.patch(set_active_menu + data_id + "/active", data=param2, headers=headers2)
        data = response2.json()

        print(data)
        validate_status = data.get('success')
        validate_message = data.get('message')['waktu_akhir_penjemputan']

        assert response2.status_code == 422
        assert validate_status == bool(False)
        assert "Waktu akhir penjemputan tidak boleh kosong." in validate_message

    def test_set_active_waktu_akhir_penjemputan_text_value(self):
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

        response = requests.get(url_get_all_merchant_menu, headers=headers)
        data_id = str(response.json().get("data")[0]["id"])

        param2 = {
            "is_tomorrow": "0",
            "stock": "100",
            "waktu_mulai_penjemputan": "07:00",
            "waktu_akhir_penjemputan": "aaa"
        }

        headers2 = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json"
        }

        response2 = requests.patch(set_active_menu + data_id + "/active", data=param2, headers=headers2)
        data = response2.json()

        print(data)
        validate_status = data.get('success')
        validate_message = data.get('message')['waktu_akhir_penjemputan']

        assert response2.status_code == 422
        assert validate_status == bool(False)
        assert "Waktu akhir penjemputan tidak cocok dengan format H:i." in validate_message
