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

def extract_paper_data(json_pth, folder_mode):
    with open(json_pth) as f:
        data = json.load(f)
    # pdf_json has an abstract section
    # pmc_json does not have an abstract section
    # the rest appear to be the same

    # get the common json sections
    paper_text = extract_body_text(data, section_key="body_text", text_key="text")
    pid = data['paper_id']
    title = data['metadata']['title']
    num_authors = len(data['metadata']['authors'])

    if folder_mode == "pdf_json":
        abstract_text = extract_abstract_text(data, section_key="abstract", text_key="text")
        paper_data = pd.DataFrame(
            data = [
                [pid, num_authors, title, abstract_text, paper_text]
            ],
            columns = ["pid", "num_authors", "title", "abstract", "text"]
        )
        return(paper_data)
    elif folder_mode == "pmc_json":
        paper_data = pd.DataFrame(
            data = [
                [pid, num_authors, title, paper_text]
            ],
            columns = ["pid", "num_authors", "title", "text"]
        )
        return(paper_data)
    else:
        raise ValueError(f"Unknown value passed into 'folder_mode': {folder_mode}")

data_sources = [
    "biorxiv_medrxiv",
    "comm_use_subset",
    "noncomm_use_subset",
]

datpb = tqdm([data_sources[1]])
for dat_source in datpb: # for each data source
    datpb.set_description(f"{dat_source}")

    ds_hr = here(f"./data/db/original/kaggle/{dat_source}/{dat_source}/", warn=False)
    fdrs = list(ds_hr.iterdir())

    # print(f"\n\n{dat_source}")

    gppb = tqdm(fdrs)
    for gp in gppb: # for each group path
        #if gp.name == "pmc_json": continue
        gppb.set_description(f"{dat_source}/{gp.name}")

        #print(f"\n\n{gp}")

        #gp_hr = here(f"./data/db/original/kaggle/{dat_source}/{dat_source}/{gp}", warn=False)
        fs = gp.iterdir()

        try:
            fs = list(fs)
        except FileNotFoundError:
            sys.exit(f"Could not find {gp_hr}, did you forget to update the Kaggle dataset?")

        papers = pd.concat(
            [extract_paper_data(jsn, folder_mode=gp.name) for jsn in tqdm(fs)]
        )

        #papers.info()

        pl.Path(here("./data/db/final/kaggle/paper_text/")).mkdir(parents=True, exist_ok=True)
        papers.to_csv(here(f"./data/db/final/kaggle/paper_text/{dat_source}_{gp.name}.tsv", warn=False),
                    sep="\t", header=True, index=False)
