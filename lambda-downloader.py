import csv
from botocore.vendore import requests

url = 'https://sisa.msal.gov.ar/datos/descargas/covid-19/files/Covid19VacunasAgrupadas.csv.zip'

def lambda_handler(event, context):
    session = requests.Session()
    raw_data = session.get(url)
    decoded = raw_data.content.decode('utf-8')
    reader = csv.reader(decoded.splitlines(), delimiter=',')
    rows = list(reader)
    data = {}
    for row in rows:
        #para testear, solo imprimir la fila
        #print(row)
        _id = rows['id']
        data[_id] = rows
    print(data)
