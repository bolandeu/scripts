import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import pandas as pd
from openpyxl import load_workbook
import os


def get_email(content):
    if content:
        email_pattern = re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", content)       
        return set([email.lower() for email in email_pattern])
    else:
        return False
    # end get_email


def get_content(url, headers="", type='text'):
    try:
        request = requests.get(url, headers=headers, timeout=(1, 10))
        if request.status_code == 200:  # если страница существует
            if type == "content":
                return request.content  # возвращаем содержимое страницы
            else:
                return request.text  # возвращаем содержимое страницы
        else:
            return False
    except requests.exceptions.ConnectTimeout:
        return False # return 'Connection timeout'        
    except requests.exceptions.ReadTimeout:
        return False # return 'Read timeout occured'        
    except requests.exceptions.ConnectionError:
        return False # return 'Seems like dns lookup failed..'        
    except requests.exceptions.HTTPError as err:
        return 'HTTP Error: {content}'.format(content=err.response.content)


def get_pages_by_marker(url, content, markers):
    links = set()  # множество ссылок    
    if content:
        soup = BeautifulSoup(content, 'lxml')
        for tag in soup.find_all('a', href=True):
            link = tag['href']  # выделяем ссылку
            # print(tag.text, link)
            # проверяем на маркеры
            for marker in markers:

                if link.find(marker) >= 0 or (tag.text).find(marker) >= 0:
                    # если относительная делаем абсолютной
                    if link.find('http') == -1:
                        link = url + link
                    # print(urlparse(url).netloc, urlparse(link).netloc)
                    # проверяем что ссылка внутренняя    
                    if urlparse(url).netloc == urlparse(link).netloc:
                        links.add(link)  # добавляем в множество
    return links


# Заголовки для парсинга
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, ke Gecko) '
                  'Chrome/61.0.3163.100 Safari/537.36'}

# Маркеры текста ссылок страницы контактов
markers = ['Контакты', 'Контактная информация', 'Контакт', 'contacts', 'contact', 'kontakty']

# Что исключать
cleaning = {'rating@mail.ru', '--rating@mail.ru'}


def parse_emails(url):

    text = get_content(url, headers)
    if text:
        emails = get_email(text)
    else:
        emails = set()

    if not emails:
        content = get_content(url, headers, "content")
        links = get_pages_by_marker(url, content, markers)
        for addr in links:
            text = get_content(addr, headers)
            emails_contact = get_email(text)
            emails.update(emails_contact)
    return emails


def main():
    
    # отрываем входные данные и пишем в словарь
    file_name = os.path.dirname(os.path.realpath(__file__)) + "/file.xlsx"
    input_sheet = pd.read_excel(file_name, u"input")
    input_dict = dict(zip(input_sheet['id'], input_sheet['url']))

    # создаем словарь с новыми данными
    output_data = {}
    count = 1	
    for id, url in input_dict.items():
        email = parse_emails(url)		
        cemails = email.difference(cleaning)
        if cemails:
            output_data[id] = ', '.join(cemails)
        else:
            output_data[id] = ''

        print(count, output_data[id])
        count += 1

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


if __name__ == '__main__':
    main()