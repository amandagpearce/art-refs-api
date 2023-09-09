import os
import requests
from db import db
import json
from dotenv import load_dotenv
from series.models import Series as SeriesModel
from movies.models import Movies as MoviesModel


load_dotenv()
trakt_api_key = os.getenv("TRAKT_API_KEY")
tmdb_api_key = os.getenv("TBDB_API_KEY")


predefined_series = [
    {"title": "Euphoria"},
    {"title": "The Simpsons"},
    {"title": "Squid Game"},
    {"title": "The Queen’s Gambit"},
    {"title": "BoJack Horseman"},
    {"title": "Futurama"},
    {"title": "Family Guy"},
    {"title": "Hannibal"},
    {"title": "Succession"},
]

predefined_movies = [
    {"title": "Shirley: Visions of Reality"},
    {"title": "Cabaret"},
    {"title": "The Dreamers"},
    {"title": "A clockwork orange"},
    {"title": "About Schmidt"},
    {"title": "The Fifth Element"},
    {"title": "Shutter Island"},
    {"title": "Passion"},
    {"title": "Mad Max Fury Road"},
    {"title": "Forrest Gump"},
]


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


def fetch_and_populate_series():
    headers = {
        "Content-Type": "application/json",
        "trakt-api-version": "2",
        "trakt-api-key": trakt_api_key,
    }

    for series_info in predefined_series:
        series_title = series_info["title"]
        trakt_api_url = f"https://api.trakt.tv/search/show?query={series_title}"

        response = requests.get(trakt_api_url, headers=headers)

        if response.status_code == 200:
            series_data = response.json()

            if series_data:
                series = series_data[0]  # Get the first result from search

                json_formatted_str = json.dumps(series, indent=2)
                print(json_formatted_str)

                trakt_id = series["show"]["ids"]["trakt"]
                series_title = series["show"]["title"]
                series_year = series["show"]["year"]
                poster_url = fetch_poster(
                    series["show"]["ids"]["tmdb"],
                    "https://api.themoviedb.org/3/tv/",
                )

                if trakt_id and series_title and series_year and poster_url:
                    series_model = SeriesModel(
                        id=trakt_id,
                        productionTitle=series_title,
                        year=series_year,
                        imageUrl=poster_url,
                    )
                    db.session.add(series_model)
                    db.session.commit()


def fetch_and_populate_movies():
    headers = {
        "Content-Type": "application/json",
        "trakt-api-version": "2",
        "trakt-api-key": trakt_api_key,
    }

    for movie in predefined_movies:
        movie_title = movie["title"]
        trakt_api_url = f"https://api.trakt.tv/search/movie?query={movie_title}"

        response = requests.get(trakt_api_url, headers=headers)

        if response.status_code == 200:
            movie_data = response.json()

            if movie_data:
                movie_data_found = movie_data[
                    0
                ]  # Get the first result from search

                print("movie_data_found")
                # print(movie_data_found)
                # json_formatted_str = json.dumps(movie_data_found, indent=2)
                # print(json_formatted_str)

                trakt_id = movie_data_found["movie"]["ids"]["trakt"]
                movie_title = movie_data_found["movie"]["title"]
                movie_year = movie_data_found["movie"]["year"]

                poster_url = fetch_poster(
                    movie_data_found["movie"]["ids"]["tmdb"],
                    "https://api.themoviedb.org/3/movie/",
                )
                print("poster_url")
                print(poster_url)

                if trakt_id and movie_title and movie_year and poster_url:
                    movie_model = MoviesModel(
                        id=trakt_id,
                        productionTitle=movie_title,
                        year=movie_year,
                        imageUrl=poster_url,
                    )
                    db.session.add(movie_model)
                    db.session.commit()
