from datetime import datetime
import itertools
import pathlib as pl
import re
import sys

import nltk.data
from nltk.tokenize import RegexpTokenizer
import pandas as pd
from pyprojroot import here
from tqdm import tqdm

# def find_pattern_in_list(sent, pattern):
#     return [bool(re.search(pattern, x)) for x in sent]


# def has_search_terms(dat, term, pattern, sent_col):
#     term_sentences = dat[sent_col].progress_apply(find_pattern_in_list, pattern=pattern)
#     new_term_string = term.replace(" ", "_")
#     dat[f"has-{new_term_string}"] = any(term_sentences)
#     dat[f"found-{new_term_string}"] = term_sentences
#     return(dat)


def convert_term_to_regex(term):
    words = term.split(" ")
    regex_pattern = ""
    for term in words:
        regex_pattern += f"(?=.*\\b{term}\\b)"
    regex_pattern += ""
    return regex_pattern
assert convert_term_to_regex("incubation period") == "(?=.*\\bincubation\\b)(?=.*\\bperiod\\b)"


def find_matches_in_list(sentences, terms):
    """Determins if a term exists in a list of sentences
    """
    matches = {}
    for trm in terms:
        #breakpoint()
        pattern = convert_term_to_regex(trm)
        for sent in sentences:
            if (re.search(pattern, sent)):
                matches[trm] = True
                break # if there is a pattern match go to the next term
    return(matches)
assert find_matches_in_list(['hello my name is dan', 'hello you', 'the quick brown fox', 'my I have a word?'],
                     ['hello dan', 'fox', 'tom nook', 'word']) == {
                         'hello dan': True,
                         'fox': True,
                         'word': True,
                     }


script = sys.argv[0]
flag_test = True if '--test' in sys.argv else False

if flag_test:
    print("running test")
    paper_df = pd.read_csv(here("./data/db/final/kaggle/paper_text/document_parses_pmc_json.tsv"),
                           sep = "\t",
                           nrows=10)
else :
    paper_df = pd.read_csv(here("./data/db/final/kaggle/paper_text/document_parses_pmc_json.tsv"),
                           sep = "\t")

start_time = datetime.now()

# break up into sentences
sent_detector = nltk.data.load('tokenizers/punkt/english.pickle') # nltk.download('punkt')

tqdm.pandas(desc="Split sentences")
paper_df["text_sent_lower"] = paper_df["text"].progress_apply(lambda x: sent_detector.tokenize(x.lower().strip()))

# search for terms
search_terms = [
    "incubation period",
    "infectiousness period",
    "recovery rate",
    "case fatality ratio",
    "case fatality rate",
    "asymptomatic fraction",
    "asymptomatic proportion",
    "asymptomatic ratio",
    "hospitalized fraction",
    "hospitalized proportion",
    "latent period",
]

tqdm.pandas(desc="Finding terms")
paper_df['found_terms'] = paper_df['text_sent_lower'].progress_apply(find_matches_in_list, terms=search_terms)

# save out working data
if not flag_test:
    pl.Path(here("./data/db/working/kaggle/id_model_inputs", warn=False)).mkdir(parents=True, exist_ok=True)
    paper_df.to_pickle(here("./data/db/working/kaggle/id_model_inputs/01-sentences-keywords-2.pickle", warn=False))

end_time = datetime.now()

print(paper_df.head())
print('Duration: {}'.format(end_time - start_time))
