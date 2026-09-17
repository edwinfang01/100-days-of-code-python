from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields.choices import SelectField
from wtforms.fields.datetime import TimeField
from wtforms.fields.simple import URLField
from wtforms.validators import DataRequired, InputRequired, ValidationError
import csv
from validators import url
import datetime

'''
Red underlines? Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
bootstrap = Bootstrap5(app)


def valid_url(form, field):
    if not url(field.data):
        raise ValidationError("not a valid URL")


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = URLField('Cafe Location on Google Maps (URL)', [InputRequired(), valid_url])
    open_time = TimeField("Opening Time e.g. 8AM", [InputRequired()])
    close_time = TimeField("Closing Time e.g. 5:30PM", [InputRequired()])

    coffee_rating = SelectField("Coffee Rating",
                                choices=[("☕️"*i) for i in range(1,6)])
    wifi_power = SelectField("Wifi Power",
                             choices=[ ("✘", "✘") if not i else ("🔌"*i, "🔌"*i) for i in range(6) ] )
    power_socket = SelectField("Power Socket Availability",
                               choices=[ ("✘", "✘") if i == 0 else ("🔌"*i, "🔌"*i) for i in range(6) ] )

    # coffee_rating = SelectField("Coffee Rating", choices=[(1, "☕️"), (2, "☕️"*2), (3, '☕️'*3), (4, '☕️'*4), (5, '☕️'*5)])
    # wifi_power = SelectField("Wifi Power", choices=[(0, "✘"), (1, "🔌"), (2, "🔌"*2), (3, '🔌'*3), (4, '🔌'*4), (5, '🔌'*5)])
    # power_socket = SelectField("Power Socket Availability", choices=[(0, "✘"), (1, "🔌"), (2, "🔌"*2), (3, '🔌'*3), (4, '🔌'*4), (5, '🔌'*5)])

    submit = SubmitField('Submit')


# Exercise:
# add: Location URL, open time, closing time, coffee rating, wifi rating, power outlet rating fields
# make coffee/wifi/power a select element with choice of 0 to 5.
#e.g. You could use emojis ☕️/💪/✘/🔌
# make all fields required except submit
# use a validator to check that the URL field has a URL entered.
# ---------------------------------------------------------------------------


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=["POST", "GET"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        form_data = [field.data.strftime("%I:%M %p")[1:] if ("time" in field.name or field.type == "TimeField") else field.data
                     for field in form if not field.type in ("CSRFTokenField", "SubmitField")]
        # print(form_data)
        form_data = ",".join(form_data)
        with open("cafe-data.csv", "a", encoding='utf-8') as f:
            f.write("\n" + form_data)

        # # for field in form:
        #     if field.type in ("CSRFTokenField", "SubmitField"):
        #         continue
        #     print(field.name, field.raw_data, field.type, field.data, type(field.data), field.data.strftime("%I:%M %p") if field.name == "open_time" else None)

    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
