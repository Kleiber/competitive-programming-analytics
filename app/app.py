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
        dbc.InputGroup([dbc.InputGroupText("Handle"),
            dbc.Input(id='handleInput', type='search', value='', placeholder="Codeforces Handle", style={'margin':'auto'}),
        ], size="lg"),

        dbc.InputGroup([dbc.InputGroupText("Year"),
            dbc.Input(id='yearInput', type='number', value=0, placeholder="Year", style={'margin':'auto'}),
        ], size="lg"),

        dbc.Button('Submit', id='submitButton', n_clicks=0, outline=True, color='light', className='me-1')

    ], style={'display':'flex', 'marginLeft':'30%', 'marginRight':'30%', 'marginTop':'2%', 'class':"container-fluid"}),

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
    app.run(debug=True, use_reloader=False)
