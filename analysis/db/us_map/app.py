import dash
import dash_core_components as dcc
import dash_html_components as html
from pyprojroot import here
import plotly.express as px
import pandas as pd
from urllib.request import urlopen
from dash.dependencies import Input, Output
import json

with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

# TODO: color "Great Salt Lake" in Utah state

external_stylesheets = [here('./analysis/db/us_map/assets/style.css')]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)

confirmed_df = pd.read_csv('https://github.com/CSSEGISandData/COVID-19/raw/master/csse_covid_19_data/'
                           'csse_covid_19_time_series/time_series_covid19_confirmed_US.csv')
# Resource for PopulationEstimates: https://www.ers.usda.gov/data-products/county-level-data-sets/download-data/
pop_df = pd.read_excel(here('./data/db/original/maps/PopulationEstimates.xls'))  # population dataset for 2019

pop_df['fips_str'] = pop_df['FIPStxt'].apply(lambda x: f'{x:05.0f}')
confirmed_df['fips_str'] = confirmed_df['FIPS'].apply(lambda x: f'{x:05.0f}')

pop_short_df = pop_df[['fips_str', 'Area_Name', 'POP_ESTIMATE_2019']]  # shorten columns in population dataset

merged_df = pd.merge(confirmed_df, pop_short_df, right_on='fips_str', left_on='fips_str')

molten_df = merged_df.melt(
    id_vars=['UID', 'iso2', 'iso3', 'code3', 'FIPS', 'Admin2',
             'Province_State', 'Country_Region', 'Lat', 'Long_', 'Combined_Key',
             'fips_str', 'Area_Name', 'POP_ESTIMATE_2019'],
    var_name=['date']
)
molten_df['date_iso'] = pd.to_datetime(molten_df['date'], format="%m/%d/%y")  # format date as 'yyyy-mm-dd'

molten_df['fips_str'] = molten_df['fips_str'].replace(['46102'], '46113')  # replace new fips code with old one

grouped_by_df = molten_df.groupby(['fips_str', 'date_iso', 'Admin2', 'POP_ESTIMATE_2019'])[
    'value'].sum().reset_index()

grouped_by_df['total_per_cap'] = grouped_by_df['value'] / grouped_by_df['POP_ESTIMATE_2019']  # get per capita value

app.layout = html.Div(children=[
    html.Header(className='header',
                children=[
                    html.H2('Virginia Tech')
                ]),

    html.Div(className='col-12',  # Define the body element
             children=[
                 html.Div(className='col-3',  # Define the left 2 elements
                          children=[
                              html.Div(className='col-7',  # Define the upper left element
                                       children=[
                                           html.H2('Here goes graph')
                                       ]),
                              html.Div(className='col-8',  # Define the lower left element
                                       children=[
                                           html.H2('Here goes another graph')
                                       ])
                          ]),
                 html.Div(className='col-9',  # Define the right element (map)
                          children=[
                              dcc.Tabs(id="tabs-styled-with-props",
                                       value='tab-1',
                                       parent_className='custom-tabs',
                                       className='custom-tabs-container',
                                       children=[
                                           dcc.Tab(label='Raw count',
                                                   value='tab-1',
                                                   className='custom-tab',
                                                   selected_className='custom-tab--selected'
                                                   ),
                                           dcc.Tab(label='Per capita',
                                                   value='tab-2',
                                                   className='custom-tab',
                                                   selected_className='custom-tab--selected'
                                                   ),
                                           dcc.Tab(label='Active',
                                                   value='tab-3',
                                                   className='custom-tab',
                                                   selected_className='custom-tab--selected'
                                                   ),
                                           dcc.Tab(label='Death count',
                                                   value='tab-4',
                                                   className='custom-tab',
                                                   selected_className='custom-tab--selected'
                                                   ),
                                       ]),
                              html.Div(id='tabs-content-props'),
                              dcc.DatePickerSingle(
                                  id='my-date-picker-single',
                                  min_date_allowed=molten_df.date_iso.iat[0],
                                  max_date_allowed=molten_df.date_iso.iat[-1],
                                  initial_visible_month=molten_df.date_iso.iat[-1],
                                  date=str(molten_df.date_iso.iat[-1])
                              )
                          ]
                          )
             ]),
    html.Footer(
        children=[
            html.P("""All rights reserved""")
        ])
])


@app.callback(Output('tabs-content-props', 'children'),
              [Input('tabs-styled-with-props', 'value')])
def render_content(tab):
    global value
    if tab == 'tab-1':
        value = 'value'
        return html.Div([
            html.Div(id='output-container-date-picker-single'),
            dcc.Graph(
                id='map'
            )
        ])
    elif tab == 'tab-2':
        value = 'total_per_cap'
        return html.Div([
            html.Div(id='output-container-date-picker-single'),
            dcc.Graph(
                id='map'
            )
        ])
    elif tab == 'tab-3':
        value = 'total_per_cap'
        return html.Div([
            html.Div(id='output-container-date-picker-single'),
            dcc.Graph(
                id='map'
            )
        ])
    elif tab == 'tab-4':
        value = 'total_per_cap'
        return html.Div([
            html.Div(id='output-container-date-picker-single'),
            dcc.Graph(
                id='map'
            )
        ])


@app.callback(
    Output('map', 'figure'),
    [Input('my-date-picker-single', 'date')])
def update_figure(date):
    plot_data = grouped_by_df[grouped_by_df.date_iso == date]
    fig = px.choropleth(plot_data,
                        geojson=counties,
                        locations=plot_data.fips_str,
                        color=value,
                        hover_data=['Admin2', value, 'POP_ESTIMATE_2019'],
                        color_continuous_scale='viridis_r',
                        range_color=(0, plot_data[value].max()),  # plot_data[value].max()
                        scope="usa",
                        # title='Confirmed cases',
                        labels={'value': 'confirmed cases'}
                        )
    fig.update_layout(
        template="gridon"
    )
    return fig


if __name__ == '__main__':
    app.run_server(
        debug=True,
        port=8070,
        host='127.0.0.1'
    )
