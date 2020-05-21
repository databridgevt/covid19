import pathlib as pl

import pandas as pd

from pyprojroot import here


incubation_df = pd.read_pickle(here("./data/db/working/kaggle/incubation/01-sentences-incubation_period_days.pickle"))
metadata = pd.read_csv(here("./data/db/original/kaggle/metadata.csv"))

# sentences that just contain "incubation"
incubation_df['incubation_sent'] = incubation_df["text_sent"].apply(lambda x: [sent for sent in x if 'incubation' in sent.lower()])

# sentences that contain "incubation period"
incubation_df['incubationPeriod_sent'] = incubation_df["text_sent"].apply(lambda x: [sent for sent in x if "incubation period" in sent.lower()])

# "incubation period" sentences that also contain "day"
incubation_df['incubationPeriod-days_sent'] = incubation_df["incubationPeriod_sent"].apply(lambda x: [sent for sent in x if "day" in sent.lower()])

incubation_df.drop(["num_authors", "text",], axis="columns", inplace=True)
incubation_df.shape

# add metadata information
incubation_metadata_df = pd.merge(incubation_df, metadata, left_on=["pid"], right_on=["pmcid"])

assert len(incubation_metadata_df) == len(incubation_df)

incubation_metadata_df

# save out working data
pl.Path(here("./data/db/working/kaggle/incubation/", warn=False)).mkdir(parents=True, exist_ok=True)
incubation_metadata_df.to_pickle(here("./data/db/working/kaggle/incubation/02-incubation_w_metadata.pickle", warn=False))
