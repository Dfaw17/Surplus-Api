# import requests
# from env import stagging
#
# setting_env = stagging
# insert_menu = f"{setting_env}/api/v2/merchant/menus"
# url_login = f"{setting_env}/api/v2/merchant/auth/login"
# email = "kopiruangvirtual@gmail.com"
# kata_sandi = "12345678"
# wrong_token = "kyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvc3RhZ2luZy5hZG1pbnN1cnBsdXMubmV0XC9hcGlcL3YyXC9tZXJjaGFudFwvYXV0aFwvbG9naW4iLCJpYXQiOjE2MTU3MDExNDIsImV4cCI6MTYxODI5MzE0MiwibmJmIjoxNjE1NzAxMTQyLCJqdGkiOiJjOFluT3BlMzRqRVVIemZSIiwic3ViIjo0MDc3LCJwcnYiOiIyNzQxMDVkYTZlOTViZWYyODA3Nzg2ZGQ4NzM4ODY3Y2Y5YzAyYWFiIn0.xxI5o6tgIvb3Eds4CCfSnXM3ThFYiQwYcTCxKmrZozI"
#
# param = {
#     "email": email,
#     "password": kata_sandi
# }
# login = requests.post(url_login, data=param,
#                       headers={'Accept': 'application/json'})
# token = login.json().get("token")
# headers = {
#     "Authorization": f"Bearer {token}"
# }
#
# nama_makanan = "Pisang Nugget"
# merchant_kategori = 60
# deskripsi = "Pisang Nugget Mix"
# harga_asli = 20000
# harga_jual = 10000
# status_halal = 0
# param2 = {
#     "nama_menu_makanan": nama_makanan,
#     "deskripsi" : deskripsi,
#     "merchant_kategori_makanan_id": merchant_kategori,
#     "harga_asli": harga_asli,
#     "harga_jual": harga_jual,
#     "is_non_halal" : status_halal
# }
# response = requests.post(insert_menu,data=param2,headers=headers)
# data = response.text
#
# assert response.status_code == 422
# assert "Whoops, looks like something went wrong." in data
