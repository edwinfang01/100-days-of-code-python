import requests
import os
import dotenv
import requests_cache
from twilio.rest import Client


requests_cache.install_cache('stock_cache', expire_after=86400)

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

dotenv.load_dotenv()

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
STOCK_API_KEY = os.environ.get("STOCK_API_KEY")
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
NEWS_API_KEY = os.environ.get("NEWS_API_KEY")
account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
OWM_token = os.environ.get('OWM_TOKEN')
my_phone_number = os.environ.get('MY_PHONE_NUMBER')

    ## STEP 1: Use https://www.alphavantage.co/documentation/#daily
# When stock price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

#Get yesterday's closing stock price. Hint: You can perform list comprehensions on Python dictionaries. e.g. [new_value for (key, value) in dictionary.items()]

stock_api_params = {
    'function': 'TIME_SERIES_DAILY',
    'symbol': STOCK_NAME,
    'apikey': STOCK_API_KEY
}
response = requests.get(url=STOCK_ENDPOINT, params=stock_api_params)
response.raise_for_status()
data: dict = response.json()['Time Series (Daily)']
data_list = [value for (key, value) in data.items()]
source: str = 'CACHE' if getattr(response, 'from_cache', False) else 'API'
print(source)

latest_date_data = data_list[0]
latest_date_closing_price: str = latest_date_data['4. close']
print(latest_date_closing_price)

#Get the day before yesterday's closing stock price

second_latest_date_closing_price: str = data_list[1]["4. close"]
print(second_latest_date_closing_price)

#Find the positive difference between 1 and 2. e.g. 40 - 20 = -20, but the positive difference is 20. Hint: https://www.w3schools.com/python/ref_func_abs.asp

difference = float(latest_date_closing_price) - float(second_latest_date_closing_price)

#Work out the percentage difference in price between closing price yesterday and closing price the day before yesterday.

diff_percent = round( (difference / float(second_latest_date_closing_price)) * 100 )

#If percentage is greater than 5 then print("Get News").

if abs(diff_percent) > 5:
    print('get news')

    ## STEP 2: https://newsapi.org/ 
    # Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 

    #Instead of printing ("Get News"), use the News API to get articles related to the COMPANY_NAME.

    news_api_params = {
        'apiKey': NEWS_API_KEY,
        'qInTitle': COMPANY_NAME
    }

    response = requests.get(url=NEWS_ENDPOINT, params=news_api_params)
    response.raise_for_status()
    tesla_news = response.json()['articles']

    #Use Python slice operator to create a list that contains the first 3 articles. Hint: https://stackoverflow.com/questions/509211/understanding-slice-notation

    three_articles = tesla_news[:3]
    # print(three_articles)

    ## STEP 3: Use twilio.com/docs/sms/quickstart/python
    #to send a separate message with each article's title and description to your phone number.

    #Create a new list of the first 3 articles' headline and description using list comprehension.

    formatted_articles: list[str] = [f"Headline: {article['title']} \nBrief: {article['description']}" for article in three_articles]

    print(formatted_articles[0])

    #Send each article as a separate message via Twilio.
    client = Client(account_sid, auth_token)
    for article in formatted_articles:
        message = client.messages.create(
        body=f"{COMPANY_NAME}: 🔺 {diff_percent} \n{article}" if diff_percent > 0 else f"{COMPANY_NAME}: 🔻 {diff_percent} \n{article}",
        from_="whatsapp:+14155238886",
        to=f"whatsapp:{my_phone_number}",
        )
        print(message.status)
