from dash import Dash, dcc, html, Input, Output

import plotly.express as px
import pandas as pd
import numpy as np

# Load Land Cruiser data
landcruisers = pd.read_csv('landcruisers-cleaned.csv')

# App layout
# ------------------------------------------------------------------------------

app = Dash(__name__)

app.layout = html.Div(children=[
    html.H2(children='BaT Land Cruiser Auction Results', style = {'margin-left' : '5%', 'margin-top' : '5%', 'textAlign' : 'left'}),

    html.Div(children=[
        html.Label('Body Style'),
        dcc.Dropdown(
            options = [60, 61, 62], 
            value = [60, 61, 62],
            placeholder = 'Select Body Style(s)',
            multi = True,
            searchable = False,
            id = 'bodystyle-dropdown'
            ),

        html.Br(),
        html.Label('Transmission'),
        dcc.Dropdown(
            options = ['Manual', 'Automatic'],
            value = ['Manual', 'Automatic'],
            placeholder = 'Select Transmission Type(s)',
            multi = True,
            searchable = False,
            id = 'transmission-dropdown'
        ),

        html.Br(),
        html.Label('Body Color'),
        dcc.Dropdown(
            options = sorted([color.capitalize() for color in landcruisers.exterior.unique()]),
            placeholder = 'Select Body Color(s)',
            multi = True,
            searchable = False
        )
    ], style={'margin-left' : '5%','width' : '20%', 'display': 'inline-block'}),

    dcc.Graph(
        id='scatter-plot',
        figure = {},
        style = {'margin-left' : '5%', 'margin-right' : '5%'}
    ),

    html.H4(id = 'median-price', children = {}, style = {'textAlign' : 'center'})
], style = {'fontFamily' : 'Helvetica'})

# App callback
# ------------------------------------------------------------------------------

@app.callback(
    Output(component_id = 'median-price', component_property = 'children'),
    Output(component_id = 'scatter-plot', component_property = 'figure'),
    Input(component_id = 'bodystyle-dropdown', component_property = 'value'),
    Input(component_id = 'transmission-dropdown', component_property = 'value'))
def update_figure(bodystyle, trans):

    # Lower case user inputs
    if len(trans):
        trans = [str.lower() for str in trans]

    # Subset landcruisers dataframe
    landcruisers_filtered = landcruisers[(landcruisers.trans.isin(trans)) & (landcruisers.body_type.isin(bodystyle))]

    # Median Price Container
    if landcruisers_filtered.shape[0]:
        median_price = np.median(landcruisers_filtered.price)
        container = 'Median Price: ${:,.0f}'.format(median_price)
    else:
        container = 'Median Price: '        

    fig = px.scatter(landcruisers_filtered, x = 'closing_date', y = 'price', 
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
                    hovertext = landcruisers_filtered.title.values,
                    name = '')

    fig.update_xaxes(
        dtick = 'M12',
        tick0 = '2017-01-01',
        tickformat = '%m/%Y',
        title_font_family = 'Helvetica'

    )

    fig.update_yaxes(
        range = [0, 140000],
        tickformat = '$,.2r',
        title_font_family = 'Helvetica'

    )

    fig.update_layout(
        font_family = 'Helvetica'
    )

    return container, fig

# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)