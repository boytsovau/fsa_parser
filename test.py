import requests


response = requests.get(url='https://pub.fsa.gov.ru/rds/declaration', verify=False)
print(response)
if response.status_code != 200:
    print(response)
