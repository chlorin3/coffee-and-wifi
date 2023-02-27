from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location_url = StringField('Cafe Location on Google Maps (URL)', validators=[DataRequired(), URL()])
    opening = StringField('Opening time e.g. 8AM', validators=[DataRequired()])
    closing = StringField('Closing time e.g. 5:30PM', validators=[DataRequired()])
    coffee_rating = SelectField('Coffee Rating',
                                choices=[(x, "☕️" * x) for x in range(1, 6)],
                                validators=[DataRequired()])
    wifi_rating = SelectField('Wifi Strength Rating',
                              choices=[(x, "💪" * x) if x else (x, "✘") for x in range(6)],
                              validators=[DataRequired()])
    power_rating = SelectField('Power Socket Availability',
                               choices=[(x, "🔌" * x) if x else (x, "✘") for x in range(6)],
                               validators=[DataRequired()])
    submit = SubmitField('Submit')


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=["POST", "GET"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        coffee_rate = "☕️" * int(form.coffee_rating.data) if int(form.coffee_rating.data) in range(1, 6) else "☕️"
        wifi_rate = "💪" * int(form.wifi_rating.data) if int(form.wifi_rating.data) in range(1, 6) else "✘"
        power_rate = "🔌" * int(form.power_rating.data) if int(form.power_rating.data) in range(1, 6) else "✘"
        with open("cafe-data.csv", "a", newline='', encoding="utf8") as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow([
                form.cafe.data,
                form.location_url.data,
                form.opening.data,
                form.closing.data,
                coffee_rate,
                wifi_rate,
                power_rate
            ])
        return redirect(url_for('cafes'))
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding="utf8") as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
