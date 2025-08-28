from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class ContactForm(FlaskForm):
    name = StringField('Name', validators=[
        DataRequired(),
        Length(min=2, max=100, message='Name must be between 2 and 100 characters')
    ])
    email = StringField('Email', validators=[
        DataRequired(),
        Email(message='Please enter a valid email address')
    ])
    subject = StringField('Subject', validators=[
        DataRequired(),
        Length(min=2, max=200, message='Subject must be between 2 and 200 characters')
    ])
    message = TextAreaField('Message', validators=[
        DataRequired(),
        Length(min=10, message='Message must be at least 10 characters long')
    ])
    submit = SubmitField('Send Message')