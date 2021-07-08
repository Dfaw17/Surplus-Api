import requests
from assertpy import assert_that

headers = {
    "Accept": "application/json",
    # "Authorization": f"Bearer {login.json().get('token')}"
}
url_index_forum = "https://5bb4e7db-1cd4-4003-ac9a-526e1696768c.mock.pstmn.io/api/v2/customer/forums"
index_forum = requests.get(url_index_forum)

validate_status = index_forum.json().get('success')
validate_message = index_forum.json().get('message')
validate_data = index_forum.json().get('data')
validate_data_donation_event = index_forum.json().get('data')['donation_event']
validate_data_popular_posts = index_forum.json().get('data')['popular_posts']
validate_data_saved_posts = index_forum.json().get('data')['saved_posts']
validate_data_newest_posts = index_forum.json().get('data')['newest_posts']

assert index_forum.status_code == 200
assert validate_status == bool(True)
assert 'Data forum berhasil ditemukan.' in validate_message
assert_that(validate_data).contains_only('donation_event','popular_posts','liked_posts','saved_posts','newest_posts')
assert_that(validate_data_donation_event).is_type_of(list)
assert_that(validate_data_popular_posts).is_type_of(list)
assert_that(validate_data_saved_posts).is_type_of(list)
assert_that(validate_data_newest_posts).is_type_of(list)
assert_that(len(validate_data_donation_event)).is_equal_to(5)
assert_that(len(validate_data_popular_posts)).is_equal_to(5)
assert_that(len(validate_data_saved_posts)).is_equal_to(5)
assert_that(len(validate_data_newest_posts)).is_equal_to(5)
assert_that(validate_data_donation_event[0]).contains_only('id','user_id','category_id','judul','konten','link','image','banyak_komentar','banyak_like','location','post_owner_name','category_name','badge_owner','is_post','is_like','is_report','is_bookmark','time_difference','images')
assert_that(validate_data_popular_posts[0]).contains_only('id','user_id','category_id','judul','konten','link','image','banyak_komentar','banyak_like','location','post_owner_name','category_name','badge_owner','is_post','is_like','is_report','is_bookmark','time_difference','images')
assert_that(validate_data_saved_posts[0]).contains_only('id','user_id','category_id','judul','konten','link','image','banyak_komentar','banyak_like','location','post_owner_name','category_name','badge_owner','is_post','is_like','is_report','is_bookmark','time_difference','images')
assert_that(validate_data_newest_posts[0]).contains_only('id','user_id','category_id','judul','konten','link','image','banyak_komentar','banyak_like','location','post_owner_name','category_name','badge_owner','is_post','is_like','is_report','is_bookmark','time_difference','images')


# print(index_forum.json())
print("Success Test Automation")
