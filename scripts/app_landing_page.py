# -*- coding: utf-8 -*-
"""
Created on Mon Nov 14 20:14:33 2022

@author: Akhilesh
"""

import pandas as pd
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from dash import Dash, dcc, html, Input, Output, dash_table, State
import pandas as pd
from plotly.subplots import make_subplots
import dash_daq as daq


import numpy as np

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"

apple_preds = pd.read_excel("../data/predictions/AAPL/predictions.xlsx")
apple_sentiments = pd.read_csv("../data/Predictions/AAPL/sentiment_out.csv")

navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=PLOTLY_LOGO, height="30px")),
                        dbc.Col(dbc.NavbarBrand("STOCKBUFF - Stock Sentiment Analyser", className="ms-2")),
                    ],
                    align="center",
                    className="g-0",
                ),
                href="https://plotly.com",
                style={"textDecoration": "none"},
            ),
            dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
        ]
    ),
    color="dark",
    dark=True,
)
def plot_line():
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        name="Actuals",
        mode="markers+lines", x=apple_preds["Date"], y=apple_preds["Actuals"],
        marker_symbol="star"
    ))
    
    fig.add_trace(go.Scatter(
        name="Predicted",
        mode="markers+lines", x=apple_preds["Date"], y=apple_preds["Predicted"],
        marker_symbol="star"
    ))
    fig.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(step="all")
            ])
        )
    )
    return fig

def plot_pie():
    fig = make_subplots(rows=1, cols=2, specs=[[{'type':'domain'}, {'type':'domain'}]])
    fig.add_trace(go.Indicator(
                mode = "gauge+number",
                value = 70,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "Volume"}),1,1
        )
    fig.add_trace(go.Indicator(
                mode = "gauge+number",
                value = 30,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "Close"}),1,2
        )

    # Use `hole` to create a donut-like pie chart

    return fig
    
def plot_table():
    return dash_table.DataTable(
        data = apple_sentiments.to_dict('records'),
        columns=[
            {'name': i, 'id': i} for i in apple_sentiments.columns
        ],
        style_data_conditional=[
            {
                'if': {
                    'filter_query': '{Polarity} > 0.7'
                },
                'backgroundColor': '#86FF33',
                'color': 'white'
            }
        ],
        style_table={
            'height': 500,
            'overflowY': 'scroll',
            'width': 750
        }
    )
def get_current_price(value, reference):
    fig = go.Figure()
    fig.add_trace(go.Indicator(
        mode = "number+delta",
        value = value,
        number = {'prefix': "$"},
        domain = {'x': [0,0], 'y': [0, 0]},
        delta = {'reference': reference, 'relative': True, 'position' : "top", 'valueformat':'.2f',},
        ))
    fig.update_layout(height = 300)
    return fig

toast_apple_current_market = dbc.Toast([
        html.Img(src="/static/images/apple_logo.jpg", height="50px"),    
        html.Div([
            dcc.Graph(figure = get_current_price(150, 162))
        ]),
        html.H5("Current News"),
        html.P("Microsoft revives SwiftKey keyboard, brings it back on iOS for Apple users"),                
        html.Br(),
        html.H5("Market Sentiment - Positive"),
        daq.Gauge(
            color={"gradient":True,"ranges":{"green":[0,6],"yellow":[6,8],"red":[8,10]}},
            value=2,            
            max=10,
            min=0,
        )
    ], header = "Apple Current Price", icon = 'src="/static/images/apple_logo.jpg"')

toast_microsoft_current_market = dbc.Toast([
        html.Img(src="/static/images/microsoft_log.jpg", height="50px"),    
        html.Div([
            dcc.Graph(figure = get_current_price(90, 98))
        ]),
        html.H5("Current News"),
        html.P("Customers want to know: How do I get more value from my data?"),
        html.Br(),
        html.H5("Market Sentiment - Neutral"),
        daq.Gauge(
            color={"gradient":True,"ranges":{"green":[0,6],"yellow":[6,8],"red":[8,10]}},
            value=5,            
            max=10,
            min=0,
        )
    ], header = "Microsoft Current Price", icon = "/static/images/microsoft_log.jpg")

toast_netflix_current_market = dbc.Toast([
        html.Img(src="/static/images/netflix-new-logo.png", height="50px"),    
        html.Div([
            dcc.Graph(figure = get_current_price(102, 105))
        ]),
        html.H5("Current News"),
        html.P("Bob Iger’s return may not boost Disney’s shares as market sends mixed signals to media stocks"),        
        html.Br(),
        html.H5("Market Sentiment - Negative"),
        daq.Gauge(
            color={"gradient":True,"ranges":{"green":[0,6],"yellow":[6,8],"red":[8,10]}},
            value=8,            
            max=10,
            min=0,
        )
    ], header = "Netflix Current Price", icon = "/static/images/netflix-new-logo.png")

toast_amazon_current_market = dbc.Toast([
        html.Img(src="/static/images/amazon_logo.png", height="50px"),    
        html.Div([
            dcc.Graph(figure = get_current_price(96, 90))
        ]),
        html.H5("Current News"),
        html.P("When will the Big Tech layoffs come to an end?"),        
        html.Br(),
        html.H5("Market Sentiment - Positive"),
        daq.Gauge(
            color={"gradient":True,"ranges":{"green":[0,6],"yellow":[6,8],"red":[8,10]}},
            value=7,            
            max=10,
            min=0,
        )
    ], header = "Amazon Current Price", icon = "/static/images/amazon_logo.png")


def toggle_modal(n1, is_open):
    if n1:
        return not is_open
    return is_open

def prepare_apple_modal():
    fig = plot_line()
    fig1 = plot_pie()
    return html.Div([
        dbc.Row([
           dbc.Col([
               dbc.Card([
                   dbc.CardHeader("Stock Predictions"),
                   dbc.CardBody(dcc.Graph(figure=fig))
               ])
               ]),
           dbc.Col([
               dbc.Card([
                    dbc.CardHeader("Comparing Stock Metrics"),
                    dbc.CardBody(dcc.Graph(figure = fig1))
                   
                   ])                      
               ])
        ]),
        dbc.Row([
        
            dbc.Card([
                dbc.CardHeader("Sentiment Data"),
                dbc.CardBody(plot_table())
            ])    
            
        ])
    ])
app.layout = html.Div([     
        dbc.Row([            
            navbar                
        ]),
        dbc.Row([
            dbc.Col([
                toast_apple_current_market,
                dbc.Button("Click for detailed analysis", color = "success",id="open-apple", n_clicks=0, style = {"width":"350px"}),
                dbc.Modal(
                    [
                        dbc.ModalHeader(dbc.ModalTitle("Detailed Analysis")),
                        dbc.ModalBody(prepare_apple_modal()),
                    ],
                    id="modal-apple",
                    size="xl",
                    is_open=False,
                ),                                
            ]),
            dbc.Col([
                toast_amazon_current_market,
                dbc.Button("Click for detailed analysis", color = "success",id="open-amazon", n_clicks=0, style = {"width":"350px"}),
                dbc.Modal(
                    [
                        dbc.ModalHeader(dbc.ModalTitle("Detailed Analysis")),
                        dbc.ModalBody("An extra large modal."),
                    ],
                    id="modal-amazon",
                    size="xl",
                    is_open=False,
                ),
            ]),
            dbc.Col([
                toast_microsoft_current_market,
                dbc.Button("Click for detailed analysis", color = "warning",id="open-microsoft", n_clicks=0, style = {"width":"350px"}),
                dbc.Modal(
                    [
                        dbc.ModalHeader(dbc.ModalTitle("Detailed Analysis")),
                        dbc.ModalBody("An extra large modal."),
                    ],
                    id="modal-microsoft",
                    size="xl",
                    is_open=False,
                ),
                
            ]),
            dbc.Col([
                toast_netflix_current_market,
                dbc.Button("Click for detailed analysis", color = "danger",id="open-netflix", n_clicks=0, style = {"width":"350px"}),
                dbc.Modal(
                    [
                        dbc.ModalHeader(dbc.ModalTitle("Detailed Analysis")),
                        dbc.ModalBody("An extra large modal."),
                    ],
                    id="modal-netflix",
                    size="xl",
                    is_open=False,
                ),
            ])
        ])        
    ])

app.callback(
    Output("modal-apple", "is_open"),
    Input("open-apple", "n_clicks"),
    State("modal-apple", "is_open"),
)(toggle_modal)

app.callback(
    Output("modal-amazon", "is_open"),
    Input("open-amazon", "n_clicks"),
    State("modal-amazon", "is_open"),
)(toggle_modal)

app.callback(
    Output("modal-microsoft", "is_open"),
    Input("open-microsoft", "n_clicks"),
    State("modal-microsoft", "is_open"),
)(toggle_modal)

app.callback(
    Output("modal-netflix", "is_open"),
    Input("open-netflix", "n_clicks"),
    State("modal-netflix", "is_open"),
)(toggle_modal)
if __name__ == '__main__':
    app.run_server(debug=True)