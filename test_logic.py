import requests


url_all_category = "https://staging.adminsurplus.net/api/v2/merchant/categories"
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
response = requests.get(url_all_category)
data = response.text

assert "Unauthorized" in data

# validate_status = data.get("success")
# validate_message = data.get("message")
# validate_data = len(data.get("data"))

# assert validate_status == bool(True)
# assert response.status_code == 200
# assert "Data menu ditemukan." in validate_message
# assert validate_data >= 1
