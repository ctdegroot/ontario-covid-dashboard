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
last_updated = df["Reported Date"].iloc[-1]

heading_style = {"textAlign" : "center"}
bar_opacity = 0.6

def get_bar_chart(x, y, name):
    return go.Bar(x=x, y=y, opacity=bar_opacity, name=name)

daily_cases = get_bar_chart(
        df["Reported Date"],
        df["Daily Cases"],
        "Daily Cases"
    )

daily_cases_avg = go.Scatter(
        x=df["Reported Date"],
        y=df["7-Day Daily Moving Avg."],
        mode="lines",
        name="7-Day Moving Avg."
    )

active_cases = get_bar_chart(
        df["Reported Date"],
        df["Confirmed Positive"],
        "Active Cases"
    )

total_cases = get_bar_chart(
        df["Reported Date"],
        df["Total Cases"],
        "Total Cases"
    )

case_layout = go.Layout(
        xaxis={"title" : "Date"},
        yaxis={"title" : "Number of Cases"},
        legend={"x" : 0, "y" : 1}
    )

def get_active_case_plot():
    return dcc.Graph(
            id='daily-cases',
            figure=
            {
                'data': [daily_cases, daily_cases_avg],
                'layout' : case_layout
            }
        )

def get_daily_case_plot():
    return dcc.Graph(
            id='daily-cases',
            figure=
            {
                'data': [daily_cases, daily_cases_avg],
                'layout' : case_layout
            }
        )

def get_active_case_plot():
    return dcc.Graph(
            id='active-cases',
            figure=
            {
                'data': [active_cases],
                'layout' : case_layout
            }
        )

def get_total_case_plot():
    return dcc.Graph(
            id='total-cases',
            figure=
            {
                'data': [total_cases],
                'layout' : case_layout
            }
        )

app.layout = dbc.Container(
    [
        html.H1("Ontario COVID-19 Data", style=heading_style),
        html.Div(
            [
                dbc.Badge("Last updated: {}".format(last_updated), color="primary", className="mr-1")
            ],
            className="text-right"
        ),
        dbc.Card(
            [
                dbc.CardHeader(html.H2("Daily Cases", style=heading_style)),
                dbc.CardBody(get_daily_case_plot()),
            ],
            className="mx-auto"
        ),
        dbc.Card(
            [
                dbc.CardHeader(html.H2("Active Cases", style=heading_style)),
                dbc.CardBody(get_active_case_plot()),
            ],
            className="mx-auto"
        ),
        dbc.Card(
            [
                dbc.CardHeader(html.H2("Total Cases", style=heading_style)),
                dbc.CardBody(get_total_case_plot()),
            ],
            className="mx-auto"),
    ],
    fluid=True
)

if __name__ == '__main__':
    app.run_server(debug=False)
