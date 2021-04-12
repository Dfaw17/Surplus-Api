import requests
from env import stagging
from pprint import pprint
from assertpy import assert_that

setting_env = stagging
url_login = f"{setting_env}/api/v2/customer/auth/login/email"
url_discover = f"{setting_env}/api/v2/customer/discover"
url_checkout = f"{setting_env}/api/v2/customer/orders/checkout"
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
    'delivery_price': '20000',
    'is_lunchbox': '0',
    'donation_price': '2500',
    'voucher_id': '62',
    'order_items[0][stock_id]': '666666',
    'order_items[0][qty]': '1'
}
headers3 = {
    "Accept": "application/json",
    "Authorization": f"Bearer {login.json().get('token')}"
}
checkout = requests.post(url_checkout, data=param3, headers=headers3)

verify_status = checkout.json().get('success')
verify_message = checkout.json().get('message')

assert checkout.status_code == 500
assert verify_status == bool(False)
assert 'Aduh! ' in verify_message


# pprint(checkout.json().get('message')['order_items.0.stock_id'][0])