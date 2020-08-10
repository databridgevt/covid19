import dash
import dash_core_components as dcc
import dash_html_components as html
from pyprojroot import here
import plotly.express as px
import pandas as pd
import numpy as np
from urllib.request import urlopen
from dash.dependencies import Input, Output
import pathlib as pl
import plotly.graph_objects as go
import plotly.io as pio
import json

with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

# TODO: color "Great Salt Lake" in Utah state

external_stylesheets = [here('./analysis/db/us_map/assets/style.css')]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)

confirmed_df = pd.read_csv('https://github.com/CSSEGISandData/COVID-19/raw/master/csse_covid_19_data/'
                           'csse_covid_19_time_series/time_series_covid19_confirmed_US.csv')
death_df = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/'
                       'csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_US.csv')
# Resource for PopulationEstimates: https://www.ers.usda.gov/data-products/county-level-data-sets/download-data/
pop_df = pd.read_excel(here('./data/db/original/maps/PopulationEstimates.xls'))  # population dataset for 2019

# format FIPS codes
pop_df['fips_str'] = pop_df['FIPStxt'].apply(lambda x: f'{x:05.0f}')
confirmed_df['fips_str'] = confirmed_df['FIPS'].apply(lambda x: f'{x:05.0f}')
death_df['fips_str'] = confirmed_df['FIPS'].apply(lambda x: f'{x:05.0f}')

pop_short_df = pop_df[['fips_str', 'Area_Name', 'POP_ESTIMATE_2019']]  # shorten columns in population dataset

# merge population dataset with confirmed and death cases on fips codes
merged_confirmed_df = pd.merge(confirmed_df, pop_short_df, right_on='fips_str', left_on='fips_str')
merged_death_df = pd.merge(death_df, pop_short_df, right_on='fips_str', left_on='fips_str')

# melt tables to have separate "date" and "values" columns
molten_df = merged_confirmed_df.melt(
    id_vars=['UID', 'iso2', 'iso3', 'code3', 'FIPS', 'Admin2',
             'Province_State', 'Country_Region', 'Lat', 'Long_', 'Combined_Key',
             'fips_str', 'Area_Name', 'POP_ESTIMATE_2019'],
    var_name=['date']
)
molten_death_df = merged_death_df.melt(
    id_vars=['UID', 'iso2', 'iso3', 'code3', 'FIPS', 'Admin2',
             'Province_State', 'Country_Region', 'Lat', 'Long_', 'Combined_Key',
             'fips_str', 'Population', 'Area_Name', 'POP_ESTIMATE_2019'],   # 'Area_Name', 'POP_ESTIMATE_2019',
    var_name=['date']
)

# change "value" column names
molten_df = molten_df.rename(columns={'value': 'confirmed_cases'})
molten_death_df = molten_death_df.rename(columns={'value': 'deaths'})

# format the date as 'yyyy-mm-dd'
molten_df['date_iso'] = pd.to_datetime(molten_df['date'], format="%m/%d/%y")  # format date as 'yyyy-mm-dd'
molten_death_df['date_iso'] = pd.to_datetime(molten_df['date'], format="%m/%d/%y")

# replace fips code of Oglala County to avoid missing counties on the map
molten_df['fips_str'] = molten_df['fips_str'].replace(['46102'], '46113')  # replace new fips code with old one
molten_death_df['fips_str'] = molten_death_df['fips_str'].replace(['46102'], '46113')

grouped_by_df = molten_df.groupby(['fips_str', 'date_iso', 'Admin2', 'Province_State', 'POP_ESTIMATE_2019'])[
    'confirmed_cases'].sum().reset_index()

grouped_by_death_df = molten_death_df.groupby(['fips_str', 'date_iso', 'Admin2','Province_State', 'POP_ESTIMATE_2019'])[
    'deaths'].sum().reset_index()

merged_grouped = pd.merge(grouped_by_df, grouped_by_death_df,
                          on=['fips_str', 'date_iso', 'Admin2', 'Province_State', 'POP_ESTIMATE_2019'])
merged_grouped["name"] = merged_grouped["Admin2"] + " County, " + merged_grouped["Province_State"]


# get per 100000 values
merged_grouped['confirmed_per_100000'] = merged_grouped['confirmed_cases'] / \
                                         merged_grouped['POP_ESTIMATE_2019'] * 100_000
merged_grouped['deaths_per_100000'] = merged_grouped['deaths'] / \
                                      merged_grouped['POP_ESTIMATE_2019'] * 100_000

merged_grouped['POP_ESTIMATE_2019_f'] = merged_grouped.apply(lambda x: "{:,}".format(x['POP_ESTIMATE_2019']), axis=1)


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
                                           dcc.Tab(label='Confirmed',
                                                   value='tab-1',
                                                   className='custom-tab',
                                                   selected_className='custom-tab--selected'
                                                   ),
                                           dcc.Tab(label='Confirmed per 100,000',
                                                   value='tab-2',
                                                   className='custom-tab',
                                                   selected_className='custom-tab--selected'
                                                   ),
                                           dcc.Tab(label='Active',
                                                   value='tab-3',
                                                   className='custom-tab',
                                                   selected_className='custom-tab--selected'
                                                   ),
                                           dcc.Tab(label='Deaths per 100,000',
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
    global title
    # global plot_data
    if tab == 'tab-1':
        value = 'confirmed_cases'
        title = '<b>County-Level View of COVID-19 Confirmed Cases</b><br>' \
                '<span style="font-size: 12px;">' \
                '<b>Confirmed</b> cases include presumptive cumulative <b>positive cases</b><br> </span>'\
                '<span style="font-size: 10px;">' \
                'Data Source: <a href="https://github.com/CSSEGISandData/COVID-19/blob/master/' \
                'csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv">' \
                'Coronavirus COVID-19 Cases by the Center for Systems Science and Engineering ' \
                'at Johns Hopkins University</span></a>'
        # plot_data = grouped_by_df
        return html.Div([
            html.Div(id='output-container-date-picker-single',),
            dcc.Graph(
                id='map'
            )
        ])
    elif tab == 'tab-2':
        value = 'confirmed_per_100000'
        title = '<b>County-Level View of COVID-19 Confirmed Cases Per 100,000</b><br>' \
                '<span style="font-size: 12px;">' \
                '<b>Confirmed</b> cases include presumptive cumulative <b>positive cases</b> ' \
                'per 100,000 population<br> </span>'\
                '<span style="font-size: 10px;">' \
                'Data Source: <a href="https://github.com/CSSEGISandData/COVID-19/blob/master/' \
                'csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv">' \
                'Coronavirus COVID-19 Cases by the Center for Systems Science and Engineering ' \
                'at Johns Hopkins University</span></a>'
        # plot_data = grouped_by_df
        return html.Div([
            html.Div(id='output-container-date-picker-single'),
            dcc.Graph(
                id='map'
            )
        ])
    elif tab == 'tab-3':
        value = 'confirmed_per_100000'
        return html.Div([
            html.Div(id='output-container-date-picker-single'),
            dcc.Graph(
                id='map'
            )
        ])
    elif tab == 'tab-4':
        value = 'deaths_per_100000'  # 'deaths' for raw count
        title = '<b>County-Level View of COVID-19 Death Cases Per 100,000</b><br>' \
                '<span style="font-size: 12px;">' \
                '<b>Death</b> cases include presumptive cumulative <b>death cases</b> ' \
                'per 100,000 population<br> </span>'\
                '<span style="font-size: 10px;">' \
                'Data Source: <a href="https://github.com/CSSEGISandData/COVID-19/blob/master/' \
                'csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_US.csv">' \
                'Coronavirus COVID-19 Cases by the Center for Systems Science and Engineering ' \
                'at Johns Hopkins University</span></a>'
        # plot_data = grouped_by_death_df
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
    # plot_d = plot_data[plot_data.date_iso == date]
    plot_data = merged_grouped[merged_grouped.date_iso == date]
    fig = px.choropleth(plot_data,
                        geojson=counties,
                        locations=plot_data.fips_str,
                        color=value,
                        hover_name='name',
                        hover_data=[value, 'POP_ESTIMATE_2019_f'],
                        color_continuous_scale='viridis_r',
                        range_color=(0, np.quantile(plot_data[value], .75)),  # plot_data[value].max()
                        scope="usa",
                        # title=title,
                        labels={'fips_str': 'Fips code',
                                'POP_ESTIMATE_2019_f': 'Population',
                                'confirmed_cases': 'Confirmed cases',
                                'confirmed_per_100000': 'Confirmed per 100,000',
                                'deaths_per_100000': 'Deaths per 100,000'}
                        )
    fig.update_layout(
        margin={"r": 0, "l": 0, "b": 0},
        title=f'{title}',
        title_font_family="Times New Roman",
        template="gridon",
        coloraxis_colorbar=dict(title='',
                                yanchor="top",
                                y=1,
                                ticks="outside",
                                ticksuffix=" cases",
                                separatethousands=True)
    )
    return fig


if __name__ == '__main__':
    app.run_server(
        debug=True,
        port=8070,
        host='127.0.0.1'
    )


'''

# Test maps separately
plot_data = merged_grouped[merged_grouped.date_iso == '2020-07-28']
title = '<b>County-Level View of COVID-19 Death Cases Per 100,000</b><br>' \
                '<span style="font-size: 12px;">' \
                '<b>Death</b> cases include presumptive cumulative <b>death cases</b> ' \
                'per 100,000 population<br> </span>'\
                '<span style="font-size: 10px;">' \
                'Data Source: <a href="https://github.com/CSSEGISandData/COVID-19/blob/master/' \
                'csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_US.csv">' \
                'Coronavirus COVID-19 Cases by the Center for Systems Science and Engineering ' \
                'at Johns Hopkins University</span></a>'
fig = px.choropleth(plot_data,
                    geojson=counties,
                    locations=plot_data.fips_str,
                    color='deaths_per_100000',
                    hover_name='name',
                    hover_data=['POP_ESTIMATE_2019_f'],
                    color_continuous_scale='viridis_r',
                    range_color=(0, np.quantile(plot_data['deaths_per_100000'], .75)),  # plot_data[value].max()
                    scope="usa",
                    title=title,
                    labels={'fips_str': 'Fips code',
                            'POP_ESTIMATE_2019_f': 'Population',
                            'confirmed_cases': 'Confirmed cases',
                            'confirmed_per_100000': 'Confirmed per 100,000',
                            'deaths_per_100000': 'Deaths per 100,000'}
                    )
fig.update_layout(
    margin={"r": 0, "l": 0, "b": 0},
    # title=f'<b>{title}</b>',
    title_font_family="Times New Roman",
    template="gridon",
    coloraxis_colorbar=dict(title='',
                            yanchor="top",
                            y=1,
                            ticks="outside",
                            ticksuffix=" cases",
                            separatethousands=True)
)
# fig.show()
pl.Path(here("./output/maps", warn=False)).mkdir(parents=True, exist_ok=True)
pio.write_html(fig,
               file=str(here("./output/maps/choropleth_us_death_cases.html", warn=False)),
               auto_open=True)
'''
