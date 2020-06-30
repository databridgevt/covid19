import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas

app = dash.Dash(__name__)
if __name__ == '__main__':
    app.run_server(
        debug=True,
        port=8050,
        host='0.0.0.0'
    )
app.layout = html.Div()
app.layout = html.Div(children=[
                      html.Div(className='row',  # Define the row element
                               children=[
                                  html.Div(className='four columns div-user-controls'),  # Define the left element
                                  html.Div(className='eight columns div-for-charts bg-grey')  # Define the right element
                                  ])
                                ])
children = [
    html.H2('COVID19 - US spread analysis'),
    html.P('''Map of confirmed cases'''),
    html.P('''Map of confirmed cases per capita''')
]