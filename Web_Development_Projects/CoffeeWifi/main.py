import os
import csv
from flask import Flask, redirect, render_template, flash, url_for
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TimeField
from wtforms.validators import DataRequired, URL
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()
app.config['SECRET_KEY'] = os.environ.get('CSRF_KEY')
Bootstrap5(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    submit = SubmitField('Submit')


# Exercise:
# add: Location URL, open time, closing time, coffee rating, wifi rating, power outlet rating fields
# make coffee/wifi/power a select element with choice of 0 to 5.
# e.g. You could use emojis ☕️/💪/✘/🔌
# make all fields required except submit
# use a validator to check that the URL field has a URL entered.
# ---------------------------------------------------------------------------


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = StringField(
        'Cafe Location on Google Maps (URL)', validators=[DataRequired(), URL()]
    )
    open_time = TimeField(
        'Opening Time e.g. 08:00 AM', validators=[DataRequired()], format='%H:%M'
    )  # Changed to TimeField
    close_time = TimeField(
        'Closing Time e.g. 05:30 PM', validators=[DataRequired()], format='%H:%M'
    )  # Changed to TimeField

    # Predefined values for ratings
    coffee_rating_choices = [
        ('✘', '✘'),
        ('☕', '☕'),
        ('☕☕', '☕☕'),
        ('☕☕☕', '☕☕☕'),
        ('☕☕☕☕', '☕☕☕☕'),
        ('☕☕☕☕☕', '☕☕☕☕☕'),
    ]
    wifi_rating_choices = [
        ('✘', '✘'),
        ('💪', '💪'),
        ('💪💪', '💪💪'),
        ('💪💪💪', '💪💪💪'),
        ('💪💪💪💪', '💪💪💪💪'),
        ('💪💪💪💪💪', '💪💪💪💪💪'),
    ]
    power_outlet_rating_choices = [
        ('✘', '✘'),
        ('🔌', '🔌'),
        ('🔌🔌', '🔌🔌'),
        ('🔌🔌🔌', '🔌🔌🔌'),
        ('🔌🔌🔌🔌', '🔌🔌🔌🔌'),
        ('🔌🔌🔌🔌🔌', '🔌🔌🔌🔌🔌'),
    ]

    coffee_rating = SelectField(
        'Coffee Rating', choices=coffee_rating_choices, validators=[DataRequired()]
    )
    wifi_rating = SelectField(
        'Wifi Strength Rating', choices=wifi_rating_choices, validators=[DataRequired()]
    )
    power_outlet_rating = SelectField(
        'Power Socket Availability Rating',
        choices=power_outlet_rating_choices,
        validators=[DataRequired()],
    )

    submit = SubmitField('Submit')


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        with open('cafe-data.csv', mode='a', newline='', encoding='utf-8') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow(
                [
                    form.cafe.data.strip(),
                    form.location.data.strip(),
                    form.open_time.data.strftime('%I:%M%p'),
                    form.close_time.data.strftime('%I:%M%p'),
                    form.coffee_rating.data,
                    form.wifi_rating.data,
                    form.power_outlet_rating.data,
                ]
            )
        flash('Cafe successfully added!', 'success')
        return redirect(url_for('add_cafe'))
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
