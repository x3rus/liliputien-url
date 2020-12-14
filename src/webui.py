#!/usr/bin/python
#
#######################################

from flask import Flask, render_template, flash, redirect,  get_flashed_messages, jsonify, abort, request
# from markupsafe import escape
from forms.add import UrlCreateEntry
from liliputien import liliputien
import liliputienErrors
import pymongo.errors

app = Flask(__name__)

# TODO change this
app.config['SECRET_KEY'] = 'you-will-never-guess'
backend = liliputien(user="root", passwd="ze_password")
if backend.connectDb() is None:
    print("not connected")


# TODO : add multiple possibility index.html index.htm
@app.route('/')
def welcome():
    return render_template('index.html', title='HomePage')


@app.route('/add', methods=['GET', 'POST'])
def add():
    form = UrlCreateEntry()
    if form.validate_on_submit():
        try:
            # urlDst = msgEvents['targetUrl']
            urlDst = form.urlTarget.data
            urlId, _ = backend.addUrlRedirection(urlDst)
        except (KeyError, pymongo.errors.ServerSelectionTimeoutError) as e:
            flash("error;" + str(e), category='error')
            return redirect('/error')
        except (liliputienErrors.urlDontMatchCriteria) as e:
            flash("error;" + str(e), category='error')
            return redirect('/error')
        # TODO : change url for /urlId/info containe detail about the link
        return render_template('added.html', urlId=urlId, urlDestination=urlDst)
    return render_template('add.html', title='Enter Url', form=form)


@app.route('/error')
def error():
    msgEvents = _get_dict_from_flashed_messages(get_flashed_messages())
    return render_template('error.html', title='HomePage', errMessage2print=msgEvents)


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
@app.route('/<urlId>')
def show_urlId(urlId):
    # show the Url Requested
    urlTarget = backend.getUrlRedirection(urlId)

    return render_template('redirect.html', title='redirection', urlTarget=urlTarget, delais=5)


def convert_url_for_json(url_entry_src):
    """ Change _id entry to string otherwize it cannot be jsonify """

    if isinstance(url_entry_src, dict):
        url_entry_src['_id'] = str(url_entry_src['_id'])
        return url_entry_src

    indexId = 0
    for url in url_entry_src:
        url_entry_src[indexId]['_id'] = str(url['_id'])
        indexId = indexId + 1

    return url_entry_src


# API ###
@app.route('/lili/api/v1.0/urls', methods=['GET'])
def get_api_urls():
    urls = backend.getUrls()
    with app.app_context():
        urlsJson = jsonify({'urls': convert_url_for_json(urls)})

    return urlsJson


@app.route('/lili/api/v1.0/urls/<string:short_url>', methods=['GET'])
def get_url(short_url):
    try:
        urlTarget = backend.getUrl(short_url)
    except liliputienErrors.urlIdNotFound:
        abort(404)
    except liliputienErrors.urlIdMultipleOccurenceFound:
        abort(404)

    return jsonify({'url': convert_url_for_json(urlTarget)})


@app.route('/lili/api/v1.0/urls', methods=['POST'])
def create_url():

    shortUrlFromUser = None
    if not request.json or 'urlDst' not in request.json:
        # TODO Add msg to informe urlDst is requiered
        abort(400)

    if 'short' in request.json:
        shortUrlFromUser = request.json['short']

    try:
        shortUrl, url = backend.addUrlRedirection(request.json['urlDst'], shortUrlFromUser)
    except liliputienErrors.urlDontMatchCriteria:
        abort(400)
    except liliputienErrors.urlIdMultipleOccurenceFound:
        abort(400)
    except liliputienErrors.unableWritingUrlEntry:
        abort(400)

    return jsonify({'url': convert_url_for_json(url)}), 201


@app.route('/lili/api/v1.0/urls/<string:shortUrl>', methods=['PUT'])
def update_api_url(shortUrl):

    if 'urlDst' not in request.json and type(request.json['urlDst']) != "unicode":
        abort(400)
    try:
        urlUpdated = backend.updateUrls(shortUrl, request.json['urlDst'])
    except liliputienErrors.urlIdNotFound:
        abort(404)

    return jsonify({'url': convert_url_for_json(urlUpdated)})


@app.route('/lili/api/v1.0/urls/<string:shortUrl>', methods=['DELETE'])
def delete_api_url(shortUrl):

    try:
        backend.deleteUrl(shortUrl)
    except liliputienErrors.urlIdNotFound:
        abort(404)

    return jsonify({'result': True})
