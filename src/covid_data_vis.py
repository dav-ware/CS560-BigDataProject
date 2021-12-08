import pandas as pd 
import geopandas
import matplotlib.pyplot as plt

state_abbreviations = ['AL','AK','AZ','AR','CA','CO','CT','DE','FL','GA','HI','ID','IL','IN','IA','KS','KY','LA','ME','MD','MA','MI','MN','MS','MO','MT','NE','NV','NH','NJ','NM','NY', 'NYC','NC','ND','OH','OK','OR','PA','RI','SC','SD','TN','TX','UT','VT',
'VA','WA','WV','WI','WY']

with open('datasets/covid19_data.csv') as file:
    df = pd.read_csv(file)

df = df[df['state'].isin(state_abbreviations)]

states = geopandas.read_file('data/usa-states-census-2014.shp')
states = states.to_crs("EPSG:3395")
states.plot()
plt.show()