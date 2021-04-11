import requests
from env import stagging
from pprint import pprint
from assertpy import assert_that

setting_env = stagging
url_login = f"{setting_env}/api/v2/customer/auth/login/email"
url_list_order = f"{setting_env}/api/v2/customer/orders"
url_detail_order = f"{setting_env}/api/v2/customer/orders/"
url_show_payment_status = f"{setting_env}/api/v2/customer/orders/"
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
headers2 = {
    "Accept": "application/json",
    "Authorization": f"Bearer {login.json().get('token')}"
}
param2 = {
    'status_order': 'done'
}
list_order = requests.get(url_list_order,params=param2 , headers=headers2)
detail_order = requests.get(url_detail_order + list_order.json().get('data')[0]['registrasi_order_number'], headers=headers2)
headers3 = {
    "Accept": "application/json",
    "Authorization": f"Bearer {login.json().get('token')}"
}
param3 = {
    # 'payment_method': detail_order.json().get('data')['metode_pembayaran']
}
show_payment = requests.get(url_show_payment_status +'S2104080334264'+ '/payment-status',params=param3, headers=headers3)

validate_status = show_payment.json().get('success')
validate_message = show_payment.json().get('message')['payment_method']

assert show_payment.status_code == 422
assert validate_status == bool(False)
assert 'Metode Pembayaran tidak boleh kosong.' in validate_message



pprint(show_payment.json())
