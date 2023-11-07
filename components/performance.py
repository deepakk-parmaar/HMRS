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

btn7_content = html.Div([
    html.H2('Performance'),
    dcc.RadioItems(
        id='input-name',
        options=[
            {'label': 'Add', 'value': 'create'},
            {'label': 'Display', 'value': 'display'}
        ],
        value='create',
        labelStyle={'display': 'block'},
        style={
            'display': 'flex',
            'padding': '10px'
        }
    ),

    html.Div(id='performance',),
    html.Div(id='performance_out',),

])
form = html.Div([
    html.H1("Performance Review Information Form"),
    html.Div([
        html.Label('Review Date'),
        dcc.DatePickerRange(id='review_date', start_date='1970-01-01',
                            end_date='1970-01-01', style={'margin-bottom': '10px', 'width': '100%'}),

        html.Label('Employee ID'),
        dcc.Input(type='number', id='employee_id3', style={
                  'margin-bottom': '10px', 'width': '100%'}),

        html.Label('Rating'),
        dcc.Input(type='number', id='rating', style={
                  'margin-bottom': '10px', 'width': '100%'}),

        html.Label('Comments'),
        dcc.Input(type='text', id='comments', style={
                  'margin-bottom': '10px', 'width': '100%'}),

        html.Button('Submit', id='submit-val', n_clicks=0,
                    style={'margin-top': '10px', 'width': '100%'}),
    ], style={'width': '50%', 'margin': 'auto', 'padding': '20px', 'border': '1px solid #ccc'})
]),


def performance_callbacks(app):
    @app.callback(Output('performance', 'children'),
                  [Input('input-name', 'value')])
    def display_page(pathname):
        if pathname == 'create':
            return form
        elif pathname == 'display':
            sqlConnect.mycursor.execute("SELECT * FROM performance_reviews")
            data = sqlConnect.mycursor.fetchall()
            myresult = pd.DataFrame(data , columns=[
                                    'review_id', 'review_date', 'employee_id', 'rating', 'comments'])
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

def performance_submit(app):
    @app.callback(Output('performance_out', 'children'),
                    [Input('submit-val', 'n_clicks')],
                    [Input('review_date', 'start_date')],
                    [Input('review_date', 'end_date')],
                    [Input('employee_id3', 'value')],
                    [Input('rating', 'value')],
                    [Input('comments', 'value')])
    def update_output(n_clicks, start_date, end_date, employee_id3, rating, comments):
        ctx = callback_context
        if ctx.triggered[0]['prop_id'] == 'submit-val.n_clicks':
            try:
                sqlConnect.mycursor.execute("INSERT INTO performance_reviews (review_date, employee_id, rating, comments) VALUES (%s, %s, %s, %s)", (start_date, employee_id3, rating, comments))
                sqlConnect.mydb.commit()
                return 'Success'
            except Exception as e:
                print(e)
                return 'Error'
