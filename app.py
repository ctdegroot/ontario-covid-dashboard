import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.graph_objs as go

import urllib.request
import json

import pandas as pd

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.UNITED])
app.title = "Ontario COVID-19 Data"
server = app.server

# Get the data
url = "https://data.ontario.ca/api/3/action/datastore_search?resource_id=ed270bb8-340b-41f9-a7c6-e8ef587e6d11&limit=1000"
res = urllib.request.urlopen(url)
data = json.loads(res.read())

# Create the dataframe
df = pd.read_json(json.dumps(data["result"]["records"]), orient="records")
df.sort_values(by="_id", inplace=True)
df["Reported Date"] = pd.to_datetime(df["Reported Date"])

# Get the date of last update
last_updated = df["Reported Date"].iloc[-1].date()

# Case data calculations
df["Daily Cases"] = df["Total Cases"].diff()
df["7-Day Case Avg."] = df["Daily Cases"].rolling(7).mean()

# Death data calculations
df["Daily Deaths"] = df["Deaths"].diff()
df["7-Day Death Avg."] = df["Daily Deaths"].rolling(7).mean()

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
        y=df["7-Day Case Avg."],
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

daily_deaths = get_bar_chart(
        df["Reported Date"],
        df["Daily Deaths"],
        "Daily Deaths"
    )

daily_death_avg = go.Scatter(
        x=df["Reported Date"],
        y=df["7-Day Death Avg."],
        mode="lines",
        name="7-Day Moving Avg."
    )

total_deaths = get_bar_chart(
        df["Reported Date"],
        df["Deaths"],
        "Total Cases"
    )

case_layout = go.Layout(
        xaxis={"title" : "Date"},
        yaxis={"title" : "Number of Cases"},
        legend={"x" : 0, "y" : 1}
    )

death_layout = go.Layout(
        xaxis={"title" : "Date"},
        yaxis={"title" : "Number of Deaths"},
        legend={"x" : 0, "y" : 1}
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

def get_daily_death_plot():
    return dcc.Graph(
            id='daily-deaths',
            figure=
            {
                'data': [daily_deaths, daily_death_avg],
                'layout' : death_layout
            }
        )

def get_total_death_plot():
    return dcc.Graph(
            id='total-deaths',
            figure=
            {
                'data': [total_deaths],
                'layout' : death_layout
            }
        )

app.layout = dbc.Container(
    [
        html.Div(
            [
                dbc.Badge("Last updated: {}".format(last_updated), color="primary", className="mr-1")
            ],
            className="text-right"
        ),
        html.H1("Ontario COVID-19 Data", style=heading_style),
        dbc.Row(
            dbc.Col(
                dbc.Card(
                    [
                        dbc.CardHeader(html.H2("Case Data", style=heading_style)),
                        dbc.CardBody(
                            [
                                dbc.Tabs(
                                    [
                                        dbc.Tab(label="Daily", tab_id="daily-cases"),
                                        dbc.Tab(label="Active", tab_id="active-cases"),
                                        dbc.Tab(label="Total", tab_id="total-cases"),
                                    ],
                                    id="case-tabs",
                                    active_tab="daily-cases",
                                ),
                                html.Div(id="case-tab-content", className="p-4"),
                            ]
                        ),
                    ]
                )
            )
        ),
        html.Br(),
        dbc.Row(
            dbc.Col(
                dbc.Card(
                    [
                        dbc.CardHeader(html.H2("Death Data", style=heading_style)),
                        dbc.CardBody(
                            [
                                dbc.Tabs(
                                    [
                                        dbc.Tab(label="Daily", tab_id="daily-deaths"),
                                        dbc.Tab(label="Total", tab_id="total-deaths"),
                                    ],
                                    id="death-tabs",
                                    active_tab="daily-deaths",
                                ),
                                html.Div(id="death-tab-content", className="p-4"),
                            ]
                        ),
                    ]
                )
            )
        ),
        html.Br(),
    ],
    fluid=True
)

@app.callback(
    Output("case-tab-content", "children"),
    [Input("case-tabs", "active_tab")],
)

def render_case_tab_content(active_tab):
    """
    This callback takes the 'active_tab' property as input and renders the tab
    content depending on what the value of 'active_tab' is.
    """
    if active_tab is not None:
        if active_tab == "daily-cases":
            return get_daily_case_plot()
        elif active_tab == "active-cases":
            return get_active_case_plot()
        elif active_tab == "total-cases":
            return get_total_case_plot()
    return "No case tab selected"

@app.callback(
    Output("death-tab-content", "children"),
    [Input("death-tabs", "active_tab")],
)

def render_case_tab_content(active_tab):
    """
    This callback takes the 'active_tab' property as input and renders the tab
    content depending on what the value of 'active_tab' is.
    """
    if active_tab is not None:
        if active_tab == "daily-deaths":
            return get_daily_death_plot()
        elif active_tab == "total-deaths":
            return get_total_death_plot()
    return "No death tab selected"

if __name__ == '__main__':
    app.run_server(debug=False)
