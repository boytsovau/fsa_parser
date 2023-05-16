import requests
import json

def get_data(url):
    
    headers = {
        'Accept': 'application/json, text/plain, */*',
        # 'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Authorization': 'Bearer eyJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkZGRhZWNlOC1hNTA4LTRiZWQtYWZkMi1mZjAyZjQyNWRiNmUiLCJzdWIiOiJhbm9ueW1vdXMiLCJleHAiOjE2ODQyMDM1MzV9.iWz0dJcaDd20tswdcgvVEhzjH9Kj-Z_fVts7YybgUQjxwvlhacQAR4GlRBpCFhnD2E4WSGaiC--dt6-4bF6ZlA',
        # 'Cache-Control': 'no-cache',
        # 'Connection': 'keep-alive',
        # # 'Cookie': '_ym_uid=1684174734789640606; _ym_d=1684174734; _ym_isad=2; JSESSIONID=node0o8mhq9j2os2j1ozkuom1hds3043304945.node0',
        # 'Pragma': 'no-cache',
        # 'Referer': 'https://pub.fsa.gov.ru/rds/declaration/view/17692047/common',
        # 'Sec-Fetch-Dest': 'empty',
        # 'Sec-Fetch-Mode': 'cors',
        # 'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
        # 'lkId': '',
        # 'orgId': '',
        # 'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
        # 'sec-ch-ua-mobile': '?0',
        # 'sec-ch-ua-platform': '"macOS"',
    }

    json_data = {
       'items': {
        'validationFormNormDoc': [
            {
                'id': [28, ],
                'fields': [
                    'id',
                    'masterId',
                    'name',
                    'docNum',
                ],
            },
        ],
       },
    }


    response = requests.get(
        url,
        headers=headers,
        # json=json_data,
        verify=False
    )
    with open(f'test2.json', "w") as file:
        json.dump(response.json(), file, indent=4, ensure_ascii=False)


def main():
    get_data(url="https://pub.fsa.gov.ru/api/v1/rds/common/declarations/17692047")


if __name__ == "__main__":
    main()