from dash import Dash, html, dcc, callback, Output, Input, State, ctx, no_update
import dash_mantine_components as dmc
from datetime import datetime
import dash_ag_grid as dag
import pandas as pd
import dash
from dash_auth import public_callback
from flask import render_template, redirect, url_for, flash
from flask_login import login_required


dash.register_page(__name__)

dic_users = {'bugsbunny':'topsecret'}

user_name = dmc.TextInput(id='user_name',label="User Name:", placeholder="Your User Name",style={"width": 250})

password = dmc.PasswordInput(
    id = 'password',
    label="Your password:",
    style={"width": 250},
    placeholder="Your password")

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

updatable_table = dag.AgGrid(
                id="reports-table",
                rowData=df.to_dict("records"),
                columnDefs=cols,
                columnSize="sizeToFit",
                defaultColDef={"editable": True, "filter": True},
                dashGridOptions={"pagination": True,
                                 "paginationPageSize": 7,
                                 "undoRedoCellEditing": True,
                                 "rowSelection": "multiple"}
            )

delete_row = dmc.Button(
                id="delete-row-btn",
                children="Delete row",
            )

add_row = dmc.Button(
                id="add-row-btn",
                children="Add row",
            )



layout = html.Div(
    [
        dmc.Tabs(
            [
                dmc.TabsList(
                    [
                        dmc.Tab("Login", value="login"),
                        dmc.Tab("Update Dashboard" ,id = "private_tab",  value="internal",disabled=True),
                    ]
                ),
            ],
            id="tabs-example",
            value="login",
        ),
        html.Div(id="tabs-content", style={"paddingTop": 10}),
    ]
)


@callback(Output("tabs-content", "children"), Input("tabs-example", "value"))
def render_content(active):
    if active == "login":
        return [dmc.Text("Please login to get access to the editable dashboard:"),user_name,password]
    else:
        return [updatable_table,delete_row,add_row]
@callback(Output("private_tab", "disabled"),
          Input("user_name", "value"),
          Input("password", "value")
          )
def update_tabs(user_name,password):
    if (user_name,password) in dic_users.items():
        return False
    else:
        #print("the pair user/password does not exist")
        return True




@callback(
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

