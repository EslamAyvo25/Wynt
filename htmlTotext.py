from bs4 import BeautifulSoup
import asyncio
import requests



async def html_to_text(html_content):
    return await asyncio.to_thread(html_to_text_sync, html_content)

def html_to_text_sync(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    text = soup.get_text(separator=' ', strip=True)
    return text

