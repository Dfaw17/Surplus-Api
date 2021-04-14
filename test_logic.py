import requests
from env import sandbox
import pprint
from assertpy import assert_that

setting_env = sandbox
url_login = f"{setting_env}/api/v2/merchant/auth/login"
url_verify = f"{setting_env}/api/v2/merchant/verify-request"
email = "vd1@gmail.com"
kata_sandi = '12345678'
wrong_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvc3RhZ2luZy5hZG1pbnN1cnBsdXMubmV0XC9hcGlcL3YyXC9jdXN0b21lclwvYXV0aFwvbG9naW5cL2VtYWlsIiwiaWF0IjoxNjE2ODA1NzI2LCJleHAiOjE2MTkzOTc3MjYsIm5iZiI6MTYxNjgwNTcyNiwianRpIjoib05ESmxFRE5hSzNrN2RtVyIsInN1YiI6NDEyNiwicHJ2IjoiMjc0MTA1ZGE2ZTk1YmVmMjgwNzc4NmRkODczODg2N2NmOWMwMmFhYiJ9.fj51xIfQrqleRvdSJUbWcdrvsxQPUn8HpccnOmTgPDI'

param = {
    'email': email,
    'password': kata_sandi
}
headers = {
    "Accept": "application/json"
}
login = requests.post(url_login, params=param, headers=headers)
param2 = {
    'certifications[certifications][0][certification_id]': '1',
    'certifications[certifications][0][name]': 'aa',
    'informations[questions][0][information_id]': '1',
    'informations[questions][0][answer]': 'aaa',
    'informations[images][0][category]': 'kitchen'
}
headers2 = {
    "Accept": "application/json",
    "Authorization": f"Bearer {login.json().get('token')}"
}
file2 = {
    "certifications[images][0]": open("pisangnug.jpg", 'rb'),
    # "informations[images][0][images][0]": ''
}
verify_toko = requests.post(url_verify, params=param2, headers=headers2, files=file2)

validate_status = verify_toko.json().get('success')
validate_message = verify_toko.json().get('message')

assert verify_toko.status_code == 500
assert validate_status == bool(False)
assert 'Aduh!' in validate_message

# pprint.pprint(verify_toko.json())
