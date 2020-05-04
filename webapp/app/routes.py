import sqlite3 as sql
import os

from flask import render_template, redirect, request, Response
from app.forms import TextForm
from app import app

# Create a database https://flaskguide.readthedocs.io/en/latest/flask/flask2.html

con = sql.connect('text.db')
con.execute("CREATE TABLE IF NOT EXISTS textdbtable (ID INTEGER PRIMARY KEY AUTOINCREMENT, \
   '+'text_input TEXT)")
con.close

@app.route('/text')
def input():
    return render_template('output.html')

@app.route('/downloadaudio')
def raudio():
    def generate():
        with open("benoy.wav", "rb") as fwav:
            data = fwav.read(1024)
            while data:
                yield data
                data = fwav.read(1024)
    return Response(generate(), mimetype="audio/x-wav")

@app.route('/input', methods=['GET','POST'])
def text_input():
    form = TextForm()
    if form.validate_on_submit():
        print("form correct")
        text = request.form['text']
        print(text)
        os.system(f"espeak-ng {text} -w benoy.wav")
        return redirect("/downloadaudio")
    return render_template('input.html', form=form)