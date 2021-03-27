import requests
from env import stagging
from pprint import pprint
from assertpy import assert_that

setting_env = stagging
register_oauth = f"{setting_env}/api/v2/customer/auth/register/oauth"
login_oauth = f"{setting_env}/api/v2/customer/auth/login/oauth"
delete_oauth = f"{setting_env}/api/v2/customer/profiles"
email = "daffafawwazmaulana170901@gmail.com"
origin = "facebook"
id_origin = "2840811776172986"


param = {
    'email': email,
    'origin' : origin,
    'id_from_origin' : ''
}
headers = {
    "Accept": "application/json"
}

# register = requests.post(register_oauth, params=param, headers=headers)
# loginfailed = requests.post(login_oauth, params=param_failed, headers=headers)
login = requests.post(login_oauth, params=param, headers=headers)
# delete = requests.delete(delete_oauth,  headers={"Authorization": f"Bearer {login.json().get('token')}"})

validate_status = login.json().get('success')
validate_message = login.json().get('message')['id_from_origin']

assert login.status_code == 422
assert validate_status == bool(False)
assert 'id from origin tidak boleh kosong.' in validate_message


pprint(login.json())







