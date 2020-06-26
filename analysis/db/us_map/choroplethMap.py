import numpy as np
import plotly.io as pio
from pyprojroot import here
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd
from urllib.request import urlopen
import pathlib as pl
import json
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

# TODO: Build line/bar graphs to check case numbers per state over a period of time
# TODO: See if rate is changing, counts over time (a 14 day sliding window count)
# TODO: Try to merge PopulationEstimates.xls to confirmed_df and remove State_FIPS.xlsx

confirmed_df = pd.read_csv('https://github.com/CSSEGISandData/COVID-19/raw/master/csse_covid_19_data/'
                           'csse_covid_19_time_series/time_series_covid19_confirmed_US.csv')
loc_df = pd.read_excel(here('./data/db/original/maps/State_FIPS.xlsx'))
pop_df = pd.read_excel(here('./data/db/original/maps/PopulationEstimates.xls'))  # population dataset for 2019

pop_df['fips_str'] = pop_df['FIPStxt'].apply(lambda x: f'{x:05.0f}')
pop_df = pop_df[['fips_str', 'Area_Name', 'POP_ESTIMATE_2019']]

merged_df = pd.merge(loc_df, confirmed_df, right_on='Admin2', left_on='Name')

merged_df['fips_str'] = merged_df['FIPS_x'].apply(lambda x: f'{x:05.0f}')  # left pad with 0 for 5 digits
molten_df = merged_df.melt(
    id_vars=['FIPS_x', 'Name', 'State', 'UID', 'iso2', 'iso3', 'code3', 'FIPS_y', 'Admin2',
             'Province_State', 'Country_Region', 'Lat', 'Long_', 'Combined_Key', 'fips_str'],
    var_name=['date']
)

molten_df['date_iso'] = pd.to_datetime(molten_df['date'], format="%m/%d/%y")  # change date to ISO8601 standard format
# fips = molten_df['fips_str'].tolist()

molten_pop_df = pd.merge(molten_df, pop_df, on='fips_str')  # add population per county
grouped_by = molten_pop_df.groupby(['fips_str', 'date_iso', 'Admin2', 'POP_ESTIMATE_2019'])['value'].sum().reset_index()
grouped_by['value'] = grouped_by['value']/grouped_by['POP_ESTIMATE_2019']   # get per capita value

plot_data = grouped_by[grouped_by.date_iso == '2020-04-01']

# confirmed cases per capita
fig = px.choropleth(plot_data,
                    geojson=counties,
                    locations=plot_data.fips_str,
                    color='value',
                    # animation_frame='date',
                    hover_data=['Admin2', 'value', 'POP_ESTIMATE_2019'],
                    color_continuous_scale='viridis_r',
                    range_color=(0, plot_data['value'].max()),
                    scope="usa",
                    title='Confirmed cases per capita',
                    labels={'value': 'confirmed cases'}
                    )
fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
pl.Path(here("./output/maps", warn=False)).mkdir(parents=True, exist_ok=True)
pio.write_html(fig,
               file=str(here("./output/maps/choropleth_us_cases.html", warn=False)),
               auto_open=False)

'''
# overall confirmed cases data
plot_data = molten_df[molten_df.date_iso == '2020-04-01']
fig = px.choropleth(plot_data,  
                    geojson=counties,
                    locations=plot_data.fips_str,
                    color='value',
                    # animation_frame='date',
                    hover_data=['State', 'value'],
                    color_continuous_scale='viridis_r',
                    range_color=(0, 500),
                    scope="usa",
                    title='Confirmed cases',
                    labels={'value': 'confirmed cases'}
                    )
fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

# save out figure
# save out working data
pl.Path(here("./output/maps", warn=False)).mkdir(parents=True, exist_ok=True)
pio.write_html(fig,
               file=str(here("./output/maps/choropleth_us_cases.html", warn=False)),
               auto_open=False)
'''