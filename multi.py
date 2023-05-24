import requests
import json
from auth import ua, get_auth


Authorization = get_auth()

def get_multi_info(id, scheme, reglaments):
    # with open('data_full_dec.json') as file:
    #     text = json.load(file)
        # Scheme = text.get('idDeclScheme')
        # Reglaments = text.get('idTechnicalReglaments')
        # id = text.get('idDeclaration')

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
        },
    }

    response = requests.post(
        'https://pub.fsa.gov.ru/nsi/api/multi',
        json=json_data,
        headers=headers,
        verify=False).json()

    data_full = {}
    decl_scheme = response.get("validationScheme2")[0].get('name')
    data_full['id'] = {id: {'scheme': decl_scheme}}

    with open('multi.json', "w") as file:
        json.dump(data_full, file, indent=4, ensure_ascii=False)
    return data_full


def main():
    get_multi_info()


if __name__ == "__main__":
    main()
