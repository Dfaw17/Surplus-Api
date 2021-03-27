import requests
from env import stagging
from pprint import pprint
from assertpy import assert_that

setting_env = stagging
url_login = f"{setting_env}/api/v2/customer/auth/login/email"
url_discover = f"{setting_env}/api/v2/customer/discover"
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
    "Authorization": wrong_token
}
discover = requests.get(url_discover, params=param2, headers=headers2)

validate_status = discover.json().get('success')
validate_message = discover.json().get('message')
#
assert discover.status_code == 401
assert validate_status == bool(False)
assert 'Unauthorized' in validate_message

# pprint(validate_menu_kategori)
