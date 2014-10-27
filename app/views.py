"""
A set of APIs for accessing data based off of place name

"""
from acorn import acorn
from app import app
import flask
from flask import request

@app.route('/geo/<place>')
def call_acorn(place):
    a = acorn.Acorn()
    
    try:
        place = a.resolve(place)
    except ValueError:
        place = 'Not Found'

    return str(place)
