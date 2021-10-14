# import pandas
import pandas as pd
import os
import pathlib
import numpy as np
import datetime as dt
import dash
import dash_core_components as dcc
import dash_html_components as html

from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
from scipy.stats import rayleigh
import plotly.express as px

from cassandrautils import *

app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)
app.title = "Dash"

server = app.server

app_color = {"graph_bg": "#082255", "graph_line": "#007ACE"}

app.layout = html.Div(
    [
        # header
        html.Div(
            [
                html.Div(
                    [
                        html.H4("Assignment 1 - Data visualization", className="app__header__title"),
                        html.P(
                            "- by Nguyen Quoc Hoang (s3697305) ",
                            className="app__header__title--grey",
                        ),
                    ],
                    className="app__header__desc",
                ),
                
            ],
            className="app__header",
        ),
        html.Div(
            [
                # weather
                html.Div(
                    [
                         html.Div([
                            html.H5("Temperature in Ho Chi Minh city"),
                            dcc.Dropdown(
                                id='checklist', 
                                value='temperature', 
                                options=[{'value': x, 'label': x} 
                                         for x in ['temp', 'temp_max', 'temp_min', 'feels_like']],
                                clearable=False
                            ),
                            dcc.Graph(id="line-chart"),
                        ])
                    ],
                    className="two-thirds column",
                ),
                html.Div(
                    [
                        # histogram
                        html.Div(
                            [
                                html.Div([
                                    html.H5("Histogram of age (Faker data)"),
                                    html.P("Number of data:"),
                                    dcc.Slider(id="num_bin", min=5, max=10, step=1, value=6),
                                    dcc.Graph(id="graph"),
                                ])
                            ],
                            className="graph__container first",
                        ),
                        
                        # histogram
                        html.Div(
                            [
                                html.Div([
                                    html.H5("Pie chart (Twitter data)"),
                                    dcc.Dropdown(
                                        id='location', 
                                        value='Tokoyo, Japan', 
                                        options=[{'value': x, 'label': x} 
                                                 for x in ['MetroVancouver']],
                                        clearable=False
                                    ),
                                    dcc.Graph(id="pie-chart"),
                                ])
                            ],
                            className="graph__container first",
                        ),
                        
                        
                        
                    ],
                    className="one-third column",
                ),
            ],
            className="app__content",
        ),
    ],
    className="app__container",
)

@app.callback(
    Output("line-chart", "figure"), 
    [Input("checklist", "value")])
def update_line_chart(col):
    df = getWeatherDF()
    df['forecast_timestamp'] = pd.to_datetime(df['forecastdate'])
    fig = px.line(df, 
        x="forecast_timestamp", y=col, color='location')
    return fig


@app.callback(
    Output("graph", "figure"), 
    [Input("num_bin", "value")])
def display_color(num_bin):
    df = getFakerDF()
    currentYear = dt.date.today().year
    df['age'] = df['year'].apply(lambda x: int(currentYear-x))
    fig = px.histogram(df['age'], nbins=num_bin, range_x=[0, 100])
    return fig


@app.callback(
    Output("pie-chart", "figure"), 
    [Input("location", "value")])
def generate_chart(location):
    df = getTwitterDF()
    df = df[df.location == location]
    value_counts = df.groupby(['classification'])['classification'].value_counts().rename_axis(['Count', 'classification']).reset_index(name='counts')
    fig = px.pie(value_counts, values='counts', names='classification')
    return fig


if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=8050, debug=True, dev_tools_ui=True)


