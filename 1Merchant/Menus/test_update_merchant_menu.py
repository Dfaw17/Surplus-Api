import requests
from env import *
from assertpy import *


class TestUpdateMerchantMenu:
    global setting_env, update_menu, url_login, email, kata_sandi, wrong_token, url_getall_menu

    setting_env = testing
    url_getall_menu = f"{setting_env}/api/v2/merchant/menus/"
    url_login = f"{setting_env}/api/v2/merchant/auth/login"
    email = "sdet@gmail.com"
    kata_sandi = "12345678"
    wrong_token = "kyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvc3RhZ2luZy5hZG1pbnN1cnBsdXMubmV0XC9hcGlcL3YyXC9tZXJjaGFudFwvYXV0aFwvbG9naW4iLCJpYXQiOjE2MTU3MDExNDIsImV4cCI6MTYxODI5MzE0MiwibmJmIjoxNjE1NzAxMTQyLCJqdGkiOiJjOFluT3BlMzRqRVVIemZSIiwic3ViIjo0MDc3LCJwcnYiOiIyNzQxMDVkYTZlOTViZWYyODA3Nzg2ZGQ4NzM4ODY3Y2Y5YzAyYWFiIn0.xxI5o6tgIvb3Eds4CCfSnXM3ThFYiQwYcTCxKmrZozI"

    def test_update_menu_kat_sayur_normal(self):
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
        get_all = requests.get(url_getall_menu, headers=headers)
        menu = get_all.json().get('data')[0]['id']

        nama_makanan = "Mie Setan"
        merchant_kategori = 5
        deskripsi = "Mie Setan Kuy"
        harga_asli = 25000
        harga_jual = 5000
        status_halal = 0
        weight_string = 200
        param2 = {
            "nama_menu_makanan": nama_makanan,
            "merchant_kategori_makanan_id": merchant_kategori,
            "deskripsi": deskripsi,
            "harga_asli": harga_asli,
            "harga_jual": harga_jual,
            "is_non_halal": "0",
            "weight": weight_string
        }
        response = requests.post(url_getall_menu + str(menu) + '?_method=PUT', data=param2, headers=headers, files={
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
        validate_weight = data.get("data")['weight']

        assert response.status_code == 200
        assert validate_status == bool(True)
        assert f"Data menu {nama_makanan} berhasil diperbarui." in validate_message
        assert_that(validate_weight).is_equal_to(weight_string)
        assert_that(validate_harga_jual).is_equal_to(harga_jual)
        assert_that(validate_harga_asli).is_equal_to(harga_asli)
        assert_that(validate_deskripsi).is_equal_to(deskripsi)
        assert_that(validate_kategori).is_equal_to(merchant_kategori)
        assert_that(validate_nama).is_equal_to(nama_makanan)

    def test_update_menu_kat_non_sayur_normal(self):
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
        get_all = requests.get(url_getall_menu, headers=headers)
        menu = get_all.json().get('data')[0]['id']

        nama_makanan = "Mie Setan"
        merchant_kategori = 1
        deskripsi = "Mie Setan Kuy"
        harga_asli = 25000
        harga_jual = 5000
        status_halal = 0
        weight_string = "200 Kotak"
        param2 = {
            "nama_menu_makanan": nama_makanan,
            "merchant_kategori_makanan_id": merchant_kategori,
            "deskripsi": deskripsi,
            "harga_asli": harga_asli,
            "harga_jual": harga_jual,
            "is_non_halal": "0",
            "weight_string": weight_string
        }
        response = requests.post(url_getall_menu + str(menu) + '?_method=PUT', data=param2, headers=headers, files={
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

        assert response.status_code == 200
        assert validate_status == bool(True)
        assert f"Data menu {nama_makanan} berhasil diperbarui." in validate_message
        assert_that(validate_weight).is_equal_to(weight_string)
        assert_that(validate_harga_jual).is_equal_to(harga_jual)
        assert_that(validate_harga_asli).is_equal_to(harga_asli)
        assert_that(validate_deskripsi).is_equal_to(deskripsi)
        assert_that(validate_kategori).is_equal_to(merchant_kategori)
        assert_that(validate_nama).is_equal_to(nama_makanan)

    def test_update_menu_wrong_token(self):
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
        get_all = requests.get(url_getall_menu, headers=headers)
        menu = get_all.json().get('data')[0]['id']

        nama_makanan = "Mie Setan"
        merchant_kategori = 1
        deskripsi = "Mie Setan Kuy"
        harga_asli = 25000
        harga_jual = 5000
        status_halal = 0
        weight_string = "200 Kotak"
        param2 = {
            "nama_menu_makanan": nama_makanan,
            "merchant_kategori_makanan_id": merchant_kategori,
            "deskripsi": deskripsi,
            "harga_asli": harga_asli,
            "harga_jual": harga_jual,
            "is_non_halal": "0",
            "weight_string": weight_string
        }
        headers = {
            "Authorization": wrong_token,
            "Accept": "application/json"
        }
        response = requests.post(url_getall_menu + str(menu) + '?_method=PUT', data=param2, headers=headers, files={
            'images[0]': open("img/ms1.jpeg", 'rb'),
            'images[1]': open("img/ms2.jpg", 'rb'),
        })
        data = response.json()

        validate_status = data.get("success")
        validate_message = data.get("message")

        assert response.status_code == 401
        assert validate_status == bool(False)
        assert "Unauthorized" in validate_message

    def test_update_menu_token_empty(self):
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
        get_all = requests.get(url_getall_menu, headers=headers)
        menu = get_all.json().get('data')[0]['id']

        nama_makanan = "Mie Setan"
        merchant_kategori = 1
        deskripsi = "Mie Setan Kuy"
        harga_asli = 25000
        harga_jual = 5000
        status_halal = 0
        weight_string = "200 Kotak"
        param2 = {
            "nama_menu_makanan": nama_makanan,
            "merchant_kategori_makanan_id": merchant_kategori,
            "deskripsi": deskripsi,
            "harga_asli": harga_asli,
            "harga_jual": harga_jual,
            "is_non_halal": "0",
            "weight_string": weight_string
        }
        headers = {
            "Authorization": "",
            "Accept": "application/json"
        }
        response = requests.post(url_getall_menu + str(menu) + '?_method=PUT', data=param2, headers=headers, files={
            'images[0]': open("img/ms1.jpeg", 'rb'),
            'images[1]': open("img/ms2.jpg", 'rb'),
        })
        data = response.json()

        validate_status = data.get("success")
        validate_message = data.get("message")

        assert response.status_code == 401
        assert validate_status == bool(False)
        assert "Unauthorized" in validate_message

    def test_update_menu_nama_makanan_empty(self):
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
        get_all = requests.get(url_getall_menu, headers=headers)
        menu = get_all.json().get('data')[0]['id']

        nama_makanan = ""
        merchant_kategori = 1
        deskripsi = "Mie Setan Kuy"
        harga_asli = 25000
        harga_jual = 5000
        status_halal = 0
        weight_string = "200 Kotak"
        param2 = {
            "nama_menu_makanan": nama_makanan,
            "merchant_kategori_makanan_id": merchant_kategori,
            "deskripsi": deskripsi,
            "harga_asli": harga_asli,
            "harga_jual": harga_jual,
            "is_non_halal": "0",
            "weight_string": weight_string
        }
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json"
        }
        response = requests.post(url_getall_menu + str(menu) + '?_method=PUT', data=param2, headers=headers, files={
            'images[0]': open("img/ms1.jpeg", 'rb'),
            'images[1]': open("img/ms2.jpg", 'rb'),
        })
        data = response.json()

        validate_status = data.get("success")
        validate_message = data.get("message")["nama_menu_makanan"]

        assert response.status_code == 422
        assert validate_status == bool(False)
        assert "Nama menu tidak boleh kosong." in validate_message

    def test_update_menu_without_param_nama_menu_makanan(self):
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
        get_all = requests.get(url_getall_menu, headers=headers)
        menu = get_all.json().get('data')[0]['id']

        nama_makanan = "sosis"
        merchant_kategori = 1
        deskripsi = "Mie Setan Kuy"
        harga_asli = 25000
        harga_jual = 5000
        status_halal = 0
        weight_string = "200 Kotak"
        param2 = {
            # "nama_menu_makanan": nama_makanan,
            "merchant_kategori_makanan_id": merchant_kategori,
            "deskripsi": deskripsi,
            "harga_asli": harga_asli,
            "harga_jual": harga_jual,
            "is_non_halal": "0",
            "weight_string": weight_string
        }
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json"
        }
        response = requests.post(url_getall_menu + str(menu) + '?_method=PUT', data=param2, headers=headers, files={
            'images[0]': open("img/ms1.jpeg", 'rb'),
            'images[1]': open("img/ms2.jpg", 'rb'),
        })
        data = response.json()

        validate_status = data.get("success")
        validate_message = data.get("message")["nama_menu_makanan"]

        assert response.status_code == 422
        assert validate_status == bool(False)
        assert "Nama menu tidak boleh kosong." in validate_message

    def test_update_menu_kategori_makanan_id_wrong_value(self):
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
        get_all = requests.get(url_getall_menu, headers=headers)
        menu = get_all.json().get('data')[0]['id']

        nama_makanan = "sosis"
        merchant_kategori = 100
        deskripsi = "Mie Setan Kuy"
        harga_asli = 25000
        harga_jual = 5000
        status_halal = 0
        weight_string = "200 Kotak"
        param2 = {
            "nama_menu_makanan": nama_makanan,
            "merchant_kategori_makanan_id": merchant_kategori,
            "deskripsi": deskripsi,
            "harga_asli": harga_asli,
            "harga_jual": harga_jual,
            "is_non_halal": "0",
            "weight_string": weight_string
        }
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json"
        }
        response = requests.post(url_getall_menu + str(menu) + '?_method=PUT', data=param2, headers=headers, files={
            'images[0]': open("img/ms1.jpeg", 'rb'),
            'images[1]': open("img/ms2.jpg", 'rb'),
        })
        data = response.json()

        validate_status = data.get("success")
        validate_message = data.get("message")

        assert response.status_code == 404
        assert validate_status == bool(False)
        assert "Data gagal dibuat." in validate_message

    def test_update_menu_kategori_makanan_id_empty(self):
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
        get_all = requests.get(url_getall_menu, headers=headers)
        menu = get_all.json().get('data')[0]['id']

        nama_makanan = "sosis"
        merchant_kategori = ""
        deskripsi = "Mie Setan Kuy"
        harga_asli = 25000
        harga_jual = 5000
        status_halal = 0
        weight_string = "200 Kotak"
        param2 = {
            "nama_menu_makanan": nama_makanan,
            "merchant_kategori_makanan_id": merchant_kategori,
            "deskripsi": deskripsi,
            "harga_asli": harga_asli,
            "harga_jual": harga_jual,
            "is_non_halal": "0",
            "weight_string": weight_string
        }
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json"
        }
        response = requests.post(url_getall_menu + str(menu) + '?_method=PUT', data=param2, headers=headers, files={
            'images[0]': open("img/ms1.jpeg", 'rb'),
            'images[1]': open("img/ms2.jpg", 'rb'),
        })
        data = response.json()

        validate_status = data.get("success")
        validate_message = data.get("message")["merchant_kategori_makanan_id"]

        assert response.status_code == 422
        assert validate_status == bool(False)
        assert "Kategori menu tidak boleh kosong." in validate_message

    def test_update_menu_without_param_kategori_makanan_id(self):
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
        get_all = requests.get(url_getall_menu, headers=headers)
        menu = get_all.json().get('data')[0]['id']

        nama_makanan = "sosis"
        merchant_kategori = 1
        deskripsi = "Mie Setan Kuy"
        harga_asli = 25000
        harga_jual = 5000
        status_halal = 0
        weight_string = "200 Kotak"
        param2 = {
            "nama_menu_makanan": nama_makanan,
            # "merchant_kategori_makanan_id": merchant_kategori,
            "deskripsi": deskripsi,
            "harga_asli": harga_asli,
            "harga_jual": harga_jual,
            "is_non_halal": "0",
            "weight_string": weight_string
        }
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json"
        }
        response = requests.post(url_getall_menu + str(menu) + '?_method=PUT', data=param2, headers=headers, files={
            'images[0]': open("img/ms1.jpeg", 'rb'),
            'images[1]': open("img/ms2.jpg", 'rb'),
        })
        data = response.json()

        validate_status = data.get("success")
        validate_message = data.get("message")["merchant_kategori_makanan_id"]

        assert response.status_code == 422
        assert validate_status == bool(False)
        assert "Kategori menu tidak boleh kosong." in validate_message

    def test_update_menu_deskripsi_empty(self):
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
        get_all = requests.get(url_getall_menu, headers=headers)
        menu = get_all.json().get('data')[0]['id']

        nama_makanan = "sosis"
        merchant_kategori = 1
        deskripsi = ""
        harga_asli = 25000
        harga_jual = 5000
        status_halal = 0
        weight_string = "200 Kotak"
        param2 = {
            "nama_menu_makanan": nama_makanan,
            "merchant_kategori_makanan_id": merchant_kategori,
            "deskripsi": deskripsi,
            "harga_asli": harga_asli,
            "harga_jual": harga_jual,
            "is_non_halal": "0",
            "weight_string": weight_string
        }
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json"
        }
        response = requests.post(url_getall_menu + str(menu) + '?_method=PUT', data=param2, headers=headers, files={
            'images[0]': open("img/ms1.jpeg", 'rb'),
            'images[1]': open("img/ms2.jpg", 'rb'),
        })
        data = response.json()

        validate_status = data.get("success")
        validate_message = data.get("message")["deskripsi"]

        assert response.status_code == 422
        assert validate_status == bool(False)
        assert "deskripsi tidak boleh kosong." in validate_message

    def test_Update_menu_without_param_deskripsi(self):
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
        get_all = requests.get(url_getall_menu, headers=headers)
        menu = get_all.json().get('data')[0]['id']

        nama_makanan = "sosis"
        merchant_kategori = 1
        deskripsi = "sosis ayam"
        harga_asli = 25000
        harga_jual = 5000
        status_halal = 0
        weight_string = "200 Kotak"
        param2 = {
            "nama_menu_makanan": nama_makanan,
            "merchant_kategori_makanan_id": merchant_kategori,
            # "deskripsi": deskripsi,
            "harga_asli": harga_asli,
            "harga_jual": harga_jual,
            "is_non_halal": "0",
            "weight_string": weight_string
        }
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json"
        }
        response = requests.post(url_getall_menu + str(menu) + '?_method=PUT', data=param2, headers=headers, files={
            'images[0]': open("img/ms1.jpeg", 'rb'),
            'images[1]': open("img/ms2.jpg", 'rb'),
        })
        data = response.json()

        validate_status = data.get("success")
        validate_message = data.get("message")["deskripsi"]

        assert response.status_code == 422
        assert validate_status == bool(False)
        assert "deskripsi tidak boleh kosong." in validate_message

    def test_update_menu_harga_asli_empty(self):
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
        get_all = requests.get(url_getall_menu, headers=headers)
        menu = get_all.json().get('data')[0]['id']

        nama_makanan = "sosis"
        merchant_kategori = 1
        deskripsi = "sosis ayam"
        harga_asli = ""
        harga_jual = 5000
        status_halal = 0
        weight_string = "200 Kotak"
        param2 = {
            "nama_menu_makanan": nama_makanan,
            "merchant_kategori_makanan_id": merchant_kategori,
            "deskripsi": deskripsi,
            "harga_asli": harga_asli,
            "harga_jual": harga_jual,
            "is_non_halal": "0",
            "weight_string": weight_string
        }
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json"
        }
        response = requests.post(url_getall_menu + str(menu) + '?_method=PUT', data=param2, headers=headers, files={
            'images[0]': open("img/ms1.jpeg", 'rb'),
            'images[1]': open("img/ms2.jpg", 'rb'),
        })
        data = response.json()

        validate_status = data.get("success")
        validate_message = data.get("message")["harga_asli"]

        assert response.status_code == 422
        assert validate_status == bool(False)
        assert "Harga asli tidak boleh kosong." in validate_message

    def test_update_menu_without_param_harga_asli(self):
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
        get_all = requests.get(url_getall_menu, headers=headers)
        menu = get_all.json().get('data')[0]['id']

        nama_makanan = "sosis"
        merchant_kategori = 1
        deskripsi = "sosis ayam"
        harga_asli = 20000
        harga_jual = 5000
        status_halal = 0
        weight_string = "200 Kotak"
        param2 = {
            "nama_menu_makanan": nama_makanan,
            "merchant_kategori_makanan_id": merchant_kategori,
            "deskripsi": deskripsi,
            # "harga_asli": harga_asli,
            "harga_jual": harga_jual,
            "is_non_halal": "0",
            "weight_string": weight_string
        }
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json"
        }
        response = requests.post(url_getall_menu + str(menu) + '?_method=PUT', data=param2, headers=headers, files={
            'images[0]': open("img/ms1.jpeg", 'rb'),
            'images[1]': open("img/ms2.jpg", 'rb'),
        })
        data = response.json()

        validate_status = data.get("success")
        validate_message = data.get("message")["harga_asli"]

        assert response.status_code == 422
        assert validate_status == bool(False)
        assert "Harga asli tidak boleh kosong." in validate_message

    def test_update_menu_harga_asli_string_value(self):
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
        get_all = requests.get(url_getall_menu, headers=headers)
        menu = get_all.json().get('data')[0]['id']

        nama_makanan = "sosis"
        merchant_kategori = 1
        deskripsi = "sosis ayam"
        harga_asli = "aa"
        harga_jual = 5000
        status_halal = 0
        weight_string = "200 Kotak"
        param2 = {
            "nama_menu_makanan": nama_makanan,
            "merchant_kategori_makanan_id": merchant_kategori,
            "deskripsi": deskripsi,
            "harga_asli": harga_asli,
            "harga_jual": harga_jual,
            "is_non_halal": "0",
            "weight_string": weight_string
        }
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json"
        }
        response = requests.post(url_getall_menu + str(menu) + '?_method=PUT', data=param2, headers=headers, files={
            'images[0]': open("img/ms1.jpeg", 'rb'),
            'images[1]': open("img/ms2.jpg", 'rb'),
        })
        data = response.json()

        validate_status = data.get("success")
        validate_message = data.get("message")["harga_asli"]

        assert response.status_code == 422
        assert validate_status == bool(False)
        assert "format harga asli yang diinputkan salah" in validate_message

    def test_update_menu_harga_jual_empty(self):
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
        get_all = requests.get(url_getall_menu, headers=headers)
        menu = get_all.json().get('data')[0]['id']

        nama_makanan = "sosis"
        merchant_kategori = 1
        deskripsi = "sosis ayam"
        harga_asli = 20000
        harga_jual = ""
        status_halal = 0
        weight_string = "200 Kotak"
        param2 = {
            "nama_menu_makanan": nama_makanan,
            "merchant_kategori_makanan_id": merchant_kategori,
            "deskripsi": deskripsi,
            "harga_asli": harga_asli,
            "harga_jual": harga_jual,
            "is_non_halal": "0",
            "weight_string": weight_string
        }
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json"
        }
        response = requests.post(url_getall_menu + str(menu) + '?_method=PUT', data=param2, headers=headers, files={
            'images[0]': open("img/ms1.jpeg", 'rb'),
            'images[1]': open("img/ms2.jpg", 'rb'),
        })
        data = response.json()

        validate_status = data.get("success")
        validate_message = data.get("message")["harga_jual"]

        assert response.status_code == 422
        assert validate_status == bool(False)
        assert "Harga jual tidak boleh kosong." in validate_message

    def test_update_menu_without_param_harga_jual(self):
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
        get_all = requests.get(url_getall_menu, headers=headers)
        menu = get_all.json().get('data')[0]['id']

        nama_makanan = "sosis"
        merchant_kategori = 1
        deskripsi = "sosis ayam"
        harga_asli = 20000
        harga_jual = 5000
        status_halal = 0
        weight_string = "200 Kotak"
        param2 = {
            "nama_menu_makanan": nama_makanan,
            "merchant_kategori_makanan_id": merchant_kategori,
            "deskripsi": deskripsi,
            "harga_asli": harga_asli,
            # "harga_jual": harga_jual,
            "is_non_halal": "0",
            "weight_string": weight_string
        }
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json"
        }
        response = requests.post(url_getall_menu + str(menu) + '?_method=PUT', data=param2, headers=headers, files={
            'images[0]': open("img/ms1.jpeg", 'rb'),
            'images[1]': open("img/ms2.jpg", 'rb'),
        })
        data = response.json()

        validate_status = data.get("success")
        validate_message = data.get("message")["harga_jual"]

        assert response.status_code == 422
        assert validate_status == bool(False)
        assert "Harga jual tidak boleh kosong." in validate_message

    def test_update_menu_harga_jual_string_value(self):
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
        get_all = requests.get(url_getall_menu, headers=headers)
        menu = get_all.json().get('data')[0]['id']

        nama_makanan = "sosis"
        merchant_kategori = 1
        deskripsi = "sosis ayam"
        harga_asli = 5000
        harga_jual = 'aaa'
        status_halal = 0
        weight_string = "200 Kotak"
        param2 = {
            "nama_menu_makanan": nama_makanan,
            "merchant_kategori_makanan_id": merchant_kategori,
            "deskripsi": deskripsi,
            "harga_asli": harga_asli,
            "harga_jual": harga_jual,
            "is_non_halal": "0",
            "weight_string": weight_string
        }
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json"
        }
        response = requests.post(url_getall_menu + str(menu) + '?_method=PUT', data=param2, headers=headers, files={
            'images[0]': open("img/ms1.jpeg", 'rb'),
            'images[1]': open("img/ms2.jpg", 'rb'),
        })
        data = response.json()

        validate_status = data.get("success")
        validate_message = data.get("message")["harga_jual"]

        assert response.status_code == 422
        assert validate_status == bool(False)
        assert "format harga jual yang diinputkan salah" in validate_message

    def test_update_menu_is_non_halal_empty(self):
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
        get_all = requests.get(url_getall_menu, headers=headers)
        menu = get_all.json().get('data')[0]['id']

        nama_makanan = "sosis"
        merchant_kategori = 1
        deskripsi = "sosis ayam"
        harga_asli = 5000
        harga_jual = 1000
        status_halal = ''
        weight_string = "200 Kotak"
        param2 = {
            "nama_menu_makanan": nama_makanan,
            "merchant_kategori_makanan_id": merchant_kategori,
            "deskripsi": deskripsi,
            "harga_asli": harga_asli,
            "harga_jual": harga_jual,
            "is_non_halal": status_halal,
            "weight_string": weight_string
        }
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json"
        }
        response = requests.post(url_getall_menu + str(menu) + '?_method=PUT', data=param2, headers=headers, files={
            'images[0]': open("img/ms1.jpeg", 'rb'),
            'images[1]': open("img/ms2.jpg", 'rb'),
        })
        data = response.json()

        validate_status = data.get("success")
        validate_message = data.get("message")["is_non_halal"]

        assert response.status_code == 422
        assert validate_status == bool(False)
        assert "Menu tidak halal tidak boleh kosong." in validate_message

    def test_update_menu_without_param_is_non_halal(self):
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
        get_all = requests.get(url_getall_menu, headers=headers)
        menu = get_all.json().get('data')[0]['id']

        nama_makanan = "sosis"
        merchant_kategori = 1
        deskripsi = "sosis ayam"
        harga_asli = 5000
        harga_jual = 1000
        status_halal = 0
        weight_string = "200 Kotak"
        param2 = {
            "nama_menu_makanan": nama_makanan,
            "merchant_kategori_makanan_id": merchant_kategori,
            "deskripsi": deskripsi,
            "harga_asli": harga_asli,
            "harga_jual": harga_jual,
            # "is_non_halal": status_halal,
            "weight_string": weight_string
        }
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json"
        }
        response = requests.post(url_getall_menu + str(menu) + '?_method=PUT', data=param2, headers=headers, files={
            'images[0]': open("img/ms1.jpeg", 'rb'),
            'images[1]': open("img/ms2.jpg", 'rb'),
        })
        data = response.json()

        validate_status = data.get("success")
        validate_message = data.get("message")["is_non_halal"]

        assert response.status_code == 422
        assert validate_status == bool(False)
        assert "Menu tidak halal tidak boleh kosong." in validate_message

    def test_update_menu_is_non_halal_wrong_value(self):
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
        get_all = requests.get(url_getall_menu, headers=headers)
        menu = get_all.json().get('data')[0]['id']

        nama_makanan = "sosis"
        merchant_kategori = 1
        deskripsi = "sosis ayam"
        harga_asli = 5000
        harga_jual = 1000
        status_halal = 'aaa'
        weight_string = "200 Kotak"
        param2 = {
            "nama_menu_makanan": nama_makanan,
            "merchant_kategori_makanan_id": merchant_kategori,
            "deskripsi": deskripsi,
            "harga_asli": harga_asli,
            "harga_jual": harga_jual,
            "is_non_halal": status_halal,
            "weight_string": weight_string
        }
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json"
        }
        response = requests.post(url_getall_menu + str(menu) + '?_method=PUT', data=param2, headers=headers, files={
            'images[0]': open("img/ms1.jpeg", 'rb'),
            'images[1]': open("img/ms2.jpg", 'rb'),
        })
        data = response.json()

        validate_status = data.get("success")
        validate_message = data.get("message")["is_non_halal"]

        assert response.status_code == 422
        assert validate_status == bool(False)
        assert "Menu tidak halal harus bernilai true atau false." in validate_message

    def test_update_menu_use_1_images(self):
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
        get_all = requests.get(url_getall_menu, headers=headers)
        menu = get_all.json().get('data')[0]['id']

        nama_makanan = "sosis"
        merchant_kategori = 1
        deskripsi = "sosis ayam"
        harga_asli = 5000
        harga_jual = 1000
        status_halal = 0
        weight_string = "200 Kotak"
        param2 = {
            "nama_menu_makanan": nama_makanan,
            "merchant_kategori_makanan_id": merchant_kategori,
            "deskripsi": deskripsi,
            "harga_asli": harga_asli,
            "harga_jual": harga_jual,
            "is_non_halal": status_halal,
            "weight_string": weight_string
        }
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json"
        }
        response = requests.post(url_getall_menu + str(menu) + '?_method=PUT', data=param2, headers=headers, files={
            'images[0]': open("img/ms1.jpeg", 'rb'),
        })
        data = response.json()

        validate_status = data.get("success")
        validate_message = data.get("message")

        assert response.status_code == 200
        assert validate_status == bool(True)
        assert f"Data menu {nama_makanan} berhasil diperbarui." in validate_message

    def test_update_menu_use_2_images(self):
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
        get_all = requests.get(url_getall_menu, headers=headers)
        menu = get_all.json().get('data')[0]['id']

        nama_makanan = "sosis"
        merchant_kategori = 1
        deskripsi = "sosis ayam"
        harga_asli = 5000
        harga_jual = 1000
        status_halal = 0
        weight_string = "200 Kotak"
        param2 = {
            "nama_menu_makanan": nama_makanan,
            "merchant_kategori_makanan_id": merchant_kategori,
            "deskripsi": deskripsi,
            "harga_asli": harga_asli,
            "harga_jual": harga_jual,
            "is_non_halal": status_halal,
            "weight_string": weight_string
        }
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json"
        }
        response = requests.post(url_getall_menu + str(menu) + '?_method=PUT', data=param2, headers=headers, files={
            'images[0]': open("img/ms1.jpeg", 'rb'),
            'images[1]': open("img/ms1.jpeg", 'rb'),
        })
        data = response.json()

        validate_status = data.get("success")
        validate_message = data.get("message")

        assert response.status_code == 200
        assert validate_status == bool(True)
        assert f"Data menu {nama_makanan} berhasil diperbarui." in validate_message

    def test_update_menu_use_3_images(self):
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
        get_all = requests.get(url_getall_menu, headers=headers)
        menu = get_all.json().get('data')[0]['id']

        nama_makanan = "sosis"
        merchant_kategori = 1
        deskripsi = "sosis ayam"
        harga_asli = 5000
        harga_jual = 1000
        status_halal = 0
        weight_string = "200 Kotak"
        param2 = {
            "nama_menu_makanan": nama_makanan,
            "merchant_kategori_makanan_id": merchant_kategori,
            "deskripsi": deskripsi,
            "harga_asli": harga_asli,
            "harga_jual": harga_jual,
            "is_non_halal": status_halal,
            "weight_string": weight_string
        }
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json"
        }
        response = requests.post(url_getall_menu + str(menu) + '?_method=PUT', data=param2, headers=headers, files={
            'images[0]': open("img/ms1.jpeg", 'rb'),
            'images[1]': open("img/ms1.jpeg", 'rb'),
            'images[2]': open("img/ms1.jpeg", 'rb'),
        })
        data = response.json()

        validate_status = data.get("success")
        validate_message = data.get("message")

        assert response.status_code == 200
        assert validate_status == bool(True)
        assert f"Data menu {nama_makanan} berhasil diperbarui." in validate_message

    def test_update_menu_sayur_without_param_weight(self):
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
        get_all = requests.get(url_getall_menu, headers=headers)
        menu = get_all.json().get('data')[0]['id']

        nama_makanan = "sosis"
        merchant_kategori = 5
        deskripsi = "sosis ayam"
        harga_asli = 5000
        harga_jual = 1000
        status_halal = 0
        weight_string = "200 Kotak"
        param2 = {
            "nama_menu_makanan": nama_makanan,
            "merchant_kategori_makanan_id": merchant_kategori,
            "deskripsi": deskripsi,
            "harga_asli": harga_asli,
            "harga_jual": harga_jual,
            "is_non_halal": status_halal,
            "weight_string": weight_string
        }
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json"
        }
        response = requests.post(url_getall_menu + str(menu) + '?_method=PUT', data=param2, headers=headers, files={
            'images[0]': open("img/ms1.jpeg", 'rb'),
        })
        data = response.json()

        validate_status = data.get("success")
        validate_message = data.get("message")['weight']

        assert response.status_code == 422
        assert validate_status == bool(False)
        assert "weight tidak boleh kosong ketika Kategori menu adalah 5." in validate_message

    def test_update_menu_sayur_weight_sting_value(self):
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
        get_all = requests.get(url_getall_menu, headers=headers)
        menu = get_all.json().get('data')[0]['id']

        nama_makanan = "sosis"
        merchant_kategori = 5
        deskripsi = "sosis ayam"
        harga_asli = 5000
        harga_jual = 1000
        status_halal = 0
        weight_string = "200 Kotak"
        param2 = {
            "nama_menu_makanan": nama_makanan,
            "merchant_kategori_makanan_id": merchant_kategori,
            "deskripsi": deskripsi,
            "harga_asli": harga_asli,
            "harga_jual": harga_jual,
            "is_non_halal": status_halal,
            "weight": weight_string
        }
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json"
        }
        response = requests.post(url_getall_menu + str(menu) + '?_method=PUT', data=param2, headers=headers, files={
            'images[0]': open("img/ms1.jpeg", 'rb'),
        })
        data = response.json()

        validate_status = data.get("success")
        validate_message = data.get("message")['weight']

        assert response.status_code == 422
        assert validate_status == bool(False)
        assert "weight harus berupa angka." in validate_message

    def test_update_menu_sayur_wight_empty_value(self):
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
        get_all = requests.get(url_getall_menu, headers=headers)
        menu = get_all.json().get('data')[0]['id']

        nama_makanan = "sosis"
        merchant_kategori = 5
        deskripsi = "sosis ayam"
        harga_asli = 5000
        harga_jual = 1000
        status_halal = 0
        weight_string = ""
        param2 = {
            "nama_menu_makanan": nama_makanan,
            "merchant_kategori_makanan_id": merchant_kategori,
            "deskripsi": deskripsi,
            "harga_asli": harga_asli,
            "harga_jual": harga_jual,
            "is_non_halal": status_halal,
            "weight": weight_string
        }
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json"
        }
        response = requests.post(url_getall_menu + str(menu) + '?_method=PUT', data=param2, headers=headers, files={
            'images[0]': open("img/ms1.jpeg", 'rb'),
        })
        data = response.json()

        validate_status = data.get("success")
        validate_message = data.get("message")['weight']

        assert response.status_code == 422
        assert validate_status == bool(False)
        assert "weight tidak boleh kosong ketika Kategori menu adalah 5." in validate_message

    def test_update_menu_non_sayur_without_param_weight_string(self):
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
        get_all = requests.get(url_getall_menu, headers=headers)
        menu = get_all.json().get('data')[0]['id']

        nama_makanan = "sosis"
        merchant_kategori = 1
        deskripsi = "sosis ayam"
        harga_asli = 5000
        harga_jual = 1000
        status_halal = 0
        weight_string = 200
        param2 = {
            "nama_menu_makanan": nama_makanan,
            "merchant_kategori_makanan_id": merchant_kategori,
            "deskripsi": deskripsi,
            "harga_asli": harga_asli,
            "harga_jual": harga_jual,
            "is_non_halal": status_halal,
            "weight": weight_string
        }
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json"
        }
        response = requests.post(url_getall_menu + str(menu) + '?_method=PUT', data=param2, headers=headers, files={
            'images[0]': open("img/ms1.jpeg", 'rb'),
        })
        data = response.json()

        validate_status = data.get("success")
        validate_message = data.get("message")["weight_string"]

        assert response.status_code == 422
        assert validate_status == bool(False)
        assert "weight string tidak boleh kosong kecuali Kategori menu ada dalam 5." in validate_message

    def test_update_menu_non_sayur_weight_string_number_value(self):
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
        get_all = requests.get(url_getall_menu, headers=headers)
        menu = get_all.json().get('data')[0]['id']

        nama_makanan = "sosis"
        merchant_kategori = 1
        deskripsi = "sosis ayam"
        harga_asli = 5000
        harga_jual = 1000
        status_halal = 0
        weight_string = 200
        param2 = {
            "nama_menu_makanan": nama_makanan,
            "merchant_kategori_makanan_id": merchant_kategori,
            "deskripsi": deskripsi,
            "harga_asli": harga_asli,
            "harga_jual": harga_jual,
            "is_non_halal": status_halal,
            "weight_string": weight_string
        }
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json"
        }
        response = requests.post(url_getall_menu + str(menu) + '?_method=PUT', data=param2, headers=headers, files={
            'images[0]': open("img/ms1.jpeg", 'rb'),
        })
        data = response.json()

        validate_status = data.get("success")
        validate_message = data.get("message")

        assert response.status_code == 200
        assert validate_status == bool(True)
        assert f"Data menu {nama_makanan} berhasil diperbarui." in validate_message

    def test_update_menu_non_sayur_wight_string_empty_value(self):
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
        get_all = requests.get(url_getall_menu, headers=headers)
        menu = get_all.json().get('data')[0]['id']

        nama_makanan = "sosis"
        merchant_kategori = 1
        deskripsi = "sosis ayam"
        harga_asli = 5000
        harga_jual = 1000
        status_halal = 0
        weight_string = ''
        param2 = {
            "nama_menu_makanan": nama_makanan,
            "merchant_kategori_makanan_id": merchant_kategori,
            "deskripsi": deskripsi,
            "harga_asli": harga_asli,
            "harga_jual": harga_jual,
            "is_non_halal": status_halal,
            "weight_string": weight_string
        }
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json"
        }
        response = requests.post(url_getall_menu + str(menu) + '?_method=PUT', data=param2, headers=headers, files={
            'images[0]': open("img/ms1.jpeg", 'rb'),
        })
        data = response.json()

        validate_status = data.get("success")
        validate_message = data.get("message")["weight_string"]

        assert response.status_code == 422
        assert validate_status == bool(False)
        assert "weight string tidak boleh kosong kecuali Kategori menu ada dalam 5." in validate_message
