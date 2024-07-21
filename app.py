import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
import json
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go

app = Dash(__name__)

# Load data
df = pd.read_csv("school_data.csv")
# geojson = px.data.election_geojson()
with open('ThailandWithName.json', 'r', encoding='utf-8') as f:
    geojson = json.load(f)

province_coords = {}
for feature in geojson['features']:
    geometry = feature['geometry']
    properties = feature['properties']
    province_name = properties['name']
    
    if geometry['type'] == 'Polygon':
        coordinates = geometry['coordinates'][0]
        lats, lons = zip(*coordinates)  # Unzip coordinates into latitudes and longitudes
        centroid_lat = sum(lats) / len(lats)
        centroid_lon = sum(lons) / len(lons)
        province_coords[province_name] = [centroid_lat, centroid_lon]

df['latitude'] = df['province_english'].map(lambda x: province_coords.get(x, [None, None])[0])
df['longitude'] = df['province_english'].map(lambda x: province_coords.get(x, [None, None])[1])

def create_map(province=None):
    if province:
        dff = df[df['schools_province'] == province]
    else:
        dff = df

    fig = px.scatter_mapbox(
        dff,
        lat="latitude",
        lon="longitude",
        hover_name="schools_province",
        hover_data={"totalstd": True, "totalmale": True, "totalfemale": True, "latitude": False, "longitude": False},
        size="totalstd",
        color="totalstd",
        size_max=15,
        zoom=5,
        mapbox_style="carto-positron"
    )
    
    return fig

                                         
# App
app.layout = html.Div([
    html.H1("School Statistics in Thailand", style={'text-align': 'center'}),
    dcc.Dropdown(df.province_english.unique(), 'Phatthalung', id='dropdown-selection'),
    html.Div(id='output_container', children=[]),
    html.Br(),

    dcc.Graph(id='map', style={'width': '100%'}),
    html.Div([
        dcc.Graph(id='pie_chart', style={'width': '51%', 'display': 'inline-block'}),
        dcc.Graph(id='table', style={'width': '49%', 'display': 'inline-block'})
    ], style={'display': 'flex', 'justify-content': 'space-between'}),
    html.Br(),
    dcc.Graph(id='bar_chart', style={'width': '100%'})
])

@app.callback(
    [Output('output_container', 'children'),
     Output('bar_chart', 'figure'),
     Output('table', 'figure'),
     Output('pie_chart', 'figure'),
     Output('map', 'figure')],
    [Input('dropdown-selection', 'value')]
)
def update_graphs(selected_province):
    container = f"The province chosen by user was: {selected_province}"

    dff = df[df["province_english"] == selected_province]

    # Bar chart
    bar_fig = px.bar(
        dff,
        x=['Total', 'Male', 'Female'],
        y=[dff['totalstd'].iloc[0], dff['totalmale'].iloc[0], dff['totalfemale'].iloc[0]],
        title=f'The quantity of graduates in  {selected_province}',
        labels={'x': 'Category', 'y': 'The quantity'},
        color_discrete_sequence=['DarkTurquoise']
    )
    bar_fig.update_layout(plot_bgcolor='black', paper_bgcolor='black', font_color= "PaleTurquoise")

    # Table
    table_data = [
        ['Gender', 'Quantity'],
        ['Male', dff['totalmale'].iloc[0]],
        ['Female', dff['totalfemale'].iloc[0]],
    ]
    table_fig = ff.create_table(table_data, height_constant=60)

    table_fig.update_layout(plot_bgcolor='PaleTurquoise', paper_bgcolor='PaleTurquoise')

    # Map
    map_fig = px.choropleth_mapbox(
        df,create_map(selected_province),
        # locations='province_english',
        color='province_english',
        featureidkey="properties.name",
        center={"lat": 13.30, "lon": 100.52}, 
        mapbox_style="carto-positron",
        zoom=4.35, opacity=1,
        labels={'province_english':'Province'}
    )

    map_fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    map_fig.add_traces(px.choropleth_mapbox(
        dff,
        geojson=geojson,
        locations='province_english',
        color='province_english',
        featureidkey="properties.name",
        center={"lat": 13.30, "lon": 100.52},
        mapbox_style="carto-positron",
        zoom=4.35, opacity=1,
        labels={'totalstd':'Province'}
    ).data)

    map_fig.update_layout(plot_bgcolor='black', paper_bgcolor='black', font_color= "PaleTurquoise")

    # Pie chart
    selected_province_data = df[df['province_english'] == selected_province]['totalstd'].sum()
    other_provinces_data = df[df['province_english'] != selected_province]['totalstd'].sum()

    pie_data = pd.DataFrame({
        'Category': [selected_province, 'Other Provinces'],
        'Total Students': [selected_province_data, other_provinces_data]
    })

    # pie chart
    pie_fig = px.pie(
        pie_data,
        names='Category',
        values='Total Students'
    )

    pie_fig.update_layout(
        title={'text': f'{selected_province} vs Other Provinces', 'x': 0.5, 'xanchor': 'center'},
        plot_bgcolor='White', paper_bgcolor='black', font_color= "PaleTurquoise")

    return container, table_fig, pie_fig, bar_fig, map_fig

if __name__ == '__main__':
    app.run_server(debug=True)