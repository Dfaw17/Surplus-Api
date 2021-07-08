import requests
from assertpy import assert_that

headers = {
    "Accept": "application/json",
    # "Authorization": f"Bearer {login.json().get('token')}"
}
url_show_forum = "https://5bb4e7db-1cd4-4003-ac9a-526e1696768c.mock.pstmn.io/api/v2/customer/forums/107"
show_forum = requests.get(url_show_forum, headers=headers)

validate_status = show_forum.json().get('success')
validate_message = show_forum.json().get('message')
validate_data = show_forum.json().get('data')

assert show_forum.status_code == 200
assert validate_status == bool(True)
assert 'Data forum berhasil ditemukan.' in validate_message
assert_that(validate_data).contains_only('id','user_id','forum_kategori_id','judul','konten','link','image','banyak_komentar','banyak_like','location','post_owner_name','email','category_name','badge_owner','is_post','is_like','is_report','is_bookmark','time_difference','images')


# print(show_forum.json())
print("Success Test Automation")
