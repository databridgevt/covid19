import geopandas as gpd
from shapely.geometry import Point, Polygon
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


loc_df = pd.read_csv('us-zip-code-latitude-and-longitude.csv', index_col=0)
print(loc_df.head())
fig = px.scatter_mapbox(loc_df, lat="lat", lon="lon", color="State")
fig.update_layout(mapbox_style="open-street-map")
fig.show()