import pandas as pd
#import spacy
from pyprojroot import here

# load the tab separated file
dat = pd.read_csv(here("./data/db/final/kaggle/paper_text/comm_use_subset.tsv"), sep="\t")

# look at the first few lines
dat.head()

# look at the column names, their data types, and number of non missing elements
dat.info()

# number of rows and columns
dat.shape