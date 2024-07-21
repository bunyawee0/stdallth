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
province_coords = {
    "กระบี่": [8.0863, 98.9063],
    "กรุงเทพมหานคร": [13.7563, 100.5018],
    "กาญจนบุรี": [14.0228, 99.5328],
    "กาฬสินธุ์": [16.4322, 103.5061],
    "กำแพงเพชร": [16.4828, 99.5228],
    "ขอนแก่น": [16.4419, 102.8356],
    "จันทบุรี": [12.6096, 102.1045],
    "ฉะเชิงเทรา": [13.6904, 101.0766],
    "ชลบุรี": [13.3611, 100.9847],
    "ชัยนาท": [15.1860, 100.1253],
    "ชัยภูมิ": [15.8064, 102.0311],
    "ชุมพร": [10.4930, 99.1800],
    "ตรัง": [7.5590, 99.6111],
    "ตราด": [12.2420, 102.5175],
    "ตาก": [16.8790, 99.1254],
    "นครนายก": [14.2069, 101.2131],
    "นครปฐม": [13.8199, 100.0622],
    "นครพนม": [17.4108, 104.7784],
    "นครราชสีมา": [14.9799, 102.0978],
    "นครศรีธรรมราช": [8.4324, 99.9631],
    "นครสวรรค์": [15.7047, 100.1372],
    "นนทบุรี": [13.8591, 100.5217],
    "นราธิวาส": [6.4260, 101.8250],
    "น่าน": [18.7835, 100.7712],
    "บึงกาฬ": [18.3607, 103.6437],
    "บุรีรัมย์": [14.9930, 103.1029],
    "ปทุมธานี": [14.0208, 100.5250],
    "ประจวบคีรีขันธ์": [11.8129, 99.7972],
    "ปราจีนบุรี": [14.0496, 101.3692],
    "ปัตตานี": [6.8688, 101.2505],
    "พระนครศรีอยุธยา": [14.3532, 100.5680],
    "พะเยา": [19.1637, 99.9996],
    "พังงา": [8.4509, 98.5267],
    "พัทลุง": [7.6167, 100.0796],
    "พิจิตร": [16.4387, 100.3498],
    "พิษณุโลก": [16.8214, 100.2659],
    "ภูเก็ต": [7.8804, 98.3923],
    "มหาสารคาม": [16.1868, 103.2980],
    "มุกดาหาร": [16.5405, 104.7222],
    "ยะลา": [6.5425, 101.2817],
    "ยโสธร": [15.7928, 104.1454],
    "ระนอง": [9.7777, 98.6160],
    "ระยอง": [12.6833, 101.2789],
    "ราชบุรี": [13.5283, 99.8134],
    "ร้อยเอ็ด": [16.0568, 103.6531],
    "ลพบุรี": [14.7995, 100.6534],
    "ลำปาง": [18.2888, 99.4908],
    "ลำพูน": [18.5789, 99.0087],
    "ศรีสะเกษ": [15.1180, 104.3228],
    "สกลนคร": [17.1558, 104.1455],
    "สงขลา": [7.1890, 100.5953],
    "สตูล": [6.6238, 100.0674],
    "สมุทรปราการ": [13.5991, 100.5994],
    "สมุทรสงคราม": [13.4090, 100.0021],
    "สมุทรสาคร": [13.5471, 100.2744],
    "สระบุรี": [14.5299, 100.9109],
    "สระแก้ว": [13.8250, 102.3484],
    "สิงห์บุรี": [14.8901, 100.3987],
    "สุพรรณบุรี": [14.4745, 100.1200],
    "สุราษฎร์ธานี": [9.1382, 99.3214],
    "สุรินทร์": [14.8818, 103.4936],
    "สุโขทัย": [17.0060, 99.8265],
    "หนองคาย": [17.8783, 102.7421],
    "หนองบัวลำภู": [17.2046, 102.4410],
    "อำนาจเจริญ": [15.8463, 104.6353],
    "อุดรธานี": [17.4075, 102.7931],
    "อุตรดิตถ์": [17.6200, 100.0993],
    "อุทัยธานี": [15.3816, 100.0244],
    "อุบลราชธานี": [15.2287, 104.8570],
    "อ่างทอง": [14.5896, 100.4557],
    "เชียงราย": [19.9072, 99.8327],
    "เชียงใหม่": [18.7883, 98.9853],
    "เพชรบุรี": [13.1117, 99.9447],
    "เพชรบูรณ์": [16.4182, 101.1606],
    "เลย": [17.4855, 101.7223],
    "แพร่": [18.1445, 100.1408],
    "แม่ฮ่องสอน": [19.3020, 97.9685]
}

# Add coordinates to the DataFrame
df['latitude'] = df['schools_province'].apply(lambda x: province_coords[x][0])
df['longitude'] = df['schools_province'].apply(lambda x: province_coords[x][1])

def create_map(province=None):
    if province:
        df_filtered = df[df['schools_province'] == province]
    else:
        df_filtered = df

    fig = px.scatter_mapbox(
        df_filtered,
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


with open('ThailandWithName.json', 'r', encoding='utf-8') as f:
    geojson = json.load(f)
                                         
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

    # สร้างแผนภูมิวงกลม
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