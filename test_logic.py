import requests
from env import stagging
from pprint import pprint
from assertpy import assert_that

setting_env = stagging
url_login = f"{setting_env}/api/v2/customer/auth/login/email"
url_forum = f"{setting_env}/api/v2/customer/forums"
url_forum_store_comment = f"{setting_env}/api/v2/customer/comments"
email = "kopiruangvirtual@gmail.com"
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
headers2 = {
    "Accept": "application/json",
    "Authorization": f"Bearer {login.json().get('token')}"
}
param2 = {
    'forum_category_id': '1',
    'perPage': '5',
    'page': '1'
}
index_forum = requests.get(url_forum, params=param2, headers=headers2)
headers3 = {
    "Accept": "application/json",
    "Authorization": f"Bearer {login.json().get('token')}"
}
param3 = {
    "forum_id": index_forum.json().get('data')['forums']['data'][0]['id'],
    # "comment": "Test komentar sendiri"
}
store_comment = requests.post(url_forum_store_comment, params=param3, headers=headers3)

validate_status = store_comment.json().get('success')
validate_message = store_comment.json().get('message')['comment']


assert store_comment.status_code == 422
assert validate_status == bool(False)
assert "Komentar tidak boleh kosong." in validate_message


pprint(store_comment.json())
