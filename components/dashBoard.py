from dash import html, dcc, Input, Output
from dash import dash_table
from dash import no_update
from dash import callback_context
from dash.dependencies import State
import pandas as pd
import os
import importlib.util

# Get the directory of the current script
current_directory = os.path.dirname(os.path.realpath(__file__))

module_path = os.path.join(current_directory, "sqlConnect.py")
spec = importlib.util.spec_from_file_location("sqlConnect", module_path)
sqlConnect = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sqlConnect)


buttons = html.Div(
    [
        html.Button("Get Employees By Department", id='btn-dept',
                    style={'margin-bottom': '10px'}),
        html.Button("Avg Dept Rating", id='btn-rating',
                    style={'margin-bottom': '10px'}),
        html.Button("Positions with No Applicants",
                    id='btn-no-applicants', style={'margin-bottom': '10px'}),
        html.Button("Details of Employees for Vacant Positions",
                    id='btn-vacant-details', style={'margin-bottom': '10px'}),
        html.Button("High Performers", id='btn-high-performers',
                    style={'margin-bottom': '10px'}),
        html.Button("Supervisors", id='btn-supervisors',
                    style={'margin-bottom': '10px'}),
        html.Button("Number of Employees per Department",
                    id='btn-employees-per-dept', style={'margin-bottom': '10px'}),
        html.Button("Average Age", id='btn-avg-age',
                    style={'margin-bottom': '10px'}),
    ],
    style={'width': '20%', 'display': 'flex', 'flex-direction': 'column'}
)
content = html.Div([
    html.H2('Welcome to the Dashboard!'),
    html.P('Please enter your name:'),
    dcc.Input(id='name', type='text', value=''),
    html.Div(id='welcome-name'),

], style={'width': '80%', 'padding': '20px'})

btn1_content = html.Div(
    children=[
        content,
        html.Div(
            children=[
                buttons,
                html.Div(
                    id='output-content', style={'width': '80%', 'float': 'left', 'margin': '20px'}),
            ], style={'display': 'flex'})]
)


def dashBoard_callbacks(app):
    @app.callback(
        Output('welcome-name', 'children'),
        [Input('name', 'value')]
    )
    def update_output(name):
        if name is not None and name != '':
            return html.Div([
                html.H3(f'Welcome, {name}!')
            ])
        else:
            return html.Div([
                html.P(f'Welcome!')
            ])


def queries_callback(app):
    @app.callback(
        Output('output-content', 'children'),
        [
            Input('btn-dept', 'n_clicks'),
            Input('btn-rating', 'n_clicks'),
            Input('btn-no-applicants', 'n_clicks'),
            Input('btn-vacant-details', 'n_clicks'),
            Input('btn-high-performers', 'n_clicks'),
            Input('btn-supervisors', 'n_clicks'),
            Input('btn-employees-per-dept', 'n_clicks'),
            Input('btn-avg-age', 'n_clicks')
        ]
    )
    def update_output(
        btn_dept,
        btn_rating,
        btn_no_applicants,
        btn_vacant_details,
        btn_high_performers,
        btn_supervisors,
        btn_employees_per_dept,
        btn_avg_age
    ):
        ctx = callback_context
        if not ctx.triggered:
            return no_update
        else:
            button_id = ctx.triggered[0]['prop_id'].split('.')[0]
            if button_id == 'btn-dept':
                # CALL GetEmployeesByDepartment('Human Resources');
                return html.Div([
                    html.H2('Get Employees By Department'),
                    html.P('Department Name:'),
                    dcc.Input(id='dept-name', type='text',
                              value='Human Resources'),
                    html.Div(id='dept-name-output')
                ])
            elif button_id == 'btn-rating':
                #                 -- Call the avgDepartmentRating function to get the average rating for Department ID 3
                # SELECT avgDepartmentRating(3) AS department_average_rating;
                # #
                return html.Div([
                    html.H2('Average Department Rating'),
                    html.P('Department ID:'),
                    dcc.Input(id='dept-name2', type='text',
                              value='3'),
                    html.Div(id='dept-rating-output')
                ])

            elif button_id == 'btn-no-applicants':
                sqlConnect.mycursor.execute(
                    '''SELECT position_id,title,description FROM positions WHERE position_id NOT IN (SELECT position_id FROM applications);''')
                data = sqlConnect.mycursor.fetchall()
                df = pd.DataFrame(
                    data, columns=['Position ID', 'Title', 'Description'])
                table = dash_table.DataTable(
                    id='table',
                    columns=[{"name": i, "id": i} for i in df.columns],
                    data=df.to_dict('records'),
                    style_cell={'textAlign': 'left'},
                    style_header={
                        'backgroundColor': 'white',
                        'fontWeight': 'bold'
                    }
                )
                if data:
                    return html.Div([
                        html.H2('Positions with No Applicants'),
                        table
                    ])
                else:
                    return html.Div([
                        html.H2('Positions with No Applicants'),
                        html.P('No positions with no applicants found.')
                    ])

            elif button_id == 'btn-vacant-details':
                sqlConnect.mycursor.execute('''SELECT e.first_name, e.last_name, p.title
                                                FROM employees e
                                                JOIN applications a ON e.employee_id = a.employee_id
                                                JOIN positions p ON a.position_id = p.position_id
                                                WHERE p.is_vacant = TRUE;''')
                data = sqlConnect.mycursor.fetchall()
                df = pd.DataFrame(
                    data, columns=['First Name', 'Last Name', 'Title'])
                table = dash_table.DataTable(
                    id='table',
                    columns=[{"name": i, "id": i} for i in df.columns],
                    data=df.to_dict('records'),
                    style_cell={'textAlign': 'left'},
                    style_header={
                        'backgroundColor': 'white',
                        'fontWeight': 'bold'
                    }
                )
                if data:
                    return html.Div([
                        html.H2('Details of Employees for Vacant Positions'),
                        table
                    ])
                else:
                    return html.Div([
                        html.H2('Details of Employees for Vacant Positions'),
                        html.P('No employees for vacant positions found.')
                    ])
            elif button_id == 'btn-high-performers':
                sqlConnect.mycursor.execute('''SELECT e.first_name, e.last_name, pr.rating, d.department_name
                                                FROM employees e
                                                JOIN performance_reviews pr ON e.employee_id = pr.employee_id
                                                JOIN departments d ON e.department_id = d.department_id
                                                WHERE pr.rating > (
                                                    SELECT AVG(pr2.rating)
                                                    FROM performance_reviews pr2
                                                    WHERE pr2.employee_id = e.employee_id
                                                );''')
                data = sqlConnect.mycursor.fetchall()
                df = pd.DataFrame(
                    data, columns=['First Name', 'Last Name', 'Rating', 'Department Name'])
                table = dash_table.DataTable(
                    id='table',
                    columns=[{"name": i, "id": i} for i in df.columns],
                    data=df.to_dict('records'),
                    style_cell={'textAlign': 'left'},
                    style_header={
                        'backgroundColor': 'white',
                        'fontWeight': 'bold'
                    }
                )
                if data:
                    return html.Div([
                        html.H2('High Performers'),
                        table
                    ])
                else:
                    return html.Div([
                        html.H2('High Performers'),
                        html.P('No high performers found.')
                    ])
            elif button_id == 'btn-supervisors':
                sqlConnect.mycursor.execute('''SELECT e.first_name, e.last_name
                                                FROM employees e
                                                WHERE e.employee_id IN (SELECT supervisor_id FROM employees WHERE supervisor_id IS NOT NULL);''')
                data = sqlConnect.mycursor.fetchall()
                df = pd.DataFrame(data, columns=['First Name', 'Last Name'])
                table = dash_table.DataTable(
                    id='table',
                    columns=[{"name": i, "id": i} for i in df.columns],
                    data=df.to_dict('records'),
                    style_cell={'textAlign': 'left'},
                    style_header={
                        'backgroundColor': 'white',
                        'fontWeight': 'bold'
                    }
                )
                if data:
                    return html.Div([
                        html.H2('Supervisors'),
                        table
                    ])
                else:
                    return html.Div([
                        html.H2('Supervisors'),
                        html.P('No supervisors found.')
                    ])
            elif button_id == 'btn-employees-per-dept':
                sqlConnect.mycursor.execute('''SELECT d.department_name, COUNT(e.employee_id) AS num_employees
                                                FROM employees e
                                                JOIN departments d ON e.department_id = d.department_id
                                                GROUP BY d.department_name;''')
                data = sqlConnect.mycursor.fetchall()
                df = pd.DataFrame(
                    data, columns=['Department Name', 'Number of Employees'])
                table = dash_table.DataTable(
                    id='table',
                    columns=[{"name": i, "id": i} for i in df.columns],
                    data=df.to_dict('records'),
                    style_cell={'textAlign': 'left'},
                    style_header={
                        'backgroundColor': 'white',
                        'fontWeight': 'bold'
                    }
                )
                if data:
                    return html.Div([
                        html.H2('Number of Employees per Department'),
                        table
                    ])
                else:
                    return html.Div([
                        html.H2('Number of Employees per Department'),
                        html.P('No employees per department found.')
                    ])

            elif button_id == 'btn-avg-age':
                sqlConnect.mycursor.execute('''SELECT d.department_name, AVG(CalculateAge(e.date_of_birth)) AS avg_age
                                                FROM employees e
                                                JOIN departments d ON e.department_id = d.department_id
                                                GROUP BY d.department_name;''')
                data = sqlConnect.mycursor.fetchall()
                df = pd.DataFrame(
                    data, columns=['Department Name', 'Average Age'])
                table = dash_table.DataTable(
                    id='table',
                    columns=[{"name": i, "id": i} for i in df.columns],
                    data=df.to_dict('records'),
                    style_cell={'textAlign': 'left'},
                    style_header={
                        'backgroundColor': 'white',
                        'fontWeight': 'bold'
                    }
                )
                if data:
                    return html.Div([
                        html.H2('Average Age'),
                        table
                    ])
                else:
                    return html.Div([
                        html.H2('Average Age'),
                        html.P('No average age found.')
                    ])


def dept_name_input(app):
    @app.callback(
        Output('dept-name-output', 'children'),
        [Input('dept-name', 'value')]
    )
    def update_output(dept_name):
        if dept_name is not None and dept_name != '' and dept_name in ['Engineering', 'Human Resources', 'Marketing', 'Sales', 'New']:
            while sqlConnect.mycursor.nextset():
                pass
            sqlConnect.mycursor.execute(
                '''CALL GetEmployeesByDepartment(%s);''', (dept_name,))
            data = sqlConnect.mycursor.fetchall()
            df = pd.DataFrame(
                data, columns=['First Name', 'Last Name', 'Department Name'])
            table = dash_table.DataTable(
                id='table',
                columns=[{"name": i, "id": i} for i in df.columns],
                data=df.to_dict('records'),
                style_cell={'textAlign': 'left'},
                style_header={
                    'backgroundColor': 'white',
                    'fontWeight': 'bold'
                }
            )
            if data:
                return html.Div([
                    html.H2('Get Employees By Department'),
                    table
                ])
            else:
                return html.Div([
                    html.H2('Get Employees By Department'),
                    html.P('No employees found for this department.')
                ])
        else:
            return html.Div([
                html.H2('Get Employees By Department'),
                html.P('Please enter a department name.')
            ])


def dept_rating_input(app):
    @app.callback(
        Output('dept-rating-output', 'children'),
        [Input('dept-name2', 'value')]
    )
    def update_output(dept_name):
        if dept_name is not None and dept_name != '' and dept_name in ['1','2','3','4','5']:
            while sqlConnect.mycursor.nextset():
                pass
            sqlConnect.mycursor.execute(
                '''SELECT avgDepartmentRating(%s) AS department_average_rating;''', (dept_name,))
            data = sqlConnect.mycursor.fetchall()
            df = pd.DataFrame(data, columns=['Department Average Rating'])
            table = dash_table.DataTable(
                id='table',
                columns=[{"name": i, "id": i} for i in df.columns],
                data=df.to_dict('records'),
                style_cell={'textAlign': 'left'},
                style_header={
                    'backgroundColor': 'white',
                    'fontWeight': 'bold'
                }
            )
            if data:
                return html.Div([
                    html.H2('Average Department Rating'),
                    table
                ])
            else:
                return html.Div([
                    html.H2('Average Department Rating'),
                    html.P('No average department rating found.')
                ])
        else:
            return html.Div([
                html.H2('Average Department Rating'),
                html.P('Please enter a department name.')
            ])
