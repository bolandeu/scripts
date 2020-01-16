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

  
def add_all_links_recursive(url, maxdepth=1):
    # print('{:>5}'.format(len(links)), url[len(HOST):])
    # извлекает все ссылки из указанного `url`
    # и рекурсивно обрабатывает их
    # глубина рекурсии не более `maxdepth`
  
    # список ссылок, от которых в конце мы рекурсивно запустимся
    links_to_handle_recursive = []
  
    # получаем html код страницы
    request = requests.get(url)
    # парсим его с помощью BeautifulSoup
    soup = BeautifulSoup(request.content, 'lxml')
    # рассматриваем все теги <a>
    for tag_a in soup.find_all('a'):
        # получаем ссылку, соответствующую тегу
        link = tag_a['href']
        # если ссылка не начинается с одного из запрещённых префиксов
        if all(not link.startswith(prefix) for prefix in FORBIDDEN_PREFIXES):
            # проверяем, является ли ссылка относительной
            # например, `/oplata` --- это относительная ссылка
            # `http://101-rosa.ru/oplata` --- это абсолютная ссылка
            if link.startswith('/') and not link.startswith('//'):
                # преобразуем относительную ссылку в абсолютную
                link = HOST + link
            # проверяем, что ссылка ведёт на нужный домен
            # и что мы ещё не обрабатывали такую ссылку
            if urlparse(link).netloc == DOMAIN and link not in links:
                links.add(link)
                links_to_handle_recursive.append(link)
  
    if maxdepth > 0:
        for link in links_to_handle_recursive:
            add_all_links_recursive(link, maxdepth=maxdepth - 1)
  
def main():
    add_all_links_recursive(HOST + '/')
    for link in links:
        print(link)
  
if __name__ == '__main__':
    main()


DOMAIN = '101-rosa.ru'
HOST = 'http://' + DOMAIN
FORBIDDEN_PREFIXES = ['#', 'tel:', 'mailto:']
links = set()  # множество всех ссылок

url = 'https://taisu-tb.ru/'
	
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, ke Gecko) Chrome/61.0.3163.100 Safari/537.36'}

content = get_content(url, headers)

soup = BeautifulSoup(content,"lxml")
print(soup)

#emails = get_email(content)

# print(emails)
