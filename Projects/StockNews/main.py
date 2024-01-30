import os
from dotenv import load_dotenv
from pathlib import Path
from stock import fetch_stock_data, calculate_percentage_change, get_last_two_dates
from news import fetch_news_data
from sms import send_sms

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
ENV_PATH = Path("..", "..", ".env")

load_dotenv(dotenv_path=ENV_PATH)

news_api_key = os.getenv("NEWS_API_KEY")
twilio_account_sid = os.getenv('TWILIO_ACCOUNT_SID')
twilio_auth_token = os.getenv('TWILIO_AUTH_TOKEN')
alphavantage_api_key = os.getenv('ALPHAVANTAGE_API_KEY')
twilio_phone_number = os.getenv('TWILIO_PHONE_NUMBER')
my_phone_number = os.getenv('MY_PHONE_NUMBER')


## Using https://www.alphavantage.co
time_series = fetch_stock_data(symbol=STOCK, api_key=alphavantage_api_key)

if time_series:
    # Calculate percentage change in stock price
    percentage_change = calculate_percentage_change(time_series)

    if percentage_change is not None:
        arrow = "🔺" if percentage_change > 0 else "🔻"
        percentage_change_str = f"{arrow}{percentage_change:.2f}%"

        # When STOCK price increase/decreases by at least 5% between yesterday and the day before yesterday
        if abs(percentage_change) >= 4:
            dates = get_last_two_dates(time_series)
            domains = [
                "dowjones.com",
                "reuters.com",
                "mtnewswires.com",
                "benzinga.com",
                "marketwatch.com",
                "zacks.com",
                "tradingview.com",
            ]
            ## Using https://newsapi.org
            # Get the first 3 news pieces for the COMPANY_NAME
            news = fetch_news_data(
                query={f'"+{COMPANY_NAME}"'},
                from_=dates[1],
                to=dates[0],
                api_key=news_api_key,
                domains=",".join(domains),
                sort_by="publishedAt",
            )

            ## Using https://www.twilio.com
            # Send a seperate message with the percentage change and each article's title and description to your phone number.
            news_body = f"{STOCK}: {percentage_change_str}\n"
            for new in news:
                headline = new['title']
                brief = new['description']
                news_body += f"Headline: {headline}.\nBrief: {brief}\n"

            send_sms(
                twilio_phone_number,
                my_phone_number,
                news_body,
                twilio_account_sid,
                twilio_auth_token,
            )
