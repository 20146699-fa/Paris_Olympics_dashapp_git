import ast
import dash
from dash import dcc, html, Input, Output, dash_table
import pandas as pd
import plotly.express as px

# Load data from CSV files
venues_df = pd.read_csv('venues.csv')
medals_total_df = pd.read_csv('medals_total.csv')
medallists_df = pd.read_csv('medallists.csv')
athletes_df = pd.read_csv('athletes.csv')

# Parse list strings in venues
venues_df['sports'] = venues_df['sports'].apply(ast.literal_eval)

# Venue coordinates dictionary
venues_coords = {
    'Aquatics Centre': (48.923470, 2.355378),
    'Bercy Arena': (48.838566, 2.378091),
    'Bordeaux Stadium': (44.897335, -0.561928),
    'Champ de Mars Arena': (48.852886, 2.302584),
    'Château de Versailles': (48.805862, 2.116167),
    'Chateauroux Shooting Centre': (46.815071, 1.756573),
    'Eiffel Tower Stadium': (48.855789, 2.298278),
    'Elancourt Hill': (48.788319, 1.967734),
    'Geoffroy-Guichard Stadium': (45.460506, 4.389225),
    'Grand Palais': (48.865990, 2.311721),
    'Hôtel de Ville': (48.8566, 2.3522),
    'Invalides': (48.856457, 2.312355),
    'La Beaujoire Stadium': (47.256008, -1.524965),
    'La Concorde': (48.865635, 2.321103),
    'Le Bourget Sport Climbing Venue': (48.937275, 2.419988),
    'Golf National': (48.754559, 2.076024),
    'Lyon Stadium': (45.765293, 4.981832),
    'Marseille Marina': (43.295055, 5.364253),
    'Marseille Stadium': (43.269852, 5.395799),
    'Nice Stadium': (43.705173, 7.192550),
    'North Paris Arena': (48.970879, 2.520466),
    'Parc des Princes': (48.841404, 2.252818),
    'Paris La Defense Arena': (48.894737, 2.229619),
    'Pierre Mauroy Stadium': (50.611835, 3.130006),
    'Pont Alexandre III': (48.8639, 2.3136),
    'Porte de La Chapelle Arena': (48.899387, 2.359653),
    'Stade Roland-Garros': (48.845875, 2.253657),
    'Saint-Quentin-en-Yvelines BMX Stadium': (48.788017, 2.034483),
    'Saint-Quentin-en-Yvelines Velodrome': (48.788017, 2.034483),
    'South Paris Arena': (48.830055, 2.290313),
    'Stade de France': (48.924454, 2.359665),
    "Teahupo'o, Tahiti": (-17.809464, -149.303421),
    'Trocadéro': (48.861618, 2.288974),
    'Vaires-sur-Marne Nautical Stadium': (48.860378, 2.637301),
    'Yves-du-Manoir Stadium': (48.929279, 2.247588)
}

# Add lat and lon to venues_df
venues_df['lat'] = venues_df['venue'].map(lambda x: venues_coords.get(x)[0] if venues_coords.get(x) else None)
venues_df['lon'] = venues_df['venue'].map(lambda x: venues_coords.get(x)[1] if venues_coords.get(x) else None)

# Initialize the Dash app
app = dash.Dash(__name__, suppress_callback_exceptions=True)

# Navigation bar

navbar = html.Div([
    dcc.Link('Home', href='/', style={'margin': '10px'}),
    dcc.Link('Sports Insights', href='/sports-insights', style={'margin': '10px'}),
    dcc.Link('About', href='/about', style={'margin': '10px'}),
], style={'textAlign': 'center', 'fontSize': '20px', 'backgroundColor': '#9370DB', 'color': 'white', 'padding': '10px'})

# Home layout

total_countries = medals_total_df['country'].nunique()
total_athletes = athletes_df[athletes_df['current'] == True].shape[0]
total_medals = medals_total_df['Total'].sum()

home_layout = html.Div([
   
    html.Div([
        html.Div(f'Total Countries: {total_countries}', style={'backgroundColor': '#FFA07A', 'padding': '10px', 'margin': '10px', 'textAlign': 'center'}),
        html.Div(f'Total Athletes: {total_athletes}', style={'backgroundColor': '#FFA07A', 'padding': '10px', 'margin': '10px', 'textAlign': 'center'}),
        html.Div(f'Total Medals: {total_medals}', style={'backgroundColor': '#FFA07A', 'padding': '10px', 'margin': '10px', 'textAlign': 'center'}),
    ], style={'display': 'flex', 'justifyContent': 'space-around'}),
    html.Div([
        dcc.Graph(figure=px.bar(medals_total_df.sort_values('Total', ascending=False).head(5), x='country', y='Total', title='<b>Medals Won by Top 5 Countries<b>', color='Total', color_continuous_scale='Viridis')),
        dcc.Graph(
    figure=px.choropleth(
        medals_total_df,
        locations='country',
        locationmode='country names',
        color='Total',
        color_continuous_scale='Plasma',
        title='<b>Total Medals Won By Countries (Hover Over The Map For Details)<b>'
    )
)
    ], style={'display': 'flex', 'justifyContent': 'space-around'}),
    html.P('Data Source: Paris Olympics 2024 | Version 1.0 | Data4All PLC', style={'textAlign': 'center', 'fontStyle': 'italic'})
], style={'backgroundColor': '#ADD8E6', 'padding': '20px'})

# Sports Insights layout

sports_options = [{'label': sport, 'value': sport} for sport in sorted(set(venue for sublist in venues_df['sports'] for venue in sublist))]
country_options = [{'label': country, 'value': country} for country in sorted(medals_total_df['country'].unique())]

sports_insights_layout = html.Div([
    html.Div([
    html.Label('Sport:', style={
        'marginRight': '8px',
        'fontWeight': 'bold',
        'color': 'green',
        'fontSize': '20px'
    }),
    dcc.Dropdown(
        id='sport-dropdown',
        options=sports_options,
        placeholder='Select Sport',
        style={
            'width': '40%',
            'marginRight': '20px',
            'fontSize': '16px'
        }
    ),

    html.Label('Country:', style={
        'marginRight': '8px',
        'fontWeight': 'bold',
        'color': 'green',
        'fontSize': '20px'
    }),
    dcc.Dropdown(
        id='country-dropdown',
        options=country_options,
        placeholder='Select Country',
        style={
            'width': '40%',
            'fontSize': '16px'
        }
    )
], style={
    'display': 'flex',
    'justifyContent': 'center',
    'alignItems': 'center',
    'gap': '10px',
    'marginBottom': '20px'
})
,
    html.Div([
        dcc.Graph(id='medal-trends-chart', figure=px.bar(title='Bar Chart - Medal Trends')),
        html.Div([
            dcc.Graph(id='venues-map', figure=px.scatter_mapbox(venues_df, lat='lat', lon='lon', hover_name='venue', hover_data=['sports'], mapbox_style='open-street-map', title='<b>Map of Paris Olympic Venues<b>', zoom=3))
        ], style={'margin-left': '-100px'})  # Shift map to the left
    ], style={'display': 'flex', 'justifyContent': 'space-around'}),
    html.P('Data Source: Paris Olympics 2024 | Version 1.0 | Data4All PLC', style={'textAlign': 'center', 'fontStyle': 'italic'})
], style={'backgroundColor': '#ADD8E6', 'padding': '20px'})

# About layout

about_layout = html.Div([
    html.H1('About', style={'textAlign': 'center'}),
    html.P('This Dashboard Provides Insights Into The Paris Olympics 2024 Data For Sports Journalists, Analysts, And Fans.', style={'textAlign': 'center', 'fontStyle': 'italic'}),
    html.P('Data Source: Paris Olympics 2024 | Version 1.0 | Data4All PLC', style={'textAlign': 'center', 'fontStyle': 'italic'})
], style={'backgroundColor': '#ADD8E6', 'padding': '20px'})
print("Unique countries:", medallists_df['country'].dropna().unique()[:20])
print("Unique disciplines:", medallists_df['discipline'].dropna().unique()[:20])
print("Unique medal types:", medallists_df['medal_type'].dropna().unique())

# Callback for Sports Insights page
@app.callback(
    Output('medal-trends-chart', 'figure'),
    [Input('sport-dropdown', 'value'), Input('country-dropdown', 'value')]
)
def update_medal_trends(selected_sport, selected_country):
    df = medallists_df.copy()

    if selected_sport:
        filtered = df[df['discipline'].str.lower() == selected_sport.lower()]
        if filtered.empty:
            return px.bar(title=f'No data for {selected_sport}')

        # Group by country and medal type
        medal_counts = filtered.groupby(['country', 'medal_type']).size().unstack(fill_value=0)

        # Sort by Gold, then Silver, then Bronze, then country name
        medal_counts = medal_counts.sort_values(
            by=['Gold Medal', 'Silver Medal', 'Bronze Medal'], ascending=[False, False, False]
        ).reset_index()

        fig = px.bar(
            medal_counts,
            x='country',
            y=['Gold Medal', 'Silver Medal', 'Bronze Medal'],
            title=f'Medals by Country in {selected_sport}',
            barmode='group'
        )
        return fig

    elif selected_country:
        filtered = df[df['country'].str.lower() == selected_country.lower()]
        if filtered.empty:
            return px.bar(title=f'No data for {selected_country}')
        medal_counts = filtered['medal_type'].value_counts().rename_axis('Medal Type').reset_index(name='Count')
        medal_counts = medal_counts.set_index('Medal Type').reindex(['Gold Medal','Silver Medal','Bronze Medal'], fill_value=0).reset_index()
        fig = px.bar(
            medal_counts,
            x='Medal Type',
            y='Count',
            color='Medal Type',
            title=f'Medals Won by {selected_country}',
            color_discrete_map={'Gold Medal': 'gold', 'Silver Medal': 'silver', 'Bronze Medal': '#cd7f32'}
        )
        return fig

    return px.bar(title='<b>Select a Sport or Country From The Dropdown Menu</b>')

    
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    navbar,
    html.Div(id='page-content')
])

# Callback to render page content
@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/sports-insights':
        return sports_insights_layout
    elif pathname == '/about':
        return about_layout
    else:
        return home_layout

if __name__ == '__main__':
    app.run(debug=True)