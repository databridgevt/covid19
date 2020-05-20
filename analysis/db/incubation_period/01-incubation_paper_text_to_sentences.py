import pathlib as pl

import nltk.data
from nltk.tokenize import RegexpTokenizer
import pandas as pd

from pyprojroot import here

paper_df = pd.read_csv(here() / "data" / "db" / "final" / "kaggle" / "paper_text" / "document_parses_pmc_json.tsv", sep = "\t")

# can also load within the here function
# paper_df = pd.read_csv(here("./data/db/final/kaggle/paper_text/document_parses_pmc_json.tsv"), sep = "\t")

contains_incubation = paper_df.text.str.contains("incubation", case=False, regex=True)

incubation_df = paper_df[contains_incubation]

# break up into sentences
#import nltk
#nltk.download('punkt')
sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')

incubation_df["text_sent"] = incubation_df["text"].apply(lambda x: sent_detector.tokenize(x.strip()))


# save out working data
pl.Path(here("./data/db/working/kaggle/incubation", warn=False)).mkdir(parents=True, exist_ok=True)
incubation_df.to_pickle(here("./data/db/working/kaggle/incubation/01-sentences-incubation_period_days.pickle", warn=False))
