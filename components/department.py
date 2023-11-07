from dash import html, dcc
from dash.dependencies import Input, Output
from dash import callback_context
from dash import dash_table
import os
import importlib.util

import pandas as pd

# Get the directory of the current script
current_directory = os.path.dirname(os.path.realpath(__file__))

module_path = os.path.join(current_directory, "sqlConnect.py")
spec = importlib.util.spec_from_file_location("sqlConnect", module_path)
sqlConnect = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sqlConnect)

btn3_content = html.Div([
    html.H2('Department'),
    dcc.RadioItems(
        id='input-name',
        options=[
            {'label': 'Create', 'value': 'create'},
            {'label': 'Display', 'value': 'display'}
        ],
        value='create',
        labelStyle={'display': 'block'},
        style={
            'display': 'flex',
            'padding': '10px'
        }
    ),
    html.Div(id='dept'),
    html.Div(id='dept_out'),

])
form = html.Div([
    html.H1("Department Information Form"),
    html.Div([
        html.Label('Department Name'),
        dcc.Input(type='text', id='department_name', style={
                  'margin-bottom': '10px', 'width': '100%'}),

        html.Label('Location'),
        dcc.Input(type='text', id='location', style={
                  'margin-bottom': '10px', 'width': '100%'}),

        html.Button('Submit', id='submit-val', n_clicks=0,
                    style={'margin-top': '10px', 'width': '100%'}),
    ], style={'width': '50%', 'margin': 'auto', 'padding': '20px', 'border': '1px solid #ccc'})
]),


def department_callbacks(app):
    @app.callback(Output('dept', 'children'),
                  [Input('input-name', 'value')])
    def display_page(pathname):
        if pathname == 'create':
            return form
        elif pathname == 'display':
            sqlConnect.mycursor.execute("SELECT * FROM departments")
            myresult = sqlConnect.mycursor.fetchall()
            myresult = pd.DataFrame(
                myresult, columns=['department_id', 'department_name', 'location'])
            table = dash_table.DataTable(
                id='table',
                columns=[{"name": i, "id": i} for i in myresult.columns],
                data=myresult.to_dict('records'),
                style_cell={'textAlign': 'left'},
                style_header={
                    'backgroundColor': 'white',
                    'fontWeight': 'bold'
                }
            )
            return table


def department_submit(app):
    @app.callback(
        Output('dept_out', 'children'),
        [Input('submit-val', 'n_clicks')],
        [Input('department_name', 'value'),
         Input('location', 'value')])
    def update_output(n_clicks, department_name, location):
        ctx = callback_context
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if button_id == 'submit-val':
            try:
                sqlConnect.mycursor.execute(
                    "INSERT INTO departments (department_name, location) VALUES (%s, %s)", (department_name, location))
                sqlConnect.mydb.commit()
                return 'The record has been created'
            except:
                return f'Error: {str(e)}'
