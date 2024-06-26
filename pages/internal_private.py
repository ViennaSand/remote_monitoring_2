from dash import Dash, html, dcc, callback, Output, Input, State, ctx, no_update
import dash_mantine_components as dmc
from datetime import datetime
import dash_ag_grid as dag
import pandas as pd
import dash
from flask_login import login_required


#dash.register_page(__name__)



df = pd.read_csv("https://raw.githubusercontent.com/Coding-with-Adam/response-reporting-dashboard/main/pages/reports.csv")
df["response-day"] = pd.to_datetime(df["response-day"]).dt.strftime('%Y-%m-%d')
df["flag-day"] = pd.to_datetime(df["flag-day"]).dt.strftime('%Y-%m-%d')


cols = [
    {
        "headerName": "User",
        "field": "vetted-user",
        "cellEditor": "agSelectCellEditor",
        "cellEditorParams": {"values": df["vetted-user"].unique()}
    },
    {
        "headerName": "Platform",
        "field": "platform",
        "cellEditor": "agSelectCellEditor",
        "cellEditorParams": {"values": df["platform"].unique()}
    },
    {
        "headerName": "Content link",
        "field": "content-link",
    },
    {
        "headerName": "Flag type",
        "field": "flag-type",
        "cellEditor": "agSelectCellEditor",
        "cellEditorParams": {"values": df["flag-type"].unique()}
    },
    {
        "headerName": "Flag day",
        "field": "flag-day",
        "filter": "agDateColumnFilter",
        'cellEditor': 'agDateStringCellEditor',
        'cellEditorParams': {'min': '2024-01-01'}
    },
    {
        "headerName": "Response type",
        "field": "response-type",
        "cellEditor": "agSelectCellEditor",
        "cellEditorParams": {"values": df["response-type"].unique()}
    },
    {
        "headerName": "Response notes",
        "field": "response-notes",
    },
    {
        "headerName": "Response day",
        "field": "response-day",
        "filter": "agDateColumnFilter",
        'cellEditor': 'agDateStringCellEditor',
        'cellEditorParams': {
            'min': '2024-01-01',
        }
    }
]





layout = html.Div([
    dcc.Location(id='url-private', refresh=False),
    html.H1('Private - editable table'),
    dcc.Input(id='password-input', type='password', placeholder='Enter password'),
    dmc.MantineProvider(
        id='private-content',
        theme={"colorScheme": "dark"},
        withGlobalStyles=True,
        children=[
            html.H1("Transparency Reporting Platform - Internal"),
            #dmc.Center(html.H4('This page content to be visible after vetted user has logged in.')),
            dag.AgGrid(
                id="reports-table",
                rowData=df.to_dict("records"),
                columnDefs=cols,
                columnSize="sizeToFit",
                defaultColDef={"editable": True, "filter": True},
                dashGridOptions={"pagination": True,
                                 "paginationPageSize": 7,
                                 "undoRedoCellEditing": True,
                                 "rowSelection": "multiple"}
            ),
            dmc.Button(
                id="delete-row-btn",
                children="Delete row",
            ),
            dmc.Button(
                id="add-row-btn",
                children="Add row",
            ),
        ]
    )
])

@login_required
@dash.callback(Output('private-content', 'reports-table'),
                    #Output("reports-table", "rowData",allow_duplicate=True),
               Input('password-input',component_property='value'),
               allow_duplicate=True
               )
def display_private_content(password):
    if password=='topsecret':
        return dag.AgGrid(
            rowData=df.to_dict("records"),
            columnDefs=[{"field": i} for i in df.columns],
            columnSize="sizeToFit",
            defaultColDef={"filter": True},
            dashGridOptions={"pagination": True, "paginationPageSize":7},
        )
    else:
        return "To get access to this page, you need to enter a valid password!"


"""
@dash.callback(
    Output("reports-table", "deleteSelectedRows",allow_duplicate=True),
    Output("reports-table", "rowData",allow_duplicate=True),
    Input("delete-row-btn", "n_clicks"),
    Input("add-row-btn", "n_clicks"),
    State("reports-table", "rowData"),
    prevent_initial_call=True,
)
def update_table(n_dlt, n_add, data):
    if ctx.triggered_id == "add-row-btn":
        new_row = {
            "vetted-user": ["user1"],
            "platform": [""],
            "content-link": [""],
            "image-link": [""],
            "report-type": [""],
            "report-time": [""],
            "response-type": [""],
            "response-notes": [""],
            "response-time": [""]
        }
        df_new_row = pd.DataFrame(new_row)
        updated_table = pd.concat(
            [pd.DataFrame(data), df_new_row]
        )  # add new row to orginal dataframe
        return False, updated_table.to_dict("records")

    elif ctx.triggered_id == "delete-row-btn":
        return True, no_update
"""

