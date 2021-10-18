import os
import csv
import pandas as pd
from flask import Blueprint, Flask, render_template, send_file
from flask.templating import render_template
from flask.wrappers import Response
from flask_login.utils import login_required
from pandas.core.frame import DataFrame


commander = Blueprint('commander', __name__)

@commander.route("/mission")
def mission():
    return render_template('commander/mission.html', title='Missie en visie')

@commander.route("/purpose")
def purpose():
    return render_template('commander/purpose.html', title='Oogmerk')

@commander.route("/planning", methods=["GET", "POST"])
@login_required
def planning():
    df = pd.read_csv('flaskapp/static/planning.csv', header=0)
    return render_template('commander/planning.html', tables=[df.to_html(classes='table')], titles=df.columns.values, title='Planning')
        

@commander.route("/sport")
@login_required
def sport():
    return render_template('commander/sport.html', title='Sportrooster')


