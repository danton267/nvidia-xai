import dash
from dash import Input, Output, html, dcc
import plotly.express as px

dash.register_page(__name__, path="/data-exploration")


def layout():
    layout = html.Div()

    return layout
