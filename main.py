import requests
import json
from day_declaration import Authorization, ua
from multi import get_multi_info

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
                    'search': 'ЕАЭС N RU Д-ES.РА04.В.11330/23',
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


def get_declaration_sorted():
    """Функция вытягивает только нужные для нас поля
    из общих данных по декларации"""

    collected_id = {}
    declaration = []
    with open('data_one_dec.json') as file:
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
        index += 1

    with open('dec_find.json', "w") as file:
        json.dump(collected_id, file, indent=4, ensure_ascii=False)


def get_id_declaration():
    with open('data_one_dec.json') as file:
        text = json.load(file)
    id = text.get('items')[0].get('id')
    return id


def get_one_full_declaraion():
    """Функция забирает более полные данные по выданой декларации.
    Далее в теле используем функцию get_multi_info() в которой
    формируется файл с информацией о схеме декларирования"""

    id = get_id_declaration()

    response = requests.get(
        url=f'https://pub.fsa.gov.ru/api/v1/rds/common/declarations/{id}',
        headers=headers,
        verify=False).json()

    scheme = response.get('idDeclScheme')
    reglaments = response.get('idTechnicalReglaments')

    result = get_multi_info(id, scheme, reglaments)

    return result

    # with open('data_full_dec.json', "w") as file:
    #     json.dump(response.json(), file, indent=4, ensure_ascii=False)


def get_result_declaration():
    """Формируем итоговый файл с нужными данными"""

    with open('dec_find.json') as file:
        declaration = json.load(file)

    with open('multi.json') as file:
        multi = json.load(file)

    for items in declaration.values():
        for i in items:
            dec_id = i.get('id')
            scheme_dec = multi.get('id').get(f'{dec_id}').get('scheme')
            i['Схема'] = scheme_dec

    with open('result.json', "w") as file:
        json.dump(declaration, file, indent=4, ensure_ascii=False)


def main():
    get_declaration()
    get_declaration_sorted()
    get_one_full_declaraion()
    get_result_declaration()


if __name__ == "__main__":
    main()
