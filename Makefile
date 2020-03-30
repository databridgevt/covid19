.PHONY: envs
envs:
	conda env export --no-builds | grep -v "prefix" > environment.yml # https://github.com/conda/conda/issues/4339
	pip freeze > requirements.txt
