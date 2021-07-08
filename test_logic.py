import requests
from assertpy import assert_that

headers = {
    "Accept": "application/json",
    # "Authorization": f"Bearer {login.json().get('token')}"
}
param = {
    "forum_id" : "107"
}
url_show_forum = "https://5bb4e7db-1cd4-4003-ac9a-526e1696768c.mock.pstmn.io/api/v2/customer/comments"
show_forum = requests.get(url_show_forum, headers=headers, params=param)

validate_status = show_forum.json().get('success')
validate_message = show_forum.json().get('message')
validate_data = show_forum.json().get('data')[0]

assert show_forum.status_code == 200
assert validate_status == bool(True)
assert 'Komentar ditemukan' in validate_message
assert_that(validate_data).contains_only('id','user_id','forum_id','komentar','banyak_like','created_at','updated_at','is_like','time_difference','is_report','is_post','commenter','email','commenter_badge')


# print(show_forum.json())
print("Success Test Automation")
