import pandas as pd
import pathlib as pl
from pyprojroot import here
from nltk.tokenize import sent_tokenize, word_tokenize
from tqdm import tqdm


tqdm.pandas()

pmc_papers = pd.read_csv(
    here("./data/db/final/kaggle/paper_text/document_parses_pmc_json.tsv"), sep="\t"
)
# pdf_papers = pd.read_csv(here("./data/db/final/kaggle/paper_text/document_parses_pdf_json.tsv"), sep = "\t")

pmc_papers["tokens"] = pmc_papers.text.progress_apply(
    word_tokenize
)  # this step takes ~20min to run

# save out working data
pl.Path(here("./data/db/working/kaggle/word_counts", warn=False)).mkdir(
    parents=True, exist_ok=True
)

pmc_papers.to_pickle(
    here("./data/db/working/kaggle/word_counts/01-word_tokens.pickle", warn=False)
)
