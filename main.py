import requests
from fake_useragent import UserAgent
import json


ua = UserAgent()

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Content-Type': 'application/json',
    'User-Agent': f'{ua.random}',
    'Origin': 'https://pub.fsa.gov.ru'
    
}

json_data = {
    'username': 'anonymous',
}

def get_cookies(url):
    response = requests.get(url, headers=headers, verify=False)

    with open(f'login.json', "w") as file:
        json.dump(response.json(), file, indent=4, ensure_ascii=False)


    # with open(f'cook.txt ', "w") as file:
    #     file.write(response.text)


def main():
    get_cookies(url="https://pub.fsa.gov.ru/lk/api/account")


if __name__ == '__main__':
    main()
