import requests
from env import stagging

class TestDeleteMerchantMenu:

    global setting_env,delete_menu,url_login,url_get_all_merchant_menu,email,kata_sandi,wrong_token,insert_menu

    setting_env = stagging
    delete_menu = f"{setting_env}/api/v2/merchant/menus/"
    url_login = f"{setting_env}/api/v2/merchant/auth/login"
    url_get_all_merchant_menu = f"{setting_env}/api/v2/merchant/menus/"
    insert_menu = f"{setting_env}/api/v2/merchant/menus"
    email = "vd1@gmail.com"
    kata_sandi = "12345678"
    wrong_token = "yJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvc3RhZ2luZy5hZG1pbnN1cnBsdXMubmV0XC9hcGlcL3YyXC9tZXJjaGFudFwvYXV0aFwvbG9naW4iLCJpYXQiOjE2MTUzOTIzMDQsImV4cCI6MTYxNzk4NDMwNCwibmJmIjoxNjE1MzkyMzA0LCJqdGkiOiJOVGJ1Qk4xODE2VU5Fd2VKIiwic3ViIjo0MDc3LCJwcnYiOiIyNzQxMDVkYTZlOTViZWYyODA3Nzg2ZGQ4NzM4ODY3Y2Y5YzAyYWFiIn0.QQqZAjqTaM6aUJ-uZU8E53iIRySWB_A9mQTIt_tUXsQ"

    def test_delete_menu_normal(self):
        param = {
            "email": email,
            "password": kata_sandi
        }
        login = requests.post(url_login, data=param, headers={'Accept': 'application/json'})
        token = login.json().get("token")
        headers = {
            "Authorization": f"Bearer {token}"
        }

        nama_makanan = "Pisang Nugget"
        merchant_kategori = 60
        deskripsi = "Pisang Nugget Mix"
        harga_asli = 20000
        harga_jual = 10000
        status_halal = 0
        param2 = {
            "nama_menu_makanan": nama_makanan,
            "merchant_kategori_makanan_id": merchant_kategori,
            "deskripsi": deskripsi,
            "harga_asli": harga_asli,
            "harga_jual": harga_jual,
            "is_non_halal": status_halal
        }
        response = requests.post(insert_menu, data=param2, headers=headers,
                                 files={'image': open("pisangnug.jpg", 'rb')})

        response = requests.get(url_get_all_merchant_menu, headers=headers)
        data_id = str(response.json().get("data")[0]["id"])

        response2 = requests.delete(delete_menu + data_id, headers=headers)
        data = response2.json()
        validate_message = data.get("message")
        validate_status = data.get("success")

        assert response2.status_code == 201
        assert validate_status == bool(True)
        assert validate_message == "Data menu berhasil dihapus."

    def test_delete_menu_wrong_id(self):
        param = {
            "email": email,
            "password": kata_sandi
        }
        login = requests.post(url_login, data=param, headers={'Accept': 'application/json'})
        token = login.json().get("token")
        headers = {
            "Authorization": f"Bearer {token}"
        }

        response = requests.get(url_get_all_merchant_menu, headers=headers)
        data_id = str(response.json().get("data")[0]["id"])

        response2 = requests.delete(delete_menu+"666", headers=headers)
        data = response2.text
        # print(data)

        assert response2.status_code == 500
        assert "Server Error" in data

    def test_delete_menu_id_empty_value(self):
        param = {
            "email": email,
            "password": kata_sandi
        }
        login = requests.post(url_login, data=param, headers={'Accept': 'application/json'})
        token = login.json().get("token")
        headers = {
            "Authorization": f"Bearer {token}"
        }

        response = requests.get(url_get_all_merchant_menu, headers=headers)
        data_id = str(response.json().get("data")[0]["id"])

        response2 = requests.delete(delete_menu, headers=headers)
        data = response2.text

        assert response2.status_code == 405
        assert "Whoops, looks like something went wrong" in data

    def test_delete_menu_token_empty_value(self):
        param = {
            "email": email,
            "password": kata_sandi
        }
        login = requests.post(url_login, data=param, headers={'Accept': 'application/json'})
        token = login.json().get("token")
        headers = {
            "Authorization": f"Bearer {token}"
        }

        response = requests.get(url_get_all_merchant_menu, headers=headers)
        data_id = str(response.json().get("data")[0]["id"])
        headers2 = {
            "Authorization": ""
        }

        response2 = requests.delete(delete_menu + data_id, headers=headers2)
        data = response2.text

        assert response2.status_code == 401
        assert "Unauthorized" in data

    def test_delete_menu_wrong_token(self):
        param = {
            "email": email,
            "password": kata_sandi
        }
        login = requests.post(url_login, data=param, headers={'Accept': 'application/json'})
        token = login.json().get("token")
        headers = {
            "Authorization": f"Bearer {token}"
        }

        response = requests.get(url_get_all_merchant_menu, headers=headers)
        data_id = str(response.json().get("data")[0]["id"])
        headers2 = {
            "Authorization": wrong_token
        }

        response2 = requests.delete(delete_menu + data_id, headers=headers2)
        data = response2.text

        assert response2.status_code == 401
        assert "Unauthorized" in data

