import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from pyprojroot import here
import plotly.io as pio
import seaborn as sns
from urllib.request import urlopen
import pathlib as pl


confirmed_df = pd.read_csv('https://github.com/CSSEGISandData/COVID-19/raw/master/csse_covid_19_data/'
                           'csse_covid_19_time_series/time_series_covid19_confirmed_US.csv')
loc_df = pd.read_excel(here('./data/db/original/maps/State_FIPS.xlsx'))

merged_df = pd.merge(loc_df, confirmed_df, right_on='Admin2', left_on='Name')

merged_df['fips_str'] = merged_df['FIPS_x'].apply(lambda x: f'{x:05.0f}')  # left pad with 0 for 5 digits
molten_df = merged_df.melt(
    id_vars=['FIPS_x', 'Name', 'State', 'UID', 'iso2', 'iso3', 'code3', 'FIPS_y', 'Admin2',
             'Province_State', 'Country_Region', 'Lat', 'Long_', 'Combined_Key', 'fips_str'],
    var_name=['date']
)

molten_df['date_iso'] = pd.to_datetime(molten_df['date'], format="%m/%d/%y")  # change date to ISO8601 standard format
# state = molten_df.loc[molten_df.Province_State == 'Virginia', molten_df.Province_State == 'New York']
# molten_df['date_iso'] = molten_df.loc[molten_df.date_iso == '2020-04-01', molten_df.date_iso == '2020-04-05']
subset = molten_df.loc[molten_df.Province_State == 'Virginia', ['Province_State', 'Admin2', 'value', 'date_iso']]

grouped_counts = subset.groupby(['date_iso', 'Province_State', 'Admin2'])['value'].sum().reset_index()

ax = sns.lineplot(x="date_iso", y="value", hue='Province_State', data=grouped_counts)  # show cases per state monthly
# ax = sns.stripplot(x="date_iso", y="value", hue='Province_State', data=grouped_counts)
# plt.tight_layout()
plt.show()
