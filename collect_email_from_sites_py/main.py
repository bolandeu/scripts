import requests
import re

'''
1. Переход на страницу контактов если нет на главной, контакты в разных вариациях
2. Правильно собирать сами ящики
'''

def get_email(t):
    email_pattern = re.findall(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', t)
    emails = set(email_pattern)
    print (emails)

	
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, ke Gecko) Chrome/61.0.3163.100 Safari/537.36'}

try:
    url = 'http://www.lukoil.ru/Company/contacts'
    r = requests.get(url, headers=headers, timeout=(1, 10))
    if r.status_code == 200: # если страница существует 
        get_email(r.text) # получаем адреса со страницы
except requests.exceptions.ConnectTimeout:
    print ('Connection tiimeout')
except requests.exceptions.ReadTimeout:
    print('Read timeout occured')
except requests.exceptions.ConnectionError:
    print('Seems like dns lookup failed..')
except requests.exceptions.HTTPError as err:
    print('Oops. HTTP Error occured')
    print('Response is: {content}'.format(content=err.response.content))   