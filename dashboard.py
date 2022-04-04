from dash import Dash, dcc, html, Input, Output

import plotly.express as px
import pandas as pd

# Load Land Cruiser data
landcruisers = pd.read_csv('landcruisers-cleaned.csv')

# toy df for plotly
df = pd.DataFrame(landcruisers.series.value_counts()).reset_index()
fig = px.bar(df, x = 'index', y = 'series')

# App layout
app = Dash(__name__)

app.layout = html.Div(children=[
    html.H1(children='Land Cruisers', style = {'textAlign' : 'center'}),

    html.Div(children='Unique Count by Series', style = {'textAlign' : 'center'}),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)

# App callback