import dash
import dash_core_components as core
import dash_html_components as html
from .dash_id import init_ids
from dash.dependencies import Input, Output
from flask_caching import Cache
from . import dash_multipage_1, dash_multipage_2, dash_multipage_3

## Multipage apps in Dash don't use the traditional HTML page structure,
## but rather displays one page and reads/writes to the URL and updates
## an internal Div dynamically. Please see the Dash documentation for
## more information.

## Used by multipage_index for URL handling
page_name = 'multipage'

ids = init_ids(['url', 
    'page-content'])

layout = html.Div([
    ## Defining an ID for core.Location allows us access to read and write from the URL
    core.Location(id=ids['url'], refresh=False),

    ## Base layout contains only a div in which we will draw all of the pages in the app
    html.Div(id=ids['page-content'])
])

## Default content of 'page-content' div
index_page = html.Div([
    core.Link('Go to Page 1', href='/dash/{0}'.format(dash_multipage_1.page_name)),
    html.Br(),
    core.Link('Go to Page 2', href='/dash/{0}'.format(dash_multipage_2.page_name)),
    html.Br(),
    core.Link('Go to Page 3', href='/dash/{0}'.format(dash_multipage_3.page_name)),
    html.Br(),
    html.A('Back to Flask', href='/..')
])


def init_callbacks(dash_app):
    ## Needed for multipage support
    dash_app.config.suppress_callback_exceptions = True

    ## Detects change in URL and outputs layout objects to page-content div
    ## Flask (dash_app.server)'s cache extension holds a map of input & output
    ## in memory to improve performance. 
    @dash_app.callback(Output(ids['page-content'], 'children'),
            [Input(ids['url'], 'pathname')])
    @dash_app.server.cache.memoize(timeout=60)
    def display_page(pathname):
        if pathname == '/dash/{0}'.format(dash_multipage_1.page_name):
            return dash_multipage_1.layout
        elif pathname == '/dash/{0}'.format(dash_multipage_2.page_name):
            return dash_multipage_2.layout
        elif pathname == '/dash/{0}'.format(dash_multipage_3.page_name):
            return dash_multipage_3.layout
        else:
            return index_page

    ## As an example of ids being local to each page, this callback
    ## outputs to dash_multipage_2's 'page-content', which is distinct
    ## from this page's 'page-content'. This callback drives the 
    ## interactivity in dash_multipage_2 despite being in the
    ## dash_multipage_index file.
    @dash_app.callback(Output(dash_multipage_2.ids['page-content'], 'children'),
            [Input(dash_multipage_2.ids['radios'], 'value')])
    @dash_app.server.cache.memoize(timeout=60)
    def page_2_radios(value):
        return 'You have selected "{0}"'.format(value)
