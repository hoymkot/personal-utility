# -*- coding: utf8 -*-
import requests

import logging
from email.mime.text import MIMEText
from email.header import Header
import smtplib

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# Third-party SMTP service for sending alert emails. 第三方 SMTP 服务，用于发送告警邮件
mail_host = "smtp.qq.com"       # SMTP server, such as QQ mailbox, need to open SMTP service in the account. SMTP服务器,如QQ邮箱，需要在账户里开启SMTP服务
mail_user = "*********@qq.com"  # Username 用户名
mail_pass = ""*********"  # Password, SMTP service password. 口令，SMTP服务密码
mail_port = 465  # SMTP service port. SMTP服务端口

# The notification list of alert emails. 告警邮件通知列表
email_notify_list = {
    "chrishouwakot@gmail.com"
}

def init():
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', filename='activity.log', level=logging.INFO)


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

def sendEmail(fromAddr, toAddr, subject, content):
    sender = fromAddr
    receivers = [toAddr]
    message = MIMEText(content, 'plain', 'utf-8')
    message['From'] = Header(fromAddr, 'utf-8')
    message['To'] = Header(toAddr, 'utf-8')
    message['Subject'] = Header(subject, 'utf-8')
    try:
        smtpObj = smtplib.SMTP_SSL(mail_host, mail_port)
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print("send email success")
        return True
    except smtplib.SMTPException as e:
        print(e)
        print("Error: send email fail")
        return False


def check_price():
    price = fetch_price()

    if (price == None):
        price = "unable to find price";

    msg = "Current Formula Price is {}".format(price)

    logging.info(msg)

    for toAddr in email_notify_list:
        sendEmail(mail_user, toAddr, msg, msg)


def main_handler(event, context):
    check_price()


if __name__ == '__main__':
    main_handler("", "")
