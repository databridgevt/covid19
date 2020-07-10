import dash
import dash_core_components as dcc
import dash_html_components as html
from pyprojroot import here
import plotly.express as px
import pandas as pd
from urllib.request import urlopen
import json

with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

external_stylesheets = [here('./analysis/db/us_map/assets/style.css')]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


confirmed_df = pd.read_csv('https://github.com/CSSEGISandData/COVID-19/raw/master/csse_covid_19_data/'
                           'csse_covid_19_time_series/time_series_covid19_confirmed_US.csv')
# Resource for State_FIPS: https://www.nrcs.usda.gov/wps/portal/nrcs/detail/national/home/?cid=nrcs143_013697
loc_df = pd.read_excel(here('./data/db/original/maps/State_FIPS.xlsx'))
# Resource for PopulationEstimates: https://www.ers.usda.gov/data-products/county-level-data-sets/download-data/
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

molten_pop_df = pd.merge(molten_df, pop_df, on='fips_str')  # add population per county
grouped_by = molten_pop_df.groupby(['fips_str', 'date_iso', 'State', 'Admin2', 'POP_ESTIMATE_2019'])['value'].sum().reset_index()
grouped_by['total_per_cap'] = grouped_by['value'] / grouped_by['POP_ESTIMATE_2019']  # get per capita value

plot_data = grouped_by[grouped_by.date_iso == '2020-04-01']  # confirmed cases on a specific day
value = 'value'   # 'value' = raw count, 'total_per_cap' = per capita

# confirmed cases per capita/raw count
fig = px.choropleth(plot_data,
                    geojson=counties,
                    locations=plot_data.fips_str,
                    color=value,
                    hover_data=['State', 'Admin2', value, 'POP_ESTIMATE_2019'],
                    color_continuous_scale='viridis_r',
                    range_color=(0, plot_data[value].max()),
                    scope="usa",
                    # title='Confirmed cases',
                    labels={'value': 'confirmed cases'}
                    )

fig.update_layout(
    template="plotly_dark"
)

app.layout = html.Div(children=[
                      html.Header(className='header',
                                  children=[
                                      html.H2('Virginia Tech')
                                  ]),

                      html.Div(className='col-12',  # Define the row element
                               children=[
                                   html.Div(className='col-3',  # Define the row element
                                            children=[
                                                html.Div(className='col-7',
                                                         children=[
                                                             html.H2('Here goes graph')
                                                         ]),  # Define the left element
                                                html.Div(className='col-8',
                                                         children=[
                                                             html.H2('Here goes another graph')
                                                         ])
                                            ]),
                                   html.Div(className='col-9',  # Define the row element
                                            children=[
                                                    dcc.Graph(
                                                        figure=fig
                                                    )
                                            ]
                                            )  # Define the right element
                                  ]),
                      html.Footer(
                                  children=[
                                      html.P('''All rights reserved''')
                                  ])
                      ])


if __name__ == '__main__':
    app.run_server(
        debug=True,
        port=8070,
        host='127.0.0.1'
    )
