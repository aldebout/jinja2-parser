# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from flask import Flask, render_template, request
from jinja2 import Environment, meta, exceptions, select_autoescape
from random import choice
from inspect import getmembers, isfunction
from cgi import escape
import logging
import logging.handlers
import json
import yaml
import config
import datetime
from babel.dates import format_datetime, get_timezone
import pytz
from dateutil import parser
import jmespath
from custom_jmespath import CustomFunctions


app = Flask(__name__)

options = jmespath.Options(custom_functions=CustomFunctions())

def get_jinja_custom_filters():
    import filters
    custom_filters = {}
    for m in getmembers(filters):
        if m[0].startswith('filter_') and isfunction(m[1]):
            filter_name = m[0][7:]
            custom_filters[filter_name] = m[1]
    return custom_filters

def get_jmespath_custom_filters():
    custom_filters = {}
    for m in [x for x in getmembers(CustomFunctions) if x[0].startswith('_func_') and isfunction(x[1]) and x[1].__module__ == 'custom_jmespath']:
        filter_name = m[0][6:]
        custom_filters[filter_name] = m[1]
    return custom_filters


@app.route("/")
def home():
    return render_template('index.html', jinja_custom_filters=get_jinja_custom_filters(), jmespath_custom_filters=get_jmespath_custom_filters())


@app.route('/convert', methods=['GET', 'POST'])
def convert():
    jinja2_env = Environment(trim_blocks=True,lstrip_blocks=True, autoescape=request.form['simulatesafe'])
    app.logger.debug('Simulate safe is '+request.form['simulatesafe'])
    app.logger.debug('Env autoescape is '+jinja2_env.autoescape)
    # Load custom jinja filters
    custom_filters = get_jinja_custom_filters()
    app.logger.debug('Add the following customer filters to Jinja environment: %s' % ', '.join(custom_filters.keys()))
    jinja2_env.filters.update(custom_filters)

    # Load the jinja template
    try:
        jinja2_tpl = jinja2_env.from_string(request.form['jinja_template'])
    except (exceptions.TemplateSyntaxError, exceptions.TemplateError) as e:
        return json.dumps({'jinja':"Syntax error in jinja2 template: {0}".format(e), 'jmespath':'An error was raised somewhere else.'})

    # Load values
    try:
        if request.form['jinja_values'] != "":
            jinja_values = json.loads(request.form['jinja_values'])
        else:
            jinja_values = {}
    except (ValueError) as e:
        return json.dumps({'jinja':'Error in JSON: {0}'.format(e), 'jmespath':'An error was raised somewhere else.'})
    try:
        if request.form['jmespath_values'] != "":
            jmespath_values = json.loads(request.form['jmespath_values'])
        else:
            jmespath_values = {}
    except (ValueError) as e:
        return json.dumps({'jinja':'An error was raised somewhere else.', 'jmespath':'Error in JSON: {0}'.format(e)})

    # If ve have empty var array or other errors we need to catch it and show
    try:
        rendered_jinja2_tpl = jinja2_tpl.render(jinja_values)
    except (ValueError, TypeError) as e:
        return json.dumps({'jinja':"Error in your values input filed: {0}".format(e), 'jmespath':'An error was raised somewhere else.'})
    except (exceptions.UndefinedError, AttributeError) as e:
        return json.dumps({'jinja':"Error when rendering template: {0}".format(e), 'jmespath':'An error was raised somewhere else.'})

    try:
        jmespath_result = json.dumps(jmespath.search(escape(rendered_jinja2_tpl).replace('\n', ''), jmespath_values, options=options))
    except (jmespath.exceptions.JMESPathError) as e:
        jmespath_result = format(e)

    if bool(int(request.form['showwhitespaces'])):
        # Replace whitespaces with a visible character (will be grayed with javascript)
        rendered_jinja2_tpl = rendered_jinja2_tpl.replace(' ', u'•')

    return json.dumps({'jinja':escape(rendered_jinja2_tpl).replace('\n', '<br />'), 'jmespath':jmespath_result})



if __name__ == "__main__":
    # Set up logging
    app.logger.setLevel(logging.__getattribute__(config.LOGGING_LEVEL))
    file_handler = logging.handlers.RotatingFileHandler(filename=config.LOGGING_LOCATION, maxBytes=10*1024*1024, backupCount=5)
    file_handler.setFormatter(logging.Formatter(config.LOGGING_FORMAT))
    file_handler.setLevel(logging.__getattribute__(config.LOGGING_LEVEL))
    app.logger.addHandler(file_handler)

    app.run(
        host=config.HOST,
        port=config.PORT,
        debug=config.DEBUG,
    )
