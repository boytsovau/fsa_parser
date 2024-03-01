import requests
import os
import logging
from fake_useragent import UserAgent


ua = UserAgent()

logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.DEBUG, filename="bot.log")


def get_multi_info(id, scheme, reglaments, status):

    logging.debug(f"get_multi__ {os.getenv('FSA_TOKEN')}")
    headers = {
            'Accept': 'application/json, text/plain, */*',
            'Authorization': os.getenv('FSA_TOKEN'),
            'Content-Type': 'application/json',
            'Origin': 'https://pub.fsa.gov.ru',
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
        # proxies=os.getnenv("PROXY"),
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
