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

#########################################
## Set up for selenium and requests calls
#########################################


wallet_id = "addr1q8vnwuz7tcn5eycs7073m3runv4r2gc7gwd6nkvtjxqtcd7g6vfkkxad5y2mml0e7tw07c6klme5md8mw5cm85lyhuwqyapkxj"
cardano_scan = f"https://cardanoscan.io/address/{wallet_id}"
r = requests.get(cardano_scan).content
# path = "C:\Program Files (x86)\chromedriver.exe"
# driver = webdriver.Chrome(path)
# driver.get(cardano_scan)
soup = bs4.BeautifulSoup(r, "lxml")

#############################################################################################################
## Getting all information of NFTs in wallet into a dictionary, sorted by asset id[0] and policy id[1] for num
##############################################################################################################
nft_dict = {0: ['asset_id', 'policy_id']}
nft = soup.find_all("option")[10:]
count = 1
for item in nft:

    asset_id = item['value']
    var = item.text
    policy_id = var.split(":")[2]
    nft_dict[count] = [asset_id, policy_id]
    count += 1

print(nft_dict)
