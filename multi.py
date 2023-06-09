import requests
# import json
from auth import ua, Authorization
from proxy_data import proxies


def get_multi_info(id, scheme, reglaments, status):

    headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'Authorization': f'{Authorization}',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json',
            'Origin': 'https://pub.fsa.gov.ru',
            'Pragma': 'no-cache',
            'Referer': f'https://pub.fsa.gov.ru/rds/declaration/view/{id}/common',
            'User-Agent': f'{ua.random}'
        }

    json_data = {
        'items': {
            'validationFormNormDoc': [
                {
                    'id': reglaments,
                    'fields': [
                        'id',
                        'masterId',
                        'name',
                        'docNum',
                    ],
                },
            ],
            'validationScheme2': [
                {
                    'id': [
                        f'{scheme}',
                    ],
                    'fields': [
                        'id',
                        'masterId',
                        'name',
                        'validityTerm',
                        'isSeriesProduction',
                        'isBatchProduction',
                        'isOneOffProduction',
                        'isProductSampleTesting',
                        'isBatchProductTesting',
                        'isOneOffProductTesting',
                        'isAccreditationLab',
                        'isApplicantManufacturer',
                        'isApplicantProvider',
                        'isPresenceOfProxy',
                        'isApplicantForeign',
                        'isApplicantEeuMember',
                    ],
                },
            ],
            'status': [
                {
                    'id': [
                        status,
                    ],
                    'fields': [
                        'id',
                        'masterId',
                        'name',
                    ],
                },
            ],
        },
    }

    response = requests.post(
        'https://pub.fsa.gov.ru/nsi/api/multi',
        json=json_data,
        headers=headers,
        proxies=proxies,
        verify=False).json()

    data_full = {}
    decl_scheme = response.get("validationScheme2")[0].get('name')
    decl_status = response.get("status")[0].get('name')
    data_full['id'] = {id: {'scheme': decl_scheme}}
    data_full['status'] = {id: {'status': decl_status}}
    # with open('data/multi_full.json', "w") as file:
    #     json.dump(response, file, indent=4, ensure_ascii=False)

    # with open('data/multi.json', "w") as file:
    #     json.dump(data_full, file, indent=4, ensure_ascii=False)
    return data_full


def main():
    get_multi_info()


if __name__ == "__main__":
    main()
