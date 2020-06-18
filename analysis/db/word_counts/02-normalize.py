from collections import Counter
import itertools
import pathlib as pl

import pandas as pd
from pyprojroot import here
from tqdm import tqdm

from nltk.corpus import stopwords  # nltk.download('stopwords')
from nltk.stem import WordNetLemmatizer  # nltk.download('wordnet')


papers_token = pd.read_pickle(
    here("./data/db/working/kaggle/word_counts/01-word_tokens.pickle")
)
# papers_token = papers_token.sample(100)

stops = stopwords.words("english")
lemmatizer = WordNetLemmatizer()
tqdm.pandas(desc="Remove stopwords and lemmatization")
papers_token["tokens-nostop-lemma"] = papers_token["tokens"].progress_apply(
    lambda x: [
        lemmatizer.lemmatize(word.lower())
        for word in x
        if word.lower() not in stops and len(word) > 1
    ]
) # this step will take ~20mins
assert len(papers_token.tokens.iloc[0]) != len(
    papers_token["tokens-nostop-lemma"].iloc[0]
)

# save out working data
pl.Path(here("./data/db/working/kaggle/word_counts", warn=False)).mkdir(
    parents=True, exist_ok=True
)
papers_token.to_pickle(
    here(
        "./data/db/working/kaggle/word_counts/02-normalized-word_tokens.pickle",
        warn=False,
    )
)
