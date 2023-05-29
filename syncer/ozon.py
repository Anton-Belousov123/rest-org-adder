import asyncio
import json
import time

import aiohttp
import requests

import db
import rst
from syncer.utils import timer

headers = {
    'Client-Id': '1131161',
    'Api-Key': '74f9218c-ab62-4915-8fd1-b6a953a32842'
}


@timer
def get_price_info(last_id=None, arr=[]):
    url = 'https://api-seller.ozon.ru/v4/product/info/prices'
    data = {
        'filter': {},
        'limit': 1000
    }
    if last_id:
        data['last_id'] = last_id
    resp = requests.post(url, data=json.dumps(data), headers=headers).json()
    if not 'result' in resp.keys():
        return arr
    for item in resp['result']['items']:
        offer_id, price = item['offer_id'], item['price']['price']
        if [offer_id, price] in arr:
            return arr
        arr.append([offer_id, price])
    return get_price_info(resp['result']['last_id'], arr)


@timer
def update_prices(prices):
    url = 'https://api-seller.ozon.ru/v1/product/import/prices'
    data = {
        "prices": prices
    }
    resp = requests.post(url, data=json.dumps(data), headers=headers).json()
    print(resp)


@timer
async def main():
    item_list = get_price_info()
    links = []
    links_from_db = db.get_all_links()
    for item in item_list:
        if not '-RT-' in item[0]:
            continue

        link = links_from_db[item[0].split('РСВ-')[1]]
        links.append([item[0], link, item[1]])

    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in links:
            task = asyncio.create_task(rst.get_item_info_rst(session, url))
            tasks.append(task)

        prices = []
        results = await asyncio.gather(*tasks)
        for i in results:
            if i[0] is None:
                continue
            new_price = int(float(i[0]))
            if new_price < 100:
                new_price = 100
            new_price *= 2

            if int(float(new_price)) == int(float(i[3])):
                continue
            prices.append(
                {
                    "auto_action_enabled": "UNKNOWN",
                    "currency_code": "RUB",
                    "offer_id": i[2],
                    "price": f"{new_price}",
                    "product_id": 0
                }
            )
        if len(prices) > 0:
            update_prices(prices)

while True:
    start = time.time()
    asyncio.run(main())
    print('FINISHED:', time.time() - start)
    time.sleep(30)