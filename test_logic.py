import requests

url_show_merchant_menu = "https://staging.adminsurplus.net/api/v2/merchant/menus/"
url_login = "https://staging.adminsurplus.net/api/v2/merchant/auth/login"
email = "kopiruangvirtual@gmail.com"
kata_sandi = "12345678"

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
get_all_merchant_menu = requests.get(url_show_merchant_menu, headers=headers)
data_menu = str(15090)
data_merchat_id = str(get_all_merchant_menu.json().get("data")[0]["merchant_id"])

response = requests.get(url_show_merchant_menu + data_menu, headers=headers)
data = response.json()

validate_status = data.get("success")
validate_message = data.get("message")


assert validate_status == bool(False)
assert response.status_code == 404
assert validate_message == "Data menu tidak ditemukan."
