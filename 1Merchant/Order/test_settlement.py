import requests
from env import stagging

class TestOrderIndex :

    global setting_env,order_settelemet,order_index,url_login,email,kata_sandi

    setting_env = stagging
    order_settelemet = f"{setting_env}/api/v2/merchant/orders/"
    order_index = f"{setting_env}/api/v2/merchant/orders"
    url_login = f"{setting_env}/api/v2/merchant/auth/login"
    email = "vd1@gmail.com"
    kata_sandi = "12345678"

    def test_settelement_sormal(self):
        param = {

            "email": email,
            "password": kata_sandi
        }
        login = requests.post(url_login, data=param, headers={'Accept': 'application/json'})
        token = login.json().get("token")
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json"
        }
        param2 = {

            "type": "ready_stock"
        }

        index = requests.get(order_index, params=param2, headers=headers)
        response = requests.post(order_settelemet + str(
        index.json().get('data')[0]['registrasi_order_number']) + "/settlement?_method=PATCH", headers=headers)
        data = response.json()

        message = data.get('message')
        print(response.json())
        assert response.status_code == 200
        assert 'Data pesanan berhasil diselesaikan' in message
