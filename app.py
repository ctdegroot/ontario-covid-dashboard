import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.graph_objs as go

import pandas as pd

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Ontario COVID-19 Data"
server = app.server

# Get the data
url = "https://data.ontario.ca/dataset/f4f86e54-872d-43f8-8a86-3892fd3cb5e6/resource/ed270bb8-340b-41f9-a7c6-e8ef587e6d11/download/covidtesting.csv"

df = pd.read_csv(url)
df["Daily Cases"] = df["Total Cases"].diff()
df["7-Day Daily Moving Avg."] = df["Daily Cases"].rolling(7).mean()

heading_style = {"textAlign" : "center"}

app.layout = html.Div([
    html.H1("Ontario COVID-19 Data", style=heading_style),
    dbc.Card(
        dbc.CardBody([
            html.H2("Daily Cases", style=heading_style),
            dcc.Graph(
                id='daily-cases',
                figure={
                    'data': [
                        go.Bar(
                            x=df["Reported Date"],
                            y=df["Daily Cases"],
                            opacity=0.8,
                            name="Daily Cases"
                        ),
                        go.Scatter(
                            x=df["Reported Date"],
                            y=df["7-Day Daily Moving Avg."],
                            mode="lines",
                            name="7-Day Moving Avg."
                        )
                    ],
                    'layout' :
                    go.Layout(
                        xaxis={"title" : "Date"},
                        yaxis={"title" : "Number of Cases"},
                        legend={"x" : 0, "y" : 1}
                    )
                }
            ),
        ]),
        className="w-75 mx-auto"
    ),
    dbc.Card(
        dbc.CardBody([
            html.H2("Active Cases", style=heading_style),
            dcc.Graph(
                id='active-cases',
                figure={
                    'data': [
                        go.Bar(
                            x=df["Reported Date"],
                            y=df["Confirmed Positive"],
                            opacity=0.8,
                            name="Active Cases"
                        )
                    ],
                    'layout' :
                    go.Layout(
                        xaxis={"title" : "Date"},
                        yaxis={"title" : "Number of Cases"}
                    )
                }
            ),
        ]),
        className="w-75 mx-auto"
    ),
    dbc.Card(
        dbc.CardBody([
            html.H2("Total Cases", style=heading_style),
            dcc.Graph(
                id='total-cases',
                figure={
                    'data': [
                        go.Bar(
                            x=df["Reported Date"],
                            y=df["Total Cases"],
                            opacity=0.8,
                            name="Total Cases"
                        )
                    ],
                    'layout' :
                    go.Layout(
                        xaxis={"title" : "Date"},
                        yaxis={"title" : "Number of Cases"}
                    )
                }
            ),
        ]),
        className="w-75 mx-auto"
    ),
])

if __name__ == '__main__':
    app.run_server(debug=False)
