import requests
from assertpy import assert_that

param2 = {
            "origin": "-6.181663,106.805884",
            "destination": "-6.188844,106.847186",
            "id_stocks[0]": "54",
        }

headers2 = {
            "Accept": "application/json"
        }
url2 = "https://5bb4e7db-1cd4-4003-ac9a-526e1696768c.mock.pstmn.io/api/v2/customer/gosend/estimate"
gosend_estimate = requests.get(url2, params=param2, headers=headers2)

param3 = {
            "origin": "-6.181663,106.805884",
            "destination": "-6.188844,106.847186",
            "paymentType": "3",
        }

headers3 = {
            "Client-ID": "surplus-indonesia-engine",
            "Pass-Key": "de513a339c192d46a079f6f822b9e144fd50cb683df2dd374604e1add228ab58"
        }
url3 = "https://integration-kilat-api.gojekapi.com/gokilat/v10/calculate/price"
gosend_estimate_real = requests.get(url3, params=param3, headers=headers3)

validate_status = gosend_estimate.json().get('success')
validate_message = gosend_estimate.json().get('message')
validate_price = gosend_estimate.json().get('data')['instant']['price']
validate_price_real = gosend_estimate_real.json().get('Instant')['price']['total_price']

assert gosend_estimate.status_code == 200
assert validate_status == bool(True)
assert 'Gosend tersedia' in validate_message
assert_that(validate_price).is_equal_to(validate_price_real+float(1000))

print(validate_price)
print(validate_price_real+float(1000))
print("Success Test")
