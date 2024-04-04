from dash import Dash, html, dcc, callback, Output, Input, State, ctx, no_update
import dash_mantine_components as dmc
from datetime import datetime
import dash_ag_grid as dag
import pandas as pd
import dash
import dash_auth



dash.register_page(__name__)

#
layout = dmc.MantineProvider(
        theme={"colorScheme": "dark"},
        withGlobalStyles=True,
        children=[
        html.H1("Transparency Reporting Platform - Internal"),
        dmc.Center(html.H4('This page content to be visible after vetted user has logged in.')),
    ]
)


