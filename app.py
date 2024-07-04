from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd

df = pd.read_csv('D:\project_eco\stdall_th.csv')
geojson = px.data.election_geojson()

app = Dash(__name__)

app.layout = html.Div([
    html.H1(children='Graduation in Thailand', style={'textAlign':'center'}),
    dcc.Dropdown(df.schools_province.unique(), 'กรุงเทพ', id='dropdown-selection'),
    dcc.Graph(id='map')
])

@callback(
    Output('map', 'figure'),
    Input('dropdown-selection', 'value')
)
def update_data(value):
    dff = df[df.schools_province == value]
    
    fig = px.choropleth_mapbox(dff, geojson=geojson, 
                               color="totalstd",
                               locations="schools_province", featureidkey="properties.province",
                               center={"lat": 13.736717, "lon": 100.523186},
                               mapbox_style="carto-positron", zoom=6)  
    
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig


if __name__ == '__main__':
    app.run(debug=True)