import json
from bs4 import BeautifulSoup
import requests

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}

#получаем ссылки основных категорий
url = 'https://hypower.ru/catalog/'
req = requests.get(url, headers=headers)
src = req.text
soup = BeautifulSoup(src, 'lxml')
cat_names = soup.find_all('li', class_='name')
cat_dict = {}
for i in cat_names:
    cat_link = 'https://hypower.ru' + i.find('a').get('href')
    cat_name = i.find('span').text
    if "/" in cat_name:
        cat_name = cat_name.replace('/', 'or')
    cat_dict[cat_name] = cat_link
with open('Основные категории.json', 'w') as file:
    json.dump(cat_dict, file, indent=4, ensure_ascii=False)

with open('Основные категории.json') as file:
    cat_links = json.load(file)
for cat_name, cat_link in cat_links.items():
    all_items = {}
    req = requests.get(url=cat_link, headers=headers)
    src = req.text
    soup = BeautifulSoup(src, 'lxml')
    try:
        pages_amount = soup.find(class_="nums").find_all('a')
    except:
        items = soup.find_all(class_="item_info N")
        for i in items:
            item_name = i.find('a').find('span').text
            item_link = i.find('a').get('href')
            all_items[item_name] = item_link
        with open(f'Товары категория {cat_name}.json', 'w') as file:
            json.dump(all_items, file, indent=4, ensure_ascii=False)
    else:
        max_page_number = int(pages_amount[-1].text)
        for j in range(1, max_page_number+1):
            url = f'{cat_link}?PAGEN_1={j}'
            req = requests.get(url=url, headers=headers)
            src = req.text
            soup = BeautifulSoup(src, 'lxml')
            items = soup.find_all(class_="item_info N")
            for i in items:
                item_name = i.find('a').find('span').text
                item_link = 'https://hypower.ru' + i.find('a').get('href')
                all_items[item_name] = item_link
    with open(f'Товары категория {cat_name}.json', 'w') as file:
        json.dump(all_items, file, indent=4, ensure_ascii=False)




