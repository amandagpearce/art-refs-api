import os
import requests
from dotenv import load_dotenv


load_dotenv()
tmdb_api_key = os.getenv("TBDB_API_KEY")


def fetch_poster(tmdb_id, tmdb_url):
    tmdb_api_url = f"{tmdb_url}{tmdb_id}?api_key={tmdb_api_key}"
    tmdb_response = requests.get(tmdb_api_url)

    if tmdb_response.status_code == 200:
        tmdb_data = tmdb_response.json()
        image_path = tmdb_data["poster_path"]
        image_size = "w500"
        complete_url = f"https://image.tmdb.org/t/p/{image_size}/{image_path}"

        return complete_url
    return None
