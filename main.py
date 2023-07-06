import requests
import json
import os
from auth import ua, Authorization
from multi import get_multi_info
from proxy_data import proxies


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


def get_declaration(dec_num):

    """Функция запрашивает информацию по декларации"""

    if not os.path.exists('data'):
        os.mkdir('data')

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
                    'search': dec_num,
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
        headers=headers,
        json=json_data,
        verify=False,
        proxies=proxies
    )
    resp = json.loads(response.text)

    if response.status_code != 200:
        print(response.status_code)
        return None
    else:
        print(response.status_code)
        if len(resp.get('items')) != 0:
            # with open('data/data_one_dec.json', "w") as file:
            #     json.dump(response.json(), file, indent=4, ensure_ascii=False)

            data = get_declaration_sorted(resp)
            result = get_one_full_declaraion(data)
            return result
        else:
            return False


def get_declaration_sorted(data):
    """Функция вытягивает только нужные для нас поля
    из общих данных по декларации"""

    collected_id = {}
    declaration = []
    # with open('data/data_one_dec.json') as file:
    #     text = json.load(file)

    index = 0
    id = data.get('items')

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

    # with open('data/dec_find.json', "w") as file:
    #     json.dump(collected_id, file, indent=4, ensure_ascii=False)
    return collected_id


def get_one_full_declaraion(data):
    """Функция забирает более полные данные по выданой декларации.
    Далее в теле используем функцию get_multi_info() в которой
    формируется файл с информацией о схеме декларирования"""

    # with open('data/dec_find.json') as file:
    #     declaration = json.load(file)

    for items in data.values():
        for i in items:
            dec_id = i.get('id')
            response = requests.get(
                url=f'https://pub.fsa.gov.ru/api/v1/rds/common/declarations/{dec_id}',
                headers=headers,
                proxies=proxies,
                verify=False).json()
            scheme = response.get('idDeclScheme')
            reglaments = response.get('idTechnicalReglaments')
            status = response.get('idStatus')
            multi = get_multi_info(dec_id, scheme, reglaments, status)
            scheme_dec = multi.get('id').get(dec_id).get('scheme')
            dec_status = multi.get('status').get(dec_id).get('status')
            i['Схема'] = scheme_dec
            i['Статус'] = dec_status

    # with open('data/result_dec.json', "w") as file:
    #     json.dump(declaration, file, indent=4, ensure_ascii=False)
    return data


def main():
    get_declaration()


if __name__ == "__main__":
    main()
