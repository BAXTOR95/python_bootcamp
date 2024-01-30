import requests


def fetch_news_data(query, from_, to, api_key, domains, sort_by="relevancy", limit=3):
    """
    Fetch the latests news from the given date period for a specific query
    """
    url = "https://newsapi.org/v2/everything"
    parameters = {
        "q": query,
        "from": from_,
        "to": to,
        "sortBy": sort_by,
        "apiKey": api_key,
        "domains": domains,
    }

    response = requests.get(url, params=parameters)

    if response.status_code == 200:
        data = response.json()
        articles = data["articles"][:limit]
        return articles
    else:
        print('Failed to retrieve news data')
        response.raise_for_status()
        return None
