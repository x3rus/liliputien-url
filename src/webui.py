#!/usr/bin/python
#
#######################################

from flask import Flask, render_template, flash, redirect
from markupsafe import escape
from flask import render_template

app = Flask(__name__)

# TODO change this
app.config['SECRET_KEY'] = 'you-will-never-guess'

# TODO : add multiple possibility index.html index.htm
@app.route('/')
def welcome():
    return render_template('index.html', title='HomePage')

# @app.route('/add', methods=['GET', 'POST'])
# def home():
#     form = UrlCreateEntry()
#     if form.validate_on_submit():
#         flash('Url requester : {}'.format(
#             form.urlTarget.data))
#         # TODO redirect to an added page showing all info and errors.
#         return redirect('/added'+form.urlTarget.data)
#     return render_template('add.html', title='Enter Url', form=form)

# # TODO : Add regex 6 car
# @app.route('/<urlId>')
# def show_urlId(urlId):
#     # show the Url Requested
#     return 'Url Id requested %s' % escape(urlId)