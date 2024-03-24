import requests
import os
from fake_useragent import UserAgent


class FsaAuth:

    """ Данный класс получает токен авторизации и проверяет его валидность"""

    def __init__(self) -> None:
        self.ua = UserAgent()
        self.proxies = {
            'https': f"http://{os.getenv('PROXYUSER')}:{os.getenv('PROXYPASS')}@{os.getenv('PROXYIP')}"}
        self.headers = {
            'Accept': 'application/json, text/plain, */*',
            'Authorization': os.getenv('FSA_TOKEN'),
            'Content-Type': 'application/json',
            'Origin': 'https://pub.fsa.gov.ru',
            'User-Agent': f'{self.ua.random}',
        }
        self.token = {'token': os.getenv('FSA_TOKEN')}
        self.json_data = {
            'username': os.getenv('FSA_USERNAME'),
            'password': os.getenv('FSA_PASSWORD'),
        }

    def get_auth(self, url='https://pub.fsa.gov.ru/login'):
        """ Получение токена авторизации"""

        response = requests.post(url, headers=self.headers,
                                 json=self.json_data,
                                 proxies=self.proxies,
                                 verify=False)
        data = dict(response.headers)
        os.environ['FSA_TOKEN'] = data.get('Authorization')

    def validation_token(self) -> bool:
        """ Проверка токена на валидность"""

        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'ru-RU,ru;q=0.9',
            'Authorization': self.token.get('token'),
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': f'{self.ua.random}',
        }
        response = requests.get('https://pub.fsa.gov.ru/token/is/actual/',
                                headers=headers,
                                proxies=self.proxies,
                                verify=False)
        valid = response.text
        return valid

    def get_token(self) -> str:
        """ Получение токена, если есть существующий,
            то проверяется его валидность"""

        if self.validation_token() == 'true':
            return self.token
        else:
            self.get_auth()
