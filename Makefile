#################################################################################
# GLOBALS                                                                       #
#################################################################################

#################################################################################
# COMMANDS                                                                      #
#################################################################################

## Get raw data
get-data:
	@echo "+ $@"
	@python3 src/get_data.py
.PHONY: get-data

## List DVC pipeline steps
dvc-pipe-list:
	@echo "+ $@"
	@python3 dvc_list_pipe.py -t list
.PHONY: dvc-pipe-list

## List DVC pipeline step details
dvc-pipe-details:
	@echo "+ $@"
	@python3 dvc_list_pipe.py -t details
.PHONY: dvc-pipe-details

## Run DVC pipeline
dvc-run-pipe:
	@echo "+ $@"
	@tox -e ci
.PHONY: dvc-run-pipe

## Run tests using containerized database
run-tests:
	@echo "+ $@"
	@tox -e test
.PHONY: run-tests

## Show test summary reports
test-summary:
	@echo "+ $@"
	@tox -e testsummary
.PHONY: test-summary

## Run tests and show summary reports
.PHONY: tests
tests: run-tests test-summary

## Show difference in DVC parameters relative to previous git commit
dvc-params-diff:
	@echo "+ $@"
	@dvc params diff --show-md
.PHONY: dvc-params-diff

## Show difference in DVC metrics relative to previous git commit
dvc-metrics-diff:
	@echo "+ $@"
	@dvc metrics diff --show-md
.PHONY: dvc-metrics-diff

## Show difference in plot relative to previous git commit
dvc-plot-diff:
	@echo "+ $@"
	@dvc plots diff -x recall -y precision
.PHONY: dvc-plot-diff

## Remove Python file artifacts
clean-py:
	@echo "+ $@"
	@find . -type f -name "*.py[co]" -delete
	@find . -type d -name "__pycache__" -delete
	@find . -name '*~' -delete
.PHONY: clean-pyc

## Remove test artifacts
clean-test-coverage:
	@echo "+ $@"
	@find "api/tests/test-logs/htmlcov" -type f -delete
	@rm -rf api/tests/test-logs/htmlcov
	@find "api/tests/test-logs/" -type f -name "*report*" -delete
	@rm -rf api/tests/test-logs/coverage.xml api/.coverage
.PHONY: clean-test-coverage

## Clean tests
.PHONY: clean-tests
clean-tests: clean-py clean-test-coverage

#################################################################################
# Self Documenting Commands                                                     #
#################################################################################

.DEFAULT_GOAL := help

# Inspired by <http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html>
# sed script explained:
# /^##/:
# 	* save line in hold space
# 	* purge line
# 	* Loop:
# 		* append newline + line to hold space
# 		* go to next line
# 		* if line starts with doc comment, strip comment character off and loop
# 	* remove target prerequisites
# 	* append hold space (+ newline) to line
# 	* replace newline plus comments by `---`
# 	* print line
# Separate expressions are necessary because labels cannot be delimited by
# semicolon; see <http://stackoverflow.com/a/11799865/1968>
.PHONY: help
help:
	@echo "$$(tput bold)Available rules:$$(tput sgr0)"
	@echo
	@sed -n -e "/^## / { \
		h; \
		s/.*//; \
		:doc" \
		-e "H; \
		n; \
		s/^## //; \
		t doc" \
		-e "s/:.*//; \
		G; \
		s/\\n## /---/; \
		s/\\n/ /g; \
		p; \
	}" ${MAKEFILE_LIST} \
	| LC_ALL='C' sort --ignore-case \
	| awk -F '---' \
		-v ncol=$$(tput cols) \
		-v indent=19 \
		-v col_on="$$(tput setaf 6)" \
		-v col_off="$$(tput sgr0)" \
	'{ \
		printf "%s%*s%s ", col_on, -indent, $$1, col_off; \
		n = split($$2, words, " "); \
		line_length = ncol - indent; \
		for (i = 1; i <= n; i++) { \
			line_length -= length(words[i]) + 1; \
			if (line_length <= 0) { \
				line_length = ncol - indent - length(words[i]) - 1; \
				printf "\n%*s ", -indent, " "; \
			} \
			printf "%s ", words[i]; \
		} \
		printf "\n"; \
	}' \
	| more $(shell test $(shell uname) = Darwin && echo '--no-init --raw-control-chars')
