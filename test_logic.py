import requests


url_reset_pass = "https://staging.adminsurplus.net/api/v2/merchant/auth/password-reset"
email = "kopiruangvirtual@gmail.com"

param = {
    "email": email
}

response =requests.post(url_reset_pass, data=param,
                        headers={'Accept': 'application/json'})

data = response.json()
validate_status = data.get("success")
validate_message = data.get("message")
print(validate_message)
assert validate_status == bool(True)
assert response.status_code == 200
assert "Kami mengirimkan link untuk reset password ke e-mail" in validate_message
