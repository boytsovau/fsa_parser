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


class Certificate():

    def __init__(self, cert_num: str) -> None:
        self.ua = UserAgent()
        self.auth = FsaAuth()
        self.auth.get_token()
        self.cert_num = cert_num
        self.proxies = {'https': f"http://{os.getenv('PROXYUSER')}:{os.getenv('PROXYPASS')}@{os.getenv('PROXYIP')}"}
        self.headers = {
            'Accept': 'application/json, text/plain, */*',
            'Authorization': os.getenv('FSA_TOKEN'),
            'Content-Type': 'application/json',
            'Origin': 'https://pub.fsa.gov.ru',
            'Referer': 'https://pub.fsa.gov.ru/rss/certificate',
            'User-Agent': f'{self.ua.random}',
        }
        self.json_data = {
            'size': 10,
            'page': 0,
            'filter': {
                'columnsSearch': [
                    {
                        'column': 'number',
                        'search': self.cert_num,
                    },
                ],
            }
        }

    def get_certificate(self) -> dict:

        """Функция запрашивает информацию по сертификату"""
        # logging.debug(self.proxies)
        # logging.debug(self.json_data)
        # logging.debug(f"get_cert____ {os.getenv('FSA_TOKEN')}")
        s = requests.session()
        try:
            response = s.post(
                'https://pub.fsa.gov.ru/api/v1/rss/common/certificates/get',
                headers=self.headers,
                json=self.json_data,
                verify=False,
                proxies=self.proxies,
            )
            # logging.debug(response)
        except Exception as ex:
            logging.debug(ex)
            return None

        # logging.info(f'Первый запрос{response}')

        if response.status_code != 200:
            return None
        else:
            resp = json.loads(response.text)
            # logging.info(f'Обработка в JSON {resp}')
            # logging.info(f'Сработал else и скрипт продолжил работу \
            #              {response.status_code}')
            if len(resp.get('items')) != 0:
                data = self.get_certificate_sorted(resp)
                result = self.get_one_full_certificate(data)
                # logging.info(result)
                return result
            else:
                return False

    def get_certificate_sorted(self, data: dict) -> dict:

        """Функция вытягивает только нужные для нас поля
        из общих данных по сертификату"""

        collected_id = {}
        certificate = []
        id = data.get('items')

        for item in id:
            certificate_id = item.get('id')
            certificate_number = item.get('number')
            date_regist = item.get('date')
            date_issue = item.get('endDate')
            applicant = item.get('applicantName')
            manufacturer = item.get('manufacterName')
            product_name = item.get('productFullName')

            certificate.append({
                'id': certificate_id,
                'number': certificate_number,
                'Register Date': date_regist,
                'Issue Date': date_issue,
                'Applicant': applicant,
                'Manufacturer': manufacturer,
                'Production': product_name
                }
            )
            collected_id['certificate'] = certificate
        # logging.info(collected_id)
        return collected_id

    def get_one_full_certificate(self, data: dict) -> dict:

        """Функция забирает более полные данные по выданому сертификату.
        Далее в теле используем функцию get_multi_info() в которой
        формируется файл с информацией о схеме сертификаата"""

        for items in data.values():
            # logging.info(items)
            for i in items:
                cert_id = i.get('id')
                response = requests.get(
                    url=f'https://pub.fsa.gov.ru/api/v1/rss/common/certificates/{cert_id}',
                    headers=self.headers,
                    proxies=self.proxies,
                    verify=False).json()
                scheme = response.get('idCertScheme', '')
                reglaments = response.get('idTechnicalReglaments', '')
                status = response.get('idStatus', '')
                # logging.debug(f" цикл {scheme}, {reglaments}, {status}")
                multi = self.get_multi_info(cert_id, scheme, reglaments, status)
                scheme_dec = multi.get('id').get(cert_id).get('scheme')
                dec_status = multi.get('status').get(cert_id).get('status')
                i['Scheme'] = scheme_dec
                i['Status'] = dec_status
        return data

    def get_multi_info(self, id: str,
                       scheme: str,
                       reglaments: str,
                       status: str) -> dict:

        '''Функция для получения развернутых данных по схеме
        и статусу сертификата'''

        # logging.debug(f"get_multi__ {os.getenv('FSA_TOKEN')}")
        headers = {
                'Accept': 'application/json, text/plain, */*',
                'Authorization': os.getenv('FSA_TOKEN'),
                'Content-Type': 'application/json',
                'Origin': 'https://pub.fsa.gov.ru',
                'Referer': 'https://pub.fsa.gov.ru/rss/certificate',
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

        # logging.info(f'Обработка в JSON_multi {response}')
        data_full = {}
        cert_scheme = response.get("validationScheme2", [{}])[0].get('name', '')
        cert_status = response.get("status")[0].get('name')
        data_full['id'] = {id: {'scheme': cert_scheme}}
        data_full['status'] = {id: {'status': cert_status}}
        # logging.info(data_full)
        return data_full
