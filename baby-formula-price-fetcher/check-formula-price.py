import requests
import logging
import time
import datetime


# send alert when the price of formula is less than 24.99
def parse_text(text):
    # section one
    # <meta property="product:price:amount" content="24.99" />
    pre = '<meta property="product:price:amount" content="'
    begin = text.find('<meta property="product:price:amount" content="')
    if (begin == -1):
        return None;
    begin = begin + len(pre)
    end = text.find('" />', begin)
    return float(text[begin:end])


def fetch_price():
    # curl
    # 'https://www.costco.com/enfagrow-premium-non-gmo-toddler-next-step-formula-stage-3%2c-36.6-oz.product.100332452.html' \
    # - H 'user-agent: Mozilla/5.0 (Linux; Android 8.0; Pixel 2 Build/OPD3.170816.012) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Mobile Safari/537.36' \
    # - H 'accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'    url = "https://www.costco.com/enfagrow-premium-non-gmo-toddler-next-step-formula-stage-3%2c-36.6-oz.product.100332452.html"

    url = 'https://www.costco.com/enfagrow-premium-non-gmo-toddler-next-step-formula-stage-3%2c-36.6-oz.product.100332452.html'

    headers = {
"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'",
"User-Agent": "Mozilla/5.0 (Linux; Android 8.0; Pixel 2 Build/OPD3.170816.012) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Mobile Safari/537.36"}

    resp = requests.get(url, headers= headers)

    if resp.status_code != 200:
        # This means something went wrong.
        logging.error('GET fail {} {}'.format(resp.status_code, resp.text))
        return None
    else:
        text = resp.text;
        try:
            return  parse_text(text);

        except Exception as exp:
            logging.error(exp);
            return None;


def init():
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', filename='activity.log', level=logging.INFO)


if __name__ == '__main__':

    init()
    start_time = time.time()

    price = fetch_price()
    if (price == None):
        logging.error("unable to find price");
    else:
        print(price)
        if price < 21:
            print("buy")
        logging.info("price is {} at {} ".format(price, datetime.date.today()))

    print("run time %s seconds"  %  (time.time() - start_time));
