import requests
from env import *
from assertpy import *


class TestInserMerchantMenu:
    global setting_env, insert_menu, url_login, email, kata_sandi, wrong_token

    setting_env = testing
    insert_menu = f"{setting_env}/api/v2/merchant/menus"
    url_login = f"{setting_env}/api/v2/merchant/auth/login"
    email = "sdet@gmail.com"
    kata_sandi = "12345678"
    wrong_token = "kyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvc3RhZ2luZy5hZG1pbnN1cnBsdXMubmV0XC9hcGlcL3YyXC9tZXJjaGFudFwvYXV0aFwvbG9naW4iLCJpYXQiOjE2MTU3MDExNDIsImV4cCI6MTYxODI5MzE0MiwibmJmIjoxNjE1NzAxMTQyLCJqdGkiOiJjOFluT3BlMzRqRVVIemZSIiwic3ViIjo0MDc3LCJwcnYiOiIyNzQxMDVkYTZlOTViZWYyODA3Nzg2ZGQ4NzM4ODY3Y2Y5YzAyYWFiIn0.xxI5o6tgIvb3Eds4CCfSnXM3ThFYiQwYcTCxKmrZozI"

    def test_insert_menu_kat_sayur_normal(self):
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

        nama_makanan = "Cessin"
        merchant_kategori = 5
        deskripsi = "Cessin Meikarta"
        harga_asli = 20000
        harga_jual = 10000
        status_halal = 0
        weight = 200
        param2 = {
            "nama_menu_makanan": nama_makanan,
            "merchant_kategori_makanan_id": merchant_kategori,
            "deskripsi": deskripsi,
            "harga_asli": harga_asli,
            "harga_jual": harga_jual,
            "is_non_halal": "0",
            "weight": weight
        }
        response = requests.post(insert_menu, data=param2, headers=headers, files={
            'images[0]': open("img/OIP.jpg", 'rb'),
            'images[1]': open("img/OIP1.jpg", 'rb'),
            'images[2]': open("img/OIP2.jpg", 'rb'),
        })
        data = response.json()

        validate_status = data.get("success")
        validate_message = data.get("message")
        validate_data = data.get("data")
        validate_nama = data.get("data")['nama_menu_makanan']
        validate_kategori = data.get("data")['merchant_kategori_makanan_id']
        validate_deskripsi = data.get("data")['deskripsi']
        validate_harga_asli = data.get("data")['harga_asli']
        validate_harga_jual = data.get("data")['harga_jual']
        validate_weight = data.get("data")['weight']

        assert response.status_code == 201
        assert validate_status == bool(True)
        assert f"Data menu {nama_makanan} berhasil ditambahkan." in validate_message
        assert_that(validate_weight).is_equal_to(weight)
        assert_that(validate_harga_jual).is_equal_to(harga_jual)
        assert_that(validate_harga_asli).is_equal_to(harga_asli)
        assert_that(validate_deskripsi).is_equal_to(deskripsi)
        assert_that(validate_kategori).is_equal_to(merchant_kategori)
        assert_that(validate_nama).is_equal_to(nama_makanan)

    def test_insert_menu_kat_non_sayur_normal(self):
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

        nama_makanan = "Mie Setan"
        merchant_kategori = 1
        deskripsi = "Mie Setan Kuy"
        harga_asli = 25000
        harga_jual = 5000
        status_halal = 0
        weight_string = "2 Mangkok"
        param2 = {
            "nama_menu_makanan": nama_makanan,
            "merchant_kategori_makanan_id": merchant_kategori,
            "deskripsi": deskripsi,
            "harga_asli": harga_asli,
            "harga_jual": harga_jual,
            "is_non_halal": "0",
            "weight_string": weight_string
        }
        response = requests.post(insert_menu, data=param2, headers=headers, files={
            'images[0]': open("img/ms1.jpeg", 'rb'),
            'images[1]': open("img/ms2.jpg", 'rb'),
        })
        data = response.json()

        validate_status = data.get("success")
        validate_message = data.get("message")
        validate_data = data.get("data")
        validate_nama = data.get("data")['nama_menu_makanan']
        validate_kategori = data.get("data")['merchant_kategori_makanan_id']
        validate_deskripsi = data.get("data")['deskripsi']
        validate_harga_asli = data.get("data")['harga_asli']
        validate_harga_jual = data.get("data")['harga_jual']
        validate_weight = data.get("data")['weight_string']

        assert response.status_code == 201
        assert validate_status == bool(True)
        assert f"Data menu {nama_makanan} berhasil ditambahkan." in validate_message
        assert_that(validate_weight).is_equal_to(weight_string)
        assert_that(validate_harga_jual).is_equal_to(harga_jual)
        assert_that(validate_harga_asli).is_equal_to(harga_asli)
        assert_that(validate_deskripsi).is_equal_to(deskripsi)
        assert_that(validate_kategori).is_equal_to(merchant_kategori)
        assert_that(validate_nama).is_equal_to(nama_makanan)

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
                                 files={'image': open("img/pisangnug.jpg", 'rb')})
        data = response.text

        assert response.status_code == 401
        assert "Unauthorized" in data

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
                                 files={'image': open("img/pisangnug.jpg", 'rb')})
        data = response.text

        assert response.status_code == 401
        assert "Unauthorized" in data

    def test_insert_menu_empty_nama_menu_value(self):
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

        nama_makanan = ""
        merchant_kategori = 5
        deskripsi = "Cessin Meikarta"
        harga_asli = 20000
        harga_jual = 10000
        status_halal = 0
        weight = 200
        param2 = {
            "nama_menu_makanan": nama_makanan,
            "merchant_kategori_makanan_id": merchant_kategori,
            "deskripsi": deskripsi,
            "harga_asli": harga_asli,
            "harga_jual": harga_jual,
            "is_non_halal": "0",
            "weight": weight
        }
        response = requests.post(insert_menu, data=param2, headers=headers, files={
            'images[0]': open("img/OIP.jpg", 'rb'),
            'images[1]': open("img/OIP1.jpg", 'rb'),
            'images[2]': open("img/OIP2.jpg", 'rb'),
        })
        data = response.json()

        validate_status = data.get("success")
        validate_message = data.get("message")['nama_menu_makanan']

        assert response.status_code == 422
        assert validate_status == bool(False)
        assert "Nama menu tidak boleh kosong." in validate_message

    def test_insert_menu_without_param_nama_menu(self):
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

        nama_makanan = "Cessin"
        merchant_kategori = 5
        deskripsi = "Cessin Meikarta"
        harga_asli = 20000
        harga_jual = 10000
        status_halal = 0
        weight = 200
        param2 = {
            "merchant_kategori_makanan_id": merchant_kategori,
            "deskripsi": deskripsi,
            "harga_asli": harga_asli,
            "harga_jual": harga_jual,
            "is_non_halal": "0",
            "weight": weight
        }
        response = requests.post(insert_menu, data=param2, headers=headers, files={
            'images[0]': open("img/OIP.jpg", 'rb'),
            'images[1]': open("img/OIP1.jpg", 'rb'),
            'images[2]': open("img/OIP2.jpg", 'rb'),
        })
        data = response.json()

        validate_status = data.get("success")
        validate_message = data.get("message")['nama_menu_makanan']

        assert response.status_code == 422
        assert validate_status == bool(False)
        assert "Nama menu tidak boleh kosong." in validate_message

    def test_insert_menu_kategori_makanan_id_wrong_value(self):
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

        nama_makanan = "Cessin"
        merchant_kategori = 500
        deskripsi = "Cessin Meikarta"
        harga_asli = 20000
        harga_jual = 10000
        status_halal = 0
        weight = "200 Kotak"
        param2 = {
            "nama_menu_makanan": nama_makanan,
            "merchant_kategori_makanan_id": merchant_kategori,
            "deskripsi": deskripsi,
            "harga_asli": harga_asli,
            "harga_jual": harga_jual,
            "is_non_halal": "0",
            "weight_string": weight
        }
        response = requests.post(insert_menu, data=param2, headers=headers, files={
            'images[0]': open("img/OIP.jpg", 'rb'),
            'images[1]': open("img/OIP1.jpg", 'rb'),
            'images[2]': open("img/OIP2.jpg", 'rb'),
        })
        data = response.json()

        validate_status = data.get("success")
        validate_message = data.get("message")

        assert response.status_code == 404
        assert validate_status == bool(False)
        assert "Data gagal dibuat." in validate_message

    def test_insert_menu_kategori_makanan_id_empty(self):
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

        nama_makanan = "Cessin"
        merchant_kategori = ""
        deskripsi = "Cessin Meikarta"
        harga_asli = 20000
        harga_jual = 10000
        status_halal = 0
        weight = "200 Kotak"
        param2 = {
            "nama_menu_makanan": nama_makanan,
            "merchant_kategori_makanan_id": merchant_kategori,
            "deskripsi": deskripsi,
            "harga_asli": harga_asli,
            "harga_jual": harga_jual,
            "is_non_halal": "0",
            "weight_string": weight
        }
        response = requests.post(insert_menu, data=param2, headers=headers, files={
            'images[0]': open("img/OIP.jpg", 'rb'),
            'images[1]': open("img/OIP1.jpg", 'rb'),
            'images[2]': open("img/OIP2.jpg", 'rb'),
        })
        data = response.json()

        validate_status = data.get("success")
        validate_message = data.get("message")['merchant_kategori_makanan_id']

        assert response.status_code == 422
        assert validate_status == bool(False)
        assert "Kategori menu tidak boleh kosong." in validate_message

    def test_insert_menu_without_param_kategori_makanan_id(self):
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

        nama_makanan = "Cessin"
        merchant_kategori = ""
        deskripsi = "Cessin Meikarta"
        harga_asli = 20000
        harga_jual = 10000
        status_halal = 0
        weight = "200 Kotak"
        param2 = {
            "nama_menu_makanan": nama_makanan,
            "merchant_kategori_makanan_id": merchant_kategori,
            "deskripsi": deskripsi,
            "harga_asli": harga_asli,
            "harga_jual": harga_jual,
            "is_non_halal": "0",
            "weight_string": weight
        }
        response = requests.post(insert_menu, data=param2, headers=headers, files={
            'images[0]': open("img/OIP.jpg", 'rb'),
            'images[1]': open("img/OIP1.jpg", 'rb'),
            'images[2]': open("img/OIP2.jpg", 'rb'),
        })
        data = response.json()

        validate_status = data.get("success")
        validate_message = data.get("message")['merchant_kategori_makanan_id']

        assert response.status_code == 422
        assert validate_status == bool(False)
        assert "Kategori menu tidak boleh kosong." in validate_message

    def test_insert_menu_deskripsi_empty(self):
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

        nama_makanan = "Cessin"
        merchant_kategori = 1
        deskripsi = ""
        harga_asli = 20000
        harga_jual = 10000
        status_halal = 0
        weight = "200 Kotak"
        param2 = {
            "nama_menu_makanan": nama_makanan,
            "merchant_kategori_makanan_id": merchant_kategori,
            "deskripsi": deskripsi,
            "harga_asli": harga_asli,
            "harga_jual": harga_jual,
            "is_non_halal": "0",
            "weight_string": weight
        }
        response = requests.post(insert_menu, data=param2, headers=headers, files={
            'images[0]': open("img/OIP.jpg", 'rb'),
            'images[1]': open("img/OIP1.jpg", 'rb'),
            'images[2]': open("img/OIP2.jpg", 'rb'),
        })
        data = response.json()

        validate_status = data.get("success")
        validate_message = data.get("message")['deskripsi']

        assert response.status_code == 422
        assert validate_status == bool(False)
        assert "deskripsi tidak boleh kosong." in validate_message

    def test_insert_menu_without_param_deskripsi(self):
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

        nama_makanan = "Cessin"
        merchant_kategori = 1
        deskripsi = "Cessin Japan"
        harga_asli = 20000
        harga_jual = 10000
        status_halal = 0
        weight = "200 Kotak"
        param2 = {
            "nama_menu_makanan": nama_makanan,
            "merchant_kategori_makanan_id": merchant_kategori,
            "harga_asli": harga_asli,
            "harga_jual": harga_jual,
            "is_non_halal": "0",
            "weight_string": weight
        }
        response = requests.post(insert_menu, data=param2, headers=headers, files={
            'images[0]': open("img/OIP.jpg", 'rb'),
            'images[1]': open("img/OIP1.jpg", 'rb'),
            'images[2]': open("img/OIP2.jpg", 'rb'),
        })
        data = response.json()

        validate_status = data.get("success")
        validate_message = data.get("message")['deskripsi']

        assert response.status_code == 422
        assert validate_status == bool(False)
        assert "deskripsi tidak boleh kosong." in validate_message

    def test_insert_menu_harga_asli_empty(self):
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

        nama_makanan = "Cessin"
        merchant_kategori = 1
        deskripsi = "Cessin Japan"
        harga_asli = ""
        harga_jual = 10000
        status_halal = 0
        weight = "200 Kotak"
        param2 = {
            "nama_menu_makanan": nama_makanan,
            "merchant_kategori_makanan_id": merchant_kategori,
            "deskripsi": deskripsi,
            "harga_asli": harga_asli,
            "harga_jual": harga_jual,
            "is_non_halal": status_halal,
            "weight_string": weight
        }
        response = requests.post(insert_menu, data=param2, headers=headers, files={
            'images[0]': open("img/OIP.jpg", 'rb'),
            'images[1]': open("img/OIP1.jpg", 'rb'),
            'images[2]': open("img/OIP2.jpg", 'rb'),
        })
        data = response.json()

        validate_status = data.get("success")
        validate_message = data.get("message")['harga_asli']

        assert response.status_code == 422
        assert validate_status == bool(False)
        assert "Harga asli tidak boleh kosong." in validate_message
        
    def test_insert_menu_without_param_harga_asli(self):
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

        nama_makanan = "Cessin"
        merchant_kategori = 1
        deskripsi = "Cessin Japan"
        harga_asli = ""
        harga_jual = 10000
        status_halal = 0
        weight = "200 Kotak"
        param2 = {
            "nama_menu_makanan": nama_makanan,
            "merchant_kategori_makanan_id": merchant_kategori,
            "deskripsi": deskripsi,
            "harga_jual": harga_jual,
            "is_non_halal": status_halal,
            "weight_string": weight
        }
        response = requests.post(insert_menu, data=param2, headers=headers, files={
            'images[0]': open("img/OIP.jpg", 'rb'),
            'images[1]': open("img/OIP1.jpg", 'rb'),
            'images[2]': open("img/OIP2.jpg", 'rb'),
        })
        data = response.json()

        validate_status = data.get("success")
        validate_message = data.get("message")['harga_asli']

        assert response.status_code == 422
        assert validate_status == bool(False)
        assert "Harga asli tidak boleh kosong." in validate_message

    def test_insert_menu_harga_asli_string_value(self):
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

        nama_makanan = "Cessin"
        merchant_kategori = 1
        deskripsi = "Cessin Japan"
        harga_asli = "aaaa"
        harga_jual = 10000
        status_halal = 0
        weight = "200 Kotak"
        param2 = {
            "nama_menu_makanan": nama_makanan,
            "merchant_kategori_makanan_id": merchant_kategori,
            "deskripsi": deskripsi,
            "harga_asli": harga_asli,
            "harga_jual": harga_jual,
            "is_non_halal": status_halal,
            "weight_string": weight
        }
        response = requests.post(insert_menu, data=param2, headers=headers, files={
            'images[0]': open("img/OIP.jpg", 'rb'),
            'images[1]': open("img/OIP1.jpg", 'rb'),
            'images[2]': open("img/OIP2.jpg", 'rb'),
        })
        data = response.json()

        validate_status = data.get("success")
        validate_message = data.get("message")['harga_asli']

        assert response.status_code == 422
        assert validate_status == bool(False)
        assert "format harga asli yang diinputkan salah" in validate_message

    def test_insert_menu_harga_jual_empty(self):
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

        nama_makanan = "Cessin"
        merchant_kategori = 1
        deskripsi = "Cessin Japan"
        harga_asli = 20000
        harga_jual = ""
        status_halal = 0
        weight = "200 Kotak"
        param2 = {
            "nama_menu_makanan": nama_makanan,
            "merchant_kategori_makanan_id": merchant_kategori,
            "deskripsi": deskripsi,
            "harga_asli": harga_asli,
            "harga_jual": harga_jual,
            "is_non_halal": status_halal,
            "weight_string": weight
        }
        response = requests.post(insert_menu, data=param2, headers=headers, files={
            'images[0]': open("img/OIP.jpg", 'rb'),
            'images[1]': open("img/OIP1.jpg", 'rb'),
            'images[2]': open("img/OIP2.jpg", 'rb'),
        })
        data = response.json()

        validate_status = data.get("success")
        validate_message = data.get("message")['harga_jual']

        assert response.status_code == 422
        assert validate_status == bool(False)
        assert "Harga jual tidak boleh kosong." in validate_message

    def test_insert_menu_without_param_harga_jual(self):
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

        nama_makanan = "Cessin"
        merchant_kategori = 1
        deskripsi = "Cessin Japan"
        harga_asli = 20000
        harga_jual = 10000
        status_halal = 0
        weight = "200 Kotak"
        param2 = {
            "nama_menu_makanan": nama_makanan,
            "merchant_kategori_makanan_id": merchant_kategori,
            "deskripsi": deskripsi,
            "harga_asli": harga_asli,
            "is_non_halal": status_halal,
            "weight_string": weight
        }
        response = requests.post(insert_menu, data=param2, headers=headers, files={
            'images[0]': open("img/OIP.jpg", 'rb'),
            'images[1]': open("img/OIP1.jpg", 'rb'),
            'images[2]': open("img/OIP2.jpg", 'rb'),
        })
        data = response.json()

        validate_status = data.get("success")
        validate_message = data.get("message")['harga_jual']

        assert response.status_code == 422
        assert validate_status == bool(False)
        assert "Harga jual tidak boleh kosong." in validate_message

    def test_insert_menu_harga_jual_string_value(self):
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

        nama_makanan = "Cessin"
        merchant_kategori = 1
        deskripsi = "Cessin Japan"
        harga_asli = 20000
        harga_jual = "aaaa"
        status_halal = 0
        weight = "200 Kotak"
        param2 = {
            "nama_menu_makanan": nama_makanan,
            "merchant_kategori_makanan_id": merchant_kategori,
            "deskripsi": deskripsi,
            "harga_asli": harga_asli,
            "harga_jual": harga_jual,
            "is_non_halal": status_halal,
            "weight_string": weight
        }
        response = requests.post(insert_menu, data=param2, headers=headers, files={
            'images[0]': open("img/OIP.jpg", 'rb'),
            'images[1]': open("img/OIP1.jpg", 'rb'),
            'images[2]': open("img/OIP2.jpg", 'rb'),
        })
        data = response.json()

        validate_status = data.get("success")
        validate_message = data.get("message")['harga_jual']

        assert response.status_code == 422
        assert validate_status == bool(False)
        assert "format harga jual yang diinputkan salah" in validate_message

    def test_insert_menu_is_non_halal_empty(self):
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

        nama_makanan = "Cessin"
        merchant_kategori = 1
        deskripsi = "Cessin Japan"
        harga_asli = 20000
        harga_jual = 100
        status_halal = ""
        weight = "200 Kotak"
        param2 = {
            "nama_menu_makanan": nama_makanan,
            "merchant_kategori_makanan_id": merchant_kategori,
            "deskripsi": deskripsi,
            "harga_asli": harga_asli,
            "harga_jual": harga_jual,
            "is_non_halal": status_halal,
            "weight_string": weight
        }
        response = requests.post(insert_menu, data=param2, headers=headers, files={
            'images[0]': open("img/OIP.jpg", 'rb'),
            'images[1]': open("img/OIP1.jpg", 'rb'),
            'images[2]': open("img/OIP2.jpg", 'rb'),
        })
        data = response.json()

        validate_status = data.get("success")
        validate_message = data.get("message")['is_non_halal']

        assert response.status_code == 422
        assert validate_status == bool(False)
        assert "Menu tidak halal tidak boleh kosong." in validate_message

    def test_insert_menu_without_param_is_non_halal(self):
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

        nama_makanan = "Cessin"
        merchant_kategori = 1
        deskripsi = "Cessin Japan"
        harga_asli = 20000
        harga_jual = 100
        status_halal = 0
        weight = "200 Kotak"
        param2 = {
            "nama_menu_makanan": nama_makanan,
            "merchant_kategori_makanan_id": merchant_kategori,
            "deskripsi": deskripsi,
            "harga_asli": harga_asli,
            "harga_jual": harga_jual,
            # "is_non_halal": status_halal,
            "weight_string": weight
        }
        response = requests.post(insert_menu, data=param2, headers=headers, files={
            'images[0]': open("img/OIP.jpg", 'rb'),
            'images[1]': open("img/OIP1.jpg", 'rb'),
            'images[2]': open("img/OIP2.jpg", 'rb'),
        })
        data = response.json()

        validate_status = data.get("success")
        validate_message = data.get("message")['is_non_halal']

        assert response.status_code == 422
        assert validate_status == bool(False)
        assert "Menu tidak halal tidak boleh kosong." in validate_message

    def test_insert_menu_is_non_halal_wrong_value(self):
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

        nama_makanan = "Cessin"
        merchant_kategori = 1
        deskripsi = "Cessin Japan"
        harga_asli = 20000
        harga_jual = 100
        status_halal = "aaa"
        weight = "200 Kotak"
        param2 = {
            "nama_menu_makanan": nama_makanan,
            "merchant_kategori_makanan_id": merchant_kategori,
            "deskripsi": deskripsi,
            "harga_asli": harga_asli,
            "harga_jual": harga_jual,
            "is_non_halal": status_halal,
            "weight_string": weight
        }
        response = requests.post(insert_menu, data=param2, headers=headers, files={
            'images[0]': open("img/OIP.jpg", 'rb'),
            'images[1]': open("img/OIP1.jpg", 'rb'),
            'images[2]': open("img/OIP2.jpg", 'rb'),
        })
        data = response.json()

        validate_status = data.get("success")
        validate_message = data.get("message")['is_non_halal']

        assert response.status_code == 422
        assert validate_status == bool(False)
        assert "Menu tidak halal harus bernilai true atau false." in validate_message

    def test_insert_menu_sayur_without_param_weight(self):
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

        nama_makanan = "Cessin"
        merchant_kategori = 5
        deskripsi = "Cessin Japan"
        harga_asli = 20000
        harga_jual = 100
        status_halal = 0
        weight = ""
        param2 = {
            "nama_menu_makanan": nama_makanan,
            "merchant_kategori_makanan_id": merchant_kategori,
            "deskripsi": deskripsi,
            "harga_asli": harga_asli,
            "harga_jual": harga_jual,
            "is_non_halal": status_halal,
            "weight": weight
        }
        response = requests.post(insert_menu, data=param2, headers=headers, files={
            'images[0]': open("img/OIP.jpg", 'rb'),
            'images[1]': open("img/OIP1.jpg", 'rb'),
            'images[2]': open("img/OIP2.jpg", 'rb'),
        })
        data = response.json()

        validate_status = data.get("success")
        validate_message = data.get("message")['weight']

        assert response.status_code == 422
        assert validate_status == bool(False)
        assert "weight tidak boleh kosong ketika Kategori menu adalah 5." in validate_message

    def test_insert_menu_sayur_wight_empty_value(self):
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

        nama_makanan = "Cessin"
        merchant_kategori = 5
        deskripsi = "Cessin Japan"
        harga_asli = 20000
        harga_jual = 100
        status_halal = 0
        weight = "200"
        param2 = {
            "nama_menu_makanan": nama_makanan,
            "merchant_kategori_makanan_id": merchant_kategori,
            "deskripsi": deskripsi,
            "harga_asli": harga_asli,
            "harga_jual": harga_jual,
            "is_non_halal": status_halal,
        }
        response = requests.post(insert_menu, data=param2, headers=headers, files={
            'images[0]': open("img/OIP.jpg", 'rb'),
            'images[1]': open("img/OIP1.jpg", 'rb'),
            'images[2]': open("img/OIP2.jpg", 'rb'),
        })
        data = response.json()

        validate_status = data.get("success")
        validate_message = data.get("message")['weight']

        assert response.status_code == 422
        assert validate_status == bool(False)
        assert "weight tidak boleh kosong ketika Kategori menu adalah 5." in validate_message

    def test_insert_menu_sayur_weight_sting_value(self):
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

        nama_makanan = "Cessin"
        merchant_kategori = 5
        deskripsi = "Cessin Japan"
        harga_asli = 20000
        harga_jual = 100
        status_halal = 0
        weight = "aa"
        param2 = {
            "nama_menu_makanan": nama_makanan,
            "merchant_kategori_makanan_id": merchant_kategori,
            "deskripsi": deskripsi,
            "harga_asli": harga_asli,
            "harga_jual": harga_jual,
            "is_non_halal": status_halal,
            "weight": weight
        }
        response = requests.post(insert_menu, data=param2, headers=headers, files={
            'images[0]': open("img/OIP.jpg", 'rb'),
            'images[1]': open("img/OIP1.jpg", 'rb'),
            'images[2]': open("img/OIP2.jpg", 'rb'),
        })
        data = response.json()

        validate_status = data.get("success")
        validate_message = data.get("message")['weight']

        assert response.status_code == 422
        assert validate_status == bool(False)
        assert "weight harus berupa angka." in validate_message

    def test_insert_menu_non_sayur_without_param_weight_string(self):
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

        nama_makanan = "Cessin"
        merchant_kategori = 1
        deskripsi = "Cessin Japan"
        harga_asli = 20000
        harga_jual = 100
        status_halal = 0
        weight = ""
        param2 = {
            "nama_menu_makanan": nama_makanan,
            "merchant_kategori_makanan_id": merchant_kategori,
            "deskripsi": deskripsi,
            "harga_asli": harga_asli,
            "harga_jual": harga_jual,
            "is_non_halal": status_halal,
            "weight_string": weight
        }
        response = requests.post(insert_menu, data=param2, headers=headers, files={
            'images[0]': open("img/OIP.jpg", 'rb'),
            'images[1]': open("img/OIP1.jpg", 'rb'),
            'images[2]': open("img/OIP2.jpg", 'rb'),
        })
        data = response.json()

        validate_status = data.get("success")
        validate_message = data.get("message")['weight_string']

        assert response.status_code == 422
        assert validate_status == bool(False)
        assert 'weight string tidak boleh kosong kecuali Kategori menu ada dalam 5.' in validate_message

    def test_insert_menu_non_sayur_wight_empty_value(self):
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

        nama_makanan = "Cessin"
        merchant_kategori = 1
        deskripsi = "Cessin Japan"
        harga_asli = 20000
        harga_jual = 100
        status_halal = 0
        weight = "200"
        param2 = {
            "nama_menu_makanan": nama_makanan,
            "merchant_kategori_makanan_id": merchant_kategori,
            "deskripsi": deskripsi,
            "harga_asli": harga_asli,
            "harga_jual": harga_jual,
            "is_non_halal": status_halal,
        }
        response = requests.post(insert_menu, data=param2, headers=headers, files={
            'images[0]': open("img/OIP.jpg", 'rb'),
            'images[1]': open("img/OIP1.jpg", 'rb'),
            'images[2]': open("img/OIP2.jpg", 'rb'),
        })
        data = response.json()

        validate_status = data.get("success")
        validate_message = data.get("message")['weight_string']

        assert response.status_code == 422
        assert validate_status == bool(False)
        assert 'weight string tidak boleh kosong kecuali Kategori menu ada dalam 5.' in validate_message

    def test_insert_menu_non_sayur_weight_int_value(self):
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

        nama_makanan = "Cessin"
        merchant_kategori = 1
        deskripsi = "Cessin Japan"
        harga_asli = 20000
        harga_jual = 100
        status_halal = 0
        weight = "1000"
        param2 = {
            "nama_menu_makanan": nama_makanan,
            "merchant_kategori_makanan_id": merchant_kategori,
            "deskripsi": deskripsi,
            "harga_asli": harga_asli,
            "harga_jual": harga_jual,
            "is_non_halal": status_halal,
            "weight_string": weight
        }
        response = requests.post(insert_menu, data=param2, headers=headers, files={
            'images[0]': open("img/OIP.jpg", 'rb'),
            'images[1]': open("img/OIP1.jpg", 'rb'),
            'images[2]': open("img/OIP2.jpg", 'rb'),
        })
        data = response.json()

        validate_status = data.get("success")
        validate_message = data.get("message")

        assert response.status_code == 201
        assert validate_status == bool(True)
        assert 'Data menu Cessin berhasil ditambahkan.' in validate_message


