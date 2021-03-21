import requests
from env import stagging

setting_env = stagging
update_menu = f"{setting_env}/api/v2/merchant/menus/"
url_get_all_merchant_menu = f"{setting_env}/api/v2/merchant/menus/"
url_login = f"{setting_env}/api/v2/merchant/auth/login"
email = "vd1@gmail.com"
kata_sandi = "12345678"
wrong_token = "kyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvc3RhZ2luZy5hZG1pbnN1cnBsdXMubmV0XC9hcGlcL3YyXC9tZXJjaGFudFwvYXV0aFwvbG9naW4iLCJpYXQiOjE2MTU3MDExNDIsImV4cCI6MTYxODI5MzE0MiwibmJmIjoxNjE1NzAxMTQyLCJqdGkiOiJjOFluT3BlMzRqRVVIemZSIiwic3ViIjo0MDc3LCJwcnYiOiIyNzQxMDVkYTZlOTViZWYyODA3Nzg2ZGQ4NzM4ODY3Y2Y5YzAyYWFiIn0.xxI5o6tgIvb3Eds4CCfSnXM3ThFYiQwYcTCxKmrZozI"

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

headers = {
    "Authorization": f"Bearer {token}"
}
nama_makanan = "Pisang Nugget"
merchant_kategori = 60
deskripsi = "Pisang Nugget Mix"
harga_asli = 20000
harga_jual = 10000
status_halal = 0
param2 = {
    "nama_menu_makanan" : nama_makanan,
    "deskripsi" : deskripsi,
    "merchant_kategori_makanan_id": merchant_kategori,
    "harga_jual": harga_jual,
    "harga_asli": harga_asli,
    "is_non_halal" : status_halal
}

response2 = requests.post(update_menu + data_id + "?_method=PUT", data=param2, headers=headers,
                                  files={'image': ""})
data = response2.text

# print(data)
assert response2.status_code == 422
assert "Whoops, looks like something went wrong" in data
# validate_status = data.get("success")
# validate_message = data.get("message")
# validate_id = str(data.get("data")["id"])
# validate_nama_menu_makanan = str(data.get("data")["nama_menu_makanan"])
# validate_merchant_kategori_makanan_id = data.get("data")["merchant_kategori_makanan_id"]
# validate_deskripsi = data.get("data")["deskripsi"]
# validate_harga_asli = data.get("data")["harga_asli"]
# validate_harga_jual = data.get("data")["harga_jual"]
# validate_is_non_halal = data.get("data")["is_non_halal"]
#
# assert validate_status == bool(True)
# assert nama_makanan in validate_message
# assert data_id == validate_id
# assert validate_nama_menu_makanan == nama_makanan
# assert validate_merchant_kategori_makanan_id == merchant_kategori
# assert validate_deskripsi == deskripsi
# assert validate_harga_asli ==harga_asli
# assert harga_jual == harga_jual
# assert validate_is_non_halal == status_halal

