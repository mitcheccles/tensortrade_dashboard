import threading
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly
from dash.dependencies import Input, Output


class Dashboard():
    def __init__(self):
        self._figure = None

    def update_figure(self, figure):
        self._figure = figure

    def get_figure(self):
        return self._figure


class DashboardServer():
    def __init__(self):

        app.layout = html.Div(
            html.Div([
                html.H4('Simulation run:'),
                dcc.Graph(id='live-update-graph'),
                dcc.Interval(
                    id='interval-component',
                    interval=100, # in milliseconds
                    n_intervals=0
                )
            ])
        )

    def run(self):
        app.run_server(debug=False)


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
dashboard = Dashboard()

@app.callback(Output('live-update-graph', 'figure'),
              [Input('interval-component', 'n_intervals')])
def update_graph_live(n):
    return dashboard.get_figure()
