import requests
import re
from bs4 import BeautifulSoup
from data_entry_bot import DataEntryBot


def scrape_zillow_clone(url):
    """
    Scrape data from the Zillow Clone webpage and fill in the research form.

    Args:
        url (str): The URL of the webpage to scrape.
    """
    # Initialize DataEntryBot
    data_entry_bot = DataEntryBot()

    try:
        # Fetch webpage
        response = requests.get(url)
        response.raise_for_status()
        web_page = response.text

        # Parse webpage
        soup = BeautifulSoup(web_page, "html.parser")

        # Extract data
        li_elements = soup.select('#grid-search-results > ul > li')
        for li in li_elements:
            raw_address = li.find('address').get_text(strip=True)
            raw_price = li.find('span', {'data-test': 'property-card-price'}).get_text(
                strip=True
            )
            href = li.find('a', {'data-test': 'property-card-link'})['href']

            # Clean up address and price
            clean_address = re.sub(r'[\n\|]+', '', raw_address).strip()
            clean_price = re.sub(r'\D*(\$\d{1,3}(,\d{3})*).+', r'\1', raw_price)

            # Fill the form with the data
            data_entry_bot.fill_form(clean_address, clean_price, href)

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Quit the browser session
        data_entry_bot.quit()


def main():
    """
    Main function.
    """
    zillow_clone_url = "https://appbrewery.github.io/Zillow-Clone/"
    scrape_zillow_clone(zillow_clone_url)


if __name__ == "__main__":
    main()
