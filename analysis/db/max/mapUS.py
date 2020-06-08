import geopandas as gpd
from shapely.geometry import Point, Polygon
import matplotlib.pyplot as plt
import pandas as pd

usa = gpd.read_file("./tl_2017_us_state/tl_2017_us_state.shp")
usa.plot()