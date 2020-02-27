import requests

# Заголовки для парсинга
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, ke Gecko) '
                  'Chrome/61.0.3163.100 Safari/537.36'}

url = "http://taisu-tb.ru"
request = requests.get(url, headers=headers, timeout=(1, 10))

print(request.url)