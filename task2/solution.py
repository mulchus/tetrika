import csv
import locale
import requests
from bs4 import BeautifulSoup
from collections import Counter


locale.setlocale(locale.LC_COLLATE, 'ru_RU.UTF-8')  # бодаемся с буквой 'Ё' при сортировке

wiki_url = 'https://ru.wikipedia.org/'
next_part_url = 'w/index.php?title=Категория:Животные_по_алфавиту'
result = ''


def get_html(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except(requests.RequestException, ValueError):
        print('Сетевая ошибка')
        return False


while len(result) < 32:
    html = get_html(wiki_url + next_part_url)
    if not html:
        break
    soup = BeautifulSoup(html, 'html.parser')
    next_part_url = soup.find('a', string = 'Следующая страница')['href']

    blocks = soup.find("div", {"class": "mw-category mw-category-columns"}).find_all("div", {"class": "mw-category-group"})
    for block in blocks:
        items = block.find_all('a')
        first_chars = [item['title'][0] for item in items]
        result = Counter(result) + Counter(first_chars)
        print(result)

result.pop('A', 0)   # Удаляем английскую А как лишнее инфо
result = sorted(result.items(), key=lambda x: locale.strxfrm(x[0]))
print(result)

with open('beasts.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerows(result)
