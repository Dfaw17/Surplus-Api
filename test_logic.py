import requests
from env import stagging
from pprint import pprint
from assertpy import assert_that

setting_env = stagging
url_login = f"{setting_env}/api/v2/customer/auth/login/email"
url_discover = f"{setting_env}/api/v2/customer/discover"
url_show_menu = f"{setting_env}/api/v2/customer/menus/"
email = "kopiruangvirtual@gmail.com"
kata_sandi = '12345678'
wrong_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvc3RhZ2luZy5hZG1pbnN1cnBsdXMubmV0XC9hcGlcL3YyXC9jdXN0b21lclwvYXV0aFwvbG9naW5cL2VtYWlsIiwiaWF0IjoxNjE2ODA1NzI2LCJleHAiOjE2MTkzOTc3MjYsIm5iZiI6MTYxNjgwNTcyNiwianRpIjoib05ESmxFRE5hSzNrN2RtVyIsInN1YiI6NDEyNiwicHJ2IjoiMjc0MTA1ZGE2ZTk1YmVmMjgwNzc4NmRkODczODg2N2NmOWMwMmFhYiJ9.fj51xIfQrqleRvdSJUbWcdrvsxQPUn8HpccnOmTgPDI'

param = {
    'email': email,
    'password': kata_sandi
}
headers = {
    "Accept": "application/json"
}
login = requests.post(url_login, params=param, headers=headers)
param2 = {
    'latitude': '-6.3823317',
    'longitude': '107.1162607'
}
headers2 = {
    "Accept": "application/json",
    "Authorization": f"Bearer {login.json().get('token')}"
}
discover = requests.get(url_discover, params=param2, headers=headers2)
param3 = {
    'latitude': '-6.3823317',
    'longitude': '107.1162607'
}
headers3 = {
    "Accept": "application/json",
    "Authorization": f"Bearer {login.json().get('token')}"
}
show_menu = requests.get(url_show_menu+'aaa', params=param3, headers=headers3)

validate_status = show_menu.json().get('success')
validate_message = show_menu.json().get('message')

assert show_menu.status_code == 404
assert validate_status == bool(False)
assert 'Data menu tidak ditemukan' in validate_message
pprint(show_menu.json())









