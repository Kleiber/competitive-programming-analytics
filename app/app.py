import dash
from dash import Dash, dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc

app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.CYBORG])

app.layout = html.Div([
    html.Div(children=[
        html.H1(children='CODEFORCES ANALYTICS')
    ], style={'textAlign': 'center', 'marginTop':'2%'}),

    html.Div(children=[
        dbc.InputGroup([dbc.InputGroupText("Handle"),
            dbc.Input(id='handleInput', type='search', value='', placeholder="Codeforces Handle", style={'margin':'auto'}),
        ], size="lg"),

        dbc.InputGroup([dbc.InputGroupText("Year"),
            dbc.Input(id='yearInput', type='number', value=0, placeholder="Year", style={'margin':'auto'}),
        ], size="lg"),

        dbc.Button('Generate', id='submitButton', n_clicks=0, color='secondary', className='me-1')

    ], style={'display':'flex', 'marginLeft':'30%', 'marginRight':'30%', 'marginTop':'2%', 'marginBottom':'2%', 'class':"container-fluid"}),

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
    print("Generating report for handle \"{}\" and \"{}\" year.".format(handle, year))

    return '/report/{}/{}'.format(handle, year)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8050')
    #app.run(debug=True, use_reloader=False)
