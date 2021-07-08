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

assert index_forum.status_code == 200
assert validate_status == bool(True)
assert 'Data forum berhasil ditemukan.' in validate_message


# print(index_forum.json())
print("Success Test")
