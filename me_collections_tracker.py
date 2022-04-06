from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from loguru import logger
import asyncio
import argparse
import json
import copy
from datetime import datetime


#command line parameters (temp until better solution)
parser = argparse.ArgumentParser(description='Startup settings for Magic Eden collections tracker')
parser.add_argument('--frequency', dest='freq',  default=60,
                    help='frequency to check in SECONDS')
parser.add_argument('--log', dest='log_level',  default='INFO',
                    help='frequency to check price in SECONDS')      
args= parser.parse_args()

#Initialize logger
logger.add("./logs/log_{time}.log", format="{time} {level} {message}", level=args.log_level, rotation="20 MB")
logger.info("MAGIC EDEN COLLECTIONS TRACKER")

previous_popular_collections_1day = {"default":"default"}
popular_collections_detailed = []
file_counter = 1

#refreshes price & volume info from dexlab once every 60 seconds
#probably need to update this to be more async friendly (in the requests.get s)
async def data_refresh():

    options = Options()
    #right now headless mode triggers captcha
    #options.add_argument('--headless')
    #options.add_argument('--disable-gpu') 
    service = Service(executable_path=ChromeDriverManager().install())
    browser = webdriver.Chrome(service=service,  chrome_options=options)


    #24hr popular collections
    browser.get('https://api-mainnet.magiceden.io/popular_collections?more=true&timeRange=24h')
    soup = BeautifulSoup(browser.page_source, "html.parser")
    popular_collections_1day = json.loads(soup.find('pre').get_text().strip())
    #print(popular_collections_1day["collections"][0])

    # loop through popular collections_1day and grab the collection_detail api for each of them
    for collection in popular_collections_1day["collections"]: 
        browser.get(f"https://api-mainnet.magiceden.io/rpc/getCollectionEscrowStats/{ collection['symbol'] }?edge_cache=true")
        soup = BeautifulSoup(browser.page_source, "html.parser")
        collection_detail = json.loads(soup.find('pre').get_text().strip())
        # 'floorPrice': 8300000000.000001, 'listedCount': 236, 'listedTotalValue': 265872650500000, 'avgPrice24hr': 6472140451.120419, 'volume24hr': 4944715304656, 'volumeAll': 20536579054765
        collection_snapshot = {"floorPrice":collection_detail["results"]['floorPrice'],"listedCount":collection_detail["results"]['listedCount'],"listedTotalValue":collection_detail["results"]['listedTotalValue'],"avgPrice24hr":collection_detail["results"]['avgPrice24hr'],"volume24hr": collection_detail["results"]['volume24hr'], "volumeAll":collection_detail["results"]['volumeAll']}
        collection_snapshot.update(collection)
        #print(collection_snapshot)
        popular_collections_detailed.append(collection_snapshot)
        await asyncio.sleep(1)

    #print(popular_collections_detailed)

    #ensure browser has focus & close it
    browser.switch_to.window(browser.window_handles[0])
    browser.close()

    # monitor how often the popular_collections_1day changes
    global previous_popular_collections_1day
    if popular_collections_1day != previous_popular_collections_1day:
        logger.info("Popular collections 1day data modified")

    previous_popular_collections_1day = popular_collections_1day

    now = datetime.now()
    with open(f"./popular_collection_24h_data/popular_collections_24h_{ now.strftime('%d_%m_%Y_%H_%M') }.json", 'w+') as outfile:
        json.dump(popular_collections_1day, outfile)

    #sleep 600 seconds & do it all over again
    await asyncio.sleep(600)


if __name__ ==  '__main__':
    loop = asyncio.get_event_loop()
    while True:
        loop.run_until_complete(data_refresh())


#all organizations
#browser.get('https://api-mainnet.magiceden.io/all_organizations')
#soup = BeautifulSoup(browser.page_source, "html.parser")
#all_organizations = json.loads(soup.find('pre').get_text().strip())
#print(all_organizations[-1]['name'])

#all collections 
#browser.get('https://api-mainnet.magiceden.io/all_collections')
#soup = BeautifulSoup(browser.page_source, "html.parser")
#all_collections = json.loads(soup.find('pre').get_text().strip())
#print(all_collections["collections"][1]["symbol"])