import requests
from flask import Flask
from bs4 import BeautifulSoup
from datetime import datetime

app = Flask(__name__)

@app.route("/<int:year>/<int:month>/<int:day>")
def unidad_de_fomento(year, month, day):
    #verify if valid date
    try:
        datetime.strptime(f'{day}-{month}-{year}', '%d-%m-%Y')
    except:
        return {'message': 'invalid date'}, 400
    
    response = requests.get(f'https://www.sii.cl/valores_y_fechas/uf/uf{year}.htm')
    soup = BeautifulSoup(response.text, 'html.parser')

    #get all months table and verify if valid
    all_table = soup.find('div', {'id':'mes_all'})
    if not all_table:
        return {'message': 'data not found'}, 400
    
    #get all days rows and verify if valid
    day_rows = all_table.div.table.tbody.find_all('tr')
    if not day_rows or len(day_rows) < day:
        return {'message': 'data not found'}, 400
    
    #get all months columns and verify if valid
    month_cols = day_rows[day-1].find_all('td')
    if not month_cols or len(month_cols) < month:
        return {'message': 'data not found'}, 400
    
    return {'response': month_cols[month-1].get_text()}, 200
