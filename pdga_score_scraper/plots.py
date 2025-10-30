from pathlib import Path

from loguru import logger
from tqdm import tqdm
import typer

import pandas as pd
import matplotlib.pyplot as plt

from pdga_score_scraper.config import FIGURES_DIR, PROCESSED_DATA_DIR

app = typer.Typer()


@app.command()
def main():

    # TODO:  eventually pull from argument
    event_id = 89433

    # Load processed data
    df = pd.read_pickle(PROCESSED_DATA_DIR / f"{event_id}-processed.pkl")

    logger.success(f"Loaded data for Event {event_id}")

    logger.info("Beginning plot generation")

    print(df.columns)


if __name__ == "__main__":
    app()
