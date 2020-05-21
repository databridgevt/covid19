import itertools
import pathlib as pl

import nltk.data
from nltk.tokenize import RegexpTokenizer
import pandas as pd
from tqdm import tqdm

from pyprojroot import here


def has_search_terms(dat, term, text_col):
    term_sentences = dat[text_col].str.contains(term, case=False, regex=True)
    new_term_string = term.replace(" ", "_")
    dat[f"has-{new_term_string}"] = term_sentences
    return(dat)


paper_df = pd.read_csv(here() / "data" / "db" / "final" / "kaggle" / "paper_text" / "document_parses_pmc_json.tsv", sep = "\t")

# can also load within the here function
# paper_df = pd.read_csv(here("./data/db/final/kaggle/paper_text/document_parses_pmc_json.tsv"), sep = "\t")

search_terms = [
    "incubation period",
    "infectiousness period",
    "recovery rate",
    "case fatality ratio",
    "asymptomatic fraction",
    "hospitalized fraction"
]

has_terms_df = paper_df

for term in tqdm(search_terms):
    has_terms_df = has_search_terms(has_terms_df, term, 'text')

# tablulate term results
display(has_terms_df
     .filter(like="has-", axis='columns')
     .apply(lambda x: x.value_counts(dropna=False))
     .assign(count=lambda x: x.apply('sum', axis='columns'))
)

# break up into sentences
#import nltk
#nltk.download('punkt')
sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')

has_terms_df["text_sent"] = has_terms_df["text"].apply(lambda x: sent_detector.tokenize(x.strip()))


# save out working data
pl.Path(here("./data/db/working/kaggle/id_model_inputs", warn=False)).mkdir(parents=True, exist_ok=True)
has_terms_df.to_pickle(here("./data/db/working/kaggle/id_model_inputs/01-sentences-keywords.pickle", warn=False))
