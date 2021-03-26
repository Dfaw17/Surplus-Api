import requests
from env import stagging
from pprint import pprint
from assertpy import assert_that

setting_env = stagging
reset_password = f"{setting_env}/api/v2/customer/auth/password-reset"
email_has_registered = "kopiruangvirtual@gmail.com"
email_hasnt_registered = "abc@gmail.com"

param = {
    'email' : ''
}
headers = {
    "Accept": "application/json"
}

response = requests.post(reset_password, params=param, headers=headers)
data = response.json()
pprint(data)

validate_status = data.get('success')
validate_message = data.get('message')['email']
#
assert response.status_code == 422
assert validate_status == bool(False)
assert 'email tidak boleh kosong.' in validate_message






