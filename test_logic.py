import requests
from env import stagging
from pprint import pprint
from assertpy import assert_that

setting_env = stagging
url_login = f"{setting_env}/api/v2/customer/auth/login/email"
url_search = f"{setting_env}/api/v2/customer/search"
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
    'longitude':'107.1162607',
    'missed' : '0',
    'menu_categories[0]':'60',
    'max_price':'500000',
    'distance': '10000',
    'preorder': '0',
    'pickup_time_start': '02:00',
    'pickup_time_end': '22:00',
    'keyword': '',
    'order_by': 'nearbyy',
    'is_active': '1'
}
headers2 = {
    "Accept": "application/json",
    "Authorization": f"Bearer {login.json().get('token')}"
}
discover = requests.get(url_search, params=param2, headers=headers2)
pprint(discover.json())
validate_status = discover.json().get('success')
validate_message = discover.json().get('message')['order_by']


assert discover.status_code == 422
assert validate_status == bool(False)
assert 'Urutan yang dipilih tidak tersedia.' in validate_message








