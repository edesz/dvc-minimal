#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import argparse
import os
from typing import Any, Iterable, Tuple

import yaml


def signal_last(it: Iterable[Any]) -> Iterable[Tuple[bool, Any]]:
    iterable = iter(it)
    ret_var = next(iterable)
    for val in iterable:
        yield False, ret_var
        ret_var = val
    yield True, ret_var


space = "    "
branch = "│   "
tee = "├── "
last = "└── "


class color:
    PURPLE = "\033[95m"
    CYAN = "\033[96m"
    DARKCYAN = "\033[36m"
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    END = "\033[0m"


def show_step_details(params):
    for is_last_step, (step, step_params) in signal_last(
        params["stages"].items()
    ):
        if is_last_step:
            sep = space
            first_sep = last
        else:
            sep = branch
            first_sep = tee
        print(first_sep + color.CYAN + step + color.END)

        for step_type in ["desc", "cmd"]:
            print(f"{sep}{last}{step_type}")
            print(f"{sep}{space}{last}{step_params[step_type]}")

        for step_type in ["deps", "params", "outs", "metrics", "plots"]:
            if step_type in step_params:
                print(f"{sep}{last}{step_type}")
                for is_last_element, dep in signal_last(step_params[step_type]):
                    if is_last_element:
                        print(f"{sep}{space}{last}{dep}")
                    else:
                        print(f"{sep}{space}{tee}{dep}")


def show_step_list(params):
    print(color.BOLD + "Available steps:\n" + color.END)
    for step, step_params in params["stages"].items():
        desc = step_params["desc"]
        print(color.DARKCYAN + f"{step:<15}" + color.END + f"{desc}")


if __name__ == "__main__":
    PROJ_ROOT_DIR = os.getcwd()
    dvc_pipe_filepath = os.path.join(PROJ_ROOT_DIR, "dvc.yaml")
    params = yaml.safe_load(open(dvc_pipe_filepath))

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-t",
        "--summary-type",
        type=str,
        dest="summary_type",
        default="steps",
        help="type of pipeline summary to be displayed",
    )
    args = parser.parse_args()
    summary_type = args.summary_type

    if summary_type == "details":
        show_step_details(params)
    else:
        show_step_list(params)
