import requests
from env import stagging
from pprint import pprint
from assertpy import assert_that

class TestCustomerStoreForum:

    global setting_env,url_login,url_forum_store,email,kata_sandi,wrong_token

    setting_env = stagging
    url_login = f"{setting_env}/api/v2/customer/auth/login/email"
    url_forum_store = f"{setting_env}/api/v2/customer/forums"
    email = "kopiruangvirtual@gmail.com"
    kata_sandi = '12345678'
    wrong_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvc3RhZ2luZy5hZG1pbnN1cnBsdXMubmV0XC9hcGlcL3YyXC9jdXN0b21lclwvYXV0aFwvbG9naW5cL2VtYWlsIiwiaWF0IjoxNjE2ODA1NzI2LCJleHAiOjE2MTkzOTc3MjYsIm5iZiI6MTYxNjgwNTcyNiwianRpIjoib05ESmxFRE5hSzNrN2RtVyIsInN1YiI6NDEyNiwicHJ2IjoiMjc0MTA1ZGE2ZTk1YmVmMjgwNzc4NmRkODczODg2N2NmOWMwMmFhYiJ9.fj51xIfQrqleRvdSJUbWcdrvsxQPUn8HpccnOmTgPDI'

    def test_store_normal(self):
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
        data = {
            "forum_category_id": "1",
            "title": "Tanya",
            "content": "test3",
            "link": "https://www.surplus.id/",
            "location": "surplus indonesia"
        }
        index_forum = requests.post(url_forum_store, data=data, headers=headers2,
                                    files={'image': open("pisangnug.jpg", 'rb')})

        validasi_status = index_forum.json().get('success')
        validasi_message = index_forum.json().get('message')

        assert index_forum.status_code == 201
        assert validasi_status == bool(True)
        assert "Data forum berhasil diposting." in validasi_message

    def test_store_token_empty_value(self):
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
            "Authorization": ""
        }
        data = {
            "forum_category_id": "1",
            "title": "Tanya",
            "content": "test3",
            "link": "https://www.surplus.id/",
            "location": "surplus indonesia"
        }
        index_forum = requests.post(url_forum_store, data=data, headers=headers2,
                                    files={'image': open("pisangnug.jpg", 'rb')})

        validasi_status = index_forum.json().get('success')
        validasi_message = index_forum.json().get('message')

        assert index_forum.status_code == 401
        assert validasi_status == bool(False)
        assert "Unauthorized" in validasi_message

    def test_store_token_empty_value(self):
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
        data = {
            "forum_category_id": "1",
            "title": "Tanya",
            "content": "test3",
            "link": "https://www.surplus.id/",
            "location": "surplus indonesia"
        }
        index_forum = requests.post(url_forum_store, data=data, headers=headers2,
                                    files={'image': open("pisangnug.jpg", 'rb')})

        validasi_status = index_forum.json().get('success')
        validasi_message = index_forum.json().get('message')

        assert index_forum.status_code == 401
        assert validasi_status == bool(False)
        assert "Unauthorized" in validasi_message

    def test_store_forum_category_id_empty_value(self):
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
        data = {
            "forum_category_id":"",
            "title": "Tanya",
            "content": "test3",
            "link": "https://www.surplus.id/",
            "location": "surplus indonesia"
        }
        index_forum = requests.post(url_forum_store, data=data, headers=headers2,
                                    files={'image': open("pisangnug.jpg", 'rb')})

        validasi_status = index_forum.json().get('success')
        validasi_message = index_forum.json().get('message')['forum_category_id']

        assert index_forum.status_code == 422
        assert validasi_status == bool(False)
        assert "Kategori forum tidak boleh kosong." in validasi_message

    def test_store_forum_without_param_category_id(self):
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
        data = {
            # "forum_category_id":"",
            "title": "Tanya",
            "content": "test3",
            "link": "https://www.surplus.id/",
            "location": "surplus indonesia"
        }
        index_forum = requests.post(url_forum_store, data=data, headers=headers2,
                                    files={'image': open("pisangnug.jpg", 'rb')})

        validasi_status = index_forum.json().get('success')
        validasi_message = index_forum.json().get('message')['forum_category_id']

        assert index_forum.status_code == 422
        assert validasi_status == bool(False)
        assert "Kategori forum tidak boleh kosong." in validasi_message

    def test_Store_forum_category_id_text_value(self):
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
        data = {
            "forum_category_id": "aaa",
            "title": "Tanya",
            "content": "test3",
            "link": "https://www.surplus.id/",
            "location": "surplus indonesia"
        }
        index_forum = requests.post(url_forum_store, data=data, headers=headers2,
                                    files={'image': open("pisangnug.jpg", 'rb')})

        validasi_status = index_forum.json().get('success')
        validasi_message = index_forum.json().get('message')['forum_category_id']

        assert index_forum.status_code == 422
        assert validasi_status == bool(False)
        assert "Kategori forum harus berupa angka." in validasi_message

    def test_store_forum_category_id_wrong_value(self):
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
        data = {
            "forum_category_id": "666",
            "title": "Tanya",
            "content": "test3",
            "link": "https://www.surplus.id/",
            "location": "surplus indonesia"
        }
        index_forum = requests.post(url_forum_store, data=data, headers=headers2,
                                    files={'image': open("pisangnug.jpg", 'rb')})

        validasi_status = index_forum.json().get('success')
        validasi_message = index_forum.json().get('message')

        assert index_forum.status_code == 500
        assert validasi_status == bool(False)
        assert "Aduh!" in validasi_message

    def test_store_forum_title_empty_value(self):
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
        data = {
            "forum_category_id": "1",
            "title": "",
            "content": "test3",
            "link": "https://www.surplus.id/",
            "location": "surplus indonesia"
        }
        index_forum = requests.post(url_forum_store, data=data, headers=headers2,
                                    files={'image': open("pisangnug.jpg", 'rb')})

        validasi_status = index_forum.json().get('success')
        validasi_message = index_forum.json().get('message')['title']

        assert index_forum.status_code == 422
        assert validasi_status == bool(False)
        assert "Judul tidak boleh kosong." in validasi_message

    def test_store_forum_without_param_title(self):
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
        data = {
            "forum_category_id": "1",
            # "title": "",
            "content": "test3",
            "link": "https://www.surplus.id/",
            "location": "surplus indonesia"
        }
        index_forum = requests.post(url_forum_store, data=data, headers=headers2,
                                    files={'image': open("pisangnug.jpg", 'rb')})

        validasi_status = index_forum.json().get('success')
        validasi_message = index_forum.json().get('message')['title']

        assert index_forum.status_code == 422
        assert validasi_status == bool(False)
        assert "Judul tidak boleh kosong." in validasi_message

    def test_store_forum_link_empty_value(self):
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
        data = {
            "forum_category_id": "1",
            "title": "haha",
            "content": "test3",
            "link": "",
            "location": "surplus indonesia"
        }
        index_forum = requests.post(url_forum_store, data=data, headers=headers2,
                                    files={'image': open("pisangnug.jpg", 'rb')})

        validasi_status = index_forum.json().get('success')
        validasi_message = index_forum.json().get('message')

        assert index_forum.status_code == 201
        assert validasi_status == bool(True)
        assert "Data forum berhasil diposting." in validasi_message

    def test_store_forum_link_number_value(self):
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
        data = {
            "forum_category_id": "1",
            "title": "haha",
            "content": "test3",
            "link": "555",
            "location": "surplus indonesia"
        }
        index_forum = requests.post(url_forum_store, data=data, headers=headers2,
                                    files={'image': open("pisangnug.jpg", 'rb')})

        validasi_status = index_forum.json().get('success')
        validasi_message = index_forum.json().get('message')

        assert index_forum.status_code == 201
        assert validasi_status == bool(True)
        assert "Data forum berhasil diposting." in validasi_message

    def test_store_forum_without_param_link(self):
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
        data = {
            "forum_category_id": "1",
            "title": "haha",
            "content": "test3",
            # "link": "555",
            "location": "surplus indonesia"
        }
        index_forum = requests.post(url_forum_store, data=data, headers=headers2,
                                    files={'image': open("pisangnug.jpg", 'rb')})

        validasi_status = index_forum.json().get('success')
        validasi_message = index_forum.json().get('message')

        assert index_forum.status_code == 201
        assert validasi_status == bool(True)
        assert "Data forum berhasil diposting." in validasi_message

    def test_store_forum_location_empty_value(self):
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
        data = {
            "forum_category_id": "1",
            "title": "haha",
            "content": "test3",
            "link": "555",
            "location": ""
        }
        index_forum = requests.post(url_forum_store, data=data, headers=headers2,
                                    files={'image': open("pisangnug.jpg", 'rb')})

        validasi_status = index_forum.json().get('success')
        validasi_message = index_forum.json().get('message')

        assert index_forum.status_code == 201
        assert validasi_status == bool(True)
        assert "Data forum berhasil diposting." in validasi_message

    def test_store_forum_location_number_value(self):
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
        data = {
            "forum_category_id": "1",
            "title": "haha",
            "content": "test3",
            "link": "555",
            "location": "232"
        }
        index_forum = requests.post(url_forum_store, data=data, headers=headers2,
                                    files={'image': open("pisangnug.jpg", 'rb')})

        validasi_status = index_forum.json().get('success')
        validasi_message = index_forum.json().get('message')

        assert index_forum.status_code == 201
        assert validasi_status == bool(True)
        assert "Data forum berhasil diposting." in validasi_message

    def test_store_forum_without_param_location(self):
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
        data = {
            "forum_category_id": "1",
            "title": "haha",
            "content": "test3",
            "link": "555",
            # "location": "232"
        }
        index_forum = requests.post(url_forum_store, data=data, headers=headers2,
                                    files={'image': open("pisangnug.jpg", 'rb')})

        validasi_status = index_forum.json().get('success')
        validasi_message = index_forum.json().get('message')

        assert index_forum.status_code == 201
        assert validasi_status == bool(True)
        assert "Data forum berhasil diposting." in validasi_message




