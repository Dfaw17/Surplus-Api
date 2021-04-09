import requests
from env import stagging

class TestInserMerchantMenu :

    global setting_env, insert_menu, url_login, email, kata_sandi, wrong_token

    setting_env = stagging
    insert_menu = f"{setting_env}/api/v2/merchant/menus"
    url_login = f"{setting_env}/api/v2/merchant/auth/login"
    email = "vd1@gmail.com"
    kata_sandi = "12345678"
    wrong_token = "kyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvc3RhZ2luZy5hZG1pbnN1cnBsdXMubmV0XC9hcGlcL3YyXC9tZXJjaGFudFwvYXV0aFwvbG9naW4iLCJpYXQiOjE2MTU3MDExNDIsImV4cCI6MTYxODI5MzE0MiwibmJmIjoxNjE1NzAxMTQyLCJqdGkiOiJjOFluT3BlMzRqRVVIemZSIiwic3ViIjo0MDc3LCJwcnYiOiIyNzQxMDVkYTZlOTViZWYyODA3Nzg2ZGQ4NzM4ODY3Y2Y5YzAyYWFiIn0.xxI5o6tgIvb3Eds4CCfSnXM3ThFYiQwYcTCxKmrZozI"

    def test_insert_menu_normal(self):
        param = {
            "email": email,
            "password": kata_sandi
        }
        login = requests.post(url_login, data=param,
                              headers={'Accept': 'application/json'})
        token = login.json().get("token")
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json"
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
        data = response.json()

        validate_status = data.get("success")
        validate_message = data.get("message")
        validate_nama_menu = data.get("data")["nama_menu_makanan"]
        validate_merchant_kategori = data.get("data")["merchant_kategori_makanan_id"]
        validate_deskripsi = data.get("data")["deskripsi"]
        validate_harga_asli = data.get("data")["harga_asli"]
        validate_harga_jual = data.get("data")["harga_jual"]
        validate_status_halal = data.get("data")["is_non_halal"]

        assert response.status_code == 201
        assert validate_status == bool(True)
        assert f"Data menu {nama_makanan} berhasil ditambahkan." in validate_message
        assert validate_nama_menu == nama_makanan
        assert validate_merchant_kategori == merchant_kategori
        assert validate_deskripsi == deskripsi
        assert validate_harga_asli == harga_asli
        assert validate_harga_jual == harga_jual
        assert validate_status_halal == status_halal

    def test_insert_menu_wrong_token(self):
        param = {
            "email": email,
            "password": kata_sandi
        }
        login = requests.post(url_login, data=param,
                              headers={'Accept': 'application/json'})
        token = login.json().get("token")
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
            "merchant_kategori_makanan_id": merchant_kategori,
            "deskripsi": deskripsi,
            "harga_asli": harga_asli,
            "harga_jual": harga_jual,
            "is_non_halal": status_halal
        }
        response = requests.post(insert_menu, data=param2, headers=headers,
                                 files={'image': open("pisangnug.jpg", 'rb')})
        data = response.text

        assert response.status_code == 401
        assert "Unauthorized" in data

    def test_insert_menu_empty_token(self):
        param = {
            "email": email,
            "password": kata_sandi
        }
        login = requests.post(url_login, data=param,
                              headers={'Accept': 'application/json'})
        token = login.json().get("token")
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
            "merchant_kategori_makanan_id": merchant_kategori,
            "deskripsi": deskripsi,
            "harga_asli": harga_asli,
            "harga_jual": harga_jual,
            "is_non_halal": status_halal
        }
        response = requests.post(insert_menu, data=param2, headers=headers,
                                 files={'image': open("pisangnug.jpg", 'rb')})
        data = response.text

        assert response.status_code == 401
        assert "Unauthorized" in data

    def test_insert_menu_empty_nama_menu_value(self):

        param = {
            "email": email,
            "password": kata_sandi
        }
        login = requests.post(url_login, data=param,
                              headers={'Accept': 'application/json'})
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
            "nama_menu_makanan": "",
            "merchant_kategori_makanan_id": merchant_kategori,
            "deskripsi": deskripsi,
            "harga_asli": harga_asli,
            "harga_jual": harga_jual,
            "is_non_halal": status_halal
        }
        response = requests.post(insert_menu, data=param2, headers=headers,
                                 files={'image': open("pisangnug.jpg", 'rb')})
        data = response.text

        assert response.status_code == 422
        assert "Whoops, looks like something went wrong." in data

    def test_insert_menu_without_param_nama_menu(self):

        param = {
            "email": email,
            "password": kata_sandi
        }
        login = requests.post(url_login, data=param,
                              headers={'Accept': 'application/json'})
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
            "merchant_kategori_makanan_id": merchant_kategori,
            "deskripsi": deskripsi,
            "harga_asli": harga_asli,
            "harga_jual": harga_jual,
            "is_non_halal": status_halal
        }
        response = requests.post(insert_menu, data=param2, headers=headers,
                                 files={'image': open("pisangnug.jpg", 'rb')})
        data = response.text

        assert response.status_code == 422
        assert "Whoops, looks like something went wrong." in data

    def test_insert_menu_empty_merchant_kategori_id_value(self):
        param = {
            "email": email,
            "password": kata_sandi
        }
        login = requests.post(url_login, data=param,
                              headers={'Accept': 'application/json'})
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
            "merchant_kategori_makanan_id": "",
            "deskripsi": deskripsi,
            "harga_asli": harga_asli,
            "harga_jual": harga_jual,
            "is_non_halal": status_halal
        }
        response = requests.post(insert_menu, data=param2, headers=headers,
                                 files={'image': open("pisangnug.jpg", 'rb')})
        data = response.text

        assert response.status_code == 422
        assert "Whoops, looks like something went wrong." in data

    def test_insert_menu_merchant_kategori_id_not_found(self):

        param = {
            "email": email,
            "password": kata_sandi
        }
        login = requests.post(url_login, data=param,
                              headers={'Accept': 'application/json'})
        token = login.json().get("token")
        headers = {
            "Authorization": f"Bearer {token}"
        }

        nama_makanan = "Pisang Nugget"
        merchant_kategori = 666
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
        data = response.text

        assert response.status_code == 404
        assert "Not Found" in data

    def test_Insert_menu_without_param_merchant_kategori_id(self):
        param = {
            "email": email,
            "password": kata_sandi
        }
        login = requests.post(url_login, data=param,
                              headers={'Accept': 'application/json'})
        token = login.json().get("token")
        headers = {
            "Authorization": f"Bearer {token}"
        }

        nama_makanan = "Pisang Nugget"
        merchant_kategori = 666
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
        response = requests.post(insert_menu, data=param2, headers=headers,
                                 files={'image': open("pisangnug.jpg", 'rb')})
        data = response.text

        assert response.status_code == 422
        assert "Whoops, looks like something went wrong." in data

    def test_insert_menu_without_param_deskripsi(self):
        param = {
            "email": email,
            "password": kata_sandi
        }
        login = requests.post(url_login, data=param,
                              headers={'Accept': 'application/json'})
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
            "harga_asli": harga_asli,
            "harga_jual": harga_jual,
            "is_non_halal": status_halal
        }
        response = requests.post(insert_menu, data=param2, headers=headers,
                                 files={'image': open("pisangnug.jpg", 'rb')})
        data = response.text

        assert response.status_code == 422
        assert "Whoops, looks like something went wrong." in data

    def test_insert_menu_deskripsi_empty_value(self):
        param = {
            "email": email,
            "password": kata_sandi
        }
        login = requests.post(url_login, data=param,
                              headers={'Accept': 'application/json'})
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
            "deskripsi": "",
            "merchant_kategori_makanan_id": merchant_kategori,
            "harga_asli": harga_asli,
            "harga_jual": harga_jual,
            "is_non_halal": status_halal
        }
        response = requests.post(insert_menu, data=param2, headers=headers,
                                 files={'image': open("pisangnug.jpg", 'rb')})
        data = response.text

        assert response.status_code == 422
        assert "Whoops, looks like something went wrong." in data

    def test_insert_menu_harga_asli_empty_value(self):
        param = {
            "email": email,
            "password": kata_sandi
        }
        login = requests.post(url_login, data=param,
                              headers={'Accept': 'application/json'})
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
            "deskripsi": deskripsi,
            "merchant_kategori_makanan_id": merchant_kategori,
            "harga_asli": "",
            "harga_jual": harga_jual,
            "is_non_halal": status_halal
        }
        response = requests.post(insert_menu, data=param2, headers=headers,
                                 files={'image': open("pisangnug.jpg", 'rb')})
        data = response.text

        assert response.status_code == 422
        assert "Whoops, looks like something went wrong." in data

    def test_insert_menu_without_param_harga_asli(self):
        param = {
            "email": email,
            "password": kata_sandi
        }
        login = requests.post(url_login, data=param,
                              headers={'Accept': 'application/json'})
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
            "deskripsi": deskripsi,
            "merchant_kategori_makanan_id": merchant_kategori,
            "harga_jual": harga_jual,
            "is_non_halal": status_halal
        }
        response = requests.post(insert_menu, data=param2, headers=headers,
                                 files={'image': open("pisangnug.jpg", 'rb')})
        data = response.text

        assert response.status_code == 422
        assert "Whoops, looks like something went wrong." in data

    def test_insert_menu_harga_asli_value_text(self):
        param = {
            "email": email,
            "password": kata_sandi
        }
        login = requests.post(url_login, data=param,
                              headers={'Accept': 'application/json'})
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
            "deskripsi": deskripsi,
            "merchant_kategori_makanan_id": merchant_kategori,
            "harga_jual": harga_jual,
            "harga_asli": "aaa",
            "is_non_halal": status_halal
        }
        response = requests.post(insert_menu, data=param2, headers=headers,
                                 files={'image': open("pisangnug.jpg", 'rb')})
        data = response.text

        assert response.status_code == 422
        assert "Whoops, looks like something went wrong." in data

    def test_insert_menu_harga_jual_empty_value(self):
        param = {
            "email": email,
            "password": kata_sandi
        }
        login = requests.post(url_login, data=param,
                              headers={'Accept': 'application/json'})
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
            "deskripsi": deskripsi,
            "merchant_kategori_makanan_id": merchant_kategori,
            "harga_jual": "",
            "harga_asli": harga_asli,
            "is_non_halal": status_halal
        }
        response = requests.post(insert_menu, data=param2, headers=headers,
                                 files={'image': open("pisangnug.jpg", 'rb')})
        data = response.text

        assert response.status_code == 422
        assert "Whoops, looks like something went wrong." in data

    def test_insert_menu_harga_jual_value_text(self):
        param = {
            "email": email,
            "password": kata_sandi
        }
        login = requests.post(url_login, data=param,
                              headers={'Accept': 'application/json'})
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
            "deskripsi": deskripsi,
            "merchant_kategori_makanan_id": merchant_kategori,
            "harga_jual": "aaa",
            "harga_asli": harga_asli,
            "is_non_halal": status_halal
        }
        response = requests.post(insert_menu, data=param2, headers=headers,
                                 files={'image': open("pisangnug.jpg", 'rb')})
        data = response.text

        assert response.status_code == 422
        assert "Whoops, looks like something went wrong." in data

    def test_insert_menu_without_param_harga_jual(self):
        param = {
            "email": email,
            "password": kata_sandi
        }
        login = requests.post(url_login, data=param,
                              headers={'Accept': 'application/json'})
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
            "deskripsi": deskripsi,
            "merchant_kategori_makanan_id": merchant_kategori,
            "harga_asli": harga_asli,
            "is_non_halal": status_halal
        }
        response = requests.post(insert_menu, data=param2, headers=headers,
                                 files={'image': open("pisangnug.jpg", 'rb')})
        data = response.text

        assert response.status_code == 422
        assert "Whoops, looks like something went wrong." in data

    def test_insert_menu_is_non_halal_empty_value(self):
        param = {
            "email": email,
            "password": kata_sandi
        }
        login = requests.post(url_login, data=param,
                              headers={'Accept': 'application/json'})
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
            "deskripsi": deskripsi,
            "merchant_kategori_makanan_id": merchant_kategori,
            "harga_asli": harga_asli,
            "harga_jual": harga_jual,
            "is_non_halal": ""
        }
        response = requests.post(insert_menu, data=param2, headers=headers,
                                 files={'image': open("pisangnug.jpg", 'rb')})
        data = response.text

        assert response.status_code == 422
        assert "Whoops, looks like something went wrong." in data

    def test_insert_menu_is_non_halal_value_text(self):
        param = {
            "email": email,
            "password": kata_sandi
        }
        login = requests.post(url_login, data=param,
                              headers={'Accept': 'application/json'})
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
            "deskripsi": deskripsi,
            "merchant_kategori_makanan_id": merchant_kategori,
            "harga_asli": harga_asli,
            "harga_jual": harga_jual,
            "is_non_halal": "aaaa"
        }
        response = requests.post(insert_menu, data=param2, headers=headers,
                                 files={'image': open("pisangnug.jpg", 'rb')})
        data = response.text

        assert response.status_code == 422
        assert "Whoops, looks like something went wrong." in data

    def test_insert_menu_without_param_is_non_halal(self):
        param = {
            "email": email,
            "password": kata_sandi
        }
        login = requests.post(url_login, data=param,
                              headers={'Accept': 'application/json'})
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
            "deskripsi": deskripsi,
            "merchant_kategori_makanan_id": merchant_kategori,
            "harga_asli": harga_asli,
            "harga_jual": harga_jual
        }
        response = requests.post(insert_menu, data=param2, headers=headers,
                                 files={'image': open("pisangnug.jpg", 'rb')})
        data = response.text

        assert response.status_code == 422
        assert "Whoops, looks like something went wrong." in data

    def test_insert_menu_without_params_image(self):
        param = {
            "email": email,
            "password": kata_sandi
        }
        login = requests.post(url_login, data=param,
                              headers={'Accept': 'application/json'})
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
            "deskripsi": deskripsi,
            "merchant_kategori_makanan_id": merchant_kategori,
            "harga_asli": harga_asli,
            "harga_jual": harga_jual,
            "is_non_halal": status_halal
        }
        response = requests.post(insert_menu, data=param2, headers=headers)
        data = response.text

        assert response.status_code == 422
        assert "Whoops, looks like something went wrong." in data





