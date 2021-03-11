import requests
from assertpy import assert_that

url_get_all_merchant_menu= "https://staging.adminsurplus.net/api/v2/merchant/menus/"
url_login = "https://staging.adminsurplus.net/api/v2/merchant/auth/login"
email = "kopiruangvirtual@gmail.com"
kata_sandi = "12345678"

param = {
            "email": email,
            "password": kata_sandi
        }
login =requests.post(url_login, data=param,
                                headers={'Accept': 'application/json'})
token = login.json().get("token")
headers = {
            "Authorization": f"Bearer {token}"
        }
response = requests.get(url_get_all_merchant_menu, headers = headers)
data = response.json()
validate_status = data.get("success")
validate_message = data.get("message")


print(data)

assert response.status_code == 200
assert validate_status == bool(True)
assert "Data menu berhasil ditemukan." in validate_message
