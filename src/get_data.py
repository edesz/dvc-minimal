#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import argparse
import logging
import os

import pandas as pd
from sklearn.datasets import fetch_openml


def download_data(raw_data_filepath):
    logger = logging.getLogger(__name__)

    if not os.path.exists(raw_data_filepath):
        logger.info("Retrieving raw data...")

        # Retrieve raw data
        X, y = fetch_openml(
            "titanic", version=1, as_frame=True, return_X_y=True
        )
        df = pd.concat([X, y], axis=1)

        # Export raw data
        df.to_csv(raw_data_filepath, index=False)
    else:
        logger.info(f"Found file at {raw_data_filepath}. Doing nothing.")

    logger.info("Done.")


if __name__ == "__main__":
    log_fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d",
        "--raw-data-filename",
        type=str,
        dest="raw_data_filename",
        default="data.csv",
        help="name of raw data file",
    )
    args = parser.parse_args()

    raw_data_filename = args.raw_data_filename

    PROJ_ROOT_DIR = os.getcwd()
    data_dir = os.path.join(PROJ_ROOT_DIR, "data")
    raw_data_filepath = os.path.join(data_dir, raw_data_filename)

    download_data(raw_data_filepath)
