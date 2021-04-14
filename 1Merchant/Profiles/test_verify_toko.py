import requests
from env import sandbox
import pprint
from assertpy import assert_that

class TestProfilesVerify:

    global setting_env, url_login, url_verify, email, kata_sandi, wrong_token

    setting_env = sandbox
    url_login = f"{setting_env}/api/v2/merchant/auth/login"
    url_verify = f"{setting_env}/api/v2/merchant/verify-request"
    email = "vd1@gmail.com"
    kata_sandi = '12345678'
    wrong_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvc3RhZ2luZy5hZG1pbnN1cnBsdXMubmV0XC9hcGlcL3YyXC9jdXN0b21lclwvYXV0aFwvbG9naW5cL2VtYWlsIiwiaWF0IjoxNjE2ODA1NzI2LCJleHAiOjE2MTkzOTc3MjYsIm5iZiI6MTYxNjgwNTcyNiwianRpIjoib05ESmxFRE5hSzNrN2RtVyIsInN1YiI6NDEyNiwicHJ2IjoiMjc0MTA1ZGE2ZTk1YmVmMjgwNzc4NmRkODczODg2N2NmOWMwMmFhYiJ9.fj51xIfQrqleRvdSJUbWcdrvsxQPUn8HpccnOmTgPDI'

    def test_insert_verify_normal(self):
        param = {
            'email': email,
            'password': kata_sandi
        }
        headers = {
            "Accept": "application/json"
        }
        login = requests.post(url_login, params=param, headers=headers)
        param2 = {
            'certifications[certifications][0][certification_id]': '7',
            'certifications[certifications][0][name]': 'aaa',
            'informations[questions][0][information_id]': '1',
            'informations[questions][0][answer]': 'information1',
            'informations[images][0][category]': 'kitchen'
        }
        headers2 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        file2 = {
            "certifications[images][0]": open("pisangnug.jpg", 'rb'),
            "informations[images][0][images][0]": open("pisangnug.jpg", 'rb')
        }
        verify_toko = requests.post(url_verify, params=param2, headers=headers2, files=file2)

        validate_status = verify_toko.json().get('success')
        validate_message = verify_toko.json().get('message')
        validate_data = verify_toko.json().get('data')

        assert verify_toko.status_code == 200
        assert validate_status == bool(True)
        assert 'Pengajuan verifikasi toko berhasil.' in validate_message
        assert_that(validate_data).is_not_none()
        assert_that(validate_data).contains_only('merchant_id', 'status_verify_request_id', 'updated_at', 'created_at',
                                                 'id')

    def test_insert_verify_just_information(self):
        param = {
            'email': email,
            'password': kata_sandi
        }
        headers = {
            "Accept": "application/json"
        }
        login = requests.post(url_login, params=param, headers=headers)
        param2 = {
            # 'certifications[certifications][0][certification_id]': '7',
            # 'certifications[certifications][0][name]': 'aaa',
            'informations[questions][0][information_id]': '1',
            'informations[questions][0][answer]': 'information1',
            'informations[images][0][category]': 'kitchen'
        }
        headers2 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        file2 = {
            # "certifications[images][0]": open("pisangnug.jpg", 'rb'),
            "informations[images][0][images][0]": open("pisangnug.jpg", 'rb')
        }
        verify_toko = requests.post(url_verify, params=param2, headers=headers2, files=file2)

        validate_status = verify_toko.json().get('success')
        validate_message = verify_toko.json().get('message')
        validate_data = verify_toko.json().get('data')

        assert verify_toko.status_code == 200
        assert validate_status == bool(True)
        assert 'Pengajuan verifikasi toko berhasil.' in validate_message
        assert_that(validate_data).is_not_none()
        assert_that(validate_data).contains_only('merchant_id', 'status_verify_request_id', 'updated_at', 'created_at',
                                                 'id')

    def test_insert_verify_just_certification(self):
        param = {
            'email': email,
            'password': kata_sandi
        }
        headers = {
            "Accept": "application/json"
        }
        login = requests.post(url_login, params=param, headers=headers)
        param2 = {
            'certifications[certifications][0][certification_id]': '7',
            'certifications[certifications][0][name]': 'aaa',
            # 'informations[questions][0][information_id]': '1',
            # 'informations[questions][0][answer]': 'information1',
            # 'informations[images][0][category]': 'kitchen'
        }
        headers2 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        file2 = {
            "certifications[images][0]": open("pisangnug.jpg", 'rb'),
            # "informations[images][0][images][0]": open("pisangnug.jpg", 'rb')
        }
        verify_toko = requests.post(url_verify, params=param2, headers=headers2, files=file2)

        validate_status = verify_toko.json().get('success')
        validate_message = verify_toko.json().get('message')
        validate_data = verify_toko.json().get('data')

        assert verify_toko.status_code == 200
        assert validate_status == bool(True)
        assert 'Pengajuan verifikasi toko berhasil.' in validate_message
        assert_that(validate_data).is_not_none()
        assert_that(validate_data).contains_only('merchant_id', 'status_verify_request_id', 'updated_at', 'created_at',
                                                 'id')

    def test_insert_verify_information_more_1(self):
        param = {
            'email': email,
            'password': kata_sandi
        }
        headers = {
            "Accept": "application/json"
        }
        login = requests.post(url_login, params=param, headers=headers)
        param2 = {
            # 'certifications[certifications][0][certification_id]': '7',
            # 'certifications[certifications][0][name]': 'aaa',
            'informations[questions][0][information_id]': '1',
            'informations[questions][0][answer]': 'information1',
            'informations[images][0][category]': 'kitchen',
            'informations[questions][1][information_id]': '2',
            'informations[questions][1][answer]': 'information2',
            'informations[images][1][category]': 'employees'
        }
        headers2 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        file2 = {
            # "certifications[images][0]": open("pisangnug.jpg", 'rb'),
            "informations[images][0][images][0]": open("pisangnug.jpg", 'rb'),
            "informations[images][1][images][0]": open("pisangnug.jpg", 'rb')
        }
        verify_toko = requests.post(url_verify, params=param2, headers=headers2, files=file2)

        validate_status = verify_toko.json().get('success')
        validate_message = verify_toko.json().get('message')
        validate_data = verify_toko.json().get('data')

        assert verify_toko.status_code == 200
        assert validate_status == bool(True)
        assert 'Pengajuan verifikasi toko berhasil.' in validate_message
        assert_that(validate_data).is_not_none()
        assert_that(validate_data).contains_only('merchant_id', 'status_verify_request_id', 'updated_at', 'created_at',
                                                 'id')

    def test_insert_verify_certification_more_1(self):
        param = {
            'email': email,
            'password': kata_sandi
        }
        headers = {
            "Accept": "application/json"
        }
        login = requests.post(url_login, params=param, headers=headers)
        param2 = {
            'certifications[certifications][0][certification_id]': '7',
            'certifications[certifications][0][name]': 'aaa',
            'certifications[certifications][1][certification_id]': '6',
            'certifications[certifications][1][name]': 'bbb',
            # 'informations[questions][0][information_id]': '1',
            # 'informations[questions][0][answer]': 'information1',
            # 'informations[images][0][category]': 'kitchen'
        }
        headers2 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        file2 = {
            "certifications[images][0]": open("pisangnug.jpg", 'rb'),
            "certifications[images][1]": open("pisangnug.jpg", 'rb'),
            # "informations[images][0][images][0]": open("pisangnug.jpg", 'rb')
        }
        verify_toko = requests.post(url_verify, params=param2, headers=headers2, files=file2)

        validate_status = verify_toko.json().get('success')
        validate_message = verify_toko.json().get('message')
        validate_data = verify_toko.json().get('data')

        assert verify_toko.status_code == 200
        assert validate_status == bool(True)
        assert 'Pengajuan verifikasi toko berhasil.' in validate_message
        assert_that(validate_data).is_not_none()
        assert_that(validate_data).contains_only('merchant_id', 'status_verify_request_id', 'updated_at', 'created_at',
                                                 'id')

    def test_insert_verify_certification_doest_match_image_and_data(self):
        param = {
            'email': email,
            'password': kata_sandi
        }
        headers = {
            "Accept": "application/json"
        }
        login = requests.post(url_login, params=param, headers=headers)
        param2 = {
            'certifications[certifications][0][certification_id]': '7',
            'certifications[certifications][0][name]': 'aaa',
            'certifications[certifications][1][certification_id]': '6',
            'certifications[certifications][1][name]': 'bbb',
            'informations[questions][0][information_id]': '1',
            'informations[questions][0][answer]': 'information1',
            'informations[images][0][category]': 'kitchen'
        }
        headers2 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        file2 = {
            "certifications[images][0]": open("pisangnug.jpg", 'rb'),
            "informations[images][0][images][0]": open("pisangnug.jpg", 'rb')
        }
        verify_toko = requests.post(url_verify, params=param2, headers=headers2, files=file2)

        validate_status = verify_toko.json().get('success')
        validate_message = verify_toko.json().get('message')

        assert verify_toko.status_code == 400
        assert validate_status == bool(False)
        assert 'Jumlah gambar harus sesuai jumlah ' in validate_message

    def test_insert_verify_information_more_4(self):
        param = {
            'email': email,
            'password': kata_sandi
        }
        headers = {
            "Accept": "application/json"
        }
        login = requests.post(url_login, params=param, headers=headers)
        param2 = {
            # 'certifications[certifications][0][certification_id]': '7',
            # 'certifications[certifications][0][name]': 'aaa',
            'informations[questions][0][information_id]': '1',
            'informations[questions][0][answer]': 'information1',
            'informations[questions][1][information_id]': '2',
            'informations[questions][1][answer]': 'information2',
            'informations[questions][2][information_id]': '3',
            'informations[questions][2][answer]': 'information3',
            'informations[questions][3][information_id]': '4',
            'informations[questions][3][answer]': 'information4',
            'informations[questions][4][information_id]': '5',
            'informations[questions][5][answer]': 'information5',
            'informations[images][0][category]': 'kitchen',
            'informations[images][1][category]': 'employees'
        }
        headers2 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        file2 = {
            # "certifications[images][0]": open("pisangnug.jpg", 'rb'),
            "informations[images][0][images][0]": open("pisangnug.jpg", 'rb'),
            "informations[images][1][images][0]": open("pisangnug.jpg", 'rb')
        }
        verify_toko = requests.post(url_verify, params=param2, headers=headers2, files=file2)

        validate_status = verify_toko.json().get('success')
        validate_message = verify_toko.json().get('message')

        assert verify_toko.status_code == 500
        assert validate_status == bool(False)
        assert 'Aduh!' in validate_message

    def test_insert_verify_certification_more_7(self):
        param = {
            'email': email,
            'password': kata_sandi
        }
        headers = {
            "Accept": "application/json"
        }
        login = requests.post(url_login, params=param, headers=headers)
        param2 = {
            'certifications[certifications][0][certification_id]': '1',
            'certifications[certifications][0][name]': 'aaa',
            'certifications[certifications][1][certification_id]': '2',
            'certifications[certifications][1][name]': 'aaa',
            'certifications[certifications][2][certification_id]': '3',
            'certifications[certifications][2][name]': 'aaa',
            'certifications[certifications][3][certification_id]': '4',
            'certifications[certifications][3][name]': 'aaa',
            'certifications[certifications][4][certification_id]': '5',
            'certifications[certifications][4][name]': 'aaa',
            'certifications[certifications][5][certification_id]': '6',
            'certifications[certifications][5][name]': 'aaa',
            'certifications[certifications][6][certification_id]': '7',
            'certifications[certifications][6][name]': 'aaa',
            'certifications[certifications][7][certification_id]': '8',
            'certifications[certifications][7][name]': 'aaa',
            # 'informations[questions][0][information_id]': '1',
            # 'informations[questions][0][answer]': 'information1',
            # 'informations[images][0][category]': 'employees'
        }
        headers2 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        file2 = {
            "certifications[images][0]": open("pisangnug.jpg", 'rb'),
            "certifications[images][1]": open("pisangnug.jpg", 'rb'),
            "certifications[images][2]": open("pisangnug.jpg", 'rb'),
            "certifications[images][3]": open("pisangnug.jpg", 'rb'),
            "certifications[images][4]": open("pisangnug.jpg", 'rb'),
            "certifications[images][5]": open("pisangnug.jpg", 'rb'),
            "certifications[images][6]": open("pisangnug.jpg", 'rb'),
            "certifications[images][7]": open("pisangnug.jpg", 'rb'),
            # "informations[images][0][images][0]": open("pisangnug.jpg", 'rb')
        }
        verify_toko = requests.post(url_verify, params=param2, headers=headers2, files=file2)

        validate_status = verify_toko.json().get('success')
        validate_message = verify_toko.json().get('message')

        assert verify_toko.status_code == 500
        assert validate_status == bool(False)
        assert 'Aduh!' in validate_message

    def test_insert_verify_empty_token(self):
        param = {
            'email': email,
            'password': kata_sandi
        }
        headers = {
            "Accept": "application/json"
        }
        login = requests.post(url_login, params=param, headers=headers)
        param2 = {
            'certifications[certifications][0][certification_id]': '1',
            'certifications[certifications][0][name]': 'aaa',
            'informations[questions][0][information_id]': '1',
            'informations[questions][0][answer]': 'information1',
            'informations[images][0][category]': 'employees'
        }
        headers2 = {
            "Accept": "application/json",
            "Authorization": ''
        }
        file2 = {
            "certifications[images][0]": open("pisangnug.jpg", 'rb'),
            "informations[images][0][images][0]": open("pisangnug.jpg", 'rb')
        }
        verify_toko = requests.post(url_verify, params=param2, headers=headers2, files=file2)

        validate_status = verify_toko.json().get('success')
        validate_message = verify_toko.json().get('message')

        assert verify_toko.status_code == 401
        assert validate_status == bool(False)
        assert 'Unauthorized' in validate_message

    def test_insert_verify_wrong_token(self):
        param = {
            'email': email,
            'password': kata_sandi
        }
        headers = {
            "Accept": "application/json"
        }
        login = requests.post(url_login, params=param, headers=headers)
        param2 = {
            'certifications[certifications][0][certification_id]': '1',
            'certifications[certifications][0][name]': 'aaa',
            'informations[questions][0][information_id]': '1',
            'informations[questions][0][answer]': 'information1',
            'informations[images][0][category]': 'employees'
        }
        headers2 = {
            "Accept": "application/json",
            "Authorization": wrong_token
        }
        file2 = {
            "certifications[images][0]": open("pisangnug.jpg", 'rb'),
            "informations[images][0][images][0]": open("pisangnug.jpg", 'rb')
        }
        verify_toko = requests.post(url_verify, params=param2, headers=headers2, files=file2)

        validate_status = verify_toko.json().get('success')
        validate_message = verify_toko.json().get('message')

        assert verify_toko.status_code == 401
        assert validate_status == bool(False)
        assert 'Unauthorized' in validate_message

    def test_insert_verify_without_param_certification_id(self):
        param = {
            'email': email,
            'password': kata_sandi
        }
        headers = {
            "Accept": "application/json"
        }
        login = requests.post(url_login, params=param, headers=headers)
        param2 = {
            # 'certifications[certifications][0][certification_id]': '1',
            'certifications[certifications][0][name]': 'aaa',
            'informations[questions][0][information_id]': '1',
            'informations[questions][0][answer]': 'information1',
            'informations[images][0][category]': 'employees'
        }
        headers2 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        file2 = {
            "certifications[images][0]": open("pisangnug.jpg", 'rb'),
            "informations[images][0][images][0]": open("pisangnug.jpg", 'rb')
        }
        verify_toko = requests.post(url_verify, params=param2, headers=headers2, files=file2)

        validate_status = verify_toko.json().get('success')
        validate_message = verify_toko.json().get('message')

        assert verify_toko.status_code == 500
        assert validate_status == bool(False)
        assert 'Aduh!' in validate_message

    def test_insert_verify_certification_id_empty_value(self):
        param = {
            'email': email,
            'password': kata_sandi
        }
        headers = {
            "Accept": "application/json"
        }
        login = requests.post(url_login, params=param, headers=headers)
        param2 = {
            'certifications[certifications][0][certification_id]': '',
            'certifications[certifications][0][name]': 'aaa',
            'informations[questions][0][information_id]': '1',
            'informations[questions][0][answer]': 'information1',
            'informations[images][0][category]': 'employees'
        }
        headers2 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        file2 = {
            "certifications[images][0]": open("pisangnug.jpg", 'rb'),
            "informations[images][0][images][0]": open("pisangnug.jpg", 'rb')
        }
        verify_toko = requests.post(url_verify, params=param2, headers=headers2, files=file2)

        validate_status = verify_toko.json().get('success')
        validate_message = verify_toko.json().get('message')

        assert verify_toko.status_code == 500
        assert validate_status == bool(False)
        assert 'Aduh!' in validate_message

    def test_insert_verify_certification_id_text_value(self):
        param = {
            'email': email,
            'password': kata_sandi
        }
        headers = {
            "Accept": "application/json"
        }
        login = requests.post(url_login, params=param, headers=headers)
        param2 = {
            'certifications[certifications][0][certification_id]': 'a',
            'certifications[certifications][0][name]': 'aaa',
            'informations[questions][0][information_id]': '1',
            'informations[questions][0][answer]': 'information1',
            'informations[images][0][category]': 'employees'
        }
        headers2 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        file2 = {
            "certifications[images][0]": open("pisangnug.jpg", 'rb'),
            "informations[images][0][images][0]": open("pisangnug.jpg", 'rb')
        }
        verify_toko = requests.post(url_verify, params=param2, headers=headers2, files=file2)

        validate_status = verify_toko.json().get('success')
        validate_message = verify_toko.json().get('message')

        assert verify_toko.status_code == 500
        assert validate_status == bool(False)
        assert 'Aduh!' in validate_message

    def test_insert_verify_certification_id_wrong_value(self):
        param = {
            'email': email,
            'password': kata_sandi
        }
        headers = {
            "Accept": "application/json"
        }
        login = requests.post(url_login, params=param, headers=headers)
        param2 = {
            'certifications[certifications][0][certification_id]': '8',
            'certifications[certifications][0][name]': 'aaa',
            'informations[questions][0][information_id]': '1',
            'informations[questions][0][answer]': 'information1',
            'informations[images][0][category]': 'employees'
        }
        headers2 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        file2 = {
            "certifications[images][0]": open("pisangnug.jpg", 'rb'),
            "informations[images][0][images][0]": open("pisangnug.jpg", 'rb')
        }
        verify_toko = requests.post(url_verify, params=param2, headers=headers2, files=file2)

        validate_status = verify_toko.json().get('success')
        validate_message = verify_toko.json().get('message')

        assert verify_toko.status_code == 500
        assert validate_status == bool(False)
        assert 'Aduh!' in validate_message

    def test_insert_verify_wihtout_param_certification_name(self):
        param = {
            'email': email,
            'password': kata_sandi
        }
        headers = {
            "Accept": "application/json"
        }
        login = requests.post(url_login, params=param, headers=headers)
        param2 = {
            'certifications[certifications][0][certification_id]': '1',
            # 'certifications[certifications][0][name]': 'aaa',
            'informations[questions][0][information_id]': '1',
            'informations[questions][0][answer]': 'information1',
            'informations[images][0][category]': 'employees'
        }
        headers2 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        file2 = {
            "certifications[images][0]": open("pisangnug.jpg", 'rb'),
            "informations[images][0][images][0]": open("pisangnug.jpg", 'rb')
        }
        verify_toko = requests.post(url_verify, params=param2, headers=headers2, files=file2)

        validate_status = verify_toko.json().get('success')
        validate_message = verify_toko.json().get('message')

        assert verify_toko.status_code == 500
        assert validate_status == bool(False)
        assert 'Aduh!' in validate_message

    def test_insert_verify_certification_name_empty_value(self):
        param = {
            'email': email,
            'password': kata_sandi
        }
        headers = {
            "Accept": "application/json"
        }
        login = requests.post(url_login, params=param, headers=headers)
        param2 = {
            'certifications[certifications][0][certification_id]': '1',
            'certifications[certifications][0][name]': '',
            'informations[questions][0][information_id]': '1',
            'informations[questions][0][answer]': 'information1',
            'informations[images][0][category]': 'employees'
        }
        headers2 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        file2 = {
            "certifications[images][0]": open("pisangnug.jpg", 'rb'),
            "informations[images][0][images][0]": open("pisangnug.jpg", 'rb')
        }
        verify_toko = requests.post(url_verify, params=param2, headers=headers2, files=file2)

        validate_status = verify_toko.json().get('success')
        validate_message = verify_toko.json().get('message')
        validate_data = verify_toko.json().get('data')

        assert verify_toko.status_code == 200
        assert validate_status == bool(True)
        assert 'Pengajuan verifikasi toko berhasil.' in validate_message
        assert_that(validate_data).is_not_none()
        assert_that(validate_data).contains_only('merchant_id', 'status_verify_request_id', 'updated_at', 'created_at',
                                                 'id')

    def test_insert_verify_certification_name_number_value(self):
        param = {
            'email': email,
            'password': kata_sandi
        }
        headers = {
            "Accept": "application/json"
        }
        login = requests.post(url_login, params=param, headers=headers)
        param2 = {
            'certifications[certifications][0][certification_id]': '1',
            'certifications[certifications][0][name]': '12341',
            'informations[questions][0][information_id]': '1',
            'informations[questions][0][answer]': 'information1',
            'informations[images][0][category]': 'employees'
        }
        headers2 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        file2 = {
            "certifications[images][0]": open("pisangnug.jpg", 'rb'),
            "informations[images][0][images][0]": open("pisangnug.jpg", 'rb')
        }
        verify_toko = requests.post(url_verify, params=param2, headers=headers2, files=file2)

        validate_status = verify_toko.json().get('success')
        validate_message = verify_toko.json().get('message')
        validate_data = verify_toko.json().get('data')

        assert verify_toko.status_code == 200
        assert validate_status == bool(True)
        assert 'Pengajuan verifikasi toko berhasil.' in validate_message
        assert_that(validate_data).is_not_none()
        assert_that(validate_data).contains_only('merchant_id', 'status_verify_request_id', 'updated_at', 'created_at',
                                                 'id')

    def test_insert_verify_certifivation_image_empty_value(self):
        param = {
            'email': email,
            'password': kata_sandi
        }
        headers = {
            "Accept": "application/json"
        }
        login = requests.post(url_login, params=param, headers=headers)
        param2 = {
            'certifications[certifications][0][certification_id]': '1',
            'certifications[certifications][0][name]': '',
            'informations[questions][0][information_id]': '1',
            'informations[questions][0][answer]': 'information1',
            'informations[images][0][category]': 'employees'
        }
        headers2 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        file2 = {
            "certifications[images][0]": '',
            "informations[images][0][images][0]": open("pisangnug.jpg", 'rb')
        }
        verify_toko = requests.post(url_verify, params=param2, headers=headers2, files=file2)

        validate_status = verify_toko.json().get('success')
        validate_message = verify_toko.json().get('message')

        assert verify_toko.status_code == 500
        assert validate_status == bool(False)
        assert 'Aduh!' in validate_message

    def test_insert_verify_without_param_certification_image(self):
        param = {
            'email': email,
            'password': kata_sandi
        }
        headers = {
            "Accept": "application/json"
        }
        login = requests.post(url_login, params=param, headers=headers)
        param2 = {
            'certifications[certifications][0][certification_id]': '1',
            'certifications[certifications][0][name]': '',
            'informations[questions][0][information_id]': '1',
            'informations[questions][0][answer]': 'information1',
            'informations[images][0][category]': 'employees'
        }
        headers2 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        file2 = {
            # "certifications[images][0]": '',
            "informations[images][0][images][0]": open("pisangnug.jpg", 'rb')
        }
        verify_toko = requests.post(url_verify, params=param2, headers=headers2, files=file2)

        validate_status = verify_toko.json().get('success')
        validate_message = verify_toko.json().get('message')

        assert verify_toko.status_code == 500
        assert validate_status == bool(False)
        assert 'Aduh!' in validate_message

    def test_insert_verify_without_param_information_id(self):
        param = {
            'email': email,
            'password': kata_sandi
        }
        headers = {
            "Accept": "application/json"
        }
        login = requests.post(url_login, params=param, headers=headers)
        param2 = {
            'certifications[certifications][0][certification_id]': '1',
            'certifications[certifications][0][name]': '',
            # 'informations[questions][0][information_id]': '1',
            'informations[questions][0][answer]': 'information1',
            'informations[images][0][category]': 'employees'
        }
        headers2 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        file2 = {
            "certifications[images][0]": open("pisangnug.jpg", 'rb'),
            "informations[images][0][images][0]": open("pisangnug.jpg", 'rb')
        }
        verify_toko = requests.post(url_verify, params=param2, headers=headers2, files=file2)

        validate_status = verify_toko.json().get('success')
        validate_message = verify_toko.json().get('message')

        assert verify_toko.status_code == 500
        assert validate_status == bool(False)
        assert 'Aduh!' in validate_message

    def test_insert_verify_information_id_empty_value(self):
        param = {
            'email': email,
            'password': kata_sandi
        }
        headers = {
            "Accept": "application/json"
        }
        login = requests.post(url_login, params=param, headers=headers)
        param2 = {
            'certifications[certifications][0][certification_id]': '1',
            'certifications[certifications][0][name]': '',
            'informations[questions][0][information_id]': '',
            'informations[questions][0][answer]': 'information1',
            'informations[images][0][category]': 'employees'
        }
        headers2 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        file2 = {
            "certifications[images][0]": open("pisangnug.jpg", 'rb'),
            "informations[images][0][images][0]": open("pisangnug.jpg", 'rb')
        }
        verify_toko = requests.post(url_verify, params=param2, headers=headers2, files=file2)

        validate_status = verify_toko.json().get('success')
        validate_message = verify_toko.json().get('message')['informations.questions.0.information_id']

        assert verify_toko.status_code == 422
        assert validate_status == bool(False)
        assert 'informations.questions.0.information_id harus berupa angka.' in validate_message

    def test_insert_verify_information_id_wrong_value(self):
        param = {
            'email': email,
            'password': kata_sandi
        }
        headers = {
            "Accept": "application/json"
        }
        login = requests.post(url_login, params=param, headers=headers)
        param2 = {
            'certifications[certifications][0][certification_id]': '1',
            'certifications[certifications][0][name]': 'aa',
            'informations[questions][0][information_id]': '5',
            'informations[questions][0][answer]': 'information1',
            'informations[images][0][category]': 'employees'
        }
        headers2 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        file2 = {
            "certifications[images][0]": open("pisangnug.jpg", 'rb'),
            "informations[images][0][images][0]": open("pisangnug.jpg", 'rb')
        }
        verify_toko = requests.post(url_verify, params=param2, headers=headers2, files=file2)

        validate_status = verify_toko.json().get('success')
        validate_message = verify_toko.json().get('message')

        assert verify_toko.status_code == 500
        assert validate_status == bool(False)
        assert 'Aduh!' in validate_message

    def test_insert_verify_information_id_text_value(self):
        param = {
            'email': email,
            'password': kata_sandi
        }
        headers = {
            "Accept": "application/json"
        }
        login = requests.post(url_login, params=param, headers=headers)
        param2 = {
            'certifications[certifications][0][certification_id]': '1',
            'certifications[certifications][0][name]': '',
            'informations[questions][0][information_id]': 'aaa',
            'informations[questions][0][answer]': 'information1',
            'informations[images][0][category]': 'employees'
        }
        headers2 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        file2 = {
            "certifications[images][0]": open("pisangnug.jpg", 'rb'),
            "informations[images][0][images][0]": open("pisangnug.jpg", 'rb')
        }
        verify_toko = requests.post(url_verify, params=param2, headers=headers2, files=file2)

        validate_status = verify_toko.json().get('success')
        validate_message = verify_toko.json().get('message')['informations.questions.0.information_id']

        assert verify_toko.status_code == 422
        assert validate_status == bool(False)
        assert 'informations.questions.0.information_id harus berupa angka.' in validate_message

    def test_insert_verify_without_param_information_answer(self):
        param = {
            'email': email,
            'password': kata_sandi
        }
        headers = {
            "Accept": "application/json"
        }
        login = requests.post(url_login, params=param, headers=headers)
        param2 = {
            'certifications[certifications][0][certification_id]': '1',
            'certifications[certifications][0][name]': 'aa',
            'informations[questions][0][information_id]': '1',
            # 'informations[questions][0][answer]': 'information1',
            'informations[images][0][category]': 'employees'
        }
        headers2 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        file2 = {
            "certifications[images][0]": open("pisangnug.jpg", 'rb'),
            "informations[images][0][images][0]": open("pisangnug.jpg", 'rb')
        }
        verify_toko = requests.post(url_verify, params=param2, headers=headers2, files=file2)

        validate_status = verify_toko.json().get('success')
        validate_message = verify_toko.json().get('message')

        assert verify_toko.status_code == 500
        assert validate_status == bool(False)
        assert 'Aduh!' in validate_message

    def test_insert_verify_information_answer_empty_value(self):
        param = {
            'email': email,
            'password': kata_sandi
        }
        headers = {
            "Accept": "application/json"
        }
        login = requests.post(url_login, params=param, headers=headers)
        param2 = {
            'certifications[certifications][0][certification_id]': '1',
            'certifications[certifications][0][name]': 'aa',
            'informations[questions][0][information_id]': '1',
            'informations[questions][0][answer]': '',
            'informations[images][0][category]': 'employees'
        }
        headers2 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        file2 = {
            "certifications[images][0]": open("pisangnug.jpg", 'rb'),
            "informations[images][0][images][0]": open("pisangnug.jpg", 'rb')
        }
        verify_toko = requests.post(url_verify, params=param2, headers=headers2, files=file2)

        validate_status = verify_toko.json().get('success')
        validate_message = verify_toko.json().get('message')['informations.questions.0.answer']

        assert verify_toko.status_code == 422
        assert validate_status == bool(False)
        assert 'informations.questions.0.answer harus merupakan string.' in validate_message

    def test_insert_verify_without_param_information_images_category(self):
        param = {
            'email': email,
            'password': kata_sandi
        }
        headers = {
            "Accept": "application/json"
        }
        login = requests.post(url_login, params=param, headers=headers)
        param2 = {
            'certifications[certifications][0][certification_id]': '1',
            'certifications[certifications][0][name]': 'aa',
            'informations[questions][0][information_id]': '1',
            'informations[questions][0][answer]': 'aaa',
            # 'informations[images][0][category]': 'employees'
        }
        headers2 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        file2 = {
            "certifications[images][0]": open("pisangnug.jpg", 'rb'),
            "informations[images][0][images][0]": open("pisangnug.jpg", 'rb')
        }
        verify_toko = requests.post(url_verify, params=param2, headers=headers2, files=file2)

        validate_status = verify_toko.json().get('success')
        validate_message = verify_toko.json().get('message')

        assert verify_toko.status_code == 500
        assert validate_status == bool(False)
        assert 'Aduh!' in validate_message

    def test_insert_verify_information_images_category_empty_value(self):
        param = {
            'email': email,
            'password': kata_sandi
        }
        headers = {
            "Accept": "application/json"
        }
        login = requests.post(url_login, params=param, headers=headers)
        param2 = {
            'certifications[certifications][0][certification_id]': '1',
            'certifications[certifications][0][name]': 'aa',
            'informations[questions][0][information_id]': '1',
            'informations[questions][0][answer]': 'aaa',
            'informations[images][0][category]': ''
        }
        headers2 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        file2 = {
            "certifications[images][0]": open("pisangnug.jpg", 'rb'),
            "informations[images][0][images][0]": open("pisangnug.jpg", 'rb')
        }
        verify_toko = requests.post(url_verify, params=param2, headers=headers2, files=file2)

        validate_status = verify_toko.json().get('success')
        validate_message = verify_toko.json().get('message')['informations.images.0.category']

        assert verify_toko.status_code == 422
        assert validate_status == bool(False)
        assert 'informations.images.0.category yang dipilih tidak tersedia.' in validate_message

    def test_insert_verify_information_images_category_wrong_value(self):
        param = {
            'email': email,
            'password': kata_sandi
        }
        headers = {
            "Accept": "application/json"
        }
        login = requests.post(url_login, params=param, headers=headers)
        param2 = {
            'certifications[certifications][0][certification_id]': '1',
            'certifications[certifications][0][name]': 'aa',
            'informations[questions][0][information_id]': '1',
            'informations[questions][0][answer]': 'aaa',
            'informations[images][0][category]': 'hoho'
        }
        headers2 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        file2 = {
            "certifications[images][0]": open("pisangnug.jpg", 'rb'),
            "informations[images][0][images][0]": open("pisangnug.jpg", 'rb')
        }
        verify_toko = requests.post(url_verify, params=param2, headers=headers2, files=file2)

        validate_status = verify_toko.json().get('success')
        validate_message = verify_toko.json().get('message')['informations.images.0.category']

        assert verify_toko.status_code == 422
        assert validate_status == bool(False)
        assert 'informations.images.0.category yang dipilih tidak tersedia.' in validate_message

    def test_insert_verify_information_images_empty_value(self):
        param = {
            'email': email,
            'password': kata_sandi
        }
        headers = {
            "Accept": "application/json"
        }
        login = requests.post(url_login, params=param, headers=headers)
        param2 = {
            'certifications[certifications][0][certification_id]': '1',
            'certifications[certifications][0][name]': 'aa',
            'informations[questions][0][information_id]': '1',
            'informations[questions][0][answer]': 'aaa',
            'informations[images][0][category]': 'kitchen'
        }
        headers2 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        file2 = {
            "certifications[images][0]": open("pisangnug.jpg", 'rb'),
            "informations[images][0][images][0]": ''
        }
        verify_toko = requests.post(url_verify, params=param2, headers=headers2, files=file2)

        validate_status = verify_toko.json().get('success')
        validate_message = verify_toko.json().get('message')['informations.images.0.images.0']

        assert verify_toko.status_code == 422
        assert validate_status == bool(False)
        assert 'The informations.images.0.images.0 must be a file of type: jpeg, jpg, png.' in validate_message

    def test_insert_verify_without_param_information_images(self):
        param = {
            'email': email,
            'password': kata_sandi
        }
        headers = {
            "Accept": "application/json"
        }
        login = requests.post(url_login, params=param, headers=headers)
        param2 = {
            'certifications[certifications][0][certification_id]': '1',
            'certifications[certifications][0][name]': 'aa',
            'informations[questions][0][information_id]': '1',
            'informations[questions][0][answer]': 'aaa',
            'informations[images][0][category]': 'kitchen'
        }
        headers2 = {
            "Accept": "application/json",
            "Authorization": f"Bearer {login.json().get('token')}"
        }
        file2 = {
            "certifications[images][0]": open("pisangnug.jpg", 'rb'),
            # "informations[images][0][images][0]": ''
        }
        verify_toko = requests.post(url_verify, params=param2, headers=headers2, files=file2)

        validate_status = verify_toko.json().get('success')
        validate_message = verify_toko.json().get('message')

        assert verify_toko.status_code == 500
        assert validate_status == bool(False)
        assert 'Aduh!' in validate_message

