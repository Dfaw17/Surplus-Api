import requests
from env import stagging
from assertpy import assert_that


setting_env = stagging
order_index = f"{setting_env}/api/v2/merchant/orders"
url_login = f"{setting_env}/api/v2/merchant/auth/login"
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
    "Authorization": f"Bearer {token}",
    "Accept":"application/json"
}
param2 = {

    "type":"1"
}

response= requests.get(order_index,params=param2, headers=headers)
data = response.json()

validate_status = data.get('success')
validate_message= data.get('message')['type']
print(data)
assert response.status_code == 422
assert validate_status == bool(False)
assert "type yang dipilih tidak tersedia." in validate_message



# response2 = requests.patch(set_active_menu+data_id+"/active", data=param2, headers=headers2)
# data = response2.json()

# print(data)
# validate_status = data.get('success')
# validate_message = data.get('message')['waktu_akhir_penjemputan']
# validate_menu = str(data.get('data')['id'])
# validate_status_menu = data.get('data')['is_tomorrow']
# validate_menu_stock = data.get('data')['stock']
# validate_menu_start = data.get('data')['waktu_mulai_penjemputan']
# validate_menu_end = data.get('data')['waktu_akhir_penjemputan']
#
# assert response2.status_code == 422
# assert validate_status == bool(False)
# print(validate_message)
# assert "Waktu akhir penjemputan tidak cocok dengan format H:i." in validate_message
# assert "Data tidak ditemukan" in validate_message
# assert validate_menu == data_id
# assert validate_status_menu == "0"
# assert validate_menu_stock == "100"
# assert validate_menu_start == "01:00"
# assert validate_menu_end == "23:00"




