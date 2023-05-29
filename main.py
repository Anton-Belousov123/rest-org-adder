import requests
from bs4 import BeautifulSoup
import dataclasses
import psycopg2


@dataclasses.dataclass
class Card:
    article: str
    name: str
    url: str
    price: float
    photo: str


def add_element(c: Card):
    conn = psycopg2.connect(
        host='188.225.42.200',
        database='default_db',
        user='gen_user',
        password='Lola2011',
    )
    cur = conn.cursor()
    cur.execute("INSERT INTO oleg (s_article, s_name, s_photo, s_price, s_url, stage) VALUES (%s, %s, %s, %s, %s, %s)",
                (c.article, c.name, c.photo, c.price, c.url, 'Source parsed'))
    conn.commit()
    conn.close()


index = 0


def scrape_card(card_block):
    global index
    index += 1

    name = card_block.find('div', {'class': 'product-preview__title'}).text.strip()
    url = 'https://rest-torg.ru' + card_block.find('a').get('href')
    price = float(card_block.find('span', {'class': 'product-preview__price-cur'}).text.split()[0].strip())
    photo = card_block.find('picture').find('img').get('data-src')
    return Card(
        article=f"RT-{index + 10000000}",
        name=name,
        url=url,
        price=price,
        photo=photo
    )


def scrape_cards(text: str):
    soup = BeautifulSoup(text, features='html.parser')
    items = soup.find_all('form', {'action': '/cart_items'})
    return items


def scrape_category(category_link: str):
    page_number = 0
    print(category_link)
    cards = []
    while True:
        page_number += 1
        request_url = category_link + f'?page={page_number}'
        response = requests.get(url=request_url)
        if 'По вашему запросу ничего не найдено' in response.text:
            break
        cards_blocks = scrape_cards(response.text)
        for card_block in cards_blocks:
            card = scrape_card(card_block)
            cards.append(card)
    print(len(cards))
    return cards


categories = [
    'https://rest-torg.ru/collection/barnye-prinadlezhnosti',
    'https://rest-torg.ru/collection/kancelyarskie-tovary',
    'https://rest-torg.ru/collection/bytovaya-himiya',
    'https://rest-torg.ru/collection/konteynery-i-korobki',
    'https://rest-torg.ru/collection/krasota-i-zdorove',
    'https://rest-torg.ru/collection/odnorazovaya-odezhda',
    'https://rest-torg.ru/collection/odnorazovaya-posuda',
    'https://rest-torg.ru/collection/pakety',
    'https://rest-torg.ru/collection/spetsodezhda',
    'https://rest-torg.ru/collection/upakovochnye-materialy',
    'https://rest-torg.ru/collection/hozyajstvennye-tovary'
]

for category in categories:
    resp = scrape_category(category_link=category)
    for r in resp:
        add_element(r)
