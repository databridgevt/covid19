import geopandas as gpd
from shapely.geometry import Point, Polygon
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import geopandas as geop
import plotly.graph_objects as go
import plotly.figure_factory as ff
import numpy as np

# read file and build the map
loc_df = pd.read_csv('https://github.com/CSSEGISandData/COVID-19/raw/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv')
print(loc_df.info())
fig = px.scatter_mapbox(loc_df, lat="Lat", lon="Long_", color="Province_State")
fig.update_layout(mapbox_style="open-street-map")
fig.show()
# assert len(df_merged) == len(df1)
# Dataset on case numbers: https://opendata.ecdc.europa.eu/covid19/casedistribution/csv
# Dataset on case numbers2: https://data.humdata.org/hxlproxy/api/data-preview.csv?url=https%3A%2F%2Fraw.githubusercontent.com%2FCSSEGISandData%2FCOVID-19%2Fmaster%2Fcsse_covid_19_data%2Fcsse_covid_19_time_series%2Ftime_series_covid19_confirmed_global.csv&filename=time_series_covid19_confirmed_global.csv
# Dataset on time series confirmed cases in the US: https://github.com/CSSEGISandData/COVID-19/raw/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv

# merge 2 tables
# cases = pd.read_csv("https://github.com/CSSEGISandData/COVID-19/raw/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv")
# df = px.data.gapminder()
# fig = px.scatter_geo(df, locations="iso_alpha", color="continent", hover_name="country", size="year", projection="natural earth")
# fig.update_layout(mapbox_style="open-street-map")
# fig.show()
# print(cases.head())
# print(cases['Province_State'].unique())
# print(cases['Province_State'].value_counts(dropna=False))

# cities_names = pd.read_csv('us-zip-code-latitude-and-longitude.csv')
# print(cities_names.head())
# print(cities_names['State'].unique())

# merged_data = pd.merge(cases, cities_names)
# print(merged_data.head())

# country_names = cases[['Country/Region', 'State']]
# city_names = cases[['City', 'State']]
# city_names = city_names.merge(country_names, on='State')
# print(cases.head())
# world = geop.read_file(geop.datasets.get_path('naturalearth_lowres'))
# cities = geop.read_file(geop.datasets.get_path('naturalearth_cities'))
# country_shapes = world[['geometry', 'iso_a3']]
# country_names = world[['name', 'iso_a3']]
# country_shapes = country_shapes.merge(country_names, on='iso_a3')


# fig = px.scatter_mapbox(cases, lat="Lat", lon="Long", color="Country/Region")
# fig.update_layout(mapbox_style="open-street-map")

# cases.plot(style='m.')
# plt.show()  # bar graph of case numbers

# colored plot
# px.set_mapbox_access_token(open(".mapbox_token").read())
# df = px.data.carshare()
# fig = px.scatter_mapbox(df, lat="Lat", lon="Long", color="Country/Region", size="6/6/20",
#                  color_continuous_scale=px.colors.cyclical.IceFire, size_max=15, zoom=10)
# fig.show()

'''
# From ChoroplethMap

# merged_df = df.merge(loc_df, left_on='Admin2', right_on='Name')
# print(merged_df.head())
# print(df['Admin2'].value_counts(dropna=False))
# print(loc_df['Name'].value_counts(dropna=False))

# df['FIPS'] = df['FIPS'].apply(lambda x: str(x).zfill(5))
# merged_df['FIPS'] = merged_df['FIPS'].apply(lambda x: str(x).zfill(5))
# merged_df['State FIPS Code'] = merged_df['State FIPS Code'].apply(lambda x: str(x).zfill(2))
# merged_df['FIPS'] = merged_df['State FIPS Code'] + merged_df['County FIPS Code']
'''