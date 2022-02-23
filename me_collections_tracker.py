from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from loguru import logger
import argparse
import json

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

previous_popular_collections_1day = {}


options = Options()
#right now headless mode triggers captcha
#options.add_argument('--headless')
#options.add_argument('--disable-gpu') 
service = Service(executable_path=ChromeDriverManager().install())
browser = webdriver.Chrome(service=service,  chrome_options=options)

#all organizations
browser.get('https://api-mainnet.magiceden.io/all_organizations')
soup = BeautifulSoup(browser.page_source, "html.parser")
all_organizations = json.loads(soup.find('pre').get_text().strip())

#24hr popular collections
browser.get('https://api-mainnet.magiceden.io/popular_collections?more=true&timeRange=24h')
soup = BeautifulSoup(browser.page_source, "html.parser")
popular_collections_1day = json.loads(soup.find('pre').get_text().strip())

#all collections 
browser.get('https://api-mainnet.magiceden.io/all_collections')
soup = BeautifulSoup(browser.page_source, "html.parser")
all_collections = json.loads(soup.find('pre').get_text().strip())

#example listed data(honey genesis bees)
browser.get('https://api-mainnet.magiceden.io/rpc/getCollectionEscrowStats/honey_genesis_bee?edge_cache=true')
soup = BeautifulSoup(browser.page_source, "html.parser")
collection_detail = json.loads(soup.find('pre').get_text().strip())

# boom
print(all_organizations[-1]['name'])
print(all_collections["collections"][1]["symbol"])
print(popular_collections_1day["collections"][1]["symbol"])
print(collection_detail["results"]["floorPrice"])

# now...loop through popular collections_1day and grab the collection_detail api for each of them

# monitor how often the popular_collections_1day changes
if popular_collections_1day != previous_popular_collections_1day:
    logger.info("Popular collections 1day data modified")


previous_popular_collections_1day = popular_collections_1day