import requests
from bs4 import BeautifulSoup

url = "https://www.empireonline.com/movies/features/best-movies-2/"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9"
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

movies = [movie.text for movie in soup.select('strong') if any(char.isdigit() for char in movie.text[:3]) and ")" in movie.text]
movies.reverse()
# print(movies)

with open("Top 100 Movies.txt", 'w', encoding="utf-8") as file:
    file.write("\n".join(movies))