import dash_html_components as html
import dash_core_components as core
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import pandas as pd
import plotly.graph_objects as go
from .dash_id import init_ids
from flask_caching import Cache

## Displays a page containing a scatter plot, a slider which controls which
## data gets displayed on the graph (via the URL), and a dropdown which locks
## or unlocks changing the graph by slider or URL.

## Use pandas to read data from csv
df = pd.read_csv(
    'https://raw.githubusercontent.com/plotly/'
    'datasets/master/gapminderDataFiveYear.csv')

page_name = 'complex-page'

ids = init_ids(['scatter-plot', 'year-slider', 'url', 'dropdown'])

layout = html.Div([
    core.Location(id=ids['url'], refresh=False),

    ## Graph is empty by default. Callback will automatically draw graph here
    ## on page load.
    core.Graph(id=ids['scatter-plot']),
    core.Slider(
        id=ids['year-slider'],
        min=df['year'].min(),
        max=df['year'].max(),
        value=df['year'].min(),
        marks={str(year): str(year) for year in df['year'].unique()},
        step=None
    ),
    ## This dropdown controls whether the slider and URL are able to update the
    ## graph.
    core.Dropdown(
        id=ids['dropdown'],
        options = [
            {'label': 'Editable', 'value': 'editable'},
            {'label': 'Uneditable', 'value': 'uneditable'}
        ],
        value = 'editable'
    )
])

def init_callbacks(dash_app):
    ## On change of dropdown's value, return true if 'uneditable'.
    ## Return value gets output to 'disabled' property of slider,
    ## greying out and freezing slider interactivity.
    @dash_app.callback(
        Output(ids['year-slider'], 'disabled'),
        [Input(ids['dropdown'], 'value')]
    )
    def disableSliderOnUneditable(dropdown_value):
        # if 'uneditable', slider disabled is true
        return dropdown_value == 'uneditable'

    ## On change of slider's value, take value and make it the URL's hash
    @dash_app.callback(
        Output(ids['url'], 'hash'),
        [Input(ids['year-slider'], 'value')]
    )
    @dash_app.server.cache.memoize(timeout=60)
    def onSlide(value):
        return '#'+str(value)

    ## State allows you to get the values of layout elements without
    ## triggering callbacks on change in the element.
    ## On change of URL (including initial access) build a scatter plot
    ## based on hash (eg #1997), unless dropdown has been set to 'uneditable',
    ## return graph to display in layout.
    @dash_app.callback(
        Output(ids['scatter-plot'], 'figure'),
        [Input(ids['url'], 'hash')],
        [State(ids['dropdown'], 'value')])
    @dash_app.server.cache.memoize(timeout=60)
    def update_figure(selected_year, dropdown_value):
        if dropdown_value == 'uneditable':
            ## raising PreventUpdate is one of two ways to cancel executing
            ## a callback. Please see the Dash documentation for more details.
            raise PreventUpdate
        
        ## Remove first character (#) from hash and convert to int
        selected_year = int(selected_year[1:])
        filtered_df = df[df.year == selected_year]
        traces = []
        for i in filtered_df.continent.unique():
            df_by_continent = filtered_df[filtered_df['continent'] == i]

            ## Use go.Scattergl (and other WebGL graphs) whenever possible for
            ## improved performance. These render using the client's GPU rather
            ## than as SVG.
            traces.append(go.Scattergl(
                x=df_by_continent['gdpPercap'],
                y=df_by_continent['lifeExp'],
                text=df_by_continent['country'],
                mode='markers',
                opacity=0.7,
                marker={
                    'size': 15,
                    'line': {'width': 0.5, 'color': 'white'}
                },
                name=i
            ))
    
        return {
            'data': traces,
            'layout': go.Layout(
                xaxis={'type': 'log', 'title': 'GDP Per Capita'},
                yaxis={'title': 'Life Expectancy', 'range': [20, 90]},
                margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                legend={'x': 0, 'y': 1},
                hovermode='closest'
            )
        }

