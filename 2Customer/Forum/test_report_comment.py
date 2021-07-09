import requests
from env import *
from pprint import pprint
from assertpy import assert_that


class TestCustomerReportForum:
    global setting_env, url_login, url_forum, url_forum_report_comment, email, kata_sandi, wrong_token

    setting_env = mock
    url_login = f"{setting_env}/api/v2/customer/auth/login/email"
    url_forum = f"{setting_env}/api/v2/customer/forums"
    url_forum_report_comment = f"{setting_env}/api/v2/customer/reports/comment"
    email = "kopiruangvirtual@gmail.com"
    kata_sandi = '12345678'
    wrong_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvc3RhZ2luZy5hZG1pbnN1cnBsdXMubmV0XC9hcGlcL3YyXC9jdXN0b21lclwvYXV0aFwvbG9naW5cL2VtYWlsIiwiaWF0IjoxNjE2ODA1NzI2LCJleHAiOjE2MTkzOTc3MjYsIm5iZiI6MTYxNjgwNTcyNiwianRpIjoib05ESmxFRE5hSzNrN2RtVyIsInN1YiI6NDEyNiwicHJ2IjoiMjc0MTA1ZGE2ZTk1YmVmMjgwNzc4NmRkODczODg2N2NmOWMwMmFhYiJ9.fj51xIfQrqleRvdSJUbWcdrvsxQPUn8HpccnOmTgPDI'

    def test_report_comment_normal(self):
        param = {
            'email': email,
            'password': kata_sandi
        }
        headers = {
            "Accept": "application/json"
        }
        login = requests.post(url_login, params=param, headers=headers)
        headers = {
            "Accept": "application/json",
            # "Authorization": f"Bearer {login.json().get('token')}"
        }

        param = {
            "forum_id": "414",
            "forum_komentar_id": "433",
            "forum_report_kategori_id": "4",
            "content": "Posting data pribadi"
        }
        report_comment = requests.post(url_forum_report_comment, headers=headers, params=param)

        validate_status = report_comment.json().get('success')
        validate_message = report_comment.json().get('message')

        assert report_comment.status_code == 200
        assert validate_status == bool(True)
        assert 'Komentar berhasil dilaporkan! Admin Surplus akan menindaklanjuti pelaporan kamu ya' in validate_message
