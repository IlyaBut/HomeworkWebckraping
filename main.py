# Домашнее задание к лекции 6.«Web-scrapping»
from gettext import textdomain
from http.client import responses
from pprint import pprint

import requests
from bs4 import BeautifulSoup
from fake_headers import Headers
import json

from html5lib.filters.sanitizer import data_content_type

# нужно вытащить:
# Вакансию (Текст)
# Ссылку
# зп
# Название компании
# Город

# Теги
# Тег ленты - div class = "sticky-sidebar-wrapper--RTbyDwpLW4VFIqtosB0I"
# Тег "квадратика" = div 'vacancy-info--umZA61PpMY07JVJtomBA'
# Тег Вакансии - h2 data-qa = "bloko-header-2"
# Тег ссылки - a class = "custom-color-magritte-link--TGWm0usZjBiWA6x0tvhy vacancy-name-wrapper--tzZ1sS33pe6ELop6_Cte"
# Тег зп - span data-qa="vacancy-salary-compensation-type-net"
# Тег компании - span data-qa="vacancy-serp__vacancy-employer-text"
# Тег города - span data-qa="vacancy-serp__vacancy-address"


url = "https://spb.hh.ru/search/vacancy?text=python&area=1&area=2"
params = {
    'area': (1, 2),
    'text': 'python django flask'
}

def get_headers():
    return Headers(browser = 'chrome', os = 'win').generate()


main_response = requests.get(url, params = params, headers = get_headers())
main_html = main_response.text
main_soup = BeautifulSoup(main_html, 'lxml')

tag_feed = main_soup.find('main', class_= "vacancy-serp-content")
tag_blocks = tag_feed.find_all(class_="magritte-redesign")

parsed_date =[]


for tag in tag_blocks:
    text_title = tag.find('h2', class_ = "bloko-header-section-2").text
    link_vacancy = tag.find('a').get('href')
    company = tag.find('div', class_ = "company-name-badges-container--kC8yYUJPFyg6J6XQs62Y").text.replace('\xa0','')
    city = tag.find('span', {'data-qa': 'vacancy-serp__vacancy-address'}).text
    #salary = tag.find('span', {'data-sentry-source-file':"index.tsx"})
    salary = tag.find('span', class_ = "magritte-text___pbpft_3-0-16 magritte-text_style-primary___AQ7MW_3-0-16 magritte-text_typography-label-1-regular___pi3R-_3-0-16")
    if salary is None:
        salary = 'Не указано'
    else:
        salary = salary.text.replace('\u202f', '')
        salary = salary.replace('\xa0','')



    parsed_date.append(
        {
            "вакансия":text_title,
            "ссылка":link_vacancy,
            "зарплата":salary,
            "название компании": company,
            "город": city
        }
    )

#pprint(parsed_date)

with open('vacancys.json', 'w', encoding='utf-8') as f:
    json.dump(parsed_date, f, ensure_ascii=False, indent=5)






