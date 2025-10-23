from pathlib import Path
import random
import sys

from loguru import logger
from tqdm import tqdm
import typer

import pickle
import requests
import time


from pdga_score_scraper.config import PROCESSED_DATA_DIR, RAW_DATA_DIR

app = typer.Typer()


@app.command()
def main(
    event_id,
):

    headers = {
        "value": "application/json, text/javascript, */*; q=0.01",
        "accept": "application/json, text/javascript, */*; q=0.01",
        "cookie": "cookie-agreed-version=1.0.1; clientSettings=%7B%22favoritePlayers%22%3A%5B%5D%2C%22showFavorites%22%3Atrue%2C%22metric%22%3Afalse%2C%22colorAccessibility%22%3Afalse%2C%22darkMode%22%3Atrue%2C%22throwTracker%22%3Atrue%2C%22userTimeZoneEnabled%22%3Atrue%7D",
    }

    url = "https://www.pdga.com/apps/tournament/live-api/live_results_fetch_event?TournID="

    page = requests.get(url + str(event_id), headers=headers)

    tournament_info = page.json()["data"]

    # Create division list from 'tournament_info'
    divisions = []
    for div in tournament_info["Divisions"]:
        divisions.append(div["Division"])

    # Grab 'live_layout'
    url = (
        "https://www.pdga.com/api/v1/live-tournaments/"
        + str(event_id)
        + "/live-layouts?include=LiveLayoutDetails"
    )
    live_layout = requests.get(url, headers=headers).json()

    # Create list of ResultID's
    result_ids = []
    baseurl = (
        "https://www.pdga.com/apps/tournament/live-api/live_results_fetch_updated_round_scores?TournID="
        + str(event_id)
        + "&Division="
    )

    for div in divisions:
        url = baseurl + div
        page = requests.get(url, headers=headers)
        data = page.json()["data"]

        for d in data:
            result_ids.append(d["ResultID"])

    # Get scoring for each 'ResultID'
    results = []

    baseurl = "https://www.pdga.com/apps/tournament/live-api/live_results_fetch_player?ResultID="

    logger.info("Beginning score grabbing.")
    for i, id in tqdm(enumerate(result_ids)):
        logger.info(f"Grabbing {i} of {len(result_ids)}")

        page = requests.get(baseurl + str(id))
        data = page.json()["data"]

        results.append(data)

        time.sleep(1)  # don't overload server, 0.25s is too short

        # Randomize wait times
        pause = random.choice([0.5 + x / 100 for x in range(50)])
        time.sleep(pause)

    logger.success("Completed grabbing scores.")

    # Place everything in a dictionary and pickle it
    data = {}

    data["tournament_info"] = tournament_info
    data["divisions"] = divisions
    data["live_layout"] = live_layout
    data["result_ids"] = result_ids
    data["results"] = results

    # Save data

    # TODO: use config filepaths
    with open(RAW_DATA_DIR / f"{event_id}.pkl", "wb") as f:
        pickle.dump(data, f)

    return


if __name__ == "__main__":
    app()
