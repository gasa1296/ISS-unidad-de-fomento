import json
from app import app
from datetime import datetime, timedelta
def test_date_route():
    response = app.test_client().get('/2023/02/01')
    assert response.status_code >= 200
    assert response.status_code < 300

def test_invalid_date():
    response = app.test_client().get('/2023/02/30')
    res = json.loads(response.data.decode('utf-8')).get("message")
    assert response.status_code >= 400 
    assert res != None
    assert res == 'invalid date'

def test_year_under_2013():
    response = app.test_client().get('/2012/02/01')
    res = json.loads(response.data.decode('utf-8')).get("message")
    assert response.status_code >= 400
    assert res != None
    assert res == 'data not found'

def test_future_year_date():
    '''test a date with a year more than current date'''
    future_datetime = datetime.now() + timedelta(days=366)
    response = app.test_client().get(f'/{future_datetime.year}/02/01')
    res = json.loads(response.data.decode('utf-8')).get("message")
    assert response.status_code >= 400
    assert res != None
    assert res == 'data not found'

def test_future_date():
    future_datetime = datetime.now() + timedelta(days=1)
    response = app.test_client().get(f'/{future_datetime.year}/02/01')
    res = json.loads(response.data.decode('utf-8')).get("response")
    assert response.status_code >= 200
    assert response.status_code < 300
    assert res != None
    
    res = json.loads(response.data.decode('utf-8')).get("message")
    assert res == None