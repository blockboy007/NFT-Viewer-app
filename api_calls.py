from selenium import webdriver
import requests
import lxml
import bs4
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


def price_api(policy_id='ffa56051fda3d106a96f09c3d209d4bf24a117406fb813fb8b4548e3'):

    response_API = requests.get(
        f"https://api.opencnft.io/1/policy/{policy_id}/floor_price")
    print(response_API.status_code)
    data = response_API.text
    parse_json = json.loads(data)
    floor_price = int(parse_json['floor_price'])/1000000
    print(f'floor price is: {floor_price}')


def ada_price_api():
    r = requests.get('https://www.coingecko.com/en/coins/cardano')
    soup = bs4.BeautifulSoup(r.content, 'lxml')
    gecko = soup.select(".no-wrap")[0]
    for item in gecko:
        ada_price = float(item[1:])
    return(ada_price)


wallet_id = input("Input your wallet address here to get your NFTs.")

PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)
driver.get("https://pool.pm/search/")

element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "search"))
        )
search = driver.find_element(By.ID, "search")
search.send_keys(str(wallet_id))
search.send_keys(Keys.RETURN)
