library(readr)
library(ggplot2)
library(here)
library(dplyr)
library(tidyr)


df = readr::read_tsv(here('./data/db/final/kaggle/id_model_inputs/03-covid_kw_sentences_-hand_parsed.tsv'))

df

plot_dat <- df %>%
  dplyr::filter(match_type == "sent-incubation_period_day") %>%
  dplyr::select(match_type, point, range_lower, range_upper) %>%
  tidyr::pivot_longer(-match_type)

ggplot(plot_dat, aes(value, fill = name)) +
geom_histogram() +
theme_minimal() +
ggtitle("COVID19 incubation point estimate, lower bound, and upper bound values")


ggplot(plot_dat, aes(x = name, y =value, color = name)) +
  geom_violin() +
  theme_minimal() +
  ggtitle("COVID19 incubation point estimate, lower bound, and upper bound values") +
  xlab("") +
  ylab("")
