from dash import dcc, html, Dash, dash_table
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd

app = Dash(__name__)

app.layout = html.Div(children=[
    html.H1('Vix Dashboard'),
    html.H2("Voici le cours de l'indice VIX (aka l'indice de volatilité du S&P 500) au cours d'une journée"),
    dcc.Graph(id='vix-graph'),
    html.H3("Daily Report : "),
    html.Div(id='daily-metrics',style={
           'border-collapse': 'collapse','margin': 'auto', 'width': '75%'}),
    dcc.Interval(
        id='graph-update',
        interval=5*60*1000,  # in milliseconds
        n_intervals=0
    ),
])

@app.callback(Output('vix-graph', 'figure'),
              [Input('graph-update', 'n_intervals')])

def update_graph(n):
    # read data from text file
    # read data from text file
    value = pd.read_csv('vix.txt',sep='\t',header=None,names=['value'])
    date = pd.read_csv('vix_date.txt',sep='\t',header=None,names=['date'])

    # combine value and date DataFrames
    df = pd.concat([date, value], axis=1)
    df['date'] = pd.to_datetime(df['date'])
    df['date'] = df['date'] + pd.Timedelta(hours=2)
    # create graph
    fig = {
        'data': [{'x': df['date'].dt.strftime('%Y-%m-%d %H:%M'), 'y': df['value'], 'type': 'line'}],
        'layout': {
            'title': 'VIX Index Time Series',
            'xaxis': {'title': 'Time'},
            'yaxis': {'title': 'Value'}
        }
    }
    return fig

@app.callback(Output('daily-metrics', 'children'),
              [Input('graph-update', 'n_intervals')])

def update_daily_metrics(n):
    # read metrics data from text file
    with open('metrics.txt', 'r') as f:
        met = f.read().splitlines()
        metrics_list = [i.split(": ") for i in met]

    metrics_dict = {}
    for i in range(len(metrics_list)):
        j=0
        metrics_dict[metrics_list[i][j]] =  metrics_list[i][j+1]

    # créer un tableau HTML à partir du dictionnaire de métriques
    table = html.Table([
        html.Thead(
            html.Tr([html.Th('Metrics'), html.Th('Value')]) ),
        html.Tbody([
                html.Tr([html.Td(metric,style={'padding': '10px', 'border': '1px solid grey'}),
                         html.Td(value,style={'padding': '10px', 'border': '1px solid grey'})]) for metric, value in metrics_dict.items()
        ])
    ])
    return table

if __name__ == '__main__':
    app.run_server(host='0.0.0.0',port=8050,debug=True)
