all : commands

## commands        : show all commands.
commands :
	@grep -E '^##' Makefile | sed -e 's/## //g'

## requirements    : creates requirements.txt from environment.yml
.PHONY: requirements
requirements:
	python scripts/env_conda2pip.py

## setup_env       : set up the conda environment using the environment.yml
.PHONY: setup_env
setup:
	conda activate base
	conda remove --name db_covid19 --all # removes the env if it already exists
	conda config --add channels conda-forge # adds conda forge as default channel
	conda config --set channel_priority strict
	conda env create --file environmet.yml

## update_env      : updates the conda environment using the environment.yml
.PHONY: update_env
update:
	conda activate db_covid19
	conda update --file environment.yml

## data_kaggle     : downloads he kaggle source data for the repository
.PHONY: data_kaggle
data_kaggle:
	kaggle datasets download allen-institute-for-ai/CORD-19-research-challenge -p ./data/db/original/kaggle --unzip

## data_kaggle     : downloads he kaggle source data for the repository
.PHONY: data_kgl_text
data_kgl_text:
	python ./analysis/db/dan/load_data.py
