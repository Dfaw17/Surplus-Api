import requests
from assertpy import assert_that

url_profile= "https://staging.adminsurplus.net//api/v2/merchant/profiles"
url_login = "https://staging.adminsurplus.net/api/v2/merchant/auth/login"
email = "kopiruangvirtual@gmail.com"
kata_sandi = "12345678"

param = {
            "email": email,
            "password": kata_sandi
        }
login =requests.post(url_login, data=param,
                                headers={'Accept': 'application/json'})
token = login.json().get("token")
headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {token}"
        }
response = requests.get(url_profile, headers = headers)
data = response.json()

print(data)

validate_status = data.get("success")
validate_message = data.get("message")
validate_data = data.get("data")["name"]
validate_email = data.get("data")["email"]
validate_outlet = data.get("data")["outlet"]
validate_location = data.get("data")["location"]

print(validate_outlet)

assert validate_status == bool(True)
assert response.status_code == 200
assert "Data merchant ditemukan." in validate_message
assert_that(validate_data).is_not_empty()
assert_that(validate_outlet).is_not_empty()
assert_that(validate_location).is_not_empty()
assert validate_email == email
# assert validate_data >= 1
