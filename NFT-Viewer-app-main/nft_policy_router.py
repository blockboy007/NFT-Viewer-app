from scrapy.http import TextResponse
import requests
import lxml
import bs4
import time
from api_calls import ada_price_api
from api_calls import price_api


#########################################
# Set up for selenium and requests calls
#########################################


wallet_id = "addr1q8s3nu0awkp6twyd5xszagqvqc7vzpfer8cuxmx46spapjlx4vzk560guuw4tyvhuwpeknkc0l25jp2hxckhvp5g0ygs7j59qw"
nft_dict={}


def create_dict(wallet_id):

    req = requests.get(f"https://cardanoscan.io/address/{wallet_id}")
    soup = bs4.BeautifulSoup(req.content,"html5lib")
    nft = soup.find_all("option")[10:]
    ##### Need to start at 10, because the :9 are built into the cardanoscan website and not relevant
    count = 1
    for item in nft:

        asset_id = item['value']
        var = item.text
        policy_id = var.split(":")[2][:56]
        asset_name = var.split(":")[0]
        nft_dict[count] = [asset_name, asset_id, policy_id]
        count += 1

    # for key, val in nft_dict.items():
    #     print(f"{key} --- Asset Name: {val[0]} --- Asset ID: {val[1]} --- Policy ID: {val[2]}")

    return nft_dict


def get_img_id(create_dict):
    #########################
    # Getting NFT image
    #########################

    url = 'https://www.coingecko.com/en/coins/cardano'
    resp = requests.get(url)
    resp = TextResponse(body=resp.content, url=url)

    resp.css('img.tw-rounded-full').attrib['src']

    ##################################################
    # getting the real asset #
    #######################################

    for key, val in nft_dict.items():
        cs_url = f"https://cardanoscan.io/token/{nft_dict[key][1]}"
        try:
            get_assetid = requests.get(cs_url)
            get_assetid = TextResponse(body=get_assetid.content, url=url)
            var1 = str(get_assetid.css('div#fingerprintButton').attrib['onclick']
                       .replace('copyToClipboard', '')
                       .replace("(", "")
                       .replace(")", "")
                       .replace("fingerprintButton", "")

                       )

            new_id = (var1.split(",")[0])[1:-1]

            ### open cexplorer.io with real asset id
            ceexplorer = f"https://cexplorer.io/asset/{new_id}"

            ### grab img address
            get_img = requests.get(ceexplorer)
            get_img = TextResponse(body=get_img.content, url=url)

            img = get_img.css('img.img-fluid').attrib['src']
            nft_dict[key].append(img)
        except:
            # print('This is a native token, not an NFT')
            nft_dict[key].append("https://miro.medium.com/max/1168/1*7MR5KsgkJad8QTo2e7DVjg.png")


#############################################################
# Get the ADA and USD price from each policy_id
#############################################################





# my_iter = iter(nft_dict.items())
# print(next(my_iter))
