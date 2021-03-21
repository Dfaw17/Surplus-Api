import requests
from env import stagging
import json


setting_env = stagging
delete_menu = f"{setting_env}/api/v2/merchant/menus/"
url_login = f"{setting_env}/api/v2/merchant/auth/login"
url_get_all_merchant_menu = f"{setting_env}/api/v2/merchant/menus/"
insert_menu = f"{setting_env}/api/v2/merchant/menus"
email = "vd1@gmail.com"
kata_sandi = "12345678"
wrong_token = "yJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvc3RhZ2luZy5hZG1pbnN1cnBsdXMubmV0XC9hcGlcL3YyXC9tZXJjaGFudFwvYXV0aFwvbG9naW4iLCJpYXQiOjE2MTUzOTIzMDQsImV4cCI6MTYxNzk4NDMwNCwibmJmIjoxNjE1MzkyMzA0LCJqdGkiOiJOVGJ1Qk4xODE2VU5Fd2VKIiwic3ViIjo0MDc3LCJwcnYiOiIyNzQxMDVkYTZlOTViZWYyODA3Nzg2ZGQ4NzM4ODY3Y2Y5YzAyYWFiIn0.QQqZAjqTaM6aUJ-uZU8E53iIRySWB_A9mQTIt_tUXsQ"

param = {

    "email": email,
    "password": kata_sandi
}
login = requests.post(url_login, data=param,headers={'Accept': 'application/json'})
token = login.json().get("token")
headers = {
    "Authorization": f"Bearer {token}"
}

response= requests.get(url_get_all_merchant_menu, headers=headers)
data_id = str(response.json().get("data")[0]["id"])
headers2 = {
    "Authorization": wrong_token
}

response2 = requests.delete(delete_menu+data_id, headers=headers2)
data = response2.text

assert response2.status_code == 401
assert "Unauthorized" in data

# print(data)


