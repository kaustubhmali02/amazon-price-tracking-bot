import os
from email.message import EmailMessage

import requests
from bs4 import BeautifulSoup
import smtplib

MY_ACCOUNT = os.environ['MY_ACCOUNT']
MY_PASSWORD = os.environ['MY_PASSWORD']

PRODUCT_URL = "https://www.amazon.com/Instant-Pot-Duo-Evo-Plus/dp/B07W55DDFB/ref=sr_1_1?qid=1597662463"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
}

response = requests.get(
    url=PRODUCT_URL,
    headers=headers)

soup = BeautifulSoup(response.text, "lxml")
product_price = float(soup.find(name="span", class_="a-offscreen").getText().strip("$"))
product_name = str(soup.find(name="span", id="productTitle").getText().strip())
target_price = 270

if target_price >= product_price:
    message = f"{product_name}\n is now at ${product_price}\n" \
              f"Link for purchase: {PRODUCT_URL}"
    em = EmailMessage()
    em.set_content(message)
    em['To'] = MY_ACCOUNT
    em['From'] = MY_ACCOUNT
    em['Subject'] = "Low Price alart"
    with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:
        smtp.starttls()
        smtp.login(user=MY_ACCOUNT, password=MY_PASSWORD)
        smtp.send_message(em)
