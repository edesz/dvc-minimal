#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os
import argparse
import logging

import pandas as pd


def get_features(
    training_data_filepath,
    testing_data_filepath,
    training_features_filepath,
    testing_features_filepath,
):
    logger = logging.getLogger(__name__)
    logger.info("Getting features...")

    # Load train/test datasets
    train = pd.read_csv(training_data_filepath)
    test = pd.read_csv(testing_data_filepath)

    # ########## Add/Extract/Merge Non-ML related Features - START ##########
    # Exclude standardization, normalization, Categorical Encoding
    # ########## Add/Extract/Merge Non-ML related Features - END ##########

    # Export to train/test featurized datasets
    train.to_csv(training_features_filepath, index=False)
    test.to_csv(testing_features_filepath, index=False)

    logger.info("Done.")


if __name__ == "__main__":
    log_fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-r",
        "--train-filename",
        type=str,
        dest="train_filename",
        default="train.csv",
        help="name of training data file",
    )
    parser.add_argument(
        "-s",
        "--test-filename",
        type=str,
        dest="test_filename",
        default="test.csv",
        help="name of testing data file",
    )
    args = parser.parse_args()
    training_data_filename = args.train_filename
    testing_data_filename = args.test_filename

    data_dir = "data"
    prepared_data_dir = os.path.join(data_dir, "prepared")
    features_dir = os.path.join(data_dir, "features")
    train_filepath = os.path.join(prepared_data_dir, training_data_filename)
    test_filepath = os.path.join(prepared_data_dir, testing_data_filename)
    training_features_filepath = os.path.join(
        features_dir, training_data_filename
    )
    testing_features_filepath = os.path.join(
        features_dir, testing_data_filename
    )

    get_features(
        train_filepath,
        test_filepath,
        training_features_filepath,
        testing_features_filepath,
    )
