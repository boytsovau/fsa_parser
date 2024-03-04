import requests
import json
import os
import logging
from auth import FsaAuth
from fake_useragent import UserAgent


logging.basicConfig(format='%(asctime)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S',
                    level=logging.DEBUG,
                    filename="bot.log")


class Declaration():

    def __init__(self, dec_num: str) -> None:
        self.ua = UserAgent()
        self.auth = FsaAuth()
        self.auth.get_token()
        self.dec_num = dec_num
        self.proxies = {'https': f"http://{os.getenv('PROXYUSER')}:{os.getenv('PROXYPASS')}@{os.getenv('PROXYIP')}"}
        self.headers = {
            'Accept': 'application/json, text/plain, */*',
            'Authorization': os.getenv('FSA_TOKEN'),
            'Content-Type': 'application/json',
            'Origin': 'https://pub.fsa.gov.ru',
            'Referer': 'https://pub.fsa.gov.ru/rds/declaration',
            'User-Agent': f'{self.ua.random}',
        }
        self.json_data = {
            'size': 10,
            'page': 0,
            'filter': {
                'columnsSearch': [
                    {
                        'name': 'number',
                        'search': self.dec_num,
                        'type': 9,
                        'translated': False,
                    },
                ],
            }
        }

    def get_declaration(self) -> dict:

        """Функция запрашивает информацию по декларации"""
        logging.debug(self.proxies)
        logging.debug(self.json_data)
        logging.debug(f"get_dec____ {os.getenv('FSA_TOKEN')}")
        s = requests.session()
        try:
            response = s.post(
                'https://pub.fsa.gov.ru/api/v1/rds/common/declarations/get',
                headers=self.headers,
                json=self.json_data,
                verify=False,
                proxies=self.proxies,
            )
            logging.debug(response)
        except Exception as ex:
            logging.debug(ex)
            return None

        logging.info(f'Первый запрос{response}')

        if response.status_code != 200:
            return None
        else:
            resp = json.loads(response.text)
            logging.info(f'Обработка в JSON {resp}')
            logging.info(f'Сработал else и скрипт продолжил работу \
                         {response.status_code}')
            if len(resp.get('items')) != 0:
                data = self.get_declaration_sorted(resp)
                result = self.get_one_full_declaraion(data)
                logging.info(result)
                return result
            else:
                return False

    def get_declaration_sorted(self, data: dict) -> dict:

        """Функция вытягивает только нужные для нас поля
        из общих данных по декларации"""

        collected_id = {}
        declaration = []
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
        logging.info(collected_id)
        return collected_id

    def get_one_full_declaraion(self, data: dict) -> dict:

        """Функция забирает более полные данные по выданой декларации.
        Далее в теле используем функцию get_multi_info() в которой
        формируется файл с информацией о схеме декларирования"""

        for items in data.values():
            logging.info(items)
            for i in items:
                dec_id = i.get('id')
                response = requests.get(
                    url=f'https://pub.fsa.gov.ru/api/v1/rds/common/declarations/{dec_id}',
                    headers=self.headers,
                    proxies=self.proxies,
                    verify=False).json()
                scheme = response.get('idDeclScheme', '')
                reglaments = response.get('idTechnicalReglaments', '')
                status = response.get('idStatus', '')
                logging.debug(f" цикл {scheme}, {reglaments}, {status}")
                multi = self.get_multi_info(dec_id, scheme, reglaments, status)
                scheme_dec = multi.get('id').get(dec_id).get('scheme')
                dec_status = multi.get('status').get(dec_id).get('status')
                i['Scheme'] = scheme_dec
                i['Status'] = dec_status
        return data

    def get_multi_info(self, id: str,
                       scheme: str,
                       reglaments: str,
                       status: str) -> dict:

        '''Функция для получения развернутых данных по схеме
        и статусу декларации'''

        logging.debug(f"get_multi__ {os.getenv('FSA_TOKEN')}")
        headers = {
                'Accept': 'application/json, text/plain, */*',
                'Authorization': os.getenv('FSA_TOKEN'),
                'Content-Type': 'application/json',
                'Origin': 'https://pub.fsa.gov.ru',
                'Referer': f'https://pub.fsa.gov.ru/rds/declaration/view/{id}/common',
                'User-Agent': f'{self.ua.random}'
            }

        json_data_full = {
            'items': {
                'validationFormNormDoc': [
                    {
                        'id': reglaments,
                    },
                ],
                'validationScheme2': [
                    {
                        'id': [
                            f'{scheme}',
                        ],
                    },
                ],
                'status': [
                    {
                        'id': [
                            status,
                        ],
                    },
                ],
            },
        }

        json_data_small = {
            'items': {
                'status': [
                    {
                        'id': [
                            status,
                        ],
                    },
                ],
            },
        }

        if scheme is None:
            json_data = json_data_small
        else:
            json_data = json_data_full

        response = requests.post(
            'https://pub.fsa.gov.ru/nsi/api/multi',
            json=json_data,
            headers=headers,
            proxies=self.proxies,
            verify=False).json()

        logging.info(f'Обработка в JSON_multi {response}')
        data_full = {}
        decl_scheme = response.get("validationScheme2", [{}])[0].get('name', '')
        decl_status = response.get("status")[0].get('name')
        data_full['id'] = {id: {'scheme': decl_scheme}}
        data_full['status'] = {id: {'status': decl_status}}
        logging.info(data_full)
        return data_full
