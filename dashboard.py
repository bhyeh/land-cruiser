from dash import Dash, dcc, html, Input, Output

import plotly.express as px
import pandas as pd

# Load Land Cruiser data
landcruisers = pd.read_csv('landcruisers-cleaned.csv')
landcruisers['closing_date'] = pd.to_datetime(landcruisers.closing_date)

# Figure
fig = px.scatter(landcruisers, x = 'closing_date', y = 'price', 
                 color = 'result', 
                 color_discrete_map = {
                     'sold' : 'light blue',
                     'reserve not met' : 'orange'
                 },
                 labels = {'closing_date' : 'Auction Date',
                           'price' : 'Closing Bid (USD)',
                           'result' : 'Auction Result'})

fig.update_traces(showlegend = False,
                  hovertemplate = '<b>%{hovertext}</b><br>Bid to %{y:$,} on %{x|%m/%d/%Y}',
                  hovertext = landcruisers.title.values,
                  name = '')

fig.update_xaxes(
    dtick = 'M12',
    tick0 = '2017-01-01',
    tickformat = '%m/%Y'
)

fig.update_yaxes(
    tickformat = '$,.2r'
)

fig.update_layout(
    font_family = 'Arial'
)

# App layout
app = Dash(__name__)

app.layout = html.Div(children=[
    html.H2(children='BAT Land Cruiser Auction Results', style = {'textAlign' : 'left'}),

    html.Div(children=[
        html.Label('Body Style'),
        dcc.Dropdown(
            options = ['60', '61', '62'], 
            placeholder = 'Select Body Style',
            multi = True,
            searchable = False
            ),

        html.Br(),
        html.Label('Transmission'),
        dcc.Dropdown(
            options = ['Manual', 'Automatic'],
            placeholder = 'Select Transmission Type',
            multi = True,
            searchable = False
        ),

        html.Br(),
        html.Label('Body Color'),
        dcc.Dropdown(
            options = sorted([color.capitalize() for color in landcruisers.exterior.unique()]),
            placeholder = 'Select Body Color',
            multi = True,
            searchable = False
        )
    ]),

    dcc.Graph(
        id='scatter-plot',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)

# App callback