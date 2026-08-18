import requests
from bs4 import BeautifulSoup
from ytmusicapi import YTMusic
import requests_cache

requests_cache.install_cache(
    "songs_cache",
    urls_expire_after={
        "*": 3600,
    }
)

input_date = input("Which Year do you want to travel to? Type the date in this format YYYY-MM-DD (eg. 2020-06-06)\n")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36"
}

response = requests.get(f"https://www.billboard.com/charts/hot-100/{input_date}", headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

song_titles = [song.text.strip() for song in soup.select(".o-chart-results-list-row h3#title-of-a-story.c-title")]

print(song_titles)

yt = YTMusic("browser.json")
playlists = yt.get_library_playlists()

for playlist in playlists:
    print(playlist)

playlistId = yt.create_playlist(f"{input_date} Billboard 100", f"top 100 songs from {input_date}")

videoIds = []

for song in song_titles:
    search_results = yt.search(query=song,filter="songs")
    videoIds.append(search_results[0]['videoId'])

print(videoIds)


try:
    add_song_response = yt.add_playlist_items(videoIds=videoIds, playlistId="PLOFrUYhV5pO0")
    print(add_song_response)
except Exception as error:
    print(f"error: {error}")