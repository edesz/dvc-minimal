#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import argparse
import logging
import os

import pandas as pd
import yaml
from sklearn.model_selection import train_test_split


def prepare_dataset(
    raw_data_filepath,
    test_frac,
    train_filepath,
    test_filepath,
    categorical_columns,
    numerical_columns,
):
    logger = logging.getLogger(__name__)
    logger.info("Begin train-test split preparation...")

    df = pd.read_csv(raw_data_filepath)

    target = "survived"

    # Get features and target
    df = df[categorical_columns + numerical_columns + [target]]
    y = df[target]

    # Train-test split
    train, test = train_test_split(
        df, stratify=y, test_size=test_frac, random_state=42
    )

    train.to_csv(train_filepath, index=False)
    test.to_csv(test_filepath, index=False)

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
    raw_data_file = args.raw_data_filename

    params = yaml.safe_load(open("params.yaml"))["prepare"]
    test_frac = params["test_frac"]
    categorical_columns = params["categorical_columns"]
    numerical_columns = params["numerical_columns"]

    data_dir = "data"
    prepared_data_dir = os.path.join(data_dir, "prepared")
    raw_data_filepath = os.path.join(data_dir, raw_data_file)
    train_filepath = os.path.join(prepared_data_dir, "train.csv")
    test_filepath = os.path.join(prepared_data_dir, "test.csv")

    prepare_dataset(
        raw_data_filepath,
        test_frac,
        train_filepath,
        test_filepath,
        categorical_columns,
        numerical_columns,
    )
