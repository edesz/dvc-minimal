#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import argparse
import json
import logging
import os
import pickle

import pandas as pd
import sklearn.metrics as metrics
from sklearn.metrics import precision_recall_curve


def evaluate_pipe(
    testing_data_filepath,
    scores_filepath,
    plot_filepath,
    trained_model_filepath,
):
    with open(trained_model_filepath, "rb") as fd:
        pipe = pickle.load(fd)

    # Load testing data
    test = pd.read_csv(testing_data_filepath)

    # Extract features and target
    X_test, y_test = test.iloc[:, :-1], test["survived"]

    # Inference
    y_pred = pipe.predict_proba(X_test)[:, 1]

    # Metrics and Plot
    precision, recall, thresholds = precision_recall_curve(y_test, y_pred)

    auc = metrics.auc(recall, precision)

    with open(scores_filepath, "w") as fd:
        json.dump({"auc": auc}, fd)

    with open(plot_filepath, "w") as fd:
        json.dump(
            {
                "prc": [
                    {"precision": p, "recall": r, "threshold": t}
                    for p, r, t in zip(precision, recall, thresholds)
                ]
            },
            fd,
        )


if __name__ == "__main__":
    log_fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-s",
        "--test-filename",
        type=str,
        dest="test_filename",
        default="test.csv",
        help="name of testing data file",
    )
    parser.add_argument(
        "-c",
        "--scores-filename",
        type=str,
        dest="scores_filename",
        default="scores.json",
        help="name of json file to log metrics",
    )
    parser.add_argument(
        "-p",
        "--plot-filename",
        type=str,
        dest="plot_filename",
        default="prc.json",
        help="name of json file to log metrics for plotting",
    )
    parser.add_argument(
        "-m",
        "--trained-model-filename",
        type=str,
        dest="trained_model_filename",
        default="model.pkl",
        help="name of saved model artifact, exported after training",
    )
    args = parser.parse_args()
    testing_data_filename = args.test_filename
    scores_filename = args.scores_filename
    plot_filename = args.plot_filename
    trained_model_filename = args.trained_model_filename

    data_dir = "data"
    features_dir = os.path.join(data_dir, "features")
    testing_features_filepath = os.path.join(
        features_dir, testing_data_filename
    )
    PROJ_ROOT_DIR = os.getcwd()
    scores_filepath = os.path.join(PROJ_ROOT_DIR, scores_filename)
    plot_filepath = os.path.join(PROJ_ROOT_DIR, plot_filename)
    trained_model_filepath = os.path.join(PROJ_ROOT_DIR, trained_model_filename)

    evaluate_pipe(
        testing_features_filepath,
        scores_filepath,
        plot_filepath,
        trained_model_filepath,
    )
