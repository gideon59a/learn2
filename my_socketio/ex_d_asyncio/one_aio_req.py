''' A client based on async http. It sends messages to a server that in this case happens to be synchronous,
specifically, the one in ex_b.  '''

import aiohttp
import asyncio

url1 = "http://127.0.0.1:5902/get_op_status/1"

async def main():

    async with aiohttp.ClientSession() as session:
        async with session.get(url1) as resp:
            jresponse = await resp.json()
            print(f'{type(jresponse)} {jresponse}')

asyncio.run(main())
