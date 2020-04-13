#!/usr/bin/python3
#
#################################################

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class UrlCreateEntry(FlaskForm):
    urlTarget = StringField('Destination URL', validators=[DataRequired()])
    submit = SubmitField('Generate URL')
