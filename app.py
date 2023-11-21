from flask import Flask, render_template, request, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_migrate import Migrate
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flight_reservation.db'
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['UPLOAD_FOLDER'] = 'uploads'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}

class Passenger(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    english_name = db.Column(db.String(80))
    baptism_name = db.Column(db.String(80))
    grade = db.Column(db.String(10))
    phone_number = db.Column(db.String(15))

class ReservationForm(FlaskForm):
    image = FileField('여권 사진 업로드', validators=[FileAllowed(ALLOWED_EXTENSIONS, '이미지 파일만 허용됩니다.')])
    name = StringField('이름', validators=[DataRequired()])
    english_name = StringField('영문 이름')
    baptism_name = StringField('세례명')
    grade = StringField('학년')
    phone_number = StringField('전화번호', validators=[DataRequired()])
    submit = SubmitField('예약')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = ReservationForm()

    if form.validate_on_submit():
        name = form.name.data
        english_name = form.english_name.data
        baptism_name = form.baptism_name.data
        grade = form.grade.data
        phone_number = form.phone_number.data
        image = form.image.data

        if image:
            name = form.name.data
            custom_filename = secure_filename(name + '.' + image.filename.rsplit('.', 1)[1])
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], custom_filename))
        else:
            custom_filename = None

        passenger = Passenger(name=name, english_name=english_name, baptism_name=baptism_name, grade=grade, phone_number=phone_number)
        db.session.add(passenger)
        db.session.commit()
        return jsonify({'message': '예약이 완료되었습니다.'})

    return render_template('index.html', form=form)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
