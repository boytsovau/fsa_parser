import requests
from fake_useragent import UserAgent


ua = UserAgent()


headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'Authorization': 'Bearer null',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json',
    # 'Cookie': '_ym_uid=1684354438114283584; _ym_d=1684354438',
    'Origin': 'https://pub.fsa.gov.ru',
    'Referer': 'https://pub.fsa.gov.ru/rds/declaration',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': f'{ua.random}',
    'lkId': '',
    'orgId': '',
    'sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
}


json_data = {
    'username': 'anonymous',
    'password': 'hrgesf7HDR67Bd',
}


def get_auth(url='https://pub.fsa.gov.ru/login'):
    response = requests.post(url, headers=headers, json=json_data, verify=False)
    data = dict(response.headers)
    return data.get('Authorization')


# def main():
#     get_auth(url='https://pub.fsa.gov.ru/login')


# if __name__ == "__main__":
#     main()
