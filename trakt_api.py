import os
import requests
from models import Series as SeriesModel
from db import db

from dotenv import load_dotenv

load_dotenv()
trakt_api_key = os.getenv("TRAKT_API_KEY")
tmdb_api_key = os.getenv("TBDB_API_KEY")


def fetch_and_populate_series():
    trakt_api_url = "https://api.trakt.tv/shows/popular"
    headers = {
        "Content-Type": "application/json",
        "trakt-api-version": "2",
        "trakt-api-key": trakt_api_key,
    }
    params = {"limit": 100}

    response = requests.get(trakt_api_url, headers=headers, params=params)

    if response.status_code == 200:
        series_data = response.json()

        for series_info in series_data:
            trakt_id = series_info["ids"]["trakt"]
            tmdb_id = series_info["ids"]["tmdb"]
            series_title = series_info["title"]
            series_year = series_info["year"]
            poster_url = fetch_series_poster(tmdb_id)

            if trakt_id and series_title and series_year and poster_url:
                series = SeriesModel(
                    id=trakt_id,
                    title=series_title,
                    year=series_year,
                    imageUrl=poster_url,
                )
                db.session.add(series)
                db.session.commit()


def fetch_series_poster(tmdb_id):
    tmdb_api_url = (
        f"https://api.themoviedb.org/3/tv/{tmdb_id}?api_key={tmdb_api_key}"
    )
    tmdb_response = requests.get(tmdb_api_url)

    if tmdb_response.status_code == 200:
        tmdb_data = tmdb_response.json()
        image_path = tmdb_data["poster_path"]
        image_size = "w500"
        complete_url = f"https://image.tmdb.org/t/p/{image_size}/{image_path}"

        return complete_url
    return None
