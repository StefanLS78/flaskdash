from flask.globals import request
from flask import Blueprint
from flask_googlemaps import Map
from flask.templating import render_template

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home():
    return render_template('home.html') 
    

@main.route("/about")
def about():
    return render_template('about.html', title='About')

@main.route("/maps")
def map_func():
    return render_template('maps.html')