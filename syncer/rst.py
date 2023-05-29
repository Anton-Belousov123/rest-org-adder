import asyncio
import aiohttp

from syncer.utils import timer


@timer
async def get_item_info_rst(session, data):
    async with session.get(data[1]) as resp:
        try:
            data2 = await resp.text()
            count = int(data2.split('quantity&quot;:')[1].split(',')[0])
            price = data2.split('price&quot;:&quot;')[1].split('&')[0]
            return price, count, data[0], data[2]
        except:
            return None, None, data[0], data[2]

