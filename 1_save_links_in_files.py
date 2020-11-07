import json
import requests
from time import sleep
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
    'Upgrade-Insecure-Requests': '1',
    'Cache-Control': 'max-age=0'
}

save_dir_name = 'E:\\\\_tmp'

money_periods = [
    # 3 800
    ('0', '50_000'),
    # 2 600
    ('50_000', '100_000'),
    # 4 700
    ('100_000', '400_000'),
    # 4 400
    ('400_000', '1_000_000'),
    # 4 300
    ('1_000_000', '1_800_000'),
    # 4 800
    ('1_800_000', '3_100_000'),
    # 4 600
    ('3_100_000', '5_000_000'),
    # 4 100
    ('5_000_000', '8_000_000'),
    # 4 400
    ('8_000_000', '15_000_000'),
    # 4 700
    ('15_000_000', '40_000_000'),
    # 2 200
    ('40_000_000', '150_000_000'),
    # 430
    ('150_000_000', '9_000_000_000')
]


def edit_money_period(money_period):
    return str(int(money_period))


def build_page_file(page_num, prefix):
    return save_dir_name + '\\' + prefix + str(page_num) + '.json'


def create_url_by_interval(page_number, money_period):
    records_per_page = 50
    base_url = 'https://zakupki.gov.ru/epz/capitalrepairs/search/results.html'
    params = [
        ('searchString', ''),
        ('morphology', 'on'),
        ('priceFrom', edit_money_period(money_period[0])),
        ('priceTo', edit_money_period(money_period[1])),
        ('search-filter', '%D0%94%D0%B0%D1%82%D0%B5+%D1%80%D0%B0%D0%B7%D0%BC%D0%B5%D1%89%D0%B5%D0%BD%D0%B8%D1%8F'),
        ('contractStage_0', 'on'),
        ('contractStage_2', 'on'),
        ('contractStage', '0%2C2'),
        ('selectedSubjectsIdNameHidden', '%7B%7D'),
        ('sortBy', 'PUBLISH_DATE'),
        ('pageNumber', str(page_number)),
        ('sortDirection', 'false'),
        ('recordsPerPage', '_' + str(records_per_page)),
        ('showLotsInfoHidden', 'false')
    ]
    return base_url + '?' + '&'.join([p[0] + '=' + p[1] for p in params])


def build_end_page_msg(page_num, period, result):
    return 'Мы вернулись на первую страницу для интервала: {0}, хотя текущая страница: {1}, начинаем проверять следующий интервал, всего ссылок на текущем интервале: {2}'.format(
        str(period),
        str(page_num),
        str(len(result[page_num]))
    )


def get_page(page_num, money_period):
    page_url = create_url_by_interval(page_num, money_period)
    response = requests.get(page_url, headers=headers)
    page = BeautifulSoup(response.content, 'html.parser')
    return page


def main():
    num_period = 0
    start_period_num = 4
    for money_period in money_periods:
        prefix = str(num_period).zfill(2) + '__' + money_period[0] + '__'
        if start_period_num > num_period:
            num_period += 1
            continue
        else:
            num_period += 1
        result = {}
        page_num = 0
        while True:
            page_num = page_num + 1
            sleep(0.05)
            page = get_page(page_num, money_period)
            current_page_num_in_page = page.find('a', class_='page__link_active')
            if current_page_num_in_page is None:
                print('Empty page: {0}, page_number: {1}'.format(prefix, str(page_num)))
                continue
            if page_num != 1 and current_page_num_in_page.text == '1':
                print(build_end_page_msg(page_num, money_period, result))
                break
            entries_block_raw = page.find_all('div', class_='search-registry-entrys-block')
            if len(entries_block_raw) == 0:
                print("!!!Empty entries block for page num = " + str(page_num))
                break
            entries_block = entries_block_raw[0]
            link_elements = entries_block.find_all('div', class_='registry-entry__header-mid__number')
            for element in link_elements:
                if page_num not in result:
                    acc = []
                    result[page_num] = acc
                else:
                    acc = result[page_num]
                href = element.find('a')['href']
                acc.append(href)
            if len(link_elements) == 0:
                break
            with open(build_page_file(page_num, prefix), 'w') as f:
                json.dump(result[page_num], f, ensure_ascii=False, indent=4)
                print('write page')


if __name__ == '__main__':
    main()
