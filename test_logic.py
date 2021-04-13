import requests
from env import stagging
from pprint import pprint
from assertpy import assert_that

setting_env = stagging
url_login = f"{setting_env}/api/v2/customer/auth/login/email"
url_discover = f"{setting_env}/api/v2/customer/discover"
url_delivery = f"{setting_env}/api/v2/customer/orders/delivery"
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
    "payment_method_id": "1",
    "is_lunchbox": "0",
    "donation_price": "2500",
    "voucher_id": "62",
    "order_items[0][qty]": "1",
    "order_items[0][stock_id]": discover.json().get('data')['nearby_menu'][0]['stock_id'],
    "address": "Megaregency",
    "note": "hai",
    "delivery_price": "20000",
    "delivery_method": "Instant",
    "origin_contact_name": "Fawwa 1",
    "origin_contact_phone": "081386356616",
    "origin_address": "Perumahan Megaregency 1",
    "origin_lat_long": "-6.3772882,107.1062917",
    "destination_contact_name": "Fawwaz 2",
    "destination_contact_phone": "085710819443",
    "destination_address": "Perumahan Megaregency 2",
    "destination_lat_long": "-6.3823027,107.1162164",
    "phone_number": "19:00"
}
headers3 = {
    "Accept": "application/json",
    "Authorization": f"Bearer {login.json().get('token')}"
}
delivery = requests.post(url_delivery, data=param3, headers=headers3)

verify_status = delivery.json().get('success')
verify_message = delivery.json().get('message')['phone_number']

assert delivery.status_code == 422
assert verify_status == bool(False)
assert "The No. HP format wrong." in verify_message

print(delivery.json())
# discover.json().get('data')['nearby_menu'][0]['stock_id']