.PHONY: envs
envs:
	conda env export --no-builds | grep -v "prefix" > environment.yml # https://github.com/conda/conda/issues/4339
	pip freeze > requirements.txt

.PHONY: setup
setup:
	conda env create --file environmet.yml

.PHONY: update
update:
	conda activate db_covid19
	conda update --file environment.yml

.PHONY: data
data:
	kaggle datasets download allen-institute-for-ai/CORD-19-research-challenge -p ./data/db/original/kaggle --unzip
