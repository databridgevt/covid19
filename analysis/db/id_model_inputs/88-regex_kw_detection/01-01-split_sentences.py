from datetime import datetime
import pathlib as pl
import sys

import nltk.data
import pandas as pd
from pyprojroot import here
from tqdm import tqdm

script = sys.argv[0]
flag_test = True if '--test' in sys.argv else False

start_time = datetime.now()

if flag_test:
    print("running test")
    paper_df = pd.read_csv(here("./data/db/final/kaggle/paper_text/document_parses_pmc_json.tsv"),
                           sep = "\t",
                           nrows=10)
else :
    paper_df = pd.read_csv(here("./data/db/final/kaggle/paper_text/document_parses_pmc_json.tsv"),
                           sep = "\t")


# break up into sentences
sent_detector = nltk.data.load('tokenizers/punkt/english.pickle') # nltk.download('punkt')

tqdm.pandas(desc="Split sentences")
paper_df["text_sent_lower"] = paper_df["text"].progress_apply(lambda x: sent_detector.tokenize(x.lower().strip())) # about 15 minutes

pl.Path(here("./data/db/working/kaggle/id_model_inputs", warn=False)).mkdir(parents=True, exist_ok=True)
paper_df.to_pickle(here("./data/db/working/kaggle/id_model_inputs/01-01-split_sentences.pickle", warn=False)) # about 5 minutes

end_time = datetime.now()
print('Duration: {}'.format(end_time - start_time))
