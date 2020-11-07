import os
import csv
import codecs
from bs4 import BeautifulSoup

base_url = 'https://zakupki.gov.ru'
save_dir_name = 'E:\\\\_tmp'
page_save_dir_name = save_dir_name + '\\pages'
result_file_name = save_dir_name + '\\pages\\result\\result.csv'


class ContractInfo:
    status = None
    full_name_customer = None
    short_name_customer = None
    customer_inn = None
    executor_inn = None
    executor_name = None
    executor_address = None
    source_of_money = None
    money_value = None
    about = None
    type_of_service = None
    conclusion_of_contract_date = None
    start_date = None
    end_date = None
    auction_end_date = None
    rts_number = None
    foundation = None
    number = None
    region = None

    def __init__(self):
        pass

    def is_test(self):
        return (self.full_name_customer is not None and self.full_name_customer.startswith('Тестовая организация')) \
            or (self.executor_address is not None and self.executor_address.startswith('тест'))

    def as_dict(self):
        return {
            'status': self.status,
            'full_name_customer': self.full_name_customer,
            'short_name_customer': self.short_name_customer,
            'customer_inn': self.customer_inn,
            'executor_inn': self.executor_inn,
            'executor_name': self.executor_name,
            'executor_address': self.executor_address,
            'source_of_money': self.source_of_money,
            'money_value': self.money_value,
            'about': self.about,
            'type_of_service': self.type_of_service,
            'conclusion_of_contract_date': self.conclusion_of_contract_date,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'auction_end_date': self.auction_end_date,
            'rts_number': self.rts_number,
            'foundation': self.foundation,
            'number': self.number,
            'region': self.region
        }


def find_all_files():
    for _, _, files in os.walk(page_save_dir_name):
        return files


def main_block_1_parse(page, contact_info):
    search_block = page.find_all('div', class_='registry-entry__body-block')
    for el in search_block:
        title = el.find('div', class_='registry-entry__body-title').text.strip()
        value = el.find('div', class_='registry-entry__body-value').text.strip()
        if title == 'Субъект РФ':
            contact_info.region = value
    return contact_info


def section_info_parse(page, contact_info):
    section_info_els = page.find_all('section', class_='blockInfo__section')
    for section_el in section_info_els:
        title = section_el.find('span', class_='section__title').text.strip()
        value = section_el.find('span', class_='section__info').text.strip()
        if title == 'Этап договора':
            contact_info.status = value
        elif title == 'Полное наименование заказчика':
            contact_info.full_name_customer = value
        elif title == 'Сокращенное наименование заказчика':
            contact_info.short_name_customer = value
        elif title == 'ИНН':
            section_name = section_el.parent.parent.find('h2').text.strip()
            if section_name == 'Информация о заказчике':
                contact_info.customer_inn = value
            elif section_name == 'Информация о подрядчике':
                contact_info.executor_inn = value
        elif title == 'Полное наименование ЮЛ / ФИО индивидуального предпринимателя':
            contact_info.executor_name = value
        elif title == 'Источники финансирования':
            contact_info.source_of_money = value
        elif title == 'Цена договора, рублей':
            contact_info.money_value = value
        elif title == 'Предмет электронного аукциона':
            contact_info.about = value
        elif title == 'Виды работ (услуг)':
            contact_info.type_of_service = value
        elif title == 'Дата заключения договора':
            contact_info.conclusion_of_contract_date = value
        elif title == 'Дата начала исполнения договора':
            contact_info.start_date = value
        elif title == 'Дата окончания исполнения договора':
            contact_info.end_date = value
        elif title == 'Дата подведения результатов электронного аукциона':
            contact_info.auction_end_date = value
        elif title == 'Адрес места нахождения':
            contact_info.executor_address = value
        elif title == 'Номер договора':
            contact_info.rts_number = value
        elif title == 'Реквизиты документа, подтверждающего основание заключения договора':
            contact_info.foundation = value
        elif title == 'Номер реестровой записи':
            contact_info.number = value
    return contact_info


def parse_html_docs():
    files = find_all_files()
    result = []
    for file in files:
        with open(page_save_dir_name + '\\' + file, 'r', encoding='utf8') as f:
            # try:
            page = BeautifulSoup(f, 'html.parser')
            contact_info = ContractInfo()
            contact_info = main_block_1_parse(page, contact_info)
            contact_info = section_info_parse(page, contact_info)
            if not contact_info.is_test():
                result.append(contact_info.as_dict())
            # except:
            #     print(file)
            #     exit(1)
    with codecs.open(result_file_name, 'w', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=[
            'number',
            'rts_number',
            'money_value',
            'start_date',
            'end_date',
            'auction_end_date',
            'conclusion_of_contract_date',
            'status',
            'region',
            'full_name_customer',
            'short_name_customer',
            'customer_inn',
            'executor_name',
            'executor_inn',
            'executor_address',
            'about',
            'source_of_money',
            'type_of_service',
            'foundation',
        ])
        writer.writeheader()
        for row in result:
            writer.writerow(row)


if __name__ == '__main__':
    parse_html_docs()
