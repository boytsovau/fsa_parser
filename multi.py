import requests
from auth import get_auth
from fake_useragent import UserAgent
from proxy_data import proxies

ua = UserAgent()


def get_multi_info(id, scheme, reglaments, status):

    Authorization = get_auth()

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
        # proxies=proxies,
        verify=False).json()

    data_full = {}
    decl_scheme = response.get("validationScheme2")[0].get('name')
    decl_status = response.get("status")[0].get('name')
    data_full['id'] = {id: {'scheme': decl_scheme}}
    data_full['status'] = {id: {'status': decl_status}}
    return data_full


def main():
    get_multi_info()


if __name__ == "__main__":
    main()
