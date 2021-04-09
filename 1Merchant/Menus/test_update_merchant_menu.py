import requests
from env import stagging

class TestUpdateMerchantMenu :

    global setting_env, update_menu, url_login, email, kata_sandi, wrong_token, url_get_all_merchant_menu

    setting_env = stagging
    update_menu = f"{setting_env}/api/v2/merchant/menus/"
    url_get_all_merchant_menu = f"{setting_env}/api/v2/merchant/menus/"
    url_login = f"{setting_env}/api/v2/merchant/auth/login"
    email = "vd1@gmail.com"
    kata_sandi = "12345678"
    wrong_token = "kyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvc3RhZ2luZy5hZG1pbnN1cnBsdXMubmV0XC9hcGlcL3YyXC9tZXJjaGFudFwvYXV0aFwvbG9naW4iLCJpYXQiOjE2MTU3MDExNDIsImV4cCI6MTYxODI5MzE0MiwibmJmIjoxNjE1NzAxMTQyLCJqdGkiOiJjOFluT3BlMzRqRVVIemZSIiwic3ViIjo0MDc3LCJwcnYiOiIyNzQxMDVkYTZlOTViZWYyODA3Nzg2ZGQ4NzM4ODY3Y2Y5YzAyYWFiIn0.xxI5o6tgIvb3Eds4CCfSnXM3ThFYiQwYcTCxKmrZozI"

    def test_update_menu_normal(self):
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

        nama_makanan = "Pisang Nugget"
        merchant_kategori = 60
        deskripsi = "Pisang Nugget Mix"
        harga_asli = 20000
        harga_jual = 10000
        status_halal = 0
        param2 = {
            "nama_menu_makanan": nama_makanan,
            "deskripsi": deskripsi,
            "merchant_kategori_makanan_id": merchant_kategori,
            "harga_asli": harga_asli,
            "harga_jual": harga_jual,
            "is_non_halal": status_halal
        }
        response = requests.post(update_menu + data_id + "?_method=PUT", data=param2, headers=headers,
                                 files={'image': open("pisangnug.jpg", 'rb')})
        response = response.json()

        validate_status = response.get("success")
        validate_message = response.get("message")
        validate_id = str(response.get("data")["id"])
        validate_nama_menu_makanan = str(response.get("data")["nama_menu_makanan"])
        validate_merchant_kategori_makanan_id = response.get("data")["merchant_kategori_makanan_id"]
        validate_deskripsi = response.get("data")["deskripsi"]
        validate_harga_asli = response.get("data")["harga_asli"]
        validate_harga_jual = response.get("data")["harga_jual"]
        validate_is_non_halal = response.get("data")["is_non_halal"]

        assert validate_status == bool(True)
        assert nama_makanan in validate_message
        assert data_id == validate_id
        assert validate_nama_menu_makanan == nama_makanan
        assert validate_merchant_kategori_makanan_id == merchant_kategori
        assert validate_deskripsi == deskripsi
        assert validate_harga_asli == harga_asli
        assert validate_harga_jual == harga_jual
        assert validate_is_non_halal == status_halal

    def test_update_menu_wrong_token(self):
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

        headers = {
            "Authorization": wrong_token
        }
        nama_makanan = "Pisang Nugget"
        merchant_kategori = 60
        deskripsi = "Pisang Nugget Mix"
        harga_asli = 20000
        harga_jual = 10000
        status_halal = 0
        param2 = {
            "nama_menu_makanan": nama_makanan,
            "deskripsi": deskripsi,
            "merchant_kategori_makanan_id": merchant_kategori,
            "harga_asli": harga_asli,
            "harga_jual": harga_jual,
            "is_non_halal": status_halal
        }
        response2 = requests.post(update_menu + data_id + "?_method=PUT", data=param2, headers=headers,
                                  files={'image': open("pisangnug.jpg", 'rb')})
        data = response2.text

        assert response2.status_code == 401
        assert "Unauthorized" in data

    def test_update_menu_token_empty(self):
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

        headers = {
            "Authorization": ""
        }
        nama_makanan = "Pisang Nugget"
        merchant_kategori = 60
        deskripsi = "Pisang Nugget Mix"
        harga_asli = 20000
        harga_jual = 10000
        status_halal = 0
        param2 = {
            "nama_menu_makanan": nama_makanan,
            "deskripsi": deskripsi,
            "merchant_kategori_makanan_id": merchant_kategori,
            "harga_asli": harga_asli,
            "harga_jual": harga_jual,
            "is_non_halal": status_halal
        }
        response2 = requests.post(update_menu + data_id + "?_method=PUT", data=param2, headers=headers,
                                  files={'image': open("pisangnug.jpg", 'rb')})
        data = response2.text

        assert response2.status_code == 401
        assert "Unauthorized" in data

    def test_update_menu_token_empty(self):
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

        headers = {

        }
        nama_makanan = "Pisang Nugget"
        merchant_kategori = 60
        deskripsi = "Pisang Nugget Mix"
        harga_asli = 20000
        harga_jual = 10000
        status_halal = 0
        param2 = {
            "nama_menu_makanan": nama_makanan,
            "deskripsi": deskripsi,
            "merchant_kategori_makanan_id": merchant_kategori,
            "harga_asli": harga_asli,
            "harga_jual": harga_jual,
            "is_non_halal": status_halal
        }
        response2 = requests.post(update_menu + data_id + "?_method=PUT", data=param2, headers=headers,
                                  files={'image': open("pisangnug.jpg", 'rb')})
        data = response2.text

        assert response2.status_code == 401
        assert "Unauthorized" in data

    def test_update_menu_nama_menu_empty_value(self):
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
            "nama_menu_makanan": "",
            "deskripsi": deskripsi,
            "merchant_kategori_makanan_id": merchant_kategori,
            "harga_asli": harga_asli,
            "harga_jual": harga_jual,
            "is_non_halal": status_halal
        }
        response2 = requests.post(update_menu + data_id + "?_method=PUT", data=param2, headers=headers,
                                  files={'image': open("pisangnug.jpg", 'rb')})
        data = response2.text

        assert response2.status_code == 422
        assert "Whoops, looks like something went wrong." in data

    def test_update_menu_without_param_nama_menu(self):
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

            "deskripsi": deskripsi,
            "merchant_kategori_makanan_id": merchant_kategori,
            "harga_asli": harga_asli,
            "harga_jual": harga_jual,
            "is_non_halal": status_halal
        }
        response2 = requests.post(update_menu + data_id + "?_method=PUT", data=param2, headers=headers,
                                  files={'image': open("pisangnug.jpg", 'rb')})
        data = response2.text

        assert response2.status_code == 422
        assert "Whoops, looks like something went wrong." in data

    def test_update_menu_merchant_kategoriid_empty_value(self):
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
            "deskripsi": deskripsi,
            "merchant_kategori_makanan_id": "",
            "harga_asli": harga_asli,
            "harga_jual": harga_jual,
            "is_non_halal": status_halal
        }
        response2 = requests.post(update_menu + data_id + "?_method=PUT", data=param2, headers=headers,
                                  files={'image': open("pisangnug.jpg", 'rb')})
        data = response2.text

        assert response2.status_code == 422
        assert "Whoops, looks like something went wrong." in data

    def test_update_menu_without_param_merchant_kategoriid(self):
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
            "deskripsi": deskripsi,
            "harga_asli": harga_asli,
            "harga_jual": harga_jual,
            "is_non_halal": status_halal
        }
        response2 = requests.post(update_menu + data_id + "?_method=PUT", data=param2, headers=headers,
                                  files={'image': open("pisangnug.jpg", 'rb')})
        data = response2.text

        assert response2.status_code == 422
        assert "Whoops, looks like something went wrong." in data

    def test_update_menu_merchant_kategoriid_text_value(self):
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
            "deskripsi": deskripsi,
            "merchant_kategori_makanan_id": "aaa",
            "harga_asli": harga_asli,
            "harga_jual": harga_jual,
            "is_non_halal": status_halal
        }
        response2 = requests.post(update_menu + data_id + "?_method=PUT", data=param2, headers=headers,
                                  files={'image': open("pisangnug.jpg", 'rb')})
        data = response2.text

        assert response2.status_code == 422
        assert "Whoops, looks like something went wrong." in data

    def test_update_menu_merchant_kategoriid_not_found(self):
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

        headers = {
            "Authorization": f"Bearer {token}"
        }
        nama_makanan = "Pisang Nugget"
        merchant_kategori = 600
        deskripsi = "Pisang Nugget Mix"
        harga_asli = 20000
        harga_jual = 10000
        status_halal = 0
        param2 = {
            "nama_menu_makanan": nama_makanan,
            "deskripsi": deskripsi,
            "merchant_kategori_makanan_id": merchant_kategori,
            "harga_asli": harga_asli,
            "harga_jual": harga_jual,
            "is_non_halal": status_halal
        }
        response2 = requests.post(update_menu + data_id + "?_method=PUT", data=param2, headers=headers,
                                  files={'image': open("pisangnug.jpg", 'rb')})
        data = response2.text

        assert response2.status_code == 404
        assert "Not Found" in data

    def test_update_menu_without_param_deskripsi(self):
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
            "harga_asli": harga_asli,
            "harga_jual": harga_jual,
            "is_non_halal": status_halal
        }
        response2 = requests.post(update_menu + data_id + "?_method=PUT", data=param2, headers=headers,
                                  files={'image': open("pisangnug.jpg", 'rb')})
        data = response2.text

        assert response2.status_code == 422
        assert "Whoops, looks like something went wrong" in data

    def test_update_menu_deskripsi_empty_value(self):
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
            "deskripsi": "",
            "merchant_kategori_makanan_id": merchant_kategori,
            "harga_asli": harga_asli,
            "harga_jual": harga_jual,
            "is_non_halal": status_halal
        }
        response2 = requests.post(update_menu + data_id + "?_method=PUT", data=param2, headers=headers,
                                  files={'image': open("pisangnug.jpg", 'rb')})
        data = response2.text

        assert response2.status_code == 422
        assert "Whoops, looks like something went wrong" in data

    def test_update_menu_harga_asli_text_value(self):
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
            "deskripsi": deskripsi,
            "merchant_kategori_makanan_id": merchant_kategori,
            "harga_asli": "harga_asli",
            "harga_jual": harga_jual,
            "is_non_halal": status_halal
        }
        response2 = requests.post(update_menu + data_id + "?_method=PUT", data=param2, headers=headers,
                                  files={'image': open("pisangnug.jpg", 'rb')})
        data = response2.text

        assert response2.status_code == 422
        assert "Whoops, looks like something went wrong" in data

    def test_update_menu_harga_asli_empty_value(self):
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
            "deskripsi": deskripsi,
            "merchant_kategori_makanan_id": merchant_kategori,
            "harga_asli": "",
            "harga_jual": harga_jual,
            "is_non_halal": status_halal
        }
        response2 = requests.post(update_menu + data_id + "?_method=PUT", data=param2, headers=headers,
                                  files={'image': open("pisangnug.jpg", 'rb')})
        data = response2.text

        assert response2.status_code == 422
        assert "Whoops, looks like something went wrong" in data

    def test_update_menu_without_param_harga_asli(self):
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
            "deskripsi": deskripsi,
            "merchant_kategori_makanan_id": merchant_kategori,
            "harga_jual": harga_jual,
            "is_non_halal": status_halal
        }
        response2 = requests.post(update_menu + data_id + "?_method=PUT", data=param2, headers=headers,
                                  files={'image': open("pisangnug.jpg", 'rb')})
        data = response2.text

        assert response2.status_code == 422
        assert "Whoops, looks like something went wrong" in data

    def test_update_menu_harga_jual_text_value(self):
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
            "deskripsi": deskripsi,
            "merchant_kategori_makanan_id": merchant_kategori,
            "harga_asli": harga_asli,
            "harga_jual": "harga_jual",
            "is_non_halal": status_halal
        }
        response2 = requests.post(update_menu + data_id + "?_method=PUT", data=param2, headers=headers,
                                  files={'image': open("pisangnug.jpg", 'rb')})
        data = response2.text

        assert response2.status_code == 422
        assert "Whoops, looks like something went wrong" in data

    def test_update_menu_harga_jual_empty_value(self):
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
            "deskripsi": deskripsi,
            "merchant_kategori_makanan_id": merchant_kategori,
            "harga_asli": harga_asli,
            "harga_jual": "",
            "is_non_halal": status_halal
        }
        response2 = requests.post(update_menu + data_id + "?_method=PUT", data=param2, headers=headers,
                                  files={'image': open("pisangnug.jpg", 'rb')})
        data = response2.text

        assert response2.status_code == 422
        assert "Whoops, looks like something went wrong" in data

    def test_update_menu_without_param_harga_jual(self):
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
            "deskripsi": deskripsi,
            "merchant_kategori_makanan_id": merchant_kategori,
            "harga_asli": harga_asli,
            "is_non_halal": status_halal
        }
        response2 = requests.post(update_menu + data_id + "?_method=PUT", data=param2, headers=headers,
                                  files={'image': open("pisangnug.jpg", 'rb')})
        data = response2.text

        assert response2.status_code == 422
        assert "Whoops, looks like something went wrong" in data

    def test_update_menu_menu_is_halal_wrong_value(self):
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
            "deskripsi": deskripsi,
            "merchant_kategori_makanan_id": merchant_kategori,
            "harga_jual": harga_jual,
            "harga_asli": harga_asli,
            "is_non_halal": 12
        }
        response2 = requests.post(update_menu + data_id + "?_method=PUT", data=param2, headers=headers,
                                  files={'image': open("pisangnug.jpg", 'rb')})
        data = response2.text

        assert response2.status_code == 422
        assert "Whoops, looks like something went wrong" in data

    def test_update_menu_menu_is_halal_empty_value(self):
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
            "deskripsi": deskripsi,
            "merchant_kategori_makanan_id": merchant_kategori,
            "harga_jual": harga_jual,
            "harga_asli": harga_asli,
            "is_non_halal": ""
        }
        response2 = requests.post(update_menu + data_id + "?_method=PUT", data=param2, headers=headers,
                                  files={'image': open("pisangnug.jpg", 'rb')})
        data = response2.text

        assert response2.status_code == 422
        assert "Whoops, looks like something went wrong" in data

    def test_update_menu_without_param_menu_is_halal(self):
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
            "deskripsi": deskripsi,
            "merchant_kategori_makanan_id": merchant_kategori,
            "harga_jual": harga_jual,
            "harga_asli": harga_asli
        }
        response2 = requests.post(update_menu + data_id + "?_method=PUT", data=param2, headers=headers,
                                  files={'image': open("pisangnug.jpg", 'rb')})
        data = response2.text

        assert response2.status_code == 422
        assert "Whoops, looks like something went wrong" in data

    def test_update_menu_without_param_image(self):
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
            "deskripsi": deskripsi,
            "merchant_kategori_makanan_id": merchant_kategori,
            "harga_jual": harga_jual,
            "harga_asli": harga_asli,
            "is_non_halal": status_halal
        }
        response2 = requests.post(update_menu + data_id + "?_method=PUT", data=param2, headers=headers)
        data = response2.json()

        validate_status = data.get("success")
        validate_message = data.get("message")
        validate_id = str(data.get("data")["id"])
        validate_nama_menu_makanan = str(data.get("data")["nama_menu_makanan"])
        validate_merchant_kategori_makanan_id = data.get("data")["merchant_kategori_makanan_id"]
        validate_deskripsi = data.get("data")["deskripsi"]
        validate_harga_asli = data.get("data")["harga_asli"]
        validate_harga_jual = data.get("data")["harga_jual"]
        validate_is_non_halal = data.get("data")["is_non_halal"]

        assert validate_status == bool(True)
        assert nama_makanan in validate_message
        assert data_id == validate_id
        assert validate_nama_menu_makanan == nama_makanan
        assert validate_merchant_kategori_makanan_id == merchant_kategori
        assert validate_deskripsi == deskripsi
        assert validate_harga_asli == harga_asli
        assert harga_jual == harga_jual
        assert validate_is_non_halal == status_halal

    def test_update_menu_image_empty_value(self):
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
            "deskripsi": deskripsi,
            "merchant_kategori_makanan_id": merchant_kategori,
            "harga_jual": harga_jual,
            "harga_asli": harga_asli,
            "is_non_halal": status_halal
        }

        response2 = requests.post(update_menu + data_id + "?_method=PUT", data=param2, headers=headers,
                                  files={'image': ""})
        data = response2.text

        assert response2.status_code == 422
        assert "Whoops, looks like something went wrong" in data





