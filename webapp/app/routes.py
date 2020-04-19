from flask import render_template
from app.forms import TextForm
from app import app

@app.route('/text')
def input():
    return render_template('index.html')

@app.route('/input')
def text_input():
    form = TextForm()
    return render_template('input.html', form=form)