from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField
from wtforms.validators import DataRequired 

class TextForm(FlaskForm):
    text = StringField('Enter the required text', validators=[DataRequired()])
    agree = BooleanField('Agree to T&C', validators=[DataRequired()])
    submit = SubmitField("Submit to MTTS")
