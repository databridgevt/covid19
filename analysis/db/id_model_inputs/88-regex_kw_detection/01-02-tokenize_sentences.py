from datetime import datetime

from nltk.tokenize import word_tokenize
import pandas as pd
from pyprojroot import here
from tqdm import tqdm

start_time = datetime.now()

paper_df = pd.read_pickle(here("./data/db/working/kaggle/id_model_inputs/01-01-split_sentences.pickle"))

tqdm.pandas(desc="Tokenizing sentences")
paper_df['sent_set'] = paper_df['text_sent_lower'].progress_apply(lambda x: [set(word_tokenize(sent)) for sent in x])

paper_df.to_pickle(here("./data/db/working/kaggle/id_model_inputs/01-02-tokenize_sentences.pickle", warn=False))

end_time = datetime.now()
print('Duration: {}'.format(end_time - start_time))
