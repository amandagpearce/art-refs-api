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
        production_year = production_info["year"]

        if production_year and production_title:
            trakt_api_url = f"https://api.trakt.tv/search/{api_endpoint}?query={production_title}"

            response = requests.get(trakt_api_url, headers=headers)

            if response.status_code == 200:
                trakt_response = response.json()
                print("trakt_response", trakt_response)

                if trakt_response:
                    # Check if there are multiple results
                    if len(trakt_response) > 1:
                        # Iterate through the results and find the one with a matching production_year
                        for result in trakt_response:
                            if result[api_endpoint]["year"] == production_year:
                                selected_result = result
                                break  # Stop iterating once a match is found

                        # If no match was found, you can choose a different handling logic or raise an exception
                        if selected_result is None:
                            print(
                                "No matching result found for the specified production_year."
                            )

                    # If there's only one result, select it
                    elif len(trakt_response) == 1:
                        selected_result = trakt_response[0]

                    print("selected_result", selected_result)

                    trakt_id = selected_result[api_endpoint]["ids"]["trakt"]

                    poster_url = fetch_poster(
                        selected_result[api_endpoint]["ids"]["tmdb"],
                        tmdb_base_url,
                    )

                    print("trakt_id", trakt_id)
                    print("poster_url", poster_url)

                    if trakt_id and poster_url:
                        production_model = model_class(
                            id=trakt_id,
                            productionTitle=production_title,
                            year=production_year,
                            imageUrl=poster_url,
                        )
                        db.session.add(production_model)
                        db.session.commit()

                        print("trakt_id", trakt_id)
                        print("len(production_data)", len(production_data))

                        if len(production_data) == 1:
                            print("return trakt_id", trakt_id)
                            return trakt_id
                    else:
                        print("Trakt query did not return data")
                        return
        else:
            print("production_year and production_title must be provided.")
            return
