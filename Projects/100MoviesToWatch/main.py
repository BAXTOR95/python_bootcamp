import requests
import re
from bs4 import BeautifulSoup

URL = "https://web.archive.org/web/20200518073855/https://www.empireonline.com/movies/features/best-movies-2/"

response = requests.get(URL)
response.raise_for_status()

web_page = response.text

soup = BeautifulSoup(web_page, "html.parser")

movies = soup.find_all(name="h3", class_="title")

movie_titles = []
for movie in movies:
    # Split the text
    split_titles = re.split(r'\)|:', movie.getText())
    # Remove empty strings and strip whitespace
    split_titles = [title.strip() for title in split_titles if title]
    # Convert the first element to int and keep the rest as is
    split_titles[0] = int(split_titles[0])
    movie_titles.append(split_titles)

# reversing the movie lists to get the movies in the correct order
sorted_movie_titles = movie_titles[::-1]

# Open a file named 'movies.txt' in write mode
with open('movies.txt', 'w', encoding='utf-8') as file:
    # Iterate over each element in the sorted list
    for movie in sorted_movie_titles:
        file.write(f"{movie[0]}) {movie[1]}\n")
