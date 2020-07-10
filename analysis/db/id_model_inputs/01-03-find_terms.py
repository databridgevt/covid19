from datetime import datetime

from nltk.tokenize import word_tokenize
import pandas as pd
from pyprojroot import here
from tqdm import tqdm


def find_set_in_list(sent_set, terms):
    """Determins if a term exists in a list of sentences
    """
    matches = {}
    for trm in terms:
        trm_set = set(trm.split(" "))
        for st in sent_set:
            if (trm_set.issubset(st)):
                matches[trm] = True
                break # if there is a pattern match go to the next term
    return(matches)


# testing function
test_sent = ['dan hello', 'hello you', 'the quick brown fox', 'my I have a word?']
test_sent_set = [set(word_tokenize(sent)) for sent in test_sent]
assert find_set_in_list(test_sent_set,
                        ['hello dan', 'fox', 'tom nook', 'word']) == {
                          'hello dan': True,
                          'fox': True,
                          'word': True,
                        }


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

start_time = datetime.now()

paper_df = pd.read_pickle(here("./data/db/working/kaggle/id_model_inputs/01-02-tokenize_sentences.pickle"))


tqdm.pandas(desc="Finding terms")
paper_df["found_terms"] = paper_df["sent_set"].progress_apply(find_set_in_list, terms=search_terms)

paper_df.to_pickle(here("./data/db/working/kaggle/id_model_inputs/01-03-sent_keywords.pickle", warn=False))

end_time = datetime.now()

print(paper_df.head())
print('Duration: {}'.format(end_time - start_time))
