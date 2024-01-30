import requests


def fetch_stock_data(symbol, api_key):
    """
    Fetch the latest two days of stock data for the given symbol
    """
    url = "https://www.alphavantage.co/query"
    parameters = {
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol,
        "apikey": api_key,
        "outputsize": "compact",  # Retrieves the latest 100 data points
    }

    response = requests.get(url, params=parameters)

    if response.status_code == 200:
        data = response.json()
        time_series = data["Time Series (Daily)"]
        return time_series
    else:
        print('Failed to retrieve stock data')
        response.raise_for_status()
        return None


def get_last_two_dates(time_series):
    """
    Get last two available dates from a time_series
    """
    return list(time_series.keys())[:2]  # Get the last two dates


def calculate_percentage_change(time_series):
    """
    Calculate the percentage change in closing price between the last two available days.
    """
    dates = get_last_two_dates(time_series)

    if len(dates) < 2:
        print("Not enough data available.")
        return None

    # Extract closing prices for the last two days
    closing_prices = [float(time_series[date]['4. close']) for date in dates]

    # Calculate the percentage change between the two days
    percentage_change = (
        (closing_prices[0] - closing_prices[1]) / closing_prices[1]
    ) * 100

    return percentage_change
