from collections import Counter
import itertools
import pathlib as pl

import json
from numpy import vectorize
import matplotlib.pyplot as plt
from pyprojroot import here
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from tqdm import tqdm


@vectorize
def compute_tf(counter, total_words):
    return {word: count / total_words for word, count in counter.items()}


normalized_tokens = pd.read_pickle(
    here("./data/db/working/kaggle/word_counts/02-normalized-word_tokens.pickle")
)

# bag of words frequencies
bag_of_words = list(
    itertools.chain.from_iterable(normalized_tokens["tokens-nostop-lemma"])
)
assert len(bag_of_words) == normalized_tokens["tokens-nostop-lemma"].apply(len).sum()
counts = Counter(bag_of_words)
df_tf = pd.DataFrame(counts.most_common(), columns=["word", "count"])

pl.Path(here("./data/db/final/kaggle/word_counts", warn=False)).mkdir(
    parents=True, exist_ok=True
)
df_tf.to_csv(
    here("./data/db/final/kaggle/word_counts/03-bag_of_word_counts.csv"), index=False
)

# base counts for tf-idf
# tqdm.pandas(desc="tf counter")
# normalized_tokens["tokens-nostop-lemma-counter"] = normalized_tokens["tokens-nostop-lemma"].progress_apply(Counter)
# normalized_tokens["wordcount_normalized"] = normalized_tokens["tokens-nostop-lemma"].apply(len)

# tf
# Term Frequency (tf): gives us the frequency of the word in each document in the corpus.
# It is the ratio of number of times the word appears in a document compared to the total number of words in that document.
# It increases as the number of occurrences of that word within the document increases.
# Each document has its own tf.
# normalized_tokens["tf"] = compute_tf(normalized_tokens["tokens-nostop-lemma-counter"],
#                                     normalized_tokens["wordcount_normalized"])

# idf


# tf-idf
corpus = normalized_tokens["tokens-nostop-lemma"].apply(lambda x: ' '.join(x))
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(corpus)

#doc_mat_df = pd.DataFrame(X.toarray(), columns=vectorizer.get_feature_names())
#doc_mat_df.to_csv(here("./data/db/final/kaggle/word_counts/03-tfidf.csv"), index=False)

# top 100
top100_tfidf = (
    doc_mat_df.apply(sum).sort_values(ascending=False).head(100).index.tolist()
)
top100_tf = df_tf.word.iloc[:100].tolist()

top100_tf = set(top100_tf)
top100_tfidf = set(top100_tfidf)

# convert set into list so we can write to json
both = list(top100_tfidf.intersection(top100_tf))
unique_tfidf = list(top100_tfidf.difference(top100_tf))
unique_tf = list(top100_tf.difference(top100_tfidf))

pl.Path(here("./data/db/final/kaggle/word_counts", warn=False)).mkdir(
    parents=True, exist_ok=True
)
with open(
    here("./data/db/final/kaggle/word_counts/03-words-both.json", warn=False), "w"
) as filehandle:
    json.dump(both, filehandle)
with open(
    here("./data/db/final/kaggle/word_counts/03-words-tfidf.json", warn=False), "w"
) as filehandle:
    json.dump(unique_tfidf, filehandle)
with open(
    here("./data/db/final/kaggle/word_counts/03-words-tf.json", warn=False), "w"
) as filehandle:
    json.dump(unique_tf, filehandle)
