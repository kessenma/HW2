## SI 364
## Winter 2018
## HW 2 - Part 1

## This homework has 3 parts, all of which should be completed inside this file (and a little bit inside the /templates directory).

## Add view functions and any other necessary code to this Flask application code below so that the routes described in the README exist and render the templates they are supposed to (all templates provided are inside the templates/ directory, where they should stay).

## As part of the homework, you may also need to add templates (new .html files) to the templates directory.

#############################
##### IMPORT STATEMENTS #####
#############################
from flask import Flask, request, render_template, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, ValidationError
from wtforms.validators import Required

import json
import requests

#####################
##### APP SETUP #####
#####################

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hardtoguessstring'

####################
###### FORMS #######
####################

class Artistform(FlaskForm):
    artist = StringField("Enter Artist", validators=[Required()])
    submit = SubmitField('Submit')

class AlbumEntryForm(FlaskForm):
    album = StringField("Enter the name of an album:", validators=[Required()])
    radio = RadioField("How much do you like this album?", choices=[(1,1),(2,2),(3,3)], validators=[Required()])
    submit = SubmitField('Submit')


####################
###### ROUTES ######
####################

###### ✨HELLO WORLD ######
@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/user/<name>')
def hello_user(name):
    return '<h1>Hello {0}<h1>'.format(name)

 ## ✨ (1) rendering the template that asks the user to type in an artist to search for.
@app.route('/artistform')
def artist_form():
	return(render_template('artistform.html'))

## ✨ (2) fomats the information the user inputted into an API request to iTunes
@app.route('/artistinfo')
def artist_info():
    if request.method == 'GET':
        result = request.args
        x = {}
        x['term'] = result.get('artist')
        resp = requests.get('https://itunes.apple.com/search?', params = x)
        data = json.loads(resp.text)
        return render_template('artist_info.html',objects = data['results'])

## ✨Example hyperlinks a user can enter
@app.route('/artistlinks')
def get_artist_links():
	return(render_template('artist_links.html'))

## ✨ (3) This is what happens after the API Request is completed. 
@app.route('/specific/song/<artist_name>')
def Artists_Display(artist_name):
    if request.method == 'GET':
        result = request.args
        params = {} 
        params['term'] = artist_name
        params['limit'] = 3
        resp = requests.get('https://itunes.apple.com/search?',params =params)
        data = json.loads(resp.text)
        return render_template('specific_artist.html',results=data['results'])



## Album

@app.route('/specific/song/<album_entry>')
def artistentry():
    return render_template('album_entry.html')

@app.route('/album_data.html')
def artistdata():
    return render_template('album_data.html')


@app.route('/album_entry')
def get_album_entry():
    simpleForm = AlbumEntryForm()
    return(render_template('album_entry.html', form= simpleForm))


@app.route('/album_result', methods = ['POST','GET'])
def album_result():
    form = AlbumEntryForm(request.form)
    if request.method == 'POST':
        abc = request.form['album']
        r = request.form['radio']
        results = {}
        results['abc'] = abc
        results['r'] = results
        return render_template("album_data.html",results=results, form=form)
    flash('All fields are required!')
    return redirect(url_for('album_entry'))

'''
@app.route('/album_data')
def get_album_result():
	return(render_template('album_entry.html'))
'''



'''
✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨
✨✨✨✨✨✨✨✨✨ DO NOT DELETE BELOW THIS✨✨✨✨✨✨✨✨
✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨
'''

if __name__ == '__main__':
    app.run(use_reloader=True,debug=True)