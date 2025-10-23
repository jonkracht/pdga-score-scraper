from pathlib import Path

from loguru import logger
from tqdm import tqdm
import typer

import pandas as pd

from pdga_score_scraper.config import RAW_DATA_DIR, PROCESSED_DATA_DIR

app = typer.Typer()


def parse_score(score):
    hole_scores = score["HoleScores"]
    layout = score["Layout"]

    parsed_score = score.copy()
    del parsed_score["HoleScores"]
    del parsed_score["Layout"]

    # Extract layout features of interest
    parsed_score["CourseName"] = layout["CourseName"]
    parsed_score["LayoutName"] = layout["Name"]
    parsed_score["Holes"] = layout["Holes"]
    parsed_score["Par"] = layout["Par"]
    parsed_score["Length"] = layout["Length"]
    parsed_score["LengthUnits"] = layout["Units"]

    # Recast Hole scores
    for i in range(1, 19):
        parsed_score["Hole " + str(i)] = hole_scores[str(i)]

    return parsed_score


@app.command()
def main(event_id):

    # Load raw data
    # event_id = input("\nEnter tournament ID:  ")
    # event_id = sys.argv[1]

    print(f"Processing data from event {event_id}.")

    # data = pd.read_pickle(f"data/raw/{event_id}.pkl")
    data = pd.read_pickle(RAW_DATA_DIR / f"{event_id}.pkl")

    rounds = []

    for result in data["results"]:

        player_info = result.copy()

        scores = result["Scores"]
        del player_info["Scores"]

        for score in result["Scores"]:
            parsed_score = parse_score(score)
            rounds.append(player_info | parsed_score)

    df = pd.DataFrame(rounds)

    # Discard unwanted information
    df.drop(
        [
            "TournID",  # all data from same tournament
            "Pool",  # not sure what this even is
            "PlaceRank",  # unsure what this should mean but looks to be duplicate of DNF
            "Name",  # duplicated
            "TierLetter",
            "TierType",  # describes what tier tournament is
            "Teammates",  # completely empty; for doubles tournaments?
            "ThrowStatusID",  # something for real-time scoring
            "RoundField",  # duplicated information
            "HotRound",  # all values of False - not properly encoded?
            "RoundComplete",  # scope of this study is post-round analysis
        ],
        axis=1,
        inplace=True,
    )

    df = df[
        [
            "ResultID",
            "FirstName",
            "LastName",
            "PDGANum",
            "Division",
            "Place",
            "ToPar",
            "Tied",
            "Prize",
            "DNF",
            "Total",
            #'Avatar', 'ProfileURL', 'DivisionName',
            "FormattedPlace",
            "Class",
            "Rating",
            "RatingEffectiveDate",
            "Location",
            "Country",
            "Nationality",
            #'AvatarURL',
            "AverageRoundRating",
            "RatingDiff",
            #'ToParString',
            "ScoreID",
            "Round",
            #'RoundDate', #all rounds show same date
            "TeeTime",
            #'TeeStart',  # all started on Hole 1 e.g. tee times
            "RoundScore",
            "ScoreToPar",
            #'RoundToPar',
            "Birdies",
            #'BirdieHoles',
            "Bogeys",
            #'BogeyHoles',
            #'RoundComplete',
            "RoundRating",
            "CourseName",
            "LayoutName",
            "Holes",
            "Par",
            "Length",
            #'LengthUnits',
            "Hole 1",
            "Hole 2",
            "Hole 3",
            "Hole 4",
            "Hole 5",
            "Hole 6",
            "Hole 7",
            "Hole 8",
            "Hole 9",
            "Hole 10",
            "Hole 11",
            "Hole 12",
            "Hole 13",
            "Hole 14",
            "Hole 15",
            "Hole 16",
            "Hole 17",
            "Hole 18",
        ]
    ].copy()

    ### Rename columns
    rename_dict = {
        "ResultID": "result_id",
        "FirstName": "first_name",
        "LastName": "last_name",
        "PDGANum": "pdga_num",
        "Division": "tournament_division",
        "Place": "tournament_place",
        "ToPar": "tournament_total_to_par",
        "Tied": "tied_finish",
        "Prize": "prize",
        "DNF": "tournament_dnf",
        "Total": "shot_total",
        "FormattedPlace": "formatted_place",
        "Class": "player_class",
        "Rating": "player_rating",
        "RatingEffectiveDate": "rating_effective_date",
        "Location": "location",
        "Country": "country",
        "Nationality": "nationality",
        "AverageRoundRating": "tournament_average_rating",
        "RatingDiff": "tournament_rating_delta",
        "ScoreID": "score_id",
        "Round": "round",
        "TeeTime": "tee_time",
        "RoundScore": "round_score",
        "ScoreToPar": "score_to_par",
        "Birdies": "num_birdies",
        "Bogeys": "num_bogeys",
        "RoundRating": "round_rating",
        "CourseName": "course_name",
        "LayoutName": "layout_name",
        "Holes": "num_holes",
        "Par": "par",
        "Length": "layout_length",
    }

    df = df.rename(columns=rename_dict).reset_index(drop=True).copy()

    # Split "location" into town and state
    df[["city", "state"]] = df.location.str.split(",", expand=True)
    df = df.drop(["location"], axis=1).copy()

    # Recast prize into prize_usd so that it may be an integer
    df["prize"] = df.prize.replace(
        {
            "": "$0",
        }
    )
    df["prize_usd"] = df.prize.str.extract(r"(\d+)")
    df["prize_usd"] = df["prize_usd"].astype("int64")

    df = df.drop(["prize"], axis=1).copy()

    # Recast "player_rating" to be an Int64 dtype which allows missing values
    df["player_rating"] = df["player_rating"].astype("Int64")
    df["round_rating"] = df["round_rating"].astype("Int64")

    # Create "round_dnf" column
    df["round_dnf"] = df["round_score"] == 999

    # Recast "score_to_par" as an integer
    df["score_to_par"] = df.score_to_par.replace({"E": 0})
    df["score_to_par"] = df.score_to_par.astype(int)

    ## Reorder columns for readability
    new_col_order = [
        "first_name",
        "last_name",
        "city",
        "state",
        "country",
        "nationality",
        "pdga_num",
        "player_rating",
        "rating_effective_date",
        "player_class",
        "result_id",
        "tournament_division",
        "tournament_place",
        "tied_finish",
        "formatted_place",
        "shot_total",
        "tournament_total_to_par",
        "prize_usd",
        "tournament_dnf",
        "tournament_average_rating",
        "tournament_rating_delta",
        "score_id",
        "round",
        "tee_time",
        "course_name",
        "layout_name",
        "par",
        "round_score",
        "score_to_par",
        "round_dnf",
        "num_birdies",
        "num_bogeys",
        "round_rating",
        "num_holes",
        "layout_length",
        "Hole 1",
        "Hole 2",
        "Hole 3",
        "Hole 4",
        "Hole 5",
        "Hole 6",
        "Hole 7",
        "Hole 8",
        "Hole 9",
        "Hole 10",
        "Hole 11",
        "Hole 12",
        "Hole 13",
        "Hole 14",
        "Hole 15",
        "Hole 16",
        "Hole 17",
        "Hole 18",
    ]

    df = df[new_col_order].copy()

    df["rating_effective_date"] = pd.to_datetime(df["rating_effective_date"])

    # Save data
    pd.to_pickle(df, PROCESSED_DATA_DIR / f"{event_id}-processed.pkl")
    df.to_csv(PROCESSED_DATA_DIR / f"{event_id}-processed.csv")


if __name__ == "__main__":
    app()
