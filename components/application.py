from dash import html, dcc
from dash.dependencies import Input, Output
from dash import callback_context
from dash import dash_table
from dash import dash_table
import os
import importlib.util

import pandas as pd

current_directory = os.path.dirname(os.path.realpath(__file__))  # Get the directory of the current script

module_path = os.path.join(current_directory, "sqlConnect.py")
spec = importlib.util.spec_from_file_location("sqlConnect", module_path)
sqlConnect = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sqlConnect)

btn8_content = html.Div([   
    html.H2('Application'),
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
    html.Div(id='application',),
    html.Div(id='application_out',),

    ])
form  = html.Div([
    html.H1("Application Form"),
    html.Div([
        html.Label('Position ID'),
        dcc.Input(type='number', id='position_id2', style={'margin-bottom': '10px', 'width': '100%'}),

        html.Label('Employee ID'),
        dcc.Input(type='number', id='employee_id4', style={'margin-bottom': '10px', 'width': '100%'}),

        html.Label('Status'),
        dcc.Input(type='text', id='status', style={'margin-bottom': '10px', 'width': '100%'}),

        html.Button('Submit', id='submit-val', n_clicks=0, style={'margin-top': '10px', 'width': '100%'}),
    ], style={'width': '50%', 'margin': 'auto', 'padding': '20px', 'border': '1px solid #ccc'})
]),

def application_callbacks(app):
    @app.callback(Output('application', 'children'),
                  [Input('input-name', 'value')])
    def display_page(pathname):
        if pathname == 'create':
            return form
        elif pathname == 'display':
            sqlConnect.mycursor.execute("SELECT * FROM applications")
            myresult = sqlConnect.mycursor.fetchall()
            myresult = pd.DataFrame(myresult, columns=['application_id','position_id', 'employee_id', 'status'])
            table = dash_table.DataTable(
                id='table',
                columns=[{"name": i, "id": i} for i in myresult.columns],
                data=myresult.to_dict('records'),
                style_cell={'textAlign': 'left'},
                style_header={
                    'backgroundColor': 'white',
                    'fontWeight': 'bold'
                },
                style_data_conditional=[{
                    'if': {'row_index': 'odd'},
                    'backgroundColor': 'rgb(248, 248, 248)'
                }],
            )
            return table
        
def application_submit(app):
    @app.callback(Output('application_out', 'children'),
                  [Input('submit-val', 'n_clicks')],
                  [Input('position_id2', 'value')],
                    [Input('employee_id4', 'value')],
                    [Input('status', 'value')])
    def update_output(n_clicks, position_id, employee_id, status):
        ctx = callback_context
        if ctx.triggered[0]['prop_id'] == 'submit-val.n_clicks':
            try:
                sqlConnect.mycursor.execute("INSERT INTO applications (position_id, employee_id, status) VALUES (%s, %s, %s)", (position_id, employee_id, status))
                sqlConnect.mydb.commit()
                return "Application Submitted"
            except Exception as e:
                return str(e)   