import requests
import xml.etree.ElementTree as ET
import pytest

def test_cbr_api(date=None):

    url = 'http://www.cbr.ru/scripts/XML_daily.asp'
    if date:
        url += f'?date_req={date}'
    response = requests.get(url)
    assert response.status_code == 200
    root = ET.fromstring(response.text)
    for valute in root.findall('Valute'):
        assert valute.find('NumCode') is not None
        assert valute.find('CharCode') is not None
        assert valute.find('Nominal') is not None
        assert valute.find('Name') is not None
        assert valute.find('Value') is not None

        assert valute.find('NumCode').text.isdigit()
        assert float(valute.find('Value').text.replace(',', '.'))

    assert root.attrib['Date'] is not None
    print(f"Date attribute in root element: {root.attrib['Date']}")

    assert len(root.findall('Valute')) > 0
    print(f"Number of currency quotes returned: {len(root.findall('Valute'))}")

    currency_codes = [valute.find('CharCode').text for valute in root.findall('Valute')]
    assert len(currency_codes) == len(set(currency_codes))
    print(f"Number of unique currency codes: {len(set(currency_codes))}")

test_cbr_api(date='02/03/2023')
