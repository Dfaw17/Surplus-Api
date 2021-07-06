import requests
from assertpy import assert_that

url = "https://5bb4e7db-1cd4-4003-ac9a-526e1696768c.mock.pstmn.io/api/v2/customer/profile-forums"
test = requests.get(url, headers={'Accept': 'application/json'})

validate_status = test.json().get('success')
validate_message = test.json().get('message')
validate_owner = test.json().get('data')['post_owner_name']
validate_badge_owner = test.json().get('data')['badge_owner']
validate_total_post = test.json().get('data')['total_post']
validate_total_like = test.json().get('data')['total_like']
validate_total_saved = test.json().get('data')['total_saved']
validate_forums = test.json().get('data')['forums']
calculate_like = sum([a['banyak_like'] for a in validate_forums])
calculate_saved = sum([a['banyak_disimpan'] for a in validate_forums])

assert test.status_code == 200
assert validate_status == bool(True)
assert 'Data profile forum ditemukan.' in validate_message
assert_that(validate_owner).is_not_empty() and assert_that(validate_owner).is_not_none()
assert_that(validate_badge_owner).is_not_none()
assert_that(validate_total_post).is_not_none()
assert_that(validate_total_like).is_not_none()
assert_that(validate_total_saved).is_not_none()
assert_that(validate_forums).is_type_of(list)
assert_that(validate_total_post).is_equal_to(len(validate_forums))
assert_that(validate_total_like).is_equal_to(calculate_like)
assert_that(validate_total_saved).is_equal_to(calculate_saved)
assert_that(test.json().get('data')).contains_only('post_owner_name', 'badge_owner', 'total_post', 'total_like',
                                                   'total_saved', 'forums')

print("Success Test")
# print(test.json())
