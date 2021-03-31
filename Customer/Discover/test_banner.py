import requests
from env import stagging
from pprint import pprint
from assertpy import assert_that

class TestCustomerBanner:

    global setting_env,url_login,url_banner,email,kata_sandi

    setting_env = stagging
    url_login = f"{setting_env}/api/v2/customer/auth/login/email"
    url_banner = f"{setting_env}/api/v2/customer/banners"
    email = "kopiruangvirtual@gmail.com"
    kata_sandi = '12345678'

    def test_banner_normal(self):
        param = {
            'email': email,
            'password': kata_sandi
        }
        headers = {
            "Accept": "application/json"
        }
        login = requests.post(url_login, params=param, headers=headers)

        banner = requests.get(url_banner)
        validate_status = banner.json().get('success')
        validate_message = banner.json().get('message')

        assert banner.status_code == 200
        assert validate_status == bool(True)
        assert 'Data banner berhasil ditemukan.' in validate_message