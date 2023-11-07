from dash import html, dcc
from dash.dependencies import Input, Output
from dash import callback_context
from dash import dash_table
import os
import importlib.util

import pandas as pd

current_directory = os.path.dirname(os.path.realpath(__file__))  # Get the directory of the current script

module_path = os.path.join(current_directory, "sqlConnect.py")
spec = importlib.util.spec_from_file_location("sqlConnect", module_path)
sqlConnect = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sqlConnect)

btn5_content = html.Div([   
    html.H2('Attendence'),
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
    
    html.Div(id='attendance',),
    html.Div(id='attendance_out',),

    ])

form = html.Div([
    html.H1("Attendance Information Form"),
    html.Div([
        html.Label('Employee ID'),
        dcc.Input(type='number', id='employee_id', style={'margin-bottom': '10px', 'width': '100%'}),

        html.Label('Date'),
        dcc.DatePickerSingle(id='date',date='1970-01-01', style={'margin-bottom': '10px', 'width': '100%'}),

        html.Label('Is Present'),
        dcc.Dropdown(
            id='is_present',
            options=[
                {'label': 'True', 'value': 'True'},
                {'label': 'False', 'value': 'False'}
            ],
            value='True',
            style={'width': '100%'}
        ),

        html.Button('Submit', id='submit-val', n_clicks=0, style={'margin-top': '10px', 'width': '100%'}),
    ], style={'width': '50%', 'margin': 'auto', 'padding': '20px', 'border': '1px solid #ccc'})
]),

def attendance_callbacks(app):
    @app.callback(Output('attendance', 'children'),
                  [Input('input-name', 'value')])
    def display_page(pathname):
        if pathname == 'create':
            return form
        elif pathname == 'display':
            mydb, cursor = sqlConnect.connect()
            cursor.execute("SELECT * FROM attendance")
            myresult = cursor.fetchall()
            myresult = pd.DataFrame(myresult, columns=['employee_id', 'date', 'is_present'])
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

def attendance_submit(app):
    @app.callback(Output('attendance_out', 'children'),
                  [Input('submit-val', 'n_clicks')],
                  [Input('employee_id', 'value'),
                     Input('date', 'date'),
                     Input('is_present', 'value')])
    def update_output(n_clicks, employee_id, date, is_present):
        ctx = callback_context
        if ctx.triggered[0]['prop_id'] == 'submit-val.n_clicks':
            try:
                mydb, cursor =sqlConnect.connect()
                cursor.execute("INSERT INTO attendance (employee_id, date, is_present) VALUES (%s, %s, %s)", (employee_id, date, 1 if is_present else 0))
                sqlConnect.commit(mydb)
                return html.Div([html.H3('Attendance information added successfully.')])
            except Exception as e:
                return html.Div([html.H3('There was an error updating the table.'), str(e)])