<div align="center">
  <h1>Data Version Control (DVC) minimal project for ML</h1>
</div>

<div align="center">
  <a href="https://opensource.org/licenses/MIT"><img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-brightgreen.svg"></a>
  <a href="https://github.com/edesz/dvc-minimal/pulls"><img alt="PRs Welcome" src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square"></a>
  <a href="https://github.com/edesz/dvc-minimal/actions">
    <img src="https://github.com/edesz/dvc-minimal/workflows/CI/badge.svg"/>
  </a>
  <a href="https://github.com/edesz/dvc-minimal/actions">
    <img src="https://github.com/edesz/dvc-minimal/workflows/CodeQL/badge.svg"/>
  </a>
  <a href="https://en.wikipedia.org/wiki/Open-source_software"><img alt="Open Source?: Yes" src="https://badgen.net/badge/Open%20Source%20%3F/Yes%21/blue?icon=github"></a>
  <a href="https://pyup.io/repos/github/edesz/dvc-minimal/"><img src="https://pyup.io/repos/github/edesz/dvc-minimal/shield.svg" alt="Updates" /></a>
</div>
<div align="center">
<a href="https://codecov.io/gh/edesz/dvc-minimal">
    <img src="https://codecov.io/gh/edesz/dvc-minimal/branch/main/graph/badge.svg?token=JYERV7HUHM"/>
  </a>
  <a href="https://www.codacy.com/gh/edesz/dvc-minimal/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=edesz/dvc-minimal&amp;utm_campaign=Badge_Coverage"><img src="https://app.codacy.com/project/badge/Coverage/cc6ccfd808304591a67917cbb48e4183"/></a>
  <a href="https://www.codacy.com/gh/edesz/dvc-minimal/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=edesz/dvc-minimal&amp;utm_campaign=Badge_Grade"><img src="https://app.codacy.com/project/badge/Grade/e131f619fdfd48ceae58f0c1f732bb04"/></a>
  <a href="https://www.codefactor.io/repository/github/edesz/dvc-minimal"><img src="https://www.codefactor.io/repository/github/edesz/dvc-minimal/badge" alt="CodeFactor" /></a>
  <a href="https://codeclimate.com/github/edesz/dvc-minimal/maintainability"><img src="https://api.codeclimate.com/v1/badges/df44861748b3fc8616f0/maintainability" /></a>
</div>

## [Table of Contents](#table-of-contents)
-   [About](#about)

-   [Usage](#usage)
    -   [Local Development](#local-development)
    -   [Testing](#testing)

-   [Future Improvements](#future-improvements)

## [About](#about)
This is a minimal version of the CML with DVC and [Github Actions](https://github.com/features/actions). The following high-level customizations have been made

-   customized directory structure
    -   `data` directory with `raw` and `processed` sub-dirs to store raw and processed datasets respectively

-   use of [`tox`](https://tox.readthedocs.io/en/latest/) to manage [Python virtual environments](https://docs.python.org/3/tutorial/venv.html)

-   `Makefile` for convenience, based on two open-source projects ([1](https://github.com/drivendata/cookiecutter-data-science/tree/new-cli-tests), [2](https://github.com/hackebrot/pytest-cookies))

## [Usage](#usage)
### [Local Development](#local-development)
1.  Install the Python packages `dvc` and `tox` system-wide
    ```bash
    pip3 install -U dvc tox
    ```

2.  Get the raw data
    ```bash
    make get-data
    ```

3.  Clone this repo
    ```bash
    git clone https://github.com/edesz/dvc-minimal.git
    ```

4.  Initialize `git` repo and add files
    ```bash
    git init
    git add .
    git commit -m "initial commit"
    ```

5.  Initialize DVC
    ```bash
    dvc init
    ```

6.  Run DVC pipeline
    ```bash
    make ci  # runs dvc repro
    ```

7.  Commit changes to `git`
    ```bash
    git add .
    git commit -m "first training run"
    ```

8.  In `params.yaml`, change line 18 from 500 to 750 and save the file.

9.  Run DVC pipeline
    ```bash
    make ci  # runs dvc repro
    ```

10.  View the resulting difference in parameters and scoring metric between previous `git` commit (first training run) and current state (modified `params.yaml`), by running
     ```bash
     make dvc-params-diff  # dvc params diff --show-md
     ```
     and
     ```bash
     make dvc-metrics-diff  # dvc metrics diff --show-md
     ```

11.  View PR curve for previous `git` commit (first training run) and current state (modified `params.yaml`), by running
     ```bash
     make dvc-plot-diff  # dvc plots diff -x recall -y precision
     ```

12.  Commit changes to `git`
     ```bash
     git add .
     git commit -m "changed n_estimators in clf step of ml pipe"
     ```

### [Testing](#testing)
1.  Run steps 1-6 from [above](#usage), and ensure that a file `./model.pkl` exists in the root directory before proceeding

2.  Run tests and show reports (test summary and code coverage)
    ```bash
    make tests
    ```

3.  Clean up
    -   python artifacts in `dvc-minimal/src`
    -   testing artifacts, summary reports and coverage reports in `dvc-minimal/src/tests`

    by running
    ```bash
    make clean-tests
    ```

## [Future Improvements](#future-improvements)
A preliminary list of features planned to be implemented is shown below

1.  Add tests
    - to improve coverage
    - that relevant to the dataset

2.  Add instructions for checking out new branch and making a pull request

3.  Add plots to `evaluate.py`
