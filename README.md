# covid19
Data analysis of the 2020 COVID-19 pandemic

## Getting Started

See [this issue](https://github.com/databridgevt/covid19/issues/3) to get started

## Git Help

Git is hard. Here's a nice cheatsheet for the git commands you need to run as you are working:

https://chendaniely.github.io/training_ds_r/help-faq.html#general-workflow

You will mainly be using the "General workflow" and "Get changes from master on your branch" sections.

## Datasets

The Call to action and Kaggle datasets:

- [White House Call to Action](https://www.whitehouse.gov/briefings-statements/call-action-tech-community-new-machine-readable-covid-19-dataset/?utm_source=link&utm_medium=header)
- [Kaggle Dataset](https://www.kaggle.com/allen-institute-for-ai/CORD-19-research-challenge)
- [Allen Institute Semantic Scholar Dataset](https://pages.semanticscholar.org/coronavirus-research)

## Download data

See [this issue](https://github.com/databridgevt/covid19/issues/3) to download the kaggle dataset

## What are we working on?

[This issue](https://github.com/databridgevt/covid19/issues/4) links to the initial student project proposals.
But they can also be found in the `analysis/db/*/README.md` files

## Update instructions

### Update the conda environment

Run the conda environment update commands with:

```
conda activate db_covid19
conda env update --file environment.yml
```

There's a make target for you to make this easier: `make update_env`

### Update your code/repository

Before you start on a new branch, make sure your repository is updated with the lastest `master` code:

```
git checkout master
git pull origin master
```

## The Makefile

The `Makefile` is a convenient way to execute a bunch of commands, you can run `make all` or simply `make` and it will give you a print out of the targets and what they do.

## Team

Introduce yourself [here](https://github.com/databridgevt/covid19/issues/1)

#### Summer 2020

- **Project Lead**: **[Daniel Chen](https://daniel.rbind.io/)**: PhD student at Virginia Tech in [GBCB](https://gbcb.graduateschool.vt.edu/) studying data science and data literacy education in medical, biomedical, and health sciences.

- **Molecular Dynamics Lead**: **[Kelsie King](https://github.com/kelsieking23)**: Masters student in the [Virginia Tech Department of Biochemistry](https://www.biochem.vt.edu/) using computational methods to inform drug discovery for amyloid diseaes.

- **Makhsuda Ibragimova**: Undergraduate student at Virginia Tech majoring in CMDA. Doing research on energy sources and having zoom meetings every day :). Interested in doing research about COVID-19.

- **[Loveish Sarolia](https://github.com/loveishsarolia)**: Freshman student at Virginia Tech majoring in [Computational Modeling and Data Analytics](https://vt.edu/academics/majors/computational-modeling-and-data-analytics.html) as well as [Economics](https://econ.vt.edu/). Interested in economic analysis and blockchain development.

#### Spring 2020

- Project Lead: **[Daniel Chen](https://daniel.rbind.io/)**: PhD student at Virginia Tech in [GBCB](https://gbcb.graduateschool.vt.edu/) studying data science and data literacy education in medical, biomedical, and health sciences.

- Molecular Dynamics Lead: **[Kelsie King](https://github.com/kelsieking23)**: Masters student in the [Virginia Tech Department of Biochemistry](https://www.biochem.vt.edu/) using computational methods to inform drug discovery for amyloid diseases.

- **Makhsuda Ibragimova**: Undergraduate student at Virginia Tech majoring in CMDA. Doing research on energy sources and having zoom meetings every day :). Interested in doing research about COVID-19.

- **Ben Rayden**: Junior at Virginia Tech majoring in CMDA.

- **Chrissi Taylor**: First-year student at Virginia Tech majoring in CMDA. Familiar with Python and interested in Machine Learning.

- **Somya Jain**: Freshman at Virginia Tech majoring in CMDA.

- **Mitch Dolby**: Freshman at Virginia Tech currently majoring in Geography. Interested in geospatial sciences.

- **[Loveish Sarolia](https://github.com/loveishsarolia)**: Freshman student at Virginia Tech majoring in [Computational Modeling and Data Analytics](https://vt.edu/academics/majors/computational-modeling-and-data-analytics.html) as well as [Economics](https://econ.vt.edu/). Interested in economic analysis and blockchain development.
