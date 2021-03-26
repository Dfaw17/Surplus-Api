import requests
from env import stagging
from pprint import pprint
from assertpy import assert_that

setting_env = stagging
register_progress = f"{setting_env}/api/v2/customer/auth/register/progress"
email = "kopiruangvirtual@gmail.com"
kata_sandi = "12345678"

param = {
    'email' : "kopiruangvirtualgmail.com"
}
headers = {
    "Accept": "application/json"
}

response = requests.get(register_progress, params=param, headers=headers)
data = response.json()
# pprint(response.json())

validate_status = data.get('success')
validate_message = data.get('message')['email']

assert response.status_code == 422
assert validate_status == bool(False)
assert 'email harus merupakan alamat email yang valid.' in validate_message






