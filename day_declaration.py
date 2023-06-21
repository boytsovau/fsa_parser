import requests
import json
import time
from auth import ua, Authorization
from multi import get_multi_info


local_time = time.strftime("%Y-%m-%d")

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

    with open('data/data.json', "w") as file:
        json.dump(response.json(), file, indent=4, ensure_ascii=False)


def get_declaration_sorted():
    """Данная функиця собирает только нужную информацию по декларациям,
    которые выпущены за день"""

    collected_id = {}
    declaration = []
    with open('data/data.json') as file:
        text = json.load(file)

    id = text.get('items')

    for item in id:
        declaration_id = item.get('id')
        declaration_number = item.get('number')
        date_regist = item.get('declDate')
        date_issue = item.get('declEndDate')
        applicant = item.get('applicantName')
        manufacturer = item.get('manufacterName')
        product_name = item.get('productFullName')

        declaration.append({
            'id': declaration_id,
            'number': declaration_number,
            'Register Date': date_regist,
            'Issue Date': date_issue,
            'Applicant': applicant,
            'Manufacturer': manufacturer,
            'Production': product_name
            }
        )
        collected_id['declaration'] = declaration

    with open('data/detailed_declaraion.json', "w") as file:
        json.dump(collected_id, file, indent=4, ensure_ascii=False)


def get_id_declaration():
    id_declaration = []
    with open('data/detailed_declaraion.json') as file:
        text = json.load(file)
    for items in text.values():
        for i in items:
            id = i.get('id')
            id_declaration.append(id)
    return id_declaration


def get_one_full_declaraion():
    with open('data/detailed_declaraion.json') as file:
        declaration = json.load(file)

    for items in declaration.values():
        for i in items[:2]:
            dec_id = i.get('id')
            response = requests.get(
                url=f'https://pub.fsa.gov.ru/api/v1/rds/common/declarations/{dec_id}',
                headers=headers,
                verify=False).json()
            scheme = response.get('idDeclScheme')
            reglaments = response.get('idTechnicalReglaments')
            multi = get_multi_info(dec_id, scheme, reglaments)
            scheme_dec = multi.get('id').get(dec_id).get('scheme')
            i['Схема'] = scheme_dec

    with open('data/result_day.json', "w") as file:
        json.dump(declaration, file, indent=4, ensure_ascii=False)


def main():
    get_day_declaration()
    get_declaration_sorted()
    # get_id_declaration()
    get_one_full_declaraion()


if __name__ == "__main__":
    main()
