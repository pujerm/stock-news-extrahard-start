from twilio.rest import Client
import requests
import datetime

import os
from dotenv import find_dotenv, load_dotenv

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

account_sid = os.getenv("ACCOUNT_SID")
auth_token = os.getenv("AUTH_TOKEN")
api_key_alpha = os.getenv("API_KEY_ALPHA")



client = Client(account_sid, auth_token)

r = requests.get(f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=TSLA&apikey=={api_key_alpha}')
data = r.json()

td_1d = datetime.timedelta(days=1)
td_2d = datetime.timedelta(days=2)

yesterday_date = datetime.date.today() - td_1d
day_before_yesterday = datetime.date.today() - td_2d

yesterday_price = float(data['Time Series (Daily)'][f'{yesterday_date}']['4. close'])

day_before_yesterday_price = float(data['Time Series (Daily)'][f'{day_before_yesterday}']['4. close'])

difference_price = ((abs(yesterday_price - day_before_yesterday_price)) / day_before_yesterday_price)*100

sign = ''
if day_before_yesterday_price > yesterday_price:
    sign = "🔻"

else:
    sign = "🔺"

if difference_price > 5:
    r2 = requests.get(
        "https://newsapi.org/v2/everything?q=tesla&language=en&sortBy=publishedAt&pageSize=3&apiKey=4b759fc89ab348cfb03445b071385923")

    data2 = r2.json()["articles"]

    message = ''
    for x in data2:

        if (x['source']['name']) is not None:
            message += '\nHeadline: ' + str(x['title'] + '\nBrief: ' + str(x['description'] + '\n\n'))

    message = client.messages \
        .create(
        body=f"TSLA: {sign}{int(difference_price)}%\n{message}",
        from_='+15736335279',
        to='+48881248882'
    )

    print(message.status)



