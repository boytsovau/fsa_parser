import requests
import json

cookies = {
    '_ym_uid': '1684174734789640606',
    '_ym_d': '1684174734',
    '_ym_isad': '2',
    'JSESSIONID': 'D87879CBA7E66258FD79B1280F541959',
}

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    #'Authorization': 'Bearer eyJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJhYmFjMjkxOS0xODNhLTRhODctYmE1Zi04NDVkMTNlNTkzMzMiLCJzdWIiOiJhbm9ueW1vdXMiLCJleHAiOjE2ODQyNTAyMzV9._nETvX_Dbh1aMLj6V7JY1LkOumQUkvuc1KvzzejfLgwq7FJuRB1wjoJOEm7_ME5RTSnrKpOiKZEPK2nllLh8ag',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json',
    # 'Cookie': '_ym_uid=1684174734789640606; _ym_d=1684174734; _ym_isad=2; JSESSIONID=D87879CBA7E66258FD79B1280F541959',
    'Origin': 'https://pub.fsa.gov.ru',
    'Pragma': 'no-cache',
    # 'Referer': 'https://pub.fsa.gov.ru/rds/declaration/view/17695724/common',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
    'lkId': '',
    'orgId': '',
    'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
}

def get_data(url):
    json_data = {
        'size': 10,
        'page': 0,
        'filter': {
            'status': [],
            'idDeclType': [],
            'idCertObjectType': [],
            'idProductType': [],
            'idGroupRU': [],
            'idGroupEEU': [],
            'idTechReg': [],
            'idApplicantType': [],
            'regDate': {
                'minDate': None,
                'maxDate': None,
            },
            'endDate': {
                'minDate': None,
                'maxDate': None,
            },
            'columnsSearch': [
                {
                    'name': 'number',
                    'search': '',
                    'type': 9,
                    'translated': False,
                },
            ],
            'idProductOrigin': [],
            'idProductEEU': [],
            'idProductRU': [],
            'idDeclScheme': [],
            'awaitForApprove': None,
            'awaitOperatorCheck': None,
            'editApp': None,
            'violationSendDate': None,
            'isProtocolInvalid': None,
            'resultChecker': None,
            'statusChecker': None,
            'protocolsChecker': None,
            'mistakeFound': None,
        },
        'columnsSort': [
            {
                'column': 'declDate',
                'sort': 'DESC',
            },
        ],
    }
    s = requests.Session()
    response = s.post(
        url,
        cookies=cookies,
        headers=headers,
        json=json_data,
        verify=False
    )
    with open(f'test.json', "w") as file:
        json.dump(response.json(), file, indent=4, ensure_ascii=False)


def get_data_declaration(url):
    # s = requests.Session()

    response = requests.get(url, cookies=cookies, headers=headers, verify=False)
    with open(f'test2.json', "w") as file:
        json.dump(response.json(), file, indent=4, ensure_ascii=False)



def main():
    get_data(url="https://pub.fsa.gov.ru/api/v1/rds/common/declarations/get")
    #get_data_declaration(url='https://pub.fsa.gov.ru/api/v1/rds/common/declarations/17695724')

if __name__ == "__main__":
    main()

