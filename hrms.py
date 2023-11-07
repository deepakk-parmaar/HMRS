import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from components import dashBoard , employee , department, position, attendance, leave, performance, application, sqlConnect
app = dash.Dash(__name__, suppress_callback_exceptions=True)

button_options = [
    {'label': 'Dashboard', 'value': 'btn1'},
    {'label': 'Employee', 'value': 'btn2'},
    {'label': 'Department', 'value': 'btn3'},
    {'label': 'Position', 'value': 'btn4'},
    {'label': 'Attendance', 'value': 'btn5'},
    {'label': 'Leave', 'value': 'btn6'},
    {'label': 'Performance', 'value': 'btn7'},
    {'label': 'Application', 'value': 'btn8'},
]

# Layout setup
app.layout = html.Div([
    html.H1('Human Resource Management System', className='heading'),

    html.Div(
        className='container',
        children=[
            html.Div(
                dcc.RadioItems(
                    id='button-selector',
                    options=button_options,
                    value=button_options[0]['value'],
                    labelStyle={'display': 'block'},
                    style={
                        'display': 'flex',
                        'flex-direction': 'column',
                        'padding': '10px'
                    }
                ),
                style={'width': '20%', 'float': 'left'}
            ),

            html.Div(
                id='dynamic-content',
                style={'width': '80%', 'float': 'left'},
                className='content-container'
            ),
        ]
    )
])

# Create content components for each button
button_content = {
    'btn1': dashBoard.btn1_content,
    'btn2': employee.btn2_content,
    'btn3': department.btn3_content,
    'btn4': position.btn4_content,
    'btn5': attendance.btn5_content,
    'btn6': leave.btn6_content,
    'btn7': performance.btn7_content,
    'btn8': application.btn8_content,
}

@app.callback(
    Output('dynamic-content', 'children'),
    [Input('button-selector', 'value')]
)
def update_content(selected_button):
    return button_content.get(selected_button, html.Div('No content to display for this button.'))

# Callbacks for each component
dashBoard.dashBoard_callbacks(app)
sqlConnect.mycursor.reset()
dashBoard.queries_callback(app)
sqlConnect.mycursor.reset()
dashBoard.dept_name_input(app)
sqlConnect.mycursor.reset()
dashBoard.dept_rating_input(app)
sqlConnect.mycursor.reset()
employee.employee_submit(app)
sqlConnect.mycursor.reset()
employee.employee_form_callbacks(app)
employee.employee_update(app)
employee.employee_display_delete(app)
sqlConnect.mycursor.reset()
department.department_callbacks(app)
sqlConnect.mycursor.reset()
department.department_submit(app)
position.position_callbacks(app)
position.position_submit(app)
attendance.attendance_callbacks(app)
attendance.attendance_submit(app)
leave.leave_callbacks(app)
leave.leave_submit(app)
performance.performance_callbacks(app)
performance.performance_submit(app)
application.application_callbacks(app)
application.application_submit(app)

if __name__ == '__main__':
    app.run_server(debug=True)
