import pandas as pd
from openpyxl import load_workbook
import requests


def get_coordinates(address):
	url = 'https://maps.googleapis.com/maps/api/geocode/json'
	key = 'AIzaSyB5lmSRMNI92oxIIwrL_6Dj_xOe7cLmfP4'
	params = {'key': key, 'address': address}
	r = requests.get(url, params=params)
	results = r.json()['results']
	location = results[0]['geometry']['location']
	return (location['lat'], location['lng'])
	

# отрываем входные данные и пишем в словарь
file_name = "file.xlsx"
input_sheet = pd.read_excel(file_name, u"input_sheet")
input_dict = dict(zip(input_sheet['id'], input_sheet['address'])) 

# создаем словарь с новыми данными
output_data = {}
for id, address in input_dict.items(): 
    coord = get_coordinates(address) # получаем координаты
    output_data[id] = f"{coord}" # присваиваем координаты к id
    
# конструируем объект pandas    
s = pd.Series(output_data)
output_sheet = pd.DataFrame(list(s.items()), columns=['id', 'coord'])

# записываем в эксель
book = load_workbook(file_name)
with pd.ExcelWriter(file_name, engine='openpyxl') as writer:
    writer.book = book
    writer.sheets = dict((ws.title, ws) for ws in book.worksheets)
    output_sheet.to_excel(writer, sheet_name=u'output_sheet', index=False)
    writer.save()