from dash import html, dcc
from dash.dependencies import Input, Output
from dash import dash_table
from dash import callback_context
import os
import importlib.util

import pandas as pd

# Get the directory of the current script
current_directory = os.path.dirname(os.path.realpath(__file__))

module_path = os.path.join(current_directory, "sqlConnect.py")
spec = importlib.util.spec_from_file_location("sqlConnect", module_path)
sqlConnect = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sqlConnect)

btn4_content = html.Div([
    html.H2('Position'),
    dcc.RadioItems(
        id='input-name',
        options=[
            {'label': 'Create', 'value': 'create'},
            {'label': 'display', 'value': 'display'}
        ],
        value='create',
        labelStyle={'display': 'block'},
        style={
            'display': 'flex',
            'padding': '10px'
        }
    ),
    html.Div(id='position',),
    html.Div(id='position_out',),

])

form = html.Div([
    html.H1("Position Information Form"),
    html.Label('Title'),
    dcc.Input(type='text', id='title', style={
              'margin-bottom': '10px', 'width': '100%'}),

    html.Label('Description'),
    dcc.Input(type='text', id='description', style={
              'margin-bottom': '10px', 'width': '100%'}),

    html.Label('Is Vacant'),
    dcc.Dropdown(
        id='is_vacant',
        options=[
            {'label': 'Yes', 'value': 'True'},
            {'label': 'No', 'value': 'False'}
        ],
        value='True',
        style={'width': '100%'}
    ),

    html.Button('Submit', id='submit-val', n_clicks=0,
                style={'margin-top': '10px', 'width': '100%'}),
], style={'width': '50%', 'margin': 'auto', 'padding': '20px', 'border': '1px solid #ccc'})


def position_callbacks(app):
    @app.callback(Output('position', 'children'),
                  [Input('input-name', 'value')])
    def display_page(pathname):
        if pathname == 'create':
            return form
        elif pathname == 'display':
            mydb, cursor = sqlConnect.connect()
            cursor.execute("SELECT * FROM positions")
            myresult = cursor.fetchall()
            myresult = pd.DataFrame(
                myresult, columns=['position_id', 'title', 'description', 'is_vacant'])
            table = dash_table.DataTable(
                id='table',
                columns=[{"name": i, "id": i} for i in myresult.columns],
                data=myresult.to_dict('records'),
                style_cell={'textAlign': 'left'},
                style_header={
                    'backgroundColor': 'white',
                    'fontWeight': 'bold'
                },
                style_data_conditional=[
                    {
                        'if': {'row_index': 'odd'},
                        'backgroundColor': 'rgb(248, 248, 248)'
                    }
                ]
            )
            sqlConnect.commit(mydb)
            return table


def position_submit(app):
    @app.callback(
        Output('position_out', 'children'),
        [Input('submit-val', 'n_clicks')],
        [Input('title', 'value'),
            Input('description', 'value'),
            Input('is_vacant', 'value')])
    def update_output(n_clicks, title, description, is_vacant):
        ctx = callback_context
        if ctx.triggered[0]['prop_id'] == 'submit-val.n_clicks':
            try:
                mydb, cursor = sqlConnect.connect()
                cursor.execute(
                    "INSERT INTO positions (title, description, is_vacant) VALUES (%s, %s, %s)",
                    (title, description, 1 if is_vacant else 0)
                )
                sqlConnect.commit(mydb)
                return "Position added successfully"
            except Exception as e:
                return f'Error adding position {e}'
