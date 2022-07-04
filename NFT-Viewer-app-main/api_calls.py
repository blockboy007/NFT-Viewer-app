import requests
import lxml
import bs4
import json


def price_api(policy_id):

    response_API = requests.get(
        f"https://api.opencnft.io/1/policy/{policy_id}/floor_price")
    data = response_API.text
    parse_json = json.loads(data)
    floor_price = int(parse_json['floor_price'])/1000000
    return floor_price


def ada_price_api():
    r = requests.get('https://www.coingecko.com/en/coins/cardano')
    soup = bs4.BeautifulSoup(r.content, 'lxml')
    gecko = soup.select(".no-wrap")[0]
    for item in gecko:
        ada_price = float(item[1:])
    return(ada_price)


################################
# Example grabbing floor price using policy id, iterating through nft_dict
################################
# for key,val in nft_dict.items():
#     price_api(val[2])
