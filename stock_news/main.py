import requests
from twilio.rest import Client
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
ALPHA_VANTAGE_API = "VANTAGE_API"
NEWS_API = "NEWS_API"
account_sid = "TWILIO_ID"
auth_token = "TWILIO_TOKEN"

news_params = {
    "apiKey": NEWS_API,
    "qInTitle": COMPANY_NAME
}

stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": ALPHA_VANTAGE_API
}

# STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
response = requests.get("https://www.alphavantage.co/query", params=stock_params)
response.raise_for_status()
stock_data = response.json()["Time Series (Daily)"]
s_data = [value for (key, value) in stock_data.items()]

yesterday_data = s_data[0]
yesterday_closing_price = float(yesterday_data["4. close"])

day_before_yesterday_data = s_data[1]
day_before_yesterday_closing_price = float(day_before_yesterday_data["4. close"])

difference = yesterday_closing_price - day_before_yesterday_closing_price
up_down = None

if difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"

diff_percent = difference / yesterday_closing_price * 100


if abs(diff_percent) > 5:
    news_response = requests.get("https://newsapi.org/v2/everything", params=news_params)
    news_response.raise_for_status()
    news_articles = news_response.json()["articles"][:3]

    formatted_articles = \
        [f"{STOCK}: {up_down}{diff_percent}%\nHeadline: {article['title']}.\n Brief: {article['description']}" for article in news_articles]

    client = Client(account_sid, auth_token)

    for article in formatted_articles:
        message = client.messages \
            .create(
                body=article,
                from_='TWILIO_NUMBER',
                to='YOUR_NUMBER'
            )

        print(message.status)

# Optional: Format the SMS message like this:
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required
 to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the 
 height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required 
to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the 
height of the coronavirus market crash.
"""
