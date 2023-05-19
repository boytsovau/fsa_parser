import requests
import json
from day_declaration import get_day_declaration, Authorization, ua


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


def get_declaration():

    """Функция запрашивает информацию по декларации"""

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
                    'search': 'ЕАЭС N RU Д-ID.РА04.В.00364/23',
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

    with open('data_one_dec.json', "w") as file:
        json.dump(response.json(), file, indent=4, ensure_ascii=False)


def count_id_declaration():
    with open('data_one_dec.json') as file:
        text = json.load(file)
    id = text.get('items')[0].get('id')

    response = requests.get(
        url=f'https://pub.fsa.gov.ru/api/v1/rds/common/declarations/{id}',
        headers=headers,
        verify=False)

    with open('data_full_dec.json', "w") as file:
        json.dump(response.json(), file, indent=4, ensure_ascii=False)


def main():
    get_day_declaration()
    get_declaration()
    count_id_declaration()


if __name__ == "__main__":
    main()
