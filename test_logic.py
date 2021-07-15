import requests
from env import *
from assertpy import *

setting_env = testing
url_getall_menu = f"{setting_env}/api/v2/merchant/menus/"
url_login = f"{setting_env}/api/v2/merchant/auth/login"
url_delete = f"{setting_env}/api/v2/merchant/menus/"
email = "sdet@gmail.com"
kata_sandi = "12345678"
wrong_token = "kyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvc3RhZ2luZy5hZG1pbnN1cnBsdXMubmV0XC9hcGlcL3YyXC9tZXJjaGFudFwvYXV0aFwvbG9naW4iLCJpYXQiOjE2MTU3MDExNDIsImV4cCI6MTYxODI5MzE0MiwibmJmIjoxNjE1NzAxMTQyLCJqdGkiOiJjOFluT3BlMzRqRVVIemZSIiwic3ViIjo0MDc3LCJwcnYiOiIyNzQxMDVkYTZlOTViZWYyODA3Nzg2ZGQ4NzM4ODY3Y2Y5YzAyYWFiIn0.xxI5o6tgIvb3Eds4CCfSnXM3ThFYiQwYcTCxKmrZozI"

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

response = requests.delete(url_delete + str(menu), headers=headers)
data = response.json()

validate_status = data.get("success")
validate_message = data.get("message")

assert response.status_code == 201
assert validate_status == bool(True)
assert "Data menu berhasil dihapus." in validate_message

print("Success Automation")
