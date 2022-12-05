# -*- coding: utf-8 -*-
"""
Created on Mon Nov 14 20:14:33 2022

@author: Akhilesh
"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from dash import Dash, dcc, html, Input, Output, dash_table, State
import pandas as pd
from plotly.subplots import make_subplots
import dash_daq as daq
import get_live_stock_data
import get_live_news
import get_live_sentiment

import numpy as np

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"

apple_sentiments_ = pd.read_csv("../outputs/Twitter_Microsoft_Sentiments_2015_2019.csv",lineterminator='\n')
apple_sentiments = apple_sentiments_[['date', 'Negative', 'Neutral', 'Positive', 'Sentiment', 'Polarity','Deep_tweet']]
min_polarity = round(min(apple_sentiments["Polarity"]),2)
max_polarity = round(max(apple_sentiments["Polarity"]),2)
apple_sentiments["date"] = pd.to_datetime(apple_sentiments["date"])
apple_sentiments['date'] = pd.to_datetime(apple_sentiments["date"].dt.strftime('%Y-%m-%d'))
apple_sentiments["Negative"] = np.round(apple_sentiments["Negative"],2)
apple_sentiments["Neutral"] = np.round(apple_sentiments["Neutral"],2)
apple_sentiments["Positive"] = np.round(apple_sentiments["Positive"],2)
apple_sentiments["Polarity"] = np.round(apple_sentiments["Polarity"],2)

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
def plot_line(apple_preds):
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
    
def plot_table(table):
    return dash_table.DataTable(
        data = table.to_dict('records'),
        columns=[
            {'name': i, 'id': i} for i in table.columns
        ],
        style_table={
            'height': 500,
            'overflowY': 'scroll',
            'width': 1100
        },
        export_format="csv",

    )
def get_current_price(value, reference):
    fig = go.Figure()
    fig.add_trace(go.Indicator(
        mode = "number+delta",
        value = value,
        number = {'prefix': "$"},
        domain = {'x': [0,0], 'y': [0, 0]},
        delta = {'reference': reference, 'relative': True, 'position' : "top", 'valueformat':'.3f'},
        ))
    fig.update_layout(height = 265)
    return fig


apple_current_price, apple_prev_price = get_live_stock_data.get_latest_stock_data("AAPL")
print(apple_current_price, apple_prev_price)
#
try:
    apple_latest_news = get_live_news.get_latest_news("AAPL")    
except:
    apple_latest_news = "Apple Falls on China Fears, but This Nasdaq Stock Is Soaring Monday"
apple_sent_dict, apple_sentiment_compound = get_live_sentiment.get_compound(apple_latest_news)
apple_sentiment = get_live_sentiment.get_sent_score(apple_sent_dict)
toast_apple_current_market = dbc.Toast([
        html.Img(src="/static/images/apple_logo.jpg", height="50px"),    
        html.Div([
            dcc.Graph(figure = get_current_price(apple_current_price, apple_prev_price))
        ]),
        
        dbc.Toast([
            html.H6(apple_latest_news),                
        ], header = "Current News")     ,   
        html.Br(),
        html.H5("Market Sentiment - %s"%apple_sentiment),
        daq.Gauge(
            color={"gradient":True,"ranges":{"green":[2,10],"yellow":[-2, 2],"red":[-10, -2]}},
            value=apple_sentiment_compound*10,            
            max=10,
            min=-10,
        )
    ], header = "Apple Current Price", icon = 'src="/static/images/apple_logo.jpg"')

microsoft_current_price, microsoft_prev_price = get_live_stock_data.get_latest_stock_data("MSFT")
try:
    microsoft_latest_news = get_live_news.get_latest_news("MSFT")
except:
    microsoft_latest_news = "Microsoft Deal, Not Earnings, Is the Focus for Activision Stock"
microsoft_sent_dict, microsoft_sentiment_compound = get_live_sentiment.get_compound(microsoft_latest_news)
microsoft_sentiment = get_live_sentiment.get_sent_score(microsoft_sent_dict)
toast_microsoft_current_market = dbc.Toast([
        html.Img(src="/static/images/microsoft_log.jpg", height="50px"),    
        html.Div([
            dcc.Graph(figure = get_current_price(microsoft_current_price, microsoft_prev_price))
        ]),

        dbc.Toast([
            html.H6(microsoft_latest_news)
        ], header = "Current News"),
        
        html.Br(),
        html.H5("Market Sentiment - %s"%microsoft_sentiment),
        daq.Gauge(
            color={"gradient":True,"ranges":{"green":[2,10],"yellow":[-2, 2],"red":[-10,-2]}},
            value=microsoft_sentiment_compound*10,            
            max=10,
            min=-10,
        )
    ], header = "Microsoft Current Price", icon = "/static/images/microsoft_log.jpg")

netflix_current_price, netflix_prev_price = get_live_stock_data.get_latest_stock_data("NFLX")
try:
    netflix_latest_news = get_live_news.get_latest_news("NFLX")
except:
    netflix_latest_news = "Netflix Explores Investing in Sports Leagues, Bidding on Streaming Rights"
netflix_sent_dict, netflix_sentiment_compound = get_live_sentiment.get_compound(netflix_latest_news)
netflix_sentiment = get_live_sentiment.get_sent_score(netflix_sent_dict)
toast_netflix_current_market = dbc.Toast([
        html.Img(src="/static/images/netflix-new-logo.png", height="50px"),    
        html.Div([
            dcc.Graph(figure = get_current_price(netflix_current_price, netflix_prev_price))
        ]),
        
        dbc.Toast([
            html.H6(netflix_latest_news),            
        ], header = "Current News"),
                
        html.Br(),
        html.H5("Market Sentiment - %s"%netflix_sentiment),
        daq.Gauge(
            color={"gradient":True,"ranges":{"green":[2,10],"yellow":[-2, 2],"red":[-10,-2]}},
            value=netflix_sentiment_compound*10,            
            max=10,
            min=-10,
        )
    ], header = "Netflix Current Price", icon = "/static/images/netflix-new-logo.png")

amazon_current_price, amazon_prev_price = get_live_stock_data.get_latest_stock_data("AMZN")
try:
    amazon_latest_news = get_live_news.get_latest_news("AMZN")
except:
    amazon_latest_news = "Amazon Stock Is Down Big. Get Ready for a Huge Rally."
amazon_sent_dict, apple_sentiment_compound = get_live_sentiment.get_compound(amazon_latest_news)
amazon_sentiment = get_live_sentiment.get_sent_score(amazon_sent_dict)
toast_amazon_current_market = dbc.Toast([
        html.Img(src="/static/images/amazon_logo.png", height="50px"),    
        html.Div([
            dcc.Graph(figure = get_current_price(amazon_current_price, amazon_prev_price))
        ]),
        
        dbc.Toast([
            html.H6(amazon_latest_news),            
        ], header = "Current News"),
        
        html.Br(),
        html.H5("Market Sentiment - %s"%amazon_sentiment),
        daq.Gauge(
            color={"gradient":True,"ranges":{"green":[2,10],"yellow":[-2, 2],"red":[-10,-2]}},
            value=apple_sentiment_compound*10,            
            max=10,
            min=-10,
        )
    ], header = "Amazon Current Price", icon = "/static/images/amazon_logo.png")


def toggle_modal(n1, is_open):
    if n1:
        return not is_open
    return is_open

def prepare_apple_modal():
    return html.Div([
        dbc.Row([
           dbc.Col([
               dbc.Card([
                   dbc.CardHeader("Stock Predictions"),
                   dbc.CardBody([
                       dcc.Dropdown(
                           options = [
                               {'label':"LSTM Predictions without Sentiments", 'value' : "lstm-basic"},
                               {'label':"LSTM Predictions with one feature - Polarity", 'value' : "lstm-one-feat"},
                               {'label':"LSTM Prediction with multi features", 'value' : "lstm-multi-feat"}    
                           ],
                           value = "lstm-basic",
                           id = "lstm-pred"
                       ),
                       dcc.Graph(id = "predictions-output")
                   ])
               ])
               ]),
        ]),
        dbc.Row([
        
            dbc.Card([
                dbc.CardHeader("Sentiment Data"),
                dbc.CardBody([
                    html.P("Select Sentiment Value"),
                    dcc.RangeSlider(min_polarity, max_polarity, 0.1, value=[-0.2, 0.4], id='my-range-slider'),                        
                    html.P("Sentiment Table"),
                    html.Div(id = "sentiment-table")                        
                    
                    
                ])
            ])    
            
        ])
    ])
app.layout = html.Div([     
        dbc.Row([            
            navbar                
        ]),
        dbc.Row([
            dbc.Col([
                toast_microsoft_current_market          ,      
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
                toast_apple_current_market,
                dbc.Button("Click for detailed analysis", color = "danger",id="open-microsoft", n_clicks=0, style = {"width":"350px"}),
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
                dbc.Button("Click for detailed analysis", color = "warning",id="open-netflix", n_clicks=0, style = {"width":"350px"}),
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

@app.callback(
    Output("predictions-output", "figure"),
    Input("lstm-pred", "value")    
)
def return_pred_graph(input_val):
    if input_val == "lstm-basic":
        apple_preds = pd.read_csv("../outputs/LSTM_Outputs_Basic.csv")
    elif input_val == "lstm-one-feat":
        apple_preds = pd.read_csv("../outputs/LSTM_Outputs_One_Feat.csv")
    else:
        apple_preds = pd.read_csv("../outputs/LSTM_Outputs_Multi_Feat.csv")
    figure = plot_line(apple_preds)
    return figure

@app.callback(
    Output("sentiment-table", "children"),
    Input("my-range-slider", "value")    
)
def return_sentiment_table(value):
    low = value[0]
    high = value[1]
    table_to_plot = apple_sentiments[(apple_sentiments["Polarity"] > low) & (apple_sentiments["Polarity"] < high)]
    dt = plot_table(table_to_plot)
    return dt
if __name__ == '__main__':
    app.run_server(debug=True)