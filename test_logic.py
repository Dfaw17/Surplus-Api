import requests
from env import sandbox
from pprint import pprint
from assertpy import assert_that

setting_env = sandbox
register_oauth = f"{setting_env}/api/v2/customer/auth/register/oauth"
login_oauth = f"{setting_env}/api/v2/customer/auth/login/oauth"
delete_account = f"{setting_env}/api/v2/customer/profiles"
email = "daffafawwazmaulana170901@gmail.com"
origin_id = "2840811776172986"
origin = "facebook"

param = {
    'email' : 'halogmail.com',
    'origin': 'facebookk',
    'id_from_origin':origin_id
}
headers = {
            "Accept": "application/json"
}
response = requests.post(register_oauth, data=param, headers=headers)
data = response.json()
pprint(data)
validate_status = data.get('success')
validate_message = data.get('message')['origin']

assert  response.status_code == 422
assert validate_status == bool(False)
assert 'Sosial media hanya boleh Google atau Facebook' in validate_message
