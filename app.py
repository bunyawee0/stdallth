import pandas as pd
import plotly.express as px
import json
from dash import Dash, dcc, html
from dash.dependencies import Input, Output

app = Dash(__name__)

# Load data
df = pd.read_csv("D:\project_eco\stdall_th.csv")
geojson = px.data.election_geojson()

df = df.groupby(['schools_province'])[['totalstd', 'totalmale', 'totalfemale']].mean().reset_index()
print(df[:5])

# App
app.layout = html.Div([
    html.H1("School Statistics in Thailand", style={'text-align': 'center'}),
    dcc.Dropdown(df.schools_province.unique(), 'พัทลุง', id='dropdown-selection'),
    html.Div(id='output_container', children=[]),
    html.Br(),

    dcc.Graph(id='bar_chart'),
    dcc.Graph(id='map')
])

@app.callback(
    [Output('output_container', 'children'),
     Output('bar_chart', 'figure'),
     Output('map', 'figure')],
    [Input('dropdown-selection', 'value')]
)
def update_graphs(selected_province):
    container = f"The province chosen by user was: {selected_province}"

    dff = df[df["schools_province"] == selected_province]

    # Bar chart
    bar_fig = px.bar(
        dff,
        x=['Total', 'Male', 'Female'],
        y=[dff['totalstd'].iloc[0], dff['totalmale'].iloc[0], dff['totalfemale'].iloc[0]],
        title=f'The quantity of graduates in  {selected_province}',
        labels={'x': 'Category', 'y': 'The quantity'}
    )

    # Map
    map_fig = px.choropleth_mapbox(
        df,geojson=geojson,
        locations='schools_province',
        color='totalstd',
        featureidkey="properties.name",
        center={"lat": 7.5435, "lon": 	99.9972}, 
        mapbox_style="carto-positron",
        zoom=5,
        opacity=0.5,
        labels={'totalstd':'Total Students'}
    )
    map_fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    map_fig.add_traces(px.choropleth_mapbox(
        df[df['schools_province'] == selected_province],
        geojson=geojson,
        locations='schools_province',
        color='totalstd',
        featureidkey="properties.name",
        center={"lat": 7.5435, "lon": 	99.9972},
        mapbox_style="carto-positron",
        zoom=4, opacity=1,
        labels={'totalstd':'Total Students'}
    ).data)

    return container, map_fig, bar_fig

if __name__ == '__main__':
    app.run_server(debug=True)