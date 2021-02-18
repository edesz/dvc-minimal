#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import argparse
import logging
import os
import pickle

import pandas as pd
import yaml
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder


def train_ml_pipeline(training_data_filepath, param_grid, cats, nums):
    logger = logging.getLogger(__name__)
    logger.info("ML training...")

    # Load training data
    train = pd.read_csv(training_data_filepath)

    # Extract features and target
    X_train, y_train = train.iloc[:, :-1], train["survived"]

    # Create ML pipeline
    clf = RandomForestClassifier()
    categorical_encoder = OneHotEncoder()
    numerical_pipe = Pipeline([("imputer", SimpleImputer())])
    preprocessing = ColumnTransformer(
        [
            ("cat", categorical_encoder, cats),
            ("num", numerical_pipe, nums),
        ]
    )
    pipe = Pipeline([("pp", preprocessing), ("clf", clf)])
    gs = GridSearchCV(pipe, param_grid, n_jobs=-1, cv=5)

    # Train
    gs.fit(X_train, y_train)

    # Dump
    with open("model.pkl", "wb") as fd:
        pickle.dump(gs.best_estimator_, fd)

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
    args = parser.parse_args()
    training_data_filename = args.train_filename

    data_dir = "data"
    features_dir = os.path.join(data_dir, "features")
    training_features_filepath = os.path.join(
        features_dir, training_data_filename
    )

    params = yaml.safe_load(open("params.yaml"))["train"]

    pipe_param_grid = {
        "pp__num__imputer__strategy": params["imputer"]["strategy"],
        "pp__cat__handle_unknown": params["ohe"]["handle_unknown"],
        "clf__random_state": params["clf"]["seed"],
        "clf__n_estimators": params["clf"]["n_estimators"],
    }

    categorical_columns = params["categoricals"]
    numerical_columns = params["numericals"]

    train_ml_pipeline(
        training_features_filepath,
        pipe_param_grid,
        categorical_columns,
        numerical_columns,
    )
