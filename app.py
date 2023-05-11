import requests
from flask import Flask
from bs4 import BeautifulSoup
from datetime import datetime

app = Flask(__name__)

@app.route("/<int:year>/<int:month>/<int:day>")
def unidad_de_fomento(year, month, day):
    #verify if valid date
    try:
        current_date = datetime.now()
        request_date = datetime.strptime(f'{day}-{month}-{year}', '%d-%m-%Y')
        if current_date < request_date:
            return '', 400
    except:
        return '', 400
    
    response = requests.get(f'https://www.sii.cl/valores_y_fechas/uf/uf{year}.htm')
    soup = BeautifulSoup(response.text, 'html.parser')

    #get all months table and verify if valid
    all_table = soup.find('div', {'id':'mes_all'})
    if not all_table:
        return '', 400
    
    #get all days rows and verify if valid
    day_rows = all_table.div.table.tbody.find_all('tr')
    if not day_rows or len(day_rows) < day:
        return '', 400
    
    #get all months columns and verify if valid
    month_cols = day_rows[day-1].find_all('td')
    if not month_cols or len(month_cols) < month:
        return '', 400
    
    #return value
    return {'response': month_cols[month-1].get_text()}, 200