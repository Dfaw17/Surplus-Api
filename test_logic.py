import requests
from env import sandbox
from pprint import pprint
from assertpy import assert_that

setting_env = sandbox
resend_otp = f"{setting_env}/api/v2/customer/auth/register/otp/resend"
email = "daffafawwazmaulana170901@gmail.com"

param = {
    'email': "daffafawwazmaulana170901 @gmail.com"
}
headers = {
            "Accept": "application/json"
}

response = requests.post(resend_otp, data=param,headers=headers)
data = response.json()
pprint(data)
validate_status = data.get('success')
validate_message = data.get('message')

assert  response.status_code == 500
assert validate_status == bool(False)
assert 'Whoops, looks like something went wrong' in validate_message
