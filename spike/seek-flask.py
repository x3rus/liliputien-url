#!/usr/bin/python
#
# REF : https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iii-web-forms
#######################################

from flask import Flask, render_template, flash, redirect
from markupsafe import escape
from seekFlaskForms import UrlCreateEntry
from flask import render_template

app = Flask(__name__)
app.config['SECRET_KEY'] = 'you-will-never-guess'

@app.route('/', methods=['GET', 'POST'])
def home():
    form = UrlCreateEntry()
    if form.validate_on_submit():
        flash('Url requester : {}'.format(
            form.urlTarget.data))
        return redirect('/'+form.urlTarget.data)
    return render_template('index.html', title='Enter Url', form=form)

@app.route('/<urlId>')
def show_urlId(urlId):
    # show the Url Requested
    return 'Url Id requested %s' % escape(urlId)
