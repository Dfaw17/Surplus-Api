import requests


url_login ="https://staging.adminsurplus.net/api/v2/merchant/auth/login"
email = "kopiruangvirtual@gmail.com"
kata_sandi = "12345678"

param = {
    "email": email,
    "password": ""
}

response =requests.post(url_login, data=param,
                        headers={'Accept': 'application/json'})
data = response.json()
validate_message = data.get("message")["password"]
print(validate_message)

assert "Kata sandi tidak boleh kosong." in validate_message
# assert response.status_code == 200