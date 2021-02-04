import requests
from bs4 import BeautifulSoup
import csv
import sys
from datetime import datetime

if sys.platform == 'linux':
    import subprocess
else:
    import os


class Buttons:
    def __init__(self, button=0):
        self.button = button

    def push(self):
        if self.button == 1:
            URL = 'https://rabota.ua/zapros/python/львов/pg1'
            return URL
        elif self.button == 2:
            URL = 'https://rabota.ua/zapros/trainee/украина/pg1'
            return URL
        else:
            URL = 'https://rabota.ua/львов/pg1'
            return URL
try:
    s = Buttons(int(input('1==python/львов, 2==trainee/украина.\n Сделать выбор:')))
except ValueError:
    s = Buttons(0)
#  print(s.push())

# URL = 'https://rabota.ua/zapros/trainee/украина/pg1'
# URL = 'https://rabota.ua/zapros/python/львов/pg1'
# URL = 'https://rabota.ua/jobsearch/vacancy_list?keyWords=Python&regionId=0'


HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/83.0.4103.116 Safari/537.36', 'accept': '*/*'}
HOST = 'https://rabota.ua'

FILE = "{}work.csv".format(datetime.now())


def get_url(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_pages_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    page = soup('dd', class_='')
    print(page)

    if page:
        print(int(page[-1].get_text()))
        return int(page[-1].get_text())
    else:
        print(1)
        return 1


def get_data(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('article', class_='card')

    work = []
    for item in items:
        work.append({
            'time': item.find('div', class_='publication-time').get_text(),
            'title': item.find('h2', class_='card-title').get_text(strip='\n'),
            'description': item.find('div', class_='card-description').get_text(),
            'link': HOST + item.find('a', class_='ga_listing').get('href'),
            'company': item.find('a', class_='company-profile-name').get_text(),
            'location': item.find('span', class_='location').get_text()

        })
    return work


def save(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(["Время", "Работа", "Расширенная информация", "Ссылка", "Компания", "Город"])
        for item in items:
            writer.writerow(
                [item["time"], item["title"], item["description"], item["link"], item["company"], item["location"]])


def parse():
    html = get_url(s.push())
    if html.status_code == 200:
        print('Соединение с сервером установлено')
        work = []
        get_data(html.text)
        pages_count = get_pages_count(html.text)
        for i in range(1, pages_count + 1):
            print(f'Получение данных со страницы {i} из {pages_count} страниц')
            html = get_url(s.push(), params={'pg': i})
            work.extend(get_data(html.text))
            save(work, FILE)
        print(f'найдено {len(work)} вакансий')
        if sys.platform == 'linux':
            opener = "open" if sys.platform == "darwin" else "xdg-open"
            subprocess.call([opener, FILE])

        else:
            os.startfile(FILE)
    else:
        print("Error connection from site")


parse()
