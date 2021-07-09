import requests
from assertpy import assert_that

headers = {
    "Accept": "application/json",
    # "Authorization": f"Bearer {login.json().get('token')}"
}

param = {
    "forum_id": "414",
    "forum_komentar_id": "433",
    "forum_report_kategori_id": "4",
    "content": "Posting data pribadi"
}
url_report_comment = "https://5bb4e7db-1cd4-4003-ac9a-526e1696768c.mock.pstmn.io/api/v2/customer/reports/comment"
report_comment= requests.post(url_report_comment, headers=headers, params=param)

validate_status = report_comment.json().get('success')
validate_message = report_comment.json().get('message')

assert report_comment.status_code == 200
assert validate_status == bool(True)
assert 'Komentar berhasil dilaporkan! Admin Surplus akan menindaklanjuti pelaporan kamu ya' in validate_message

# print(report_comment.json())
print("Success Test Automation")
