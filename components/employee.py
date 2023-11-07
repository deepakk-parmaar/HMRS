from dash import html, dcc
from dash.dependencies import Input, Output
from dash import dash_table
from dash import callback_context
import pandas as pd
import os
import importlib.util

# Get the directory of the current script
current_directory = os.path.dirname(os.path.realpath(__file__))

module_path = os.path.join(current_directory, "sqlConnect.py")
spec = importlib.util.spec_from_file_location("sqlConnect", module_path)
sqlConnect = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sqlConnect)

form_employee = html.Div(id='form_employee',
                         children=[
                            html.H1("Employee Information Form"),
                             html.Div([
                                 html.Label('First Name'),
                                 dcc.Input(type='text', id='first_name', style={
                                     'margin-bottom': '10px', 'width': '100%'}),

                                 html.Label('Last Name'),
                                 dcc.Input(type='text', id='last_name', style={
                                     'margin-bottom': '10px', 'width': '100%'}),

                                 html.Label('Date of Birth'),
                                 dcc.DatePickerSingle(id='date_of_birth', date='1970-01-01',
                                                      style={'margin-bottom': '10px', 'width': '100%'}),

                                 html.Label('Gender'),
                                 dcc.Input(type='text', id='gender', style={
                                     'margin-bottom': '10px', 'width': '100%'}),

                                 html.Label('Email'),
                                 dcc.Input(type='email', id='email', style={
                                     'margin-bottom': '10px', 'width': '100%'}),

                                 html.Label('Hire Date'),
                                 dcc.DatePickerSingle(id='hire_date', date='1970-01-01',
                                                      style={'margin-bottom': '10px', 'width': '100%'}),

                                 html.Label('Position ID'),
                                 dcc.Input(type='number', id='position_id', style={
                                     'margin-bottom': '10px', 'width': '100%'}),

                                 html.Label('Department ID'),
                                 dcc.Input(type='number', id='department_id', style={
                                     'margin-bottom': '10px', 'width': '100%'}),

                                 html.Label('Manager ID'),
                                 dcc.Input(type='number', id='manager_id', style={
                                     'margin-bottom': '10px', 'width': '100%'}),

                                 html.Button('Submit', id='submit-val', n_clicks=0,
                                             style={'margin-top': '10px', 'width': '100%'}),
                             ], style={'width': '50%', 'margin': 'auto', 'padding': '20px', 'border': '1px solid #ccc'})
                         ])

btn2_content = html.Div([
    html.Div([
        html.H2('Employee'),
        dcc.RadioItems(
            id='input-name',
            options=[
                {'label': 'Create', 'value': 'create'},
                {'label': 'Display', 'value': 'display'},
                # {'label': 'Delete', 'value': 'delete'}
            ],
            value='create',
            labelStyle={'display': 'block'},
            style={
                'display': 'flex',
                'padding': '10px'
            }
        ),
    ]),
    html.Div(id='employee'),
    html.Div(id='employee_out'),
    html.Div(id='employee_update'),
    html.Div(id='employee_delete'),

])


def employee_form_callbacks(app):
    @app.callback(Output('employee', 'children'), [Input('input-name', 'value')])
    def display_page(pathname):
        if pathname == 'create':
            return form_employee
        elif pathname == 'display':
            sqlConnect.mycursor.execute(
                "SELECT employee_id,first_name, last_name, date_of_birth, gender, email, hire_date, position_id, department_id, supervisor_id FROM employees")
            data = sqlConnect.mycursor.fetchall()
            df = pd.DataFrame(data, columns=['employee_id', 'first_name', 'last_name', 'date_of_birth',
                              'gender', 'email', 'hire_date', 'position_id', 'department_id', 'supervisor_id'])

            table = dash_table.DataTable(
                id='table',
                columns=[{"name": i, "id": i, 'editable': True, }
                         for i in df.columns],
                data=df.to_dict('records'),
                style_cell={'textAlign': 'left'},
                style_header={
                    'backgroundColor': 'white',
                    'fontWeight': 'bold'
                },
                row_selectable='single',  # Allows single row selection
                selected_rows=[],  # Initialize selected_rows
            )
            return html.Div([table, html.Button('Delete Selected', id='delete-button', n_clicks=0, style={'margin-top': '10px', 'width': '100%'})])


def employee_submit(app):
    @app.callback(Output('employee_out', 'children'),
                  Input('submit-val', 'n_clicks'),
                  [
        Input('first_name', 'value'),
        Input('last_name', 'value'),
        Input('date_of_birth', 'date'),
        Input('gender', 'value'),
        Input('email', 'value'),
        Input('hire_date', 'date'),
        Input('position_id', 'value'),
        Input('department_id', 'value'),
        Input('manager_id', 'value')
    ])
    def display(n_clicks, first_name, last_name, dob, gender, email, hire_date, position_id, department_id, manager_id):
        ctx = callback_context
        if ctx.triggered[0]['prop_id'] == 'submit-val.n_clicks':
            try:
                sqlConnect.mycursor.execute(
                    "INSERT INTO employees (first_name, last_name, date_of_birth, gender, email, hire_date, position_id, department_id, supervisor_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    (first_name, last_name, dob, gender, email,
                     hire_date, position_id, department_id, manager_id)
                )
                sqlConnect.mydb.commit()
                return 'The record was successfully added to the database'
            except Exception as e:
                return f'Error: {str(e)}'


def employee_update(app):
    @app.callback(
        Output('employee_update', 'children'),
        [Input('table', 'data_previous'), Input('table', 'data')]
    )
    def update_database(data_previous, data):
        ctx = callback_context
        if not ctx.triggered:
            return ''
        trigger = ctx.triggered[0]['prop_id'].split('.')[0]
        if trigger == 'table' and data_previous is not data and data_previous is not None and data is not None:
            try:
                for i, row in enumerate(data):
                    # Assuming 'employee_id' is in the table data
                    employee_id = row['employee_id']

                    for column, new_value in row.items():
                        old_value = data_previous[i][column]

                        # Check if the value has changed
                        if new_value != old_value and column != 'employee_id':
                            if column in ['position_id', 'department_id', 'supervisor_id']:
                                # Update foreign key columns
                                sqlConnect.mycursor.execute(
                                    f"UPDATE employees SET {column} = %s WHERE employee_id = %s",
                                    (new_value, employee_id)
                                )
                            else:
                                # Update other columns
                                sqlConnect.mycursor.execute(
                                    f"UPDATE employees SET {column} = %s WHERE employee_id = %s",
                                    (new_value, employee_id)
                                )
                            sqlConnect.mydb.commit()

                return 'Database updated successfully.'
            except Exception as e:
                return f'Error updating database: {e}'
        else:
            return ''  # No changes


def employee_display_delete(app):
    @app.callback(
        Output('employee_delete', 'children'),
        Input('delete-button', 'n_clicks'),
        Input('table', 'selected_rows'),
    )
    def delete_record(n_clicks, selected_rows):
        ctx = callback_context
        if not ctx.triggered:
            return ''
        trigger = ctx.triggered[0]['prop_id'].split('.')[0]
        if trigger == 'delete-button' and n_clicks is not None and n_clicks > 0:
            if selected_rows:
                if selected_rows[0] is not None:
                    # print(selected_rows)
                    try:
                        sqlConnect.mycursor.execute(
                            "DELETE FROM employees WHERE employee_id = %s", (selected_rows[0]+1,))
                        sqlConnect.mydb.commit()
                        return 'The record was successfully deleted from the database'
                    except Exception as e:
                        return f'Error deleting employee record: {e}'
            else:
                return 'Please select one or more records to delete.'
        return ''
