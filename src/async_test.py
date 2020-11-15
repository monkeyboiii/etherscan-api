import asyncio
import requests
from time import sleep


async def main():
    loop = asyncio.get_event_loop()
    future1 = loop.run_in_executor(None, requests.get, 'http://www.google.com')
    future2 = loop.run_in_executor(None, requests.get, 'http://www.baidu.com')  
    response1 = await future1
    response2 = await future2
    print(len(response1.text))
    print(len(response2.text))

    sleep(1)

    print('awaked')


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
