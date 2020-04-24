from flask import render_template, redirect, request
from app.forms import TextForm
from app import app

@app.route('/text')
def input():
    return render_template('index.html')

@app.route('/input', methods=['GET','POST'])
def text_input():
    form = TextForm()
    if form.validate_on_submit():
        print("form correct")
        # text = request.POST['text']
        # print(text)
        return redirect("/text")
    return render_template('input.html', form=form)