import requests
from env import stagging
from pprint import pprint
from assertpy import assert_that

setting_env = stagging
url_login = f"{setting_env}/api/v2/customer/auth/login/email"
url_forum = f"{setting_env}/api/v2/customer/forums"
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
update_passwrod = requests.get(url_forum, params=param2, headers=headers2)

validate_status = update_passwrod.json().get('success')
validate_message = update_passwrod.json().get('message')
validate_data = update_passwrod.json().get('data')
validate_data_forums = update_passwrod.json().get('data')['forums']
validate_data_categories = update_passwrod.json().get('data')['categories'][0]
validate_data_report_categories = update_passwrod.json().get('data')['report_categories'][0]
validate_data_forums_data = update_passwrod.json().get('data')['forums']['data'][0]

assert update_passwrod.status_code == 200
assert validate_status == bool(True)
assert 'Data forum berhasil ditemukan.' in validate_message
assert_that(validate_data).contains_only('forums', 'categories', 'report_categories')
assert_that(validate_data_forums).contains_only('current_page', 'data', 'first_page_url', 'from', 'last_page',
                                                'last_page_url', 'next_page_url', 'path', 'per_page', 'prev_page_url',
                                                'to', 'total')
assert_that(validate_data_categories).contains_only('id', 'kategori', 'created_at', 'updated_at')
assert_that(validate_data_report_categories).contains_only('id', 'nama', 'created_at', 'updated_at')
assert_that(validate_data_forums_data).contains_only('id', 'user_id', 'forum_kategori_id', 'judul', 'konten', 'link',
                                                     'image', 'banyak_komentar', 'banyak_like', 'location',
                                                     'post_owner_name', 'category_name', 'badge_owner', 'is_post',
                                                     'is_like', 'is_report', 'is_bookmark', 'time_difference', 'images')

# pprint(update_passwrod.json())
