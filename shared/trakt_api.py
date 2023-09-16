import os
import requests

from dotenv import load_dotenv

from db import db
from series.models import Series as SeriesModel
from movies.models import Movies as MoviesModel

from shared.tmdb_api import fetch_poster

load_dotenv()
trakt_api_key = os.getenv("TRAKT_API_KEY")


def fetch_and_populate(production_type, production_data):
    headers = {
        "Content-Type": "application/json",
        "trakt-api-version": "2",
        "trakt-api-key": trakt_api_key,
    }

    if len(production_data) == 0:
        print("production_data is empty")
        return

    if production_type == "series":
        api_endpoint = "show"
        model_class = SeriesModel
        tmdb_base_url = "https://api.themoviedb.org/3/tv/"
    elif production_type == "movie":
        api_endpoint = "movie"
        model_class = MoviesModel
        tmdb_base_url = "https://api.themoviedb.org/3/movie/"
    else:
        print("Invalid production_type")
        return

    for production_info in production_data:
        print("production_info", production_info)
        production_title = production_info["title"]
        trakt_api_url = f"https://api.trakt.tv/search/{api_endpoint}?query={production_title}"

        response = requests.get(trakt_api_url, headers=headers)

        if response.status_code == 200:
            production_data = response.json()

            if production_data:
                production_data_found = production_data[
                    0
                ]  # Get the first result from search

                production_endpoint = api_endpoint

                trakt_id = production_data_found[production_endpoint]["ids"][
                    "trakt"
                ]
                production_title = production_data_found[production_endpoint][
                    "title"
                ]
                production_year = production_data_found[production_endpoint][
                    "year"
                ]

                poster_url = fetch_poster(
                    production_data_found[production_endpoint]["ids"]["tmdb"],
                    tmdb_base_url,
                )

                if (
                    trakt_id
                    and production_title
                    and production_year
                    and poster_url
                ):
                    production_model = model_class(
                        id=trakt_id,
                        productionTitle=production_title,
                        year=production_year,
                        imageUrl=poster_url,
                    )
                    db.session.add(production_model)
                    db.session.commit()

                    if len(production_data) == 1:
                        print("return trakt_id", trakt_id)
                        return trakt_id
