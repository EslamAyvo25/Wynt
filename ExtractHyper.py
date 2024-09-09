import fitz  
import asyncio
'''
Asynced 
worked and tested 
'''
async def extract_hyperlinks_async(file):
    return await asyncio.to_thread(extract_hyperlinks, file)

#return the hyper links in list to get every thing here 
def extract_hyperlinks(file):
    hyperlinks = []
    doc = fitz.open(file)

    for page_num in range(doc.page_count):
        page = doc[page_num]
        links = page.get_links()

        for link in links:
            if link['uri']:
                hyperlinks.append(link['uri'])

    return hyperlinks


