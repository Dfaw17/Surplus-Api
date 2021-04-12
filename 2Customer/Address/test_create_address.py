import requests
from env import stagging
from pprint import pprint
from assertpy import assert_that

class TestCustomerCreateAddress:

    global setting_env,url_login,url_create_address,email,kata_sandi,wrong_token

    setting_env = stagging
    url_login = f"{setting_env}/api/v2/customer/auth/login/email"
    url_create_address = f"{setting_env}/api/v2/customer/address"
    email = "kopiruangvirtual@gmail.com"
    kata_sandi = '12345678'
    wrong_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvc3RhZ2luZy5hZG1pbnN1cnBsdXMubmV0XC9hcGlcL3YyXC9jdXN0b21lclwvYXV0aFwvbG9naW5cL2VtYWlsIiwiaWF0IjoxNjE2ODA1NzI2LCJleHAiOjE2MTkzOTc3MjYsIm5iZiI6MTYxNjgwNTcyNiwianRpIjoib05ESmxFRE5hSzNrN2RtVyIsInN1YiI6NDEyNiwicHJ2IjoiMjc0MTA1ZGE2ZTk1YmVmMjgwNzc4NmRkODczODg2N2NmOWMwMmFhYiJ9.fj51xIfQrqleRvdSJUbWcdrvsxQPUn8HpccnOmTgPDI'

    def test_create_address_normal(self):
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
            "latitude": "-6.3823317",
            "longitude": "107.1162607",
            "receiver_name": "Fawwa",
            "phone": "081386356616",
            "address": "Fawwa Home",
            "category": "Rumah",
            "title": "Fawwa Home",
            "note": "Fawwa Home 1"
        }
        create = requests.post(url_create_address, params=param2, headers=headers2)

        validate_status = create.json().get('success')
        validate_message = create.json().get('message')
        validate_data = create.json().get('data')
        validate_data_id = create.json().get('data')['id']
        validate_data_user_id = create.json().get('data')['user_id']
        validate_data_address_latitude = create.json().get('data')['address_latitude']
        validate_data_address_longitude = create.json().get('data')['address_longitude']
        validate_data_receiver = create.json().get('data')['receiver']
        validate_data_phone = create.json().get('data')['phone']
        validate_data_address = create.json().get('data')['address']
        validate_data_kategori = create.json().get('data')['kategori']
        validate_data_title = create.json().get('data')['title']
        validate_data_note = create.json().get('data')['note']

        assert create.status_code == 201
        assert validate_status == bool(True)
        assert 'Data alamat berhasil dibuat' in validate_message
        assert_that(validate_data).contains_only('id', 'user_id', 'address_latitude', 'address_longitude', 'receiver',
                                                 'phone',
                                                 'address', 'kategori', 'title', 'note')
        assert_that(validate_data_id).is_not_none()
        assert_that(validate_data_user_id).is_not_none()
        assert validate_data_address_latitude == -6.3823317
        assert validate_data_address_longitude == 107.1162607
        assert validate_data_receiver == 'Fawwa'
        assert validate_data_phone == '081386356616'
        assert validate_data_address == 'Fawwa Home'
        assert validate_data_kategori == 'Rumah'
        assert validate_data_title == 'Fawwa Home'
        assert validate_data_note == 'Fawwa Home 1'

    def test_create_address_wrong_token(self):
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
            "latitude": "-6.3823317",
            "longitude": "107.1162607",
            "receiver_name": "Fawwa",
            "phone": "081386356616",
            "address": "Fawwa Home",
            "category": "Rumah",
            "title": "Fawwa Home",
            "note": "Fawwa Home 1"
        }
        create = requests.post(url_create_address, params=param2, headers=headers2)

        validate_status = create.json().get('success')
        validate_message = create.json().get('message')

        assert create.status_code == 401
        assert validate_status == bool(False)
        assert 'Unauthorized' in validate_message

    def test_create_address_token_empty_value(self):
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
            "latitude": "-6.3823317",
            "longitude": "107.1162607",
            "receiver_name": "Fawwa",
            "phone": "081386356616",
            "address": "Fawwa Home",
            "category": "Rumah",
            "title": "Fawwa Home",
            "note": "Fawwa Home 1"
        }
        create = requests.post(url_create_address, params=param2, headers=headers2)

        validate_status = create.json().get('success')
        validate_message = create.json().get('message')

        assert create.status_code == 401
        assert validate_status == bool(False)
        assert 'Unauthorized' in validate_message

    def test_create_address_latitude_empty_value(self):
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
            "latitude": "",
            "longitude": "107.1162607",
            "receiver_name": "Fawwa",
            "phone": "081386356616",
            "address": "Fawwa Home",
            "category": "Rumah",
            "title": "Fawwa Home",
            "note": "Fawwa Home 1"
        }
        create = requests.post(url_create_address, params=param2, headers=headers2)

        validate_status = create.json().get('success')
        validate_message = create.json().get('message')['latitude']

        assert create.status_code == 422
        assert validate_status == bool(False)
        assert 'latitude tidak boleh kosong.' in validate_message

    def test_create_address_latitude_text_value(self):
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
            "latitude": "aaaaa",
            "longitude": "107.1162607",
            "receiver_name": "Fawwa",
            "phone": "081386356616",
            "address": "Fawwa Home",
            "category": "Rumah",
            "title": "Fawwa Home",
            "note": "Fawwa Home 1"
        }
        create = requests.post(url_create_address, params=param2, headers=headers2)

        validate_status = create.json().get('success')
        validate_message = create.json().get('message')

        assert create.status_code == 500
        assert validate_status == bool(False)
        assert 'Aduh!' in validate_message

    def test_create_address_without_param_latitude(self):
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
            # "latitude": "aaaaa",
            "longitude": "107.1162607",
            "receiver_name": "Fawwa",
            "phone": "081386356616",
            "address": "Fawwa Home",
            "category": "Rumah",
            "title": "Fawwa Home",
            "note": "Fawwa Home 1"
        }
        create = requests.post(url_create_address, params=param2, headers=headers2)

        validate_status = create.json().get('success')
        validate_message = create.json().get('message')['latitude']

        assert create.status_code == 422
        assert validate_status == bool(False)
        assert 'latitude tidak boleh kosong.' in validate_message

    def test_create_address_longitude_empty_value(self):
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
            "latitude": "-6.3823317",
            "longitude": "",
            "receiver_name": "Fawwa",
            "phone": "081386356616",
            "address": "Fawwa Home",
            "category": "Rumah",
            "title": "Fawwa Home",
            "note": "Fawwa Home 1"
        }
        create = requests.post(url_create_address, params=param2, headers=headers2)

        validate_status = create.json().get('success')
        validate_message = create.json().get('message')['longitude']

        assert create.status_code == 422
        assert validate_status == bool(False)
        assert 'longitude tidak boleh kosong.' in validate_message

    def test_create_address_longitude_text_value(self):
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
            "latitude": "-6.3823317",
            "longitude": "aaa",
            "receiver_name": "Fawwa",
            "phone": "081386356616",
            "address": "Fawwa Home",
            "category": "Rumah",
            "title": "Fawwa Home",
            "note": "Fawwa Home 1"
        }
        create = requests.post(url_create_address, params=param2, headers=headers2)

        validate_status = create.json().get('success')
        validate_message = create.json().get('message')

        assert create.status_code == 500
        assert validate_status == bool(False)
        assert 'Aduh!' in validate_message

    def test_create_address_without_param_longitude(self):
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
            "latitude": "-6.3823317",
            # "longitude": "aaa",
            "receiver_name": "Fawwa",
            "phone": "081386356616",
            "address": "Fawwa Home",
            "category": "Rumah",
            "title": "Fawwa Home",
            "note": "Fawwa Home 1"
        }
        create = requests.post(url_create_address, params=param2, headers=headers2)

        validate_status = create.json().get('success')
        validate_message = create.json().get('message')['longitude']

        assert create.status_code == 422
        assert validate_status == bool(False)
        assert 'longitude tidak boleh kosong.' in validate_message

    def test_create_address_receiver_name_empty_value(self):
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
            "latitude": "-6.3823317",
            "longitude": "107.1162607",
            "receiver_name": "",
            "phone": "081386356616",
            "address": "Fawwa Home",
            "category": "Rumah",
            "title": "Fawwa Home",
            "note": "Fawwa Home 1"
        }
        create = requests.post(url_create_address, params=param2, headers=headers2)

        validate_status = create.json().get('success')
        validate_message = create.json().get('message')['receiver_name']

        assert create.status_code == 422
        assert validate_status == bool(False)
        assert 'Nama penerima tidak boleh kosong.' in validate_message

    def test_create_address_receiver_name_number_value(self):
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
            "latitude": "-6.3823317",
            "longitude": "107.1162607",
            "receiver_name": "1122334455",
            "phone": "081386356616",
            "address": "Fawwa Home",
            "category": "Rumah",
            "title": "Fawwa Home",
            "note": "Fawwa Home 1"
        }
        create = requests.post(url_create_address, params=param2, headers=headers2)

        validate_status = create.json().get('success')
        validate_message = create.json().get('message')

        assert create.status_code == 201
        assert validate_status == bool(True)
        assert 'Data alamat berhasil dibuat' in validate_message

    def test_create_address_without_param_receiver_name(self):
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
            "latitude": "-6.3823317",
            "longitude": "107.1162607",
            # "receiver_name": "fawwa",
            "phone": "081386356616",
            "address": "Fawwa Home",
            "category": "Rumah",
            "title": "Fawwa Home",
            "note": "Fawwa Home 1"
        }
        create = requests.post(url_create_address, params=param2, headers=headers2)

        validate_status = create.json().get('success')
        validate_message = create.json().get('message')['receiver_name']

        assert create.status_code == 422
        assert validate_status == bool(False)
        assert 'Nama penerima tidak boleh kosong.' in validate_message

    def test_create_address_phone_empty_value(self):
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
            "latitude": "-6.3823317",
            "longitude": "107.1162607",
            "receiver_name": "fawwa",
            "phone": "",
            "address": "Fawwa Home",
            "category": "Rumah",
            "title": "Fawwa Home",
            "note": "Fawwa Home 1"
        }
        create = requests.post(url_create_address, params=param2, headers=headers2)

        validate_status = create.json().get('success')
        validate_message = create.json().get('message')['phone']

        assert create.status_code == 422
        assert validate_status == bool(False)
        assert 'No. HP tidak boleh kosong.' in validate_message

    def test_create_address_phone_text_value(self):
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
            "latitude": "-6.3823317",
            "longitude": "107.1162607",
            "receiver_name": "fawwa",
            "phone": "aaaaaaaaaaaa",
            "address": "Fawwa Home",
            "category": "Rumah",
            "title": "Fawwa Home",
            "note": "Fawwa Home 1"
        }
        create = requests.post(url_create_address, params=param2, headers=headers2)

        validate_status = create.json().get('success')
        validate_message = create.json().get('message')

        assert create.status_code == 201
        assert validate_status == bool(True)
        assert 'Data alamat berhasil dibuat' in validate_message

    def test_create_address_without_param_phone(self):
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
            "latitude": "-6.3823317",
            "longitude": "107.1162607",
            "receiver_name": "fawwa",
            # "phone": "aaaaaaaaaaaa",
            "address": "Fawwa Home",
            "category": "Rumah",
            "title": "Fawwa Home",
            "note": "Fawwa Home 1"
        }
        create = requests.post(url_create_address, params=param2, headers=headers2)

        validate_status = create.json().get('success')
        validate_message = create.json().get('message')['phone']

        assert create.status_code == 422
        assert validate_status == bool(False)
        assert 'No. HP tidak boleh kosong.' in validate_message

    def test_create_address_empty_value(self):
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
            "latitude": "-6.3823317",
            "longitude": "107.1162607",
            "receiver_name": "fawwa",
            "phone": "081386356616",
            "address": "",
            "category": "Rumah",
            "title": "Fawwa Home",
            "note": "Fawwa Home 1"
        }
        create = requests.post(url_create_address, params=param2, headers=headers2)

        validate_status = create.json().get('success')
        validate_message = create.json().get('message')['address']

        assert create.status_code == 422
        assert validate_status == bool(False)
        assert 'Alamat tidak boleh kosong.' in validate_message

    def test_create_address_value_kurang_dari10(self):
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
            "latitude": "-6.3823317",
            "longitude": "107.1162607",
            "receiver_name": "fawwa",
            "phone": "081386356616",
            "address": "aaa",
            "category": "Rumah",
            "title": "Fawwa Home",
            "note": "Fawwa Home 1"
        }
        create = requests.post(url_create_address, params=param2, headers=headers2)

        validate_status = create.json().get('success')
        validate_message = create.json().get('message')['address']

        assert create.status_code == 422
        assert validate_status == bool(False)
        assert 'Alamat setidaknya harus 10 karakter.' in validate_message

    def test_create_address_without_param_address(self):
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
            "latitude": "-6.3823317",
            "longitude": "107.1162607",
            "receiver_name": "fawwa",
            "phone": "081386356616",
            # "address": "Fawwa Home 1",
            "category": "Rumah",
            "title": "Fawwa Home",
            "note": "Fawwa Home 1"
        }
        create = requests.post(url_create_address, params=param2, headers=headers2)

        validate_status = create.json().get('success')
        validate_message = create.json().get('message')['address']

        assert create.status_code == 422
        assert validate_status == bool(False)
        assert 'Alamat tidak boleh kosong.' in validate_message

    def test_create_address_empty_value(self):
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
            "latitude": "-6.3823317",
            "longitude": "107.1162607",
            "receiver_name": "fawwa",
            "phone": "081386356616",
            "address": "",
            "category": "Rumah",
            "title": "Fawwa Home",
            "note": "Fawwa Home 1"
        }
        create = requests.post(url_create_address, params=param2, headers=headers2)

        validate_status = create.json().get('success')
        validate_message = create.json().get('message')['address']

        assert create.status_code == 422
        assert validate_status == bool(False)
        assert 'Alamat tidak boleh kosong.' in validate_message

    def test_create_address_category_number_value(self):
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
            "latitude": "-6.3823317",
            "longitude": "107.1162607",
            "receiver_name": "fawwa",
            "phone": "081386356616",
            "address": "Fawwa Home 1",
            "category": "1233211",
            "title": "Fawwa Home",
            "note": "Fawwa Home 1"
        }
        create = requests.post(url_create_address, params=param2, headers=headers2)

        validate_status = create.json().get('success')
        validate_message = create.json().get('message')

        assert create.status_code == 201
        assert validate_status == bool(True)
        assert 'Data alamat berhasil dibuat' in validate_message

    def test_create_address_category_empty(self):
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
            "latitude": "-6.3823317",
            "longitude": "107.1162607",
            "receiver_name": "fawwa",
            "phone": "081386356616",
            "address": "Fawwa Home 1",
            "category": "",
            "title": "Fawwa Home",
            "note": "Fawwa Home 1"
        }
        create = requests.post(url_create_address, params=param2, headers=headers2)

        validate_status = create.json().get('success')
        validate_message = create.json().get('message')['category']

        assert create.status_code == 422
        assert validate_status == bool(False)
        assert 'Kategori tidak boleh kosong.' in validate_message

    def test_create_address_without_param_category(self):
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
            "latitude": "-6.3823317",
            "longitude": "107.1162607",
            "receiver_name": "fawwa",
            "phone": "081386356616",
            "address": "Fawwa Home 1",
            # "category": "",
            "title": "Fawwa Home",
            "note": "Fawwa Home 1"
        }
        create = requests.post(url_create_address, params=param2, headers=headers2)

        validate_status = create.json().get('success')
        validate_message = create.json().get('message')['category']

        assert create.status_code == 422
        assert validate_status == bool(False)
        assert 'Kategori tidak boleh kosong.' in validate_message

    def test_create_address_note_empty(self):
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
            "latitude": "-6.3823317",
            "longitude": "107.1162607",
            "receiver_name": "fawwa",
            "phone": "081386356616",
            "address": "Fawwa Home 1",
            "category": "Makanam",
            "title": "Fawwa Home",
            "note": ""
        }
        create = requests.post(url_create_address, params=param2, headers=headers2)

        validate_status = create.json().get('success')
        validate_message = create.json().get('message')

        assert create.status_code == 201
        assert validate_status == bool(True)
        assert 'Data alamat berhasil dibuat' in validate_message

    def test_create_address_without_param_note(self):
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
            "latitude": "-6.3823317",
            "longitude": "107.1162607",
            "receiver_name": "fawwa",
            "phone": "081386356616",
            "address": "Fawwa Home 1",
            "category": "Makanam",
            "title": "Fawwa Home",
            # "note": ""
        }
        create = requests.post(url_create_address, params=param2, headers=headers2)

        validate_status = create.json().get('success')
        validate_message = create.json().get('message')

        assert create.status_code == 201
        assert validate_status == bool(True)
        assert 'Data alamat berhasil dibuat' in validate_message

