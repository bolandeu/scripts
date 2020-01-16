import requests
import re
from bs4 import BeautifulSoup
import lxml
from urllib.parse import urlparse

'''
1. Переход на страницу контактов если нет на главной, контакты в разных вариациях
2. Правильно собирать сами ящики
'''

def get_email(content):
    email_pattern = re.findall(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', content)
    return set(email_pattern)
# end get_email

def get_content(url, headers):
    try:   
        r = requests.get(url, headers=headers, timeout=(1, 10))
        if r.status_code == 200: # если страница существует 
            return r.text # возвращаем содержимое страницы
    except requests.exceptions.ConnectTimeout:
        return 'Connection timeout'
    except requests.exceptions.ReadTimeout:
        return 'Read timeout occured'
    except requests.exceptions.ConnectionError:
        return 'Seems like dns lookup failed..'
    except requests.exceptions.HTTPError as err:
        return 'HTTP Error: {content}'.format(content=err.response.content)    
    # end get_content


url = 'https://taisu-tb.ru/'
	
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, ke Gecko) Chrome/61.0.3163.100 Safari/537.36'}

content = get_content(url, headers)

soup = BeautifulSoup(content,"lxml")
print(soup)

#emails = get_email(content)

# print(emails)