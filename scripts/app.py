# -*- coding: utf-8 -*-
"""
Created on Fri Nov 11 17:44:23 2022

@author: Akhilesh
"""

import pandas as pd
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from dash import Dash, dcc, html, Input, Output, dash_table
import pandas as pd
from plotly.subplots import make_subplots


import numpy as np

PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"

apple_preds = pd.read_excel("../data/predictions/AAPL/predictions.xlsx")
apple_sentiments = pd.read_csv("../data/Predictions/AAPL/sentiment_out.csv")

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

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
navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=PLOTLY_LOGO, height="30px")),
                        dbc.Col(dbc.NavbarBrand("STOCKBUFF", className="ms-2")),
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

button_bar = dbc.Row([
    dbc.Col([
        dbc.Card([            
            dbc.CardBody([
                dbc.CardImg(src="/static/images/apple_logo.jpg", top=True, style = {"width":"80px","height":"35px"}),
                dbc.Button("Apple", color = "dark", id = "apple", style = {"width":"160px"})
                ])
        ], color = "light")    
    ]),
    dbc.Col([
        dbc.Card([            
            dbc.CardBody([
                dbc.CardImg(src="/static/images/netflix-new-logo.png", top=True, style = {"width":"80px","height":"35px"}),
                dbc.Button("Netflix", color = "dark", id = "netflix", style = {"width":"160px"}),
                
            ])
        ],color = "light")  
    ]),
    dbc.Col([
        dbc.Card([            
            dbc.CardBody([
                dbc.CardImg(src="/static/images/microsoft_log.jpg", top=True, style = {"width":"80px","height":"35px"}),
                dbc.Button("Microsoft", color = "dark", id = "microsoft", style = {"width":"160px"}),
                
            ])
        ],color = "light")  
    ]),
    dbc.Col([
        dbc.Card([            
            dbc.CardBody([
                dbc.CardImg(src="/static/images/amazon_logo.png", top=True, style = {"width":"80px","height":"35px"}),
                dbc.Button("Amazon", color = "dark", id = "amazon", style = {"width":"160px"}),
                
            ])
        ], color = "light")  
    ]),
    
    dbc.Col([
        dbc.Card([
             
            dbc.CardHeader("Include Sentiment?"),
            dbc.CardBody([                
                dbc.Checklist(
                    options=[
                        {"label": "Option 1", "value": 1},
                    ],
                    value=[1],
                    id="switches-input",
                    switch=True,
                ),                                
            ])

        ])
    
    ])
    
])

app.layout = html.Div([
    dbc.Row([
        navbar
    ]),
    dbc.Row([
        button_bar    
    ]),
    dbc.Row([
        
            html.Div(id = "plot_apple")    
        
    ])
    
 ])


@app.callback(Output("plot_apple", "children"),
              [Input("apple", "n_clicks")])
def update_apple_tab(n_clicks):
    fig = plot_line()
    fig1 = plot_pie()
    if n_clicks:        
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
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader("Sentiment Data"),
                        dbc.CardBody(plot_table())
                    ])    
                ]),
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader("Explainable AI"),
                        dbc.CardBody(html.P("HI"))
                    ])
                ])
            ])
        ])
if __name__ == '__main__':
    app.run_server(debug=True)
