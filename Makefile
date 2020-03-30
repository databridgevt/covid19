.PHONY: envs
envs:
	conda env export --no-builds | grep -v "prefix" > environment.yml
	pip freeze > requirements.txt
