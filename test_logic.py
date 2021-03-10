import requests


url_reset_pass = "https://staging.adminsurplus.net/api/v2/merchant/categories"
email = "kopiruangvirtual@gmail.com"

headers = {
    "Accept":"application/json",
    "Authorization":"Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvc3RhZ2luZy5hZG1pbnN1cnBsdXMubmV0XC9hcGlcL3YyXC9tZXJjaGFudFwvYXV0aFwvbG9naW4iLCJpYXQiOjE2MTUyODExOTcsImV4cCI6MTYxNzg3MzE5NywibmJmIjoxNjE1MjgxMTk3LCJqdGkiOiIyMHlLU2xEdXY0V1N3cTFBIiwic3ViIjo0MDc3LCJwcnYiOiIyNzQxMDVkYTZlOTViZWYyODA3Nzg2ZGQ4NzM4ODY3Y2Y5YzAyYWFiIn0.HaIqvP33rkandP7whxqPtt6h65KWA4RzYiN3hMreNt8"
}

response =requests.get(url_reset_pass,headers=headers)

data = response.json()
validate_available_category = len(data.get("data"))
print(validate_available_category)
# assert validate_status == bool(True)
# assert response.status_code == 200
# assert "Kami mengirimkan link untuk reset password ke e-mail" in validate_message
