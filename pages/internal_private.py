from dash import Dash, html, dcc, callback, Output, Input, State, ctx, no_update
import dash_mantine_components as dmc
from datetime import datetime
import dash_ag_grid as dag
import pandas as pd
import dash
from flask_login import login_required


dash.register_page(__name__)
layout = html.Div([
    dcc.Location(id='url-private', refresh=False),
    html.H1('Private internal'),
    dcc.Input(id='password-input', type='password', placeholder='Enter password'),
    html.Div(id='private-content')
])

@login_required
@dash.callback(Output('private-content', 'children'),
               Input('password-input',component_property='value')
               )
def display_private_content(password):
    if password=='topsecret':
        return "Well done, you can access the private page"
    else:
        return "To get access to this page, you need to enter a valid password!"


