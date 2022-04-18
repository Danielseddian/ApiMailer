import asyncio
from rest_framework import request


async def send_mailing_by_url(url, message_body):
    print(url)
    await asyncio.sleep(2)
    print(message_body)
    await asyncio.sleep(2)


