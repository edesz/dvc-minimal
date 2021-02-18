#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import sys
from importlib import import_module
from pathlib import Path

PROJECT_DIR = Path(__file__).parents[2]
MODULE_DIR = PROJECT_DIR / "src"
sys.path.append(str(MODULE_DIR))
my_mod = import_module("evaluate")
evaluate_pipe = getattr(my_mod, "evaluate_pipe")

testing_data_filename = "test.csv"
trained_model_filename = "model.pkl"

data_dir = PROJECT_DIR / "data"
features_dir = data_dir / "features"
testing_data_filepath = features_dir / testing_data_filename
trained_model_filepath = PROJECT_DIR / trained_model_filename


def test_evaluate_pipe_predict(tmp_path):
    d = tmp_path / "tests"
    d.mkdir()
    scores_filepath = d / "scores.json"
    plot_filepath = d / "prc.json"

    # Verify that the two .json files do not exist
    assert len(list(d.iterdir())) == 0

    evaluate_pipe(
        testing_data_filepath,
        str(scores_filepath),
        str(plot_filepath),
        trained_model_filepath,
    )

    # Verify that the two .json files do exist
    assert len(list(d.iterdir())) == 2
    assert list(d.iterdir()) == [scores_filepath, plot_filepath]
