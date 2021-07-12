import requests
from assertpy import assert_that

headers = {
    "Accept": "application/json",
    # "Authorization": f"Bearer {login.json().get('token')}"
}

page = 1
per_page = 5
forum_category_id = 2

param = {
    "list_owner": "all",
    "event": "newest",
    "forum_category_id": forum_category_id,
    "per_page": per_page,
    "page": page,
    "long_posted_time": "7_days",
    "has_image": "1",
    "has_link": "1"
}
url_search_filter_comment = "https://5bb4e7db-1cd4-4003-ac9a-526e1696768c.mock.pstmn.io/api/v2/customer/search-forums"
search_filter_comment = requests.get(url_search_filter_comment, headers=headers, params=param)

validate_status = search_filter_comment.json().get('success')
validate_message = search_filter_comment.json().get('message')
validate_data = search_filter_comment.json().get('data')
validate_data_page = search_filter_comment.json().get('data')['current_page']
validate_per_page = search_filter_comment.json().get('data')['per_page']
validate_post = search_filter_comment.json().get('data')['posts']
post_address = [d['location'] for d in validate_post]
post_link = [d['image'] for d in validate_post]
post_image = [d['link'] for d in validate_post]
post_forum_category_id = [d['forum_kategori_id'] for d in validate_post]

assert search_filter_comment.status_code == 200
assert validate_status == bool(True)
assert 'Data forum berhasil ditemukan.' in validate_message
assert_that(validate_data_page).is_equal_to(page)
assert_that(validate_per_page).is_equal_to(per_page)
assert_that(len(validate_data['posts'])).is_equal_to(per_page)
assert_that(post_link).does_not_contain(None)
assert_that(post_image).does_not_contain(None)
assert_that(post_forum_category_id).contains_only(forum_category_id)

# print(a)
print("Success Test Automation")
