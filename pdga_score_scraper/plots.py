from pathlib import Path

from pandas.core.common import fill_missing_names

from loguru import logger

# from tqdm import tqdm
import typer

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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

    df = df.query("course_name == 'Nockamixon State Park'").copy()

    # Drop dnf rounds
    df = df[~df.round_dnf].copy()

    df = df.reset_index(drop=True).copy()
    # df.head()

    ax = df["Hole 1"].value_counts().sort_index().plot(kind="bar")
    # plt.show()
    name = "monkey"
    plt.savefig(fname=FIGURES_DIR / f"{event_id}/{name}.png", format="png")

    vals = range(-2, 6)
    par = [5, 4, 3, 4, 3, 4, 3, 4, 4, 4, 4, 3, 4, 5, 3, 3, 4, 4]

    fig, axs = plt.subplots(6, 3, sharey=True, figsize=(9, 12))
    fig.suptitle("Histograms of hole scoring relative par", fontsize=20)

    for i in range(18):

        rel_par = df[f"Hole {i+1}"] - par[i]
        counts = rel_par.value_counts().to_dict()

        for v in vals:
            if v not in counts.keys():
                counts[v] = 0

        ax = axs[i // 3, i % 3]

        ax.bar(counts.keys(), counts.values())
        # df[f"Hole {i + 1.plot(ax=ax, kind='bar', fontsize=14, title=f"Hole {i+1}")
        ax.set_title(f"Hole {i+1}", fontsize=12)
        ax.set_xticks(vals)
        # ax.set_xlabel("")

    fig.subplots_adjust(top=0.92, left=0.05, hspace=0.5, wspace=0.1)

    plt.savefig(fname=FIGURES_DIR / f"{event_id}/dog.png", format="png")

    return


if __name__ == "__main__":
    app()
