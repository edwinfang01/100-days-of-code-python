import os
from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import Form, BooleanField, StringField, validators
from wtforms.fields.simple import PasswordField, SubmitField, EmailField
from wtforms.validators import DataRequired, InputRequired
from flask_bootstrap import Bootstrap5
from dotenv import load_dotenv


"""DataRequired checks if the input value is a truthy value, meaning if you input 0 or an empty string '' it will throw an error
InputRequired seems to be the recommended option in most cases."""

class LoginForm(FlaskForm):
    email = EmailField('Email Address', [validators.Length(min=6, max=35), InputRequired()])
    password = PasswordField('Password', [validators.Length(min=4, max=25), DataRequired()])
    submit = SubmitField(label="Log in")
    # accept_rules = BooleanField('I accept the site rules', [validators.InputRequired()])

app = Flask(__name__)
# Use a random key if the environment variable doesn't exist
load_dotenv()
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', os.urandom(24))
bootstrap = Bootstrap5(app)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/success')
def success():
    return render_template("success.html")

@app.route('/denied')
def deny():
    return render_template("denied.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        if (login_form.email.data, login_form.password.data) == ("admin@email.com", "12345678"):
            return success()
        else:
            return deny()
    return render_template('login.html', form=login_form)


if __name__ == '__main__':
    app.run(debug=True)
