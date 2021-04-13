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
    "order_items[0][qty]": "2",
    "order_items[0][stock_id]": discover.json().get('data')['nearby_menu'][0]['stock_id'],
    "address": "Megaregency",
    "note": "Test Notes",
    "delivery_price": "20000",
    "delivery_method": "Instant",
    "origin_contact_name": "Fawwaz 1",
    "origin_contact_phone": "081386356616",
    "origin_address": "Perumahan Megaregency 1",
    "origin_lat_long": "-6.3823027,107.1162164",
    "destination_contact_name": "Fawwaz 2",
    "destination_contact_phone": "0857108194",
    "destination_address": "Perumahan Megaregency 2",
    "destination_lat_long": "-6.3772882,107.1062917",
    "phone_number": "085710819443"
}
headers3 = {
    "Accept": "application/json",
    "Authorization": f"Bearer {login.json().get('token')}"
}
delivery = requests.post(url_delivery, data=param3, headers=headers3)

verify_status = delivery.json().get('success')
verify_message = delivery.json().get('message')
verify_data = delivery.json().get('data')
verify_data_merchant = delivery.json().get('data')['merchant']
verify_data_transaksi = delivery.json().get('data')['transaksi']

assert delivery.status_code == 201
assert verify_status == bool(True)
assert "Order Delivery berhasil dibuat" in verify_message
assert_that(verify_data).is_not_none()
assert_that(verify_data).contains_only('id', 'registrasi_order_number', 'alamat', 'status_order_id', 'canceled_by',
                                       'created_at', 'keterangan', 'ulasan', 'rating', 'merchant', 'transaksi')
assert_that(verify_data_merchant).contains_only('id', 'name', 'email', 'no_ponsel', 'alamat', 'auth_origin',
                                                'referal_code', 'onesignal_loc', 'latitude', 'longitude')
assert_that(verify_data_transaksi).contains_only('id', 'metode_pembayaran_id', 'order_id', 'invoice_id', 'invoice_url',
                                                 'invoice_expired', 'phone_number', 'subtotal', 'grand_total',
                                                 'grand_total_harga_asli', 'potongan_surplus', 'potongan_voucher',
                                                 'potongan_kotak_makan', 'hemat', 'komisi_merchant', 'komisi_surplus',
                                                 'kode', 'jenis_kode', 'is_tempat_makanan', 'image_lunchbox',
                                                 'is_dikirim', 'status_transaksi_id', 'status_pickup_id',
                                                 'step_progress', 'pickup_by_system', 'created_at', 'updated_at',
                                                 'voucher_id', 'shipment_price')

# pprint(delivery.json())
