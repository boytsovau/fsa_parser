import requests
import json
from day_declaration import Authorization, ua


def get_multi_info():
    with open('data_full_dec.json') as file:
        text = json.load(file)
        Scheme = text.get('idDeclScheme')
        Reglaments = text.get('idTechnicalReglaments')
        id = text.get('idDeclaration')
        print(Scheme, Reglaments)

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
                    'id': Reglaments,
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
                        f'{Scheme}',
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
            'techregProductListEEU': [
                {
                    'id': [
                        18127,
                    ],
                    'fields': [
                        'id',
                        'masterId',
                        'name',
                        'techRegId',
                    ],
                },
            ],
        },
    }

    response = requests.post(
        'https://pub.fsa.gov.ru/nsi/api/multi',
        json=json_data,
        headers=headers,
        verify=False)

    with open('multi.json', "w") as file:
        json.dump(response.json(), file, indent=4, ensure_ascii=False)


def main():
    get_multi_info()


if __name__ == "__main__":
    main()
