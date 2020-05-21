import pathlib as pl

import pandas as pd

from pyprojroot import here


kw_df = pd.read_pickle(here("./data/db/working/kaggle/id_model_inputs/01-sentences-keywords.pickle"))
metadata = pd.read_csv(here("./data/db/original/kaggle/metadata.csv"))


## "incubation period" sentences that also contain "day" helps remove sentences from bench lab studies
kw_df['sent-incubation_period_day'] = kw_df["text_sent"].apply(lambda x: [sent for sent in x if all(t in sent.lower() for t in ["incubation period", "day"])])

## search for other kw terms as-is
kw_df['sent-infectiousness_period'] = kw_df["text_sent"].apply(lambda x: [sent for sent in x if all(t in sent.lower() for t in ["infectiousness period"])])
kw_df['sent-recovery_rate'] = kw_df["text_sent"].apply(lambda x: [sent for sent in x if all(t in sent.lower() for t in ["recovery rate"])])
kw_df['sent-case_fatality_ratio'] = kw_df["text_sent"].apply(lambda x: [sent for sent in x if all(t in sent.lower() for t in ["case fatality ratio"])])
kw_df['sent-asymptomatic_fraction'] = kw_df["text_sent"].apply(lambda x: [sent for sent in x if all(t in sent.lower() for t in ["asymptomatic fraction"])])
kw_df['sent-hospitalized_fraction'] = kw_df["text_sent"].apply(lambda x: [sent for sent in x if all(t in sent.lower() for t in ["hospitalized fraction"])])

kw_df.drop(["num_authors", "text",], axis="columns", inplace=True)
kw_df.shape

# add metadata information
kw_metadata_df = pd.merge(kw_df, metadata, left_on=["pid"], right_on=["pmcid"])

assert len(kw_metadata_df) == len(kw_df)

kw_metadata_df

# save out working data
pl.Path(here("./data/db/working/kaggle/id_model_inputs/", warn=False)).mkdir(parents=True, exist_ok=True)
kw_metadata_df.to_pickle(here("./data/db/working/kaggle/id_model_inputs/02-kw_w_metadata.pickle", warn=False))
