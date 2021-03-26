import requests
from env import stagging
from pprint import pprint
from assertpy import assert_that

setting_env = stagging
login_email = f"{setting_env}/api/v2/customer/auth/login/email"
email = "kopiruangvirtual@gmail.com"
kata_sandi = "12345678"

param = {
    'email': 'kopiruangvirtualgmail.com',
    'password': kata_sandi
}
headers = {
    "Accept": "application/json"
}

response = requests.post(login_email, data=param, headers=headers)
data = response.json()
pprint(data)
validate_status = data.get('success')
validate_message = data.get('message')['email']

assert response.status_code == 422
assert validate_status == bool(False)
assert 'email harus merupakan alamat email yang valid.' in validate_message
