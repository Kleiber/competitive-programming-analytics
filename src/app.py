import dash
from dash import Dash, dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template

app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.DARKLY])

load_figure_template("DARKLY")

app.layout = html.Div([
    html.Div(children=[
        html.H1(children='CODEFORCES ANALYTICS')
    ], style={'textAlign': 'center'}),

    html.Div(children=[
        html.H4('Handle:', style={'margin':'auto'}),
        dcc.Input(id='handleInput', type='text', value='', style={'margin':'auto'}),
        html.H4('Year:', style={'margin':'auto'}),
        dcc.Input(id='yearInput', type='number', value=2024, style={'margin':'auto'}),
        dbc.Button('Submit', id='submitButton', n_clicks=0, outline=True, color='light', className='me-1')

    ], style={'display':'flex', 'marginLeft':'33%', 'marginRight':'33%', 'marginTop':'2%'}),

    dcc.Location(id='appLocation', refresh="callback-nav"),

    dash.page_container
])

@callback(
    Output('appLocation', 'pathname'),
    Input('submitButton', 'n_clicks'),
    State('handleInput', 'value'),
    State('yearInput', 'value')
)
def update_output(n_clicks, handle, year):
    return '/report/{}/{}'.format(handle, year)

if __name__ == '__main__':
    app.run(debug=True)