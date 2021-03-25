import requests
from env import stagging
from pprint import pprint
from assertpy import assert_that
from faker import Faker
fake = Faker()




setting_env = stagging
register_email = f"{setting_env}/api/v2/customer/auth/register/email"
email = fake.email()
kata_sandi = "12345678"
email_has_registered = 'kopiruangvirtual@gmail.com'

headers = {
    "Accept":"application/json"
}
param = {

    "email": email,
    'password': 'kata_sandi',
    're-password':'12345678'
}
response = requests.post(register_email, data=param,headers=headers)
data = response.json()

validate_status = data.get('success')
validate_message = data.get('message')['re-password']


assert  response.status_code == 422
assert validate_status == bool(False)
assert 're-password dan Kata sandi harus sama.' in validate_message

pprint(response.json())