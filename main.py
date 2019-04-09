import requests
import bs4 as bs
import re
import json
import logging
from threading import Thread

logging.basicConfig(level=logging.INFO, format = '%(asctime)s: %(message)s')
logging.basicConfig(filename='debug.log',level=logging.DEBUG, format = '%(asctime)s: %(message)s')

####
products_page_url = 'https://www.att.com/shop/wireless/accessories/game-of-thrones.html'
product = ''
search_url = 'https://www.att.com/shop/wireless/accessories/game-of-thrones.accessoryListGridView.html?taxoCategory=GAME-OF-THRONES&sortByProperties=newArrivals&showMoreListSize=30&offset=1&offsetValue=1&_=1554096545847'
kws = ['king', 'funko']
####

logging.info('''
    
   ____   _______   _____   _______     -------
  / __ \ |__   __| /   _ \ |__   __|  -====------
 | (__) |   | |    \  \ \_\   | |    -======------
 |  __  |   | |    /   \ __   | |    --====-------
 | |  | |   | |   |  (\ / /   | |     -----------
 |_|  |_|   |_|    \_____/    |_|       -------
    
    bot by @taquitoslayer

    sneaker twitter ruined funkos.
    ''')

headers = {
    'authority': 'www.att.com',
    'cache-control': 'max-age=0',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9,fr;q=0.8,es;q=0.7',
}

def monitor(profile):
    r = requests.session()
    r.cookies.clear()
    products = []
    fucked = False
    logging.info('MONITORING...')
    while not fucked:
        try:
            resp = r.get(search_url, headers=headers)
            soup = bs.BeautifulSoup(resp.text, 'lxml')
            for x in soup.find_all('a', {'class': 'clickStreamSingleItem'}):
                href = x.get('href')
                # line comprehension pretty cool
                if all(x in href for x in kws):
                # for y in kws:
                #     if y in x.get('href'):
                    logging.info(f'{profile} - found {kws} in url')
                    link = f'https://www.att.com{href}'
                    products.append(link)
                    products = list(set(products))
                    fucked = True
                else:
                    pass
        except Exception as e:
            logging.info(e)  
    return products, r


def get_ids(url, r):
    fucked = False
    while not fucked:
        try:
            r.get('https://www.att.com/', headers = headers)
            product_page = r.get(url, headers = headers)
            # UNRELIABLE REGEX LET'S GET IT
            next_json = re.findall(r'''__NEXT_DATA__ =(.*?);__NEXT_LOADED_PAGES__''', product_page.text)
            next_json = next_json[0].replace('//', '')
            json_load = json.loads(next_json)
            sku = json_load['props']['pageProps']['productField']['details']['selectedSkuDetails']['skuId']
            product_id = json_load['props']['pageProps']['productField']['details']['selectedSkuDetails']['productId']
            uuid = json_load['props']['pageProps']['profileInfo']['uuid']
            fucked = True
        except Exception as e:
            logging.info('add to cart sku/token scrape failed... product page not loaded?')
            logging.info(e)
            logging.info('trying again...')
            pass
    print(uuid)
    return sku, product_id, uuid

def add_to_cart(sku,pid, r):
    # lol he's making a new headers again big LOL ya fuck u try making this bot yourself
    # AND HE BROUGHT OVER THE SESSION (r)?? 
    headers = {
    'origin': 'https://www.att.com',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9,fr;q=0.8,es;q=0.7',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
    'content-type': 'application/json',
    'accept': '*/*',
    'authority': 'www.att.com',
    }
    payload = {
	"addItemCount": 1,
	"items": {
		"atg-rest-class-type": "java.util.ArrayList",
		"atg-rest-values": [{
			"catalogRefId": sku,
			"productId": pid,
			"quantity": 1,
			"atg-rest-class-type": "com.att.ecom.shopcore.view.OnlineAddCommerceItemInfo"
		}]
	},
	"pageType": "accessoryDetails",
	"wirelessBuyFlowType": "NEW"
    }
    fucked = False
    while not fucked:
        try:
            resp = r.post('https://www.att.com/services/shopwireless/model/atg/commerce/order/purchase/CartModifierActor/addItemToOrder', headers=headers, json=payload)
            cart_items = resp.json()['result']['methodReturnValue']['lobTypes']['WIRELESS']['losgs']
            for x in cart_items:
                logging.info('cart items: ' + str(resp.json()['result']['methodReturnValue']['lobTypes']['WIRELESS']['losgs'][x]['cartItems']))
                fucked = True
        except Exception as e:
            logging.info('add to cart failed...')
            logging.info(e)
            logging.info('trying again...')
            pass

def checkout(sku, product_id, uuid, fname, lname, mm, yyyy, cc_num, cvv, zip_, ship_name, address, city, zip_ship, state, email, r):
    logging.info(f'uuid found: {uuid}')
    add_to_cart(sku,product_id, r)
    logging.info('add to cart successful')
    headers = {
    'origin': 'https://www.att.com',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9,fr;q=0.8,es;q=0.7',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
    'content-type': 'application/json',
    'accept': '*/*',
    'authority': 'www.att.com',
    }
    r.get('https://www.att.com/cart/mycart.html', headers = headers)
    r.get('https://www.att.com/services/shopwireless/model/att/ecom/api/BuyFlowController/service?actionType=updateshippingmethods&delightScheduleInfo=&shippingMethod=Priority', headers = headers)
    logging.info('priority shipping selected')
    fucked = False
    while not fucked:
        try:
            # ok so technically you can grab this earlier, maybe shaving 1s off the bot, but i don't feel like rewriting this
            resp = r.get(f'https://www.att.com/apis/checkout/pre/v1/start/{uuid}', headers = headers)
            cloud_token = resp.json()['payload']['accessToken']
            logging.info(f'cloud token found: {cloud_token}')
            fucked = True
        except Exception as e:
            logging.info('cloud token not found...')
            logging.info(e)
            logging.info('trying again...')
            pass
    name_email_payload = {
	"personalInfo": {
		"contactNumbers": [{
			"type": "cell"
		}],
		"lastName": lname,
		"email": email,
		"firstName": fname
	},
	"personalAccountSetUp": {
		"content": "Do you authorize AT&T to send you automated calls or texts with information about your AT&T services? If so, select Yes."
	    }
    }
    headers = {
    'origin': 'https://www.att.com',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9,fr;q=0.8,es;q=0.7',
    'x-ccc-access-token': cloud_token,
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
    'content-type': 'application/json;charset=UTF-8',
    'accept': 'application/json, text/plain, */*',
    'referer': 'https://www.att.com/checkout/customerinformation.html',
    'authority': 'www.att.com',
    }
    #success response
    r.post(f'https://www.att.com/apis/checkout/v1/controller/{uuid}?type=personalInfo,personalAccountSetUp', headers = headers, json = name_email_payload)
    val_addy = {
	"attention": ship_name,
	"addressLine1": address,
	"city": city,
	"zipCode": zip_ship,
	"state": state,
	"addressType": "shippingAddress"
    }
    fucked = False
    while not fucked:
        try:
            resp = r.post(f'https://www.att.com/apis/checkout/address/v1/validateAddress/{uuid}', headers = headers, json = val_addy)
            if resp.json()['response']['status'] == 'success':
                logging.info('address submitted...')
                validated_addy = resp.json()['payload']['shippingAddress']['matchingAddressObjects'][0]
                fucked = True
            else:
                logging.info(resp.json()['response']['status'])
                logging.info('cannot submit address... trying again! :)')
        except Exception as e:
            logging.info('shipping address step error!')
            logging.info(e)

    validated_addy = {
	'address': {
		'shippingAddress': validated_addy
        }
    } 
    fucked = False
    while not fucked:
        try:
            resp = r.post(f'https://www.att.com/apis/checkout/v1/controller/{uuid}?type=address', headers = headers, json = validated_addy)
            if resp.json()['response']['status'] == 'success':
                logging.info('address validated...')
                fucked = True
            else:
                logging.info(resp.json())
                logging.info('cannot submit address... trying again! :)')
        except Exception as e:
            logging.info('shipping address validation step error!')
            logging.info(e)
    # didn't really check but do referer's matter? probably not. do i wanna spend time figuring that out? no.
    headers = {
    'origin': 'https://www.att.com',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9,fr;q=0.8,es;q=0.7',
    'x-ccc-access-token': cloud_token,
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
    'content-type': 'application/json;charset=UTF-8',
    'accept': 'application/json, text/plain, */*',
    'referer': 'https://www.att.com/checkout/paymentandterms.html',
    'authority': 'www.att.com',
    }
    cc_payload = {
	"paymentInfo": {
		"duetoday": {
			"type": "creditcard",
			"dueMonthly": 0,
			"name": f'{fname} {lname}',
			"expMonth": mm,
			"expYear": yyyy,
			"cardNumber": cc_num,
			"cvv": cvv,
			"zip": zip_
		    }
	    }
    } 
    fucked = False
    while not fucked:
        try:
            resp = r.post(f'https://www.att.com/apis/checkout/v1/controller/{uuid}?type=paymentInfo', headers = headers, json = cc_payload)
            if resp.json()['response']['status'] == 'success':
                logging.info('cc submitted...')
                fucked = True
            else:
                logging.info(resp.json())
                logging.info('cannot submit credit card... trying again! :)')
        except Exception as e:
            logging.info('credit card step error!')
            logging.info(e)
    headers = {
    'origin': 'https://www.att.com',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9,fr;q=0.8,es;q=0.7',
    'x-ccc-access-token': cloud_token,
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
    'content-type': 'application/json;charset=UTF-8',
    'accept': 'application/json, text/plain, */*',
    'referer': 'https://www.att.com/checkout/review.html',
    'authority': 'www.att.com',
    }
    submit_payload = {}
    fucked = False
    while not fucked:
        try:
            resp = r.post(f'https://www.att.com/apis/checkout/order/v1/submit/{uuid}', headers=headers,json = submit_payload)
            if resp.json()['response']['status'] == 'success':
                logging.info('order submitted!')
                fucked = True
            elif resp.json()['response']['status'] == 'FAILURE':
                logging.info(resp.json())
                logging.info('cc declined... trying again! :)')
            else:
                logging.info('order was not submitted... trying again! :)')
        except Exception as e:
            logging.info('credit card step error!')
            logging.info(e)
# thicc function args
def main_kw(x, fname, lname, mm, yyyy, cc_num, cvv, zip, ship_name, address, city, zip_ship, state, email):
    logging.info(f'{x} - using keywords to find item: {kws}')
    product, r = monitor(x)
    sku, product_id, uuid = get_ids(product[0], r)
    checkout(sku, product_id, uuid, fname, lname, mm, yyyy, cc_num, cvv, zip, ship_name, address, city, zip_ship, state, email, r)

# def main_link(url, x, fname, lname, mm, yyyy, cc_num, cvv, zip_, ship_name, address, city, zip_ship, state, email):
#     logging.info(f'using url to find item: {url}')
#     sku, product_id, uuid = get_ids(url)
#     checkout(sku, product_id, uuid, fname, lname, mm, yyyy, cc_num, cvv, zip_, ship_name, address, city, zip_ship, state, email)

def config():
    with open('config.json') as json_file:
        config = json.load(json_file)
    return config

config = config()


for x in config:
    fname = config[x]['fname']
    lname = config[x]['lname']
    mm = config[x]['mm']
    yyyy = config[x]['yyyy']
    cc_num = config[x]['cc_num']
    cvv = config[x]['cvv']
    zip_ = config[x]['zip']
    ship_name = config[x]['ship_name']
    address = config[x]['address']
    city = config[x]['city']
    zip_ship = config[x]['zip_ship']
    state = config[x]['state']
    email = config[x]['email']
    # cancerous function arguments let's gooooo
    kw = Thread(target=main_kw, args=(x, fname, lname, mm, yyyy, cc_num, cvv, zip_, ship_name, address, city, zip_ship, state, email))
    # l = Thread(target=main_link, args=(product, x, fname, lname, mm, yyyy, cc_num, cvv, zip_, ship_name, address, city, zip_ship, state, email))
    kw.start() 
    # l.start()
kw.join()
# hi project destroyer, let's not steal code.