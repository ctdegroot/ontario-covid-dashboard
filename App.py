import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.graph_objs as go

import pandas as pd

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# Get the data
url = "https://data.ontario.ca/dataset/f4f86e54-872d-43f8-8a86-3892fd3cb5e6/resource/ed270bb8-340b-41f9-a7c6-e8ef587e6d11/download/covidtesting.csv"

df = pd.read_csv(url)
df["Daily Cases"] = df["Total Cases"].diff()
df["7-Day Moving Avg."] = df["Daily Cases"].rolling(7).mean()

heading_style = {"textAlign" : "center"}

app.layout = html.Div([
    html.H1("Ontario COVID-19 Data", style=heading_style),
    html.H2("Daily Cases", style=heading_style),
    dcc.Graph(
        id='Graph1',
        figure={
            'data': [
                go.Bar(
                    x=df["Reported Date"],
                    y=df["Daily Cases"],
                    #text=df[df['continent'] == i]['country'],
                    #mode='lines',
                    opacity=0.8,
                    #marker={
                    #    'size': 15,
                    #    'line': {'width': 0.5, 'color': 'white'}
                    #},
                    name="Confirmed Positive"
                ),
                go.Scatter(
                    x=df["Reported Date"],
                    y=df["7-Day Moving Avg."],
                    mode='lines',
                    name="Daily Cases"
                )
            ],
            'layout' :
            go.Layout(
                xaxis={"title" : "Date"},
                yaxis={"title" : "Number of Cases"}
            )
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=False)
