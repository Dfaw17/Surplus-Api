import requests
from env import stagging

setting_env = stagging
insert_menu = f"{setting_env}/api/v2/merchant/menus"
url_login = f"{setting_env}/api/v2/merchant/auth/login"
email = "kopiruangvirtual@gmail.com"
kata_sandi = "12345678"

param = {
    "email": email,
    "password": kata_sandi
}
login = requests.post(url_login, data=param,
                      headers={'Accept': 'application/json'})
token = login.json().get("token")
headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/json"
}

nama_makanan = "Pisang Nugget"
merchant_kategori = 60
deskripsi = "Pisang Nugget Mix"
harga_asli = 20000
harga_jual = 10000
status_halal = 0
param2 = {
    "nama_menu_makanan": nama_makanan,
    "merchant_kategori_makanan_id": merchant_kategori,
    "deskripsi":deskripsi,
    "harga_asli":harga_asli,
    "harga_jual":harga_jual,
    "is_non_halal":status_halal
}
response = requests.post(insert_menu,data=param2,headers=headers, files={'image':open("pisangnug.jpg",'rb')})
data = response.json()

validate_status = data.get("success")
validate_message = data.get("message")
validate_nama_menu = data.get("data")["nama_menu_makanan"]
validate_merchant_kategori = data.get("data")["merchant_kategori_makanan_id"]
validate_deskripsi = data.get("data")["deskripsi"]
validate_harga_asli = data.get("data")["harga_asli"]
validate_harga_jual = data.get("data")["harga_jual"]
validate_status_halal = data.get("data")["is_non_halal"]

assert response.status_code == 201
assert validate_status == bool(True)
assert f"Data menu {nama_makanan} berhasil ditambahkan." in validate_message
assert validate_nama_menu == nama_makanan
assert validate_merchant_kategori == merchant_kategori
assert validate_deskripsi == deskripsi
assert validate_harga_asli == harga_asli
assert validate_harga_jual == harga_jual
assert validate_status_halal == status_halal
