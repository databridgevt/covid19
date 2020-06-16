import plotly.figure_factory as ff

import numpy as np
import pandas as pd

# ChoroplethMap using FIPS from merged data
'''
df = pd.read_csv('https://github.com/CSSEGISandData/COVID-19/raw/master/csse_covid_19_data/csse_covid_19_time_series/'
                 'time_series_covid19_confirmed_US.csv')
loc_df = pd.read_excel('State_FIPS.xlsx')
merged_df = pd.merge(loc_df, df, right_on='Admin2', left_on='Name')
# print(list(merged_df.columns))
merged_df['fips_str'] = merged_df['FIPS_x'].apply(lambda x: f'{x:05.0f}')  # left pad with 0 for 5 digits

colorscale = ["#f7fbff", "#ebf3fb", "#deebf7", "#d2e3f3", "#c6dbef", "#b3d2e9", "#9ecae1",
              "#85bcdb", "#6baed6", "#57a0ce", "#4292c6", "#3082be", "#2171b5", "#1361a9",
              "#08519c", "#0b4083", "#08306b"]
endpts = list(np.linspace(0, 3000, len(colorscale) - 1))
fips = merged_df['fips_str'].tolist()
values = merged_df['4/22/20'].tolist()

fig = ff.create_choropleth(
    fips=fips, values=values,
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
    show_hover=True, centroid_marker={'opacity': 0},
    asp=2.9, title='Confirmed cases on April 22',
    legend_title='# confirmed cases'
)

fig.layout.template = None
fig.show()
'''

# ChoroplethMap using FIPS from one dataset
'''
df = pd.read_csv('https://github.com/CSSEGISandData/COVID-19/raw/master/csse_covid_19_data/csse_covid_19_time_series/'
                 'time_series_covid19_confirmed_US.csv')
# loc_df = pd.read_excel('State_FIPS.xlsx')

df['fips_str'] = df['FIPS'].apply(lambda x: f'{x:05.0f}')  # left pad with 0 for 5 digits
df['fips_str'] = df['fips_str'].replace('00nan', '00000')  # convert '00nan' values to '00000'


colorscale = ["#f7fbff", "#ebf3fb", "#deebf7", "#d2e3f3", "#c6dbef", "#b3d2e9", "#9ecae1",
              "#85bcdb", "#6baed6", "#57a0ce", "#4292c6", "#3082be", "#2171b5", "#1361a9",
              "#08519c", "#0b4083", "#08306b"]
endpts = list(np.linspace(1, 12, len(colorscale) - 1))
fips = df['fips_str'].tolist()
values = df['4/22/20'].tolist()
print(df.loc[df.fips_str == "66"])
'''

