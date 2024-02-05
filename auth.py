import requests
from fake_useragent import UserAgent
from proxy_data import proxies

ua = UserAgent()


headers = {
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
    'User-Agent': f'{ua.random}',
}

token = {'token': 'Bearer null'}

json_data = {
    'username': 'anonymous',
    'password': 'hrgesf7HDR67Bd',
}


def get_auth(url='https://pub.fsa.gov.ru/login'):
    response = requests.post(
        url,
        headers=headers,
        json=json_data,
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
            verify=False)
    valid = response.text
    return valid


def get_token(token=token):
    if validation_token(token) == 'true':
        return token
    else:
        get_auth()


if __name__ == "__main__":
    get_token(token)
