import plotly.figure_factory as ff
import numpy as np
import plotly.io as pio
from pyprojroot import here
import plotly.express as px
import pandas as pd
from urllib.request import urlopen
import json
import pathlib as pl

with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

# TODO: Change range_color numbers in fig = px.choropleth()
# TODO: Build the map for a specific date
# TODO: Build line/bar graphs to check case numbers per state over a period of time
# TODO: Draw another version of this map, but accounts for population density per county (per capita count)
# TODO: See if rate is changing, counts over time (a 14 day sliding window count)
# Choropleth map with time slider and hover text

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

fips = molten_df['fips_str'].tolist()
# max_val = molten_df['value'].max()


fig = px.choropleth(molten_df,
                    geojson=counties,
                    locations=fips,
                    color='value',
                    animation_frame='date',
                    hover_data=['State', 'value'],
                    color_continuous_scale="Viridis",
                    range_color=(0, 300),
                    scope="usa",
                    title='Confirmed cases',
                    labels={'value': 'confirmed cases'}
                    )
fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
# fig.show()

# save out figure
# save out working data
pl.Path(here("./output/maps", warn=False)).mkdir(parents=True, exist_ok=True)
pio.write_html(fig,
               file=here("./output/maps/choropleth_us_cases.html", warn=False),
               auto_open=True)


# ChoroplethMap using FIPS from merged data
'''
confirmed_df = pd.read_csv('https://github.com/CSSEGISandData/COVID-19/raw/master/csse_covid_19_data/'
                           'csse_covid_19_time_series/time_series_covid19_confirmed_US.csv')

loc_df = pd.read_excel(here('./data/db/original/maps/State_FIPS.xlsx'))
merged_df = pd.merge(loc_df, confirmed_df, right_on='Admin2', left_on='Name')

merged_df['fips_str'] = merged_df['FIPS_x'].apply(lambda x: f'{x:05.0f}')  # left pad with 0 for 5 digits

colorscale = ["#f7fbff", "#ebf3fb", "#deebf7", "#d2e3f3", "#c6dbef", "#b3d2e9", "#9ecae1",
              "#85bcdb", "#6baed6", "#57a0ce", "#4292c6", "#3082be", "#2171b5", "#1361a9",
              "#08519c", "#0b4083", "#08306b"]

molten_df = merged_df.melt(
    id_vars=['FIPS_x', 'Name', 'State', 'UID', 'iso2', 'iso3', 'code3', 'FIPS_y', 'Admin2',
             'Province_State', 'Country_Region', 'Lat', 'Long_', 'Combined_Key', 'fips_str'],
    var_name=['date']
)

molten_df['date_iso'] = pd.to_datetime(molten_df['date'], format="%m/%d/%y")  # change date to ISO8601 standard format

endpts = list(np.linspace(0, 3000, len(colorscale) - 1))
fips = molten_df['fips_str'].tolist()
values = molten_df['date_iso'].tolist()

fig = ff.create_choropleth(
    fips=fips,
    # values=values,
    scope=['usa',
           # 'Alaska',
           # 'Puerto Rico',
           # 'American Samoa',
           # 'Commonwealth of the Northern Mariana Islands', 'Guam',
           # 'United States Virgin Islands'
           ],
    binning_endpoints=endpts,
    colorscale=colorscale,
    show_state_data=True,
    show_hover=True, 
    centroid_marker={'opacity': 0},
    asp=2.9, 
    title='Confirmed cases on April 22',
    legend_title='# confirmed cases',
    text=molten_df['fips']
)

fig.layout.template = None
fig.show()
'''



