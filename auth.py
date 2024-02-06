import requests
from fake_useragent import UserAgent
from proxy_data import proxies
from dotenv import load_dotenv


load_dotenv()

class FsaAuth:
    def __init__(self):
        self.ua = UserAgent()
        self.headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'Authorization': 'Bearer null',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json',
            'Origin': 'https://pub.fsa.gov.ru',
            'Referer': 'https://pub.fsa.gov.ru/rds/declaration',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': f'{self.ua.random}',
        }
        self.token = {'token': 'Bearer null'}
        self.json_data = {
            'username': 'anonymous',
            'password': 'hrgesf7HDR67Bd',
        }

    def get_auth(self, url='https://pub.fsa.gov.ru/login'):
        response = requests.post(url, headers=self.headers, json=self.json_data, verify=False)
        data = dict(response.headers)
        self.token['token'] = data.get('Authorization')

    def validation_token(self):
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'ru-RU,ru;q=0.9',
            'Authorization': self.token.get('token'),
            'Connection': 'keep-alive',
            'Referer': 'https://pub.fsa.gov.ru/rds/declaration',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': f'{self.ua.random}',
        }
        response = requests.get('https://pub.fsa.gov.ru/token/is/actual/', headers=headers, verify=False)
        valid = response.text
        return valid

    def get_token(self):
        if self.validation_token() == 'true':
            return self.token
        else:
            self.get_auth()


if __name__ == "__main__":
    fsa_client = FsaAuth()
    fsa_client.get_token()
