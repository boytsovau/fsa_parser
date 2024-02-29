import requests
import os
from fake_useragent import UserAgent


class FsaAuth:

    """ Данный класс получает токен авторизации и проверяет его валидность"""

    def __init__(self) -> None:
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
            'username': os.getenv('FSA_USERNAME'),
            'password': os.getenv('FSA_PASSWORD'),
        }

    def get_auth(self, url='https://pub.fsa.gov.ru/login'):

        """ Получение токена авторизации"""

        response = requests.post(url, headers=self.headers,
                                 json=self.json_data,
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

<<<<<<< HEAD
<<<<<<< HEAD
def get_auth(url='https://pub.fsa.gov.ru/login'):
    response = requests.post(
        url,
        headers=headers,
        json=json_data,
        proxies=proxies,
        verify=False)
    data = dict(response.headers)
    token['token'] = data.get('Authorization')


def validation_token(token):
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'ru-RU,ru;q=0.9',
        'Authorization': token.get('token'),
        'Connection': 'keep-alive',
        'Referer': 'https://pub.fsa.gov.ru/rds/declaration',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': f'{ua.random}',
    }
    response = requests.get(
            'https://pub.fsa.gov.ru/token/is/actual/',
            headers=headers,
            proxies=proxies,
            verify=False)
    valid = response.text
    return valid


def get_token(token=token):
    if validation_token(token) == 'true':
        return token
    else:
        get_auth()
=======
    def get_token(self):
=======
    def get_token(self) -> str:
>>>>>>> 0eb89e1 (optimize code)

        """ Получение токена, если есть существующий,
            то проверяется его валидность"""

        if self.validation_token() == 'true':
            return self.token
        else:
            self.get_auth()
<<<<<<< HEAD
>>>>>>> 0a3e18c (	modified:   auth.py)


# if __name__ == "__main__":
#     fsa_client = FsaAuth()
#     fsa_client.get_token()
=======
>>>>>>> 0eb89e1 (optimize code)
