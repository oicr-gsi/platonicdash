from flask import current_app as app
from flask import render_template
import random

## Use flask's server-side rendering to create a page from templates/index.html
## The @app.route decoration tells flask to return this content for both http://<root> and http://<root>/index
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html',
            title='Platonic-Dash Demo')

## A second page rendered by Flask rather than Dash.
## Uses Flask's templating to choose a random string from an array of 3 strings
## and insert the string into the page before serving the page to the user.
## @app.metrics allows adding Prometheus instrumentation, in this case,
## a counter of how many times the page is loaded.
@app.route('/page2')
@app.metrics.counter('page2_loads', 'Number of times page2 is loaded')
def page2():
    return render_template('page2.html',
            mystery_item=random.choice(['A', 'B', 'C']))
