# This page needs to be built out
import dash
from dash import html, dcc, Input, Output
import dash_mantine_components as dmc

dash.register_page(__name__,path='/')

layout = html.Div([
    dmc.Header(
        height=60, children=[dmc.Text("VOST response reporting")], style={"backgroundColor": "#9c86e2"}
    )

])