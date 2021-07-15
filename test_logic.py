import requests
from env import *
from assertpy import *

setting_env = testing
url_history_income = f"{setting_env}/api/v2/merchant/reports/income-history"
url_login = f"{setting_env}/api/v2/merchant/auth/login"
email = "sdet@gmail.com"
kata_sandi = "12345678"
wrong_token = "kyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvc3RhZ2luZy5hZG1pbnN1cnBsdXMubmV0XC9hcGlcL3YyXC9tZXJjaGFudFwvYXV0aFwvbG9naW4iLCJpYXQiOjE2MTU3MDExNDIsImV4cCI6MTYxODI5MzE0MiwibmJmIjoxNjE1NzAxMTQyLCJqdGkiOiJjOFluT3BlMzRqRVVIemZSIiwic3ViIjo0MDc3LCJwcnYiOiIyNzQxMDVkYTZlOTViZWYyODA3Nzg2ZGQ4NzM4ODY3Y2Y5YzAyYWFiIn0.xxI5o6tgIvb3Eds4CCfSnXM3ThFYiQwYcTCxKmrZozI"

param = {
    "email": email,
    "password": kata_sandi
}
login = requests.post(url_login, data=param, headers={'Accept': 'application/json'})
token = login.json().get("token")
headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/json"
}
param = {
    "start_date": "2020-04-01",
    "end_date": "2022-04-01"
}
response = requests.get(url_history_income, params=param, headers=headers)
data = response.json()

validate_status = data.get("success")
validate_message = data.get("message")
validate_data = data.get("data")
validate_data_omset = data.get("data")['omset']
validate_data_total_transaksi = data.get("data")['total_transaksi']

assert response.status_code == 200
assert validate_status == bool(True)
assert "Data riwayat pemasukan berhasil ditemukan" in validate_message
assert_that(validate_data).contains_only('omset', 'total_transaksi', 'date_range')
assert_that(validate_data_omset).is_type_of(int)
assert_that(validate_data_total_transaksi).is_type_of(int)

print('Success Automation')
