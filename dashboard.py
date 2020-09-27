import dash
import dash_core_components as dcc 	#This library will give us the dashboard elements (pie charts, scatter plots, bar graphs etc)
import dash_html_components as html 	#This library allows us to arrange the elements from dcc in a page as is done using html/css (how the internet generally does it)
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
from WindModel import df1
from SolarModel import df2

def get_dash(server):
    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
    app = dash.Dash(__name__, 
                    server=server,
                    routes_pathname_prefix='/dashapp/',
                    external_stylesheets=external_stylesheets
                    )

    #df = get_data()

    styles = get_styles()

    fig={'data': [{'x': df1['Date'], 'y': df1['PowerOutput_Wind'], 'type': 'bar', 'name': 'Wind_PredictedPowerOutput'},{'x': df2['Date'], 'y': df2['PowerOutput_Solar'], 'type': 'bar', 'name': 'Solar_PredictedPowerOutput'},
                    ],'layout': {'title': 'Solar and Wind Power Output Five Day Predictions'}}

    app.layout = html.Div([
        # html.H6("Change the value in the text box to see callbacks in action!"),
        html.A("Go to Home Page", href="/", style=styles["button_styles"]),
        html.Div("Welcome to the Power Output Prediction Dashboard", id='my-output',
                 style=styles["text_styles"]),
        html.Div(
            dcc.Graph(
                id='example-graph',
                figure=fig
            ),
            style=styles["fig_style"]
        )
    ])

    return app

def get_styles():
    
    base_styles = {
        "text-align": "center",
        "border": "1px solid #ddd",
        "padding": "7px",
        "border-radius": "2px",
    }
    text_styles = {
        "background-color": "#eee",
        "margin": "auto",
        "width": "50%"
    }
    text_styles.update(base_styles)

    button_styles = {
        "text-decoration": "none",
    }
    button_styles.update(base_styles)

    fig_style = {
        "padding": "10px",
        "width": "80%",
        "margin": "auto",
        "margin-top": "5px"
    }
    fig_style.update(base_styles)
    return {
        "text_styles" : text_styles,
        "base_styles" : base_styles,
        "button_styles" : button_styles,
        "fig_style": fig_style,
    }

