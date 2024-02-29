import requests
import os
from fake_useragent import UserAgent


class FsaAuth:

    """ Данный класс получает токен авторизации и проверяет его валидность"""

    def __init__(self):
        self.ua = UserAgent()
        self.headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'Authorization': os.getenv('FSA_TOKEN'),
            'Connection': 'keep-alive',
            'Content-Type': 'application/json',
            'Origin': 'https://pub.fsa.gov.ru',
            'Referer': 'https://pub.fsa.gov.ru/rds/declaration',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': f'{self.ua.random}',
        }
        self.token = {'token': os.getenv('FSA_TOKEN')}
        self.json_data = {
            'username': 'anonymous',
            'password': 'hrgesf7HDR67Bd',
        }

    def get_auth(self, url='https://pub.fsa.gov.ru/login'):

        """ Получение токена авторизации"""

        response = requests.post(url, headers=self.headers,
                                 json=self.json_data,
                                 verify=False)
        data = dict(response.headers)
        self.token['token'] = data.get('Authorization')
        os.environ['FSA_TOKEN'] = self.token['token']

    def validation_token(self):

        """ Проверка токена на валидность"""

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
        response = requests.get('https://pub.fsa.gov.ru/token/is/actual/',
                                headers=headers, verify=False)
        valid = response.text
        return valid

    def get_token(self):

        """ Получение токена, если есть существующий,
            то проверяется его валидность"""

        if self.validation_token() == 'true':
            return self.token
        else:
            self.get_auth()


if __name__ == "__main__":
    fsa_client = FsaAuth()
    fsa_client.get_token()
