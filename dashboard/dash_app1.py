# -*- coding: utf-8 -*-
"""
Created on Sun Jul  8 10:39:33 2018
@author: jimmybow
"""
import io
import base64
import datetime
import dash_table
import numpy as np
import pandas as pd
from dash import Dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, State, Output
import dash_bootstrap_components as dbc

url_base = '/dash/app1/'

# layout = html.Div([
#     html.Div('This is dash app1'), html.Br(),
#     dcc.Input(id='input_text'), html.Br(), html.Br(),
#     html.Div(id='target')
# ])

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}


def add_dash(server):
    body = html.Div(
        [
            dbc.Row(
                [
                    dbc.Col([
                        dcc.Upload(
                                id='upload-data',
                                children=html.Div([
                                    'Drag and Drop or ',
                                    html.A('Select Files')
                                ]),
                                style={
                                    'width': '100%',
                                    'height': '60px',
                                    'lineHeight': '60px',
                                    'borderWidth': '1px',
                                    'borderStyle': 'dashed',
                                    'borderRadius': '5px',
                                    'textAlign': 'center',
                                    'margin': '10px'
                                },
                                # Allow multiple files to be uploaded
                                multiple=True
                            ),

                        ],
                        md=12,
                    ),

                ]
            ),
            dbc.Row(
                [
                    dbc.Col([
                        html.Div(id='output-data-upload'),

                    ],
                        md=12,
                    ),

                ]
            )
        ],
    )

    external_stylesheets = [dbc.themes.BOOTSTRAP]

    app = Dash(server=server, url_base_pathname=url_base, external_stylesheets=external_stylesheets)
    app.layout = html.Div([body])

    def parse_contents(contents, filename, date):
        content_type, content_string = contents.split(',')

        decoded = base64.b64decode(content_string)
        try:
            if 'csv' in filename:
                # Assume that the user uploaded a CSV file
                df = pd.read_csv(
                    io.StringIO(decoded.decode('utf-8')))
            elif 'xls' in filename:
                # Assume that the user uploaded an excel file
                df = pd.read_excel(io.BytesIO(decoded))
        except Exception as e:
            print(e)
            return html.Div([
                'There was an error processing this file.'
            ])

        return html.Div([
            dash_table.DataTable(
                data=df[0:500].to_dict('records'),
                columns=[{'name': i, 'id': i} for i in df.columns]
            ),

            html.Hr(),  # horizontal line

        ])

    @app.callback(Output('output-data-upload', 'children'),
                  [Input('upload-data', 'contents')],
                  [State('upload-data', 'filename'),
                   State('upload-data', 'last_modified')])
    def update_output(list_of_contents, list_of_names, list_of_dates):
        if list_of_contents is not None:
            children = [
                parse_contents(c, n, d) for c, n, d in
                zip(list_of_contents, list_of_names, list_of_dates)]
            return children

    return app.server
