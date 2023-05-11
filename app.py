import requests
from flask import Flask
from bs4 import BeautifulSoup
from datetime import datetime

app = Flask(__name__)

@app.route("/<int:year>/<int:month>/<int:day>")
def unidad_de_fomento(year, month, day):
    try:
        current_date = datetime.now()
        request_date = datetime.strptime(f'{day}-{month}-{year}', '%d-%m-%Y')
        if current_date < request_date:
            return {'status': 400}
    except:
        return {'status': 500, 'message': 'invalid date'}
    response = requests.get(f'https://www.sii.cl/valores_y_fechas/uf/uf{year}.htm')
    soup = BeautifulSoup(response.text, 'html.parser')