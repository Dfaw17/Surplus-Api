import requests
from env import stagging
from pprint import pprint
from assertpy import assert_that

setting_env = stagging
check_email = f"{setting_env}/api/v2/customer/auth/register/check-email"
email_has_registered = "kopiruangvirtual@gmail.com"
email_hasnt_registered = "abc@gmail.com"

param = {
    'email' : 'kopiruangvirtualgmail.com'
}
headers = {
    "Accept": "application/json"
}

response = requests.post(check_email, params=param, headers=headers)
data = response.json()
pprint(data)

validate_status = data.get('success')
validate_message = data.get('message')['email']

assert response.status_code == 422
assert validate_status == bool(False)
assert 'email harus merupakan alamat email yang valid.' in validate_message






