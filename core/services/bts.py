import requests
from settings import BTS_API_URL

API_URL = 'https://api.nav.by/info/'
TOKEN_API_URL = f"{API_URL}integration_get_token.php"
DISPATCH_API_URL = f"{API_URL}integration.php"

class BtsAPIClient():
    def __init__(self, token, login=None, password=None):
        self.token = token
        self.login = login
        self.password = password
        if not self.token:
            self.token = self.get_token()

    def get_token(self):
        type = "GET_TOKEN"
        url = f"{TOKEN_API_URL}?type={type}&login={self.login}&password={self.password}"

        response = requests.get(url)
        if response.status_code == 200:
            response = response.json()
            return response['token']
        return None

    def get_vehicle_list(self):
        type = "VEHICLE_LIST"
        url = f"{DISPATCH_API_URL}?type={type}&token={self.token}"

        response = requests.get(url)
        if response.status_code == 200:
            response = response.json()
            items = response['root']['result']['items']
            return items

    def get_current_position(self, object_id=None):
        type = "CURRENT_POSITION"
        url = f"{DISPATCH_API_URL}?type={type}&token={self.token}"

        if object_id:
            url = f"{url}&object_id={object_id}"

        response = requests.get(url)
        if response.status_code == 200:
            response = response.json()
            return response['root']['result']['items']


