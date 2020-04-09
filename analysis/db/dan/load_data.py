import pathlib as pl
import json
import sys

import pandas as pd
from tqdm import tqdm

from pyprojroot import here

def extract_paper_component(paper_json, section_key, text_key="text", line_delim="\n"):
    section_text = map(lambda x: x[text_key], paper_json[section_key])
    text = line_delim.join(section_text)
    return(text)

def extract_body_text(paper_json, **kwargs):
    paper_text = extract_paper_component(paper_json, **kwargs)
    return(paper_text)

def extract_abstract_text(paper_json, **kwargs):
    abstract_text = extract_paper_component(paper_json, **kwargs)
    return(abstract_text)

def extract_paper_data(json_pth):
    with open(json_pth) as f:
        data = json.load(f)

    paper_text = extract_body_text(data, section_key="body_text", text_key="text")
    abstract_text = extract_abstract_text(data, section_key="abstract", text_key="text")
    pid = data['paper_id']
    title = data['metadata']['title']
    num_authors = len(data['metadata']['authors'])

    paper_data = pd.DataFrame(
        data = [
            [pid, num_authors, title, abstract_text, paper_text]
        ],
        columns = ["pid", "num_authors", "title", "abstract", "text"]
    )
    return(paper_data)

hr = here("./data/db/original/kaggle/comm_use_subset/comm_use_subset/pdf_json/")
fs = hr.iterdir()

try:
    fs = list(fs)
except FileNotFoundError:
    sys.exit(f"Could not find {hr}, did you forget to update the Kaggle dataset?")

papers = pd.concat(
    [extract_paper_data(jsn) for jsn in tqdm(fs)]
)

papers.info()

pl.Path(here("./data/db/final/kaggle/paper_text/")).mkdir(parents=True, exist_ok=True)
papers.to_csv(here("./data/db/final/kaggle/paper_text/comm_use_subset.tsv"), sep="\t", header=True, index=False)
