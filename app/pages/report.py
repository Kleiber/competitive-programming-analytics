import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template

import analytics
import wrapper
import utils

dash.register_page(__name__, path_template="/report/<handle>/<year>")

def layout(handle=None, year=None, **kwargs):
    load_figure_template("DARKLY")

    user = wrapper.User(handle, year)

    if user.info == None:
        message = user.message.split(':')[1]

        return html.Div(children=[
            dbc.Alert(message, color="light", style={'margin':'auto', 'fontSize':'300%'}),
        ], style = {'display':'flex', 'marginTop': '10%'}),

    dashboard = analytics.Analytics(user)

    yearTitle = "ALL"
    if int(year) != 0:
        yearTitle = str(year)

    # User
    handle = user.info.handle
    name = user.info.firstName + ' ' + user.info.lastName
    organization = user.info.organization
    country = user.info.country
    city = user.info.city
    maxRating = user.info.maxRating
    maxRank = utils.getRankName(user.info.maxRank)
    rating = user.info.rating
    rank = utils.getRankName(user.info.rank)
    colorMaxRank = utils.getRankColor(user.info.maxRank)
    colorRank = utils.getRankColor(user.info.rank)
    registrationDate = user.info.registrationDate
    lastOnlineDate = user.info.lastOnlineDate
    photo = user.info.photo

    # Contests
    countContestByDivisionGraph = dashboard.getCountContestByDivisionGraph()

    statusContestGraph = dashboard.getStatusContestGraph()
    divisionContestGraph = dashboard.getDivisionContestGraph()
    topicContestGraph = dashboard.getTopicContestGraph()
    ratingContestGraph = dashboard.getRatingContestGraph(year)

    statusContestProgressGraph = dashboard.getStatusContestProgressGraph(year)
    divisionContestProgressGraph = dashboard.getDivisionContestProgressGraph(year)
    tagContestProgressGraph = dashboard.getTagContestProgressGraph(year)
    ratingContestProgressGraph = dashboard.getRatingContestProgressGraph(year)

    # Problems
    statusProblemGraph = dashboard.getStatusProblemGraph()
    solvedTypeProblemGraph = dashboard.getSolvedTypeProblemGraph()
    topicProblemGraph = dashboard.getTopicProblemGraph()
    ratingProblemGraph = dashboard.getRatingProblemGraph()

    statusProblemProgressGraph = dashboard.getStatusProblemProgressGraph (year)
    solvedModeProblemProgressGraph = dashboard.getSolvedModetProblemProgressGraph(year)
    tagProblemProgressGraph = dashboard.getTagProblemProgressGraph(year)
    ratingProblemProgressGraph = dashboard.getRatingProblemProgressGraph(year)


    return html.Div(children=[
        # Title User Information
        html.Div(children=[
            html.H2(children='User [{}]'.format(yearTitle))
        ], style={'textAlign': 'left', 'marginLeft':'2%'}),

        html.Br(),

        # User Information
        html.Div(children=[
            html.Div(children=[
                html.Img(src=photo, width=300, height=300)

            ], style={'width':'15%', 'margin': 'auto'}),

            html.Div(children=[
                html.H6(children='Handle: {}'.format(handle)),
                html.H6(children='Name: {}'.format(name)),
                html.H6(children='Country: {}'.format(country)),
                html.H6(children='City: {}'.format(city)),
                html.H6(children='Organization: {}'.format(organization)),
                html.H6(children='Max. Rating: {}'.format(maxRating)),
                html.H6(children='Max. Rank: {}'.format(maxRank)),
                html.H6(children='Registration: {}'.format(registrationDate.strftime("%x"))),
                html.H6(children='Online: {}'.format(lastOnlineDate.strftime("%x")))

            ], style={'width':'15%', 'margin': 'auto'}),

            html.Div(children=[
                html.P(children=[html.B(children='{}'.format(rating))]),
                html.P(children=[html.B(children='{}'.format(rank))])

            ], style={'color':colorRank, 'textAlign':'center', 'fontSize':'350%', 'width':'25%', 'margin': 'auto'}),

            html.Div(children=[
                dcc.Graph(figure = countContestByDivisionGraph),

            ], style={'width':'30%', 'margin': 'auto'})

        ], style={'display':'flex', 'marginLeft':'2%', 'marginTop':'-4%'}),

        # Title Problem Analytics
        html.Div(children=[
            html.H2(children='Problem Analytics [{}]'.format(yearTitle))
        ], style={'textAlign': 'left', 'marginLeft':'2%'}),

        # Problems
        html.Div(children=[
            html.Div(children=[
                html.Div(children=dcc.Graph(figure=statusProblemGraph, style={'width': '40vw'}), style={'display':'inline-block'}),
                html.Div(children=dcc.Graph(figure=statusProblemProgressGraph, style={'width': '55vw'}), style={'display':'inline-block'})
            ]),

            html.Div(children=[
                html.Div(children=dcc.Graph(figure=solvedTypeProblemGraph, style={'width': '40vw'}), style={'display':'inline-block'}),
                html.Div(children=dcc.Graph(figure=solvedModeProblemProgressGraph, style={'width': '55vw'}), style={'display':'inline-block'})
            ]),

            html.Div(children=[
                html.Div(children=dcc.Graph(figure=topicProblemGraph, style={'width': '40vw'}), style={'display':'inline-block'}),
                html.Div(children=dcc.Graph(figure=tagProblemProgressGraph, style={'width': '55vw'}), style={'display':'inline-block'})
            ]),

            html.Div(children=[
                html.Div(children=dcc.Graph(figure=ratingProblemGraph, style={'width': '40vw'}), style={'display':'inline-block'}),
                html.Div(children=dcc.Graph(figure=ratingProblemProgressGraph, style={'width': '55vw'}), style={'display':'inline-block'})
            ]),

        ], style={'marginLeft': '2%'}),

        # Title Contest Analytics
        html.Div(children=[
            html.H2(children='Contest Analytics [{}]'.format(yearTitle))
        ], style={'textAlign': 'left', 'marginLeft':'2%'}),

        # Contest
        html.Div(children=[
            html.Div(children=[
                html.Div(children=dcc.Graph(figure=statusContestGraph, style={'width': '40vw'}), style={'display':'inline-block'}),
                html.Div(children=dcc.Graph(figure=statusContestProgressGraph, style={'width': '55vw'}), style={'display':'inline-block'})
            ]),

            html.Div(children=[
                html.Div(children=dcc.Graph(figure=divisionContestGraph, style={'width': '40vw'}), style={'display':'inline-block'}),
                html.Div(children=dcc.Graph(figure=divisionContestProgressGraph, style={'width': '55vw'}), style={'display':'inline-block'})
            ]),

            html.Div(children=[
                html.Div(children=dcc.Graph(figure=ratingContestGraph, style={'width': '40vw'}), style={'display':'inline-block'}),
                html.Div(children=dcc.Graph(figure=ratingContestProgressGraph, style={'width': '55vw'}), style={'display':'inline-block'})
            ]),

            html.Div(children=[
                html.Div(children=dcc.Graph(figure=topicContestGraph, style={'width': '40vw'}), style={'display':'inline-block'}),
                html.Div(children=dcc.Graph(figure=tagContestProgressGraph, style={'width': '55vw'}), style={'display':'inline-block'})
            ]),

        ], style={'marginLeft': '2%'}),
    ])
