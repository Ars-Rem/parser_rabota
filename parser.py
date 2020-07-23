import requests
from bs4 import BeautifulSoup
import csv
import os

URL = 'https://rabota.ua/jobsearch/vacancy_list?keyWords=Python&regionId=0'
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/83.0.4103.116 Safari/537.36', 'accept': '*/*'}
HOST = 'https://rabota.ua'
FILE = 'work.csv'


def get_url(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_pages_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    page = soup('a', class_='f-always-blue')
    if page:
        return int(page[-1].get_text())
    else:
        return 1


def get_data(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('article', class_='card')

    work = []
    for item in items:
        work.append({
            'time': item.find('div', class_='publication-time').get_text(),
            'title': item.find('p', class_='card-title').get_text(strip='\n'),
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
    html = get_url(URL)
    if html.status_code == 200:
        print('Соединение с сервером установлено')
        work = []
        get_data(html.text)
        pages_count = get_pages_count(html.text)
        for i in range(1, pages_count + 1):
            print(f'Получение данных со страницы {i} из {pages_count} страниц')
            html = get_url(URL, params={'pg': i})
            work.extend(get_data(html.text))
            save(work, FILE)
        print(f'найдено {len(work)} вакансий')
        os.startfile(FILE)
    else:
        print("Error connection from site")


if input() == '':
    parse()
elif input('1') == '1':
    parse(URL)
