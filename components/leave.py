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

btn6_content = html.Div([
    html.H2('Leave'),
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

    html.Div(id='leave',),
    html.Div(id='leave_out',),

])

form = html.Div([
    html.H1("Employee Leave Information Form"),
    html.Div([
        html.Label('Attendance'),
        dcc.Input(type='text', id='attendance', style={
                  'margin-bottom': '10px', 'width': '100%'}),

        html.Label('Employee ID'),
        dcc.Input(type='text', id='employee_id2', style={'margin-bottom': '10px', 'width': '100%'}),

        html.Label('Start Date'),
        dcc.DatePickerSingle(id='start_date', date='1970-01-01',
                             style={'margin-bottom': '10px', 'width': '100%'}),

        html.Label('End Date'),
        dcc.DatePickerSingle(id='end_date', date='1970-01-01',
                             style={'margin-bottom': '10px', 'width': '100%'}),

        html.Button('Submit', id='submit-val', n_clicks=0,
                    style={'margin-top': '10px', 'width': '100%'}),
    ], style={'width': '50%', 'margin': 'auto', 'padding': '20px', 'border': '1px solid #ccc'})
]),


def leave_callbacks(app):
    @app.callback(Output('leave', 'children'),
                  [Input('input-name', 'value')])
    def display_page(pathname):
        if pathname == 'create':
            return form
        elif pathname == 'display':
            sqlConnect.mycursor.execute("SELECT * FROM employee_leaves")
            myresult = sqlConnect.mycursor.fetchall()
            myresult = pd.DataFrame(myresult, columns=[
                                    'leave_id', 'Attendance', 'employee_id', 'start_date', 'end_date'])
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


def leave_submit(app):
    @app.callback(Output('leave_out', 'children'),
                    [Input('submit-val', 'n_clicks')],
                    [Input('attendance', 'value'),
                     Input('employee_id2', 'value'),
                     Input('start_date', 'date'),
                     Input('end_date', 'date')])
    def update_output(n_clicks, attendance, employee_id2, start_date, end_date):
        ctx = callback_context
        if ctx.triggered:
            button_id = ctx.triggered[0]['prop_id'].split('.')[0]
            if button_id == 'submit-val':
                try:
                    # print(f"Attendance: {attendance}, Employee ID: {employee_id2}, Start Date: {start_date}, End Date: {end_date}")
                    sqlConnect.mycursor.execute("INSERT INTO employee_leaves (Attendance, employee_id, start_date, end_date) VALUES (%s, %s, %s, %s)", (attendance, employee_id2, start_date, end_date))
                    sqlConnect.mydb.commit()
                    return html.Div([
                        html.H3('Leave Submitted'),
                    ])
                except Exception as e:
                    return html.Div([
                        html.H3('Error: ' + str(e)),
                        html.H3("INSERT INTO employee_leaves (Attendance, employee_id, start_date, end_date) VALUES (%s, %s, %s, %s)", (attendance, employee_id2, start_date, end_date)),
                    ])