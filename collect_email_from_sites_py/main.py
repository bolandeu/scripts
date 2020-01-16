import requests
import re
from bs4 import BeautifulSoup
import lxml
from urllib.parse import urlparse
import pandas as pd
from openpyxl import load_workbook
import os

def get_email(content):
    email_pattern = re.findall(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', content)
    emails = set(email_pattern)
    return emails
# end get_email

def get_content(url, headers, type='text'):
    try:   
        request = requests.get(url, headers=headers, timeout=(1, 10))
        if request.status_code == 200: # если страница существует 
            if type == "content":
                return request.content # возвращаем содержимое страницы
            else:
                return request.text # возвращаем содержимое страницы
    except requests.exceptions.ConnectTimeout:
        return 'Connection timeout'
    except requests.exceptions.ReadTimeout:
        return 'Read timeout occured'
    except requests.exceptions.ConnectionError:
        return 'Seems like dns lookup failed..'
    except requests.exceptions.HTTPError as err:
        return 'HTTP Error: {content}'.format(content=err.response.content)    
# end get_content

def get_pages_by_marker(content, markers):
    links = set()  # множество ссылок    
    soup = BeautifulSoup(content, 'lxml')
    for tag in soup.find_all('a', href=True):
        link = tag['href'] # выделяем ссылку            
        #print(tag.text, link)
        # проверяем на маркеры
        for marker in markers:

            if link.find(marker)>=0 or (tag.text).find(marker)>=0:
                # если относительная делаем абсолютной
                if link.find('http') == -1:
                    link = url + link
                # print(urlparse(url).netloc, urlparse(link).netloc)
                # проверяем что ссылка внутренняя    
                if urlparse(url).netloc == urlparse(link).netloc:
                    links.add(link) #добавляем в множество
    return links
# end get_pages_by_marker


# Заголовки для парсинга
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, ke Gecko) Chrome/61.0.3163.100 Safari/537.36'}

# Маркеры текста ссылок страницы контактов
markers = ['Контакты', 'Контактная информация', 'Контакт', 'contacts', 'contact', 'kontakty']

# Адрес
url = 'http://onway-logistics.com'
	

def parse_emails(url):
	emails = set() 
	text = get_content(url, headers)
    #print(text)
	emails = get_email(text)
	#print('Главная', emails, url)
	if not emails:
		content = get_content(url, headers, "content")
		links = get_pages_by_marker(content, markers)
		#print('Контакты', links)
		for addr in links:
            #print(addr)
			text = get_content(addr, headers)            
			emails_contact = get_email(text)
            #print(emails_contact)
			emails.update(emails_contact)
	return emails
# end parse_emails

def main():

	# отрываем входные данные и пишем в словарь
	file_name = os.path.dirname(os.path.realpath(__file__)) + "/file.xlsx"
	input_sheet = pd.read_excel(file_name, u"input")
	input_dict = dict(zip(input_sheet['id'], input_sheet['url'])) 

	
	# создаем словарь с новыми данными
	output_data = {}
	for id, url in input_dict.items(): 
		email = parse_emails(url)
		
		if email:
			output_data[id] = email
		else:
			output_data[id] = "none"
    
	# конструируем объект pandas    
	s = pd.Series(output_data)
	output_sheet = pd.DataFrame(list(s.items()), columns=['id', 'email'])

	# записываем в эксель
	book = load_workbook(file_name)
	with pd.ExcelWriter(file_name, engine='openpyxl') as writer:
		writer.book = book
		writer.sheets = dict((ws.title, ws) for ws in book.worksheets)
		output_sheet.to_excel(writer, sheet_name=u'output', index=False)
		writer.save()
	
# end main

if __name__ == '__main__':
    main()