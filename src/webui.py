#!/usr/bin/python
#
#######################################

from flask import Flask, render_template, flash, redirect, request, get_flashed_messages
from markupsafe import escape
from flask import render_template
from forms.add import UrlCreateEntry

app = Flask(__name__)

# TODO change this
app.config['SECRET_KEY'] = 'you-will-never-guess'

# TODO : add multiple possibility index.html index.htm
@app.route('/')
def welcome():
    return render_template('index.html', title='HomePage')

@app.route('/add', methods=['GET', 'POST'])
def add():
    form = UrlCreateEntry()
    if form.validate_on_submit():
        # TODO : check not sure it's the best way to pass info... :-/
        flash('targetUrl ; {}'.format(form.urlTarget.data))
        return redirect('/added')
    return render_template('add.html', title='Enter Url', form=form)


@app.route('/added', methods=['GET', 'POST'])
def added():
    msgEvents = _get_dict_from_flashed_messages(get_flashed_messages())
    if msgEvents is None:
        return render_template('added.html', urlId="", urlDestination="")
    urlId = "abk3s2"
    try:
        urlDst = msgEvents['targetUrl']
    except KeyError:
        urlDst = ""
    return render_template('added.html', urlId=urlId, urlDestination=urlDst)

def _get_dict_from_flashed_messages(flashedMessage):
    """ Return a dictionnary from flashed message """

    dictFlashedMsg = {}
    try:
        for message in flashedMessage:
            array = message.split(";")
            dictFlashedMsg[array[0].strip()] = array[1].strip()
    except IndexError:
        return None

    return dictFlashedMsg

# # TODO : Add regex 6 car
# @app.route('/<urlId>')
# def show_urlId(urlId):
#     # show the Url Requested
#     return 'Url Id requested %s' % escape(urlId)