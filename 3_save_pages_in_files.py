import json
import codecs
import requests
from time import sleep

base_url = 'https://zakupki.gov.ru'
save_dir_name = 'E:\\\\_tmp'
file_with_links = save_dir_name + '\\' + 'result.json'
page_save_dir_name = save_dir_name + '\\pages'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
    'Upgrade-Insecure-Requests': '1',
    'Cache-Control': 'max-age=0'
}


def save_date_to_file(link, count):
    id_name = link[57:-45]
    count_value = str(count).zfill(5)
    sleep(0.05)
    response = requests.get(base_url + link, headers=headers)
    response.encoding = 'utf-8'
    file_name = page_save_dir_name + '\\' + count_value + '__' + id_name + '.html'
    with codecs.open(file_name, 'w', 'utf-8') as f:
        f.write(response.content.decode('utf8'))


def save_all_pages():
    with open(file_with_links, 'r') as f:
        links = json.load(f)
        count = 0
        for link in links:
            save_date_to_file(link, count)
            count += 1


if __name__ == '__main__':
    save_all_pages()
