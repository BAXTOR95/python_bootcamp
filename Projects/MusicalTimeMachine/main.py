import requests
from spotify import Spotify
from bs4 import BeautifulSoup


# Function that checks if the date (str) is in the format YYYY-MM-DD
def is_valid_date(date):
    try:
        year, month, day = date.split("-")
        if len(year) == 4 and len(month) == 2 and len(day) == 2:
            return True
        else:
            return False
    except ValueError:
        return False


while True:
    user_input = input(
        "Which year do you want to travel to? Type the date in this format: YYYY-MM-DD: "
    )
    if is_valid_date(user_input):
        break
    else:
        print("Invalid date format. Please try again.")

response = requests.get(f"https://www.billboard.com/charts/hot-100/{user_input}")
response.raise_for_status()

web_page = response.text

soup = BeautifulSoup(web_page, "html.parser")

# Find all div blocks
div_blocks = soup.find_all("div", class_="o-chart-results-list-row-container")

songs_artists = []  # List to hold tuples of (Song Name, Artist)

for div in div_blocks:
    # Find the h3 tag for the song name
    song_name_tag = div.find("h3")
    song_name = song_name_tag.get_text(strip=True)

    # Use find_next_sibling to find the next span tag which is the artist
    artist_tag = song_name_tag.find_next_sibling("span")
    artist = artist_tag.get_text(strip=True) if artist_tag else "No artist found"

    # Append the tuple (Song Name, Artist) to the list
    songs_artists.append((song_name, artist))

# # Now, songs_artists contains a list of tuples of (Song Name, Artist) for each song in the Hot 100 chart
# for song, artist in songs_artists:
#     print(f"Song Name: {song}, Artist: {artist}")

# Spotify API
sp = Spotify()

user = sp.get_current_user()

songs_uri = []
for song, artist in songs_artists:
    song = sp.search_song_by_artist(song, artist)
    if song:
        songs_uri.append(song["uri"])

playlist = sp.create_playlist(
    user_id=user["id"],
    name=f"{user_input} Billboard Hot 100",
    description=f"Top 100 songs on Billboard for {user_input}",
    public=False,
)

# Add songs to the playlist if there are any
if songs_uri:
    sp.add_to_playlist(playlist_id=playlist["id"], songs_uri=songs_uri)
    print(f"Playlist created and songs added to '{user_input} Billboard Hot 100'")
