#!/usr/bin/python
#
#######################################

from flask import Flask
from markupsafe import escape
from seekFlaskForms import UrlCreateEntry
from flask import render_template

app = Flask(__name__)
app.config['SECRET_KEY'] = 'you-will-never-guess'

@app.route('/')
def home():
    form = UrlCreateEntry()
    return render_template('index.html', title='Enter Url', form=form)


@app.route('/<urlId>')
def show_urlId(urlId):
    # show the Url Requested
    return 'Url Id requested %s' % escape(urlId)
