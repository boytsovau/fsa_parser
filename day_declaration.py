import requests
from fake_useragent import UserAgent
import json
from auth import get_auth
import time


ua = UserAgent()

local_time = time.strftime("%Y-%m-%d")

Authorization = get_auth()  # Забираем токен авторизации

headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Authorization': f'{Authorization}',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Origin': 'https://pub.fsa.gov.ru',
        'Pragma': 'no-cache',
        'Referer': 'https://pub.fsa.gov.ru/rds/declaration',
        'User-Agent': f'{ua.random}',
    }


def get_day_declaration():

    """Функция запрашивает все декларации,
    которые были выпущены за текущий день"""

    json_data = {
        'size': 1000000,
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
                'minDate': f'{local_time}',
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

    s = requests.session()

    response = s.post(
        'https://pub.fsa.gov.ru/api/v1/rds/common/declarations/get',
        # cookies=cookies,
        headers=headers,
        json=json_data,
        verify=False,
    )

    with open('data.json', "w") as file:
        json.dump(response.json(), file, indent=4, ensure_ascii=False)


def get_declaration_day_sorted():
    collected_id = {}
    with open('data.json') as file:
        text = json.load(file)

    index = 0
    id = text.get('items')
    for item in id:
        declaration_id = item.get('id')
        declaration_number = item.get('number')
        date_regist = item.get('declDate')
        date_issue = item.get('declEndDate')
        applicant = item.get('applicantName')
        manufacturer = item.get('manufacterName')
        product_name = item.get('productFullName')

        collected_id[index] = {
            'id': declaration_id,
            'number': declaration_number,
            'Register Date': date_regist,
            'Issue Date': date_issue,
            'Applicant': applicant,
            'Manufacturer': manufacturer,
            'Production': product_name
        }
        index += 1

    with open('id_and_number.json', "w") as file:
        json.dump(collected_id, file, indent=4, ensure_ascii=False)


def main():
    get_day_declaration()
    get_declaration_day_sorted()


if __name__ == "__main__":
    main()
