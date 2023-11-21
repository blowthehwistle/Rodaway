from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flight_reservation.db'
app.config['UPLOAD_FOLDER'] = './uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

db = SQLAlchemy(app)

with app.app_context():
    try:
        result = db.session.execute(text("SELECT 1"))
    except Exception as e:
        print("쿼리를 실행하는 데 실패했습니다.")
        print(e)


class Passenger(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    english_name = db.Column(db.String(80))
    baptism_name = db.Column(db.String(80))
    grade = db.Column(db.String(10))
    phone_number = db.Column(db.String(15))

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # 폼 데이터 가져오기
        name = request.form['name']
        english_name = request.form.get('english_name')  # 옵션 항목
        baptism_name = request.form.get('baptism_name')  # 옵션 항목
        grade = request.form.get('grade')  # 옵션 항목
        phone_number = request.form['phone_number']
        image = request.files['image']
 
        if image and allowed_file(image.filename):
            if not os.path.exists(app.config['UPLOAD_FOLDER']):
                os.makedirs(app.config['UPLOAD_FOLDER'])

            extension = os.path.splitext(image.filename)[1]
            filename = name + extension
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # 예약 정보 데이터베이스에 저장
        passenger = Passenger(name=name, english_name=english_name, baptism_name=baptism_name, grade=grade, phone_number=phone_number)
        
        try:
            db.session.add(passenger)
            db.session.commit()
            return '예약이 완료되었습니다.'
        except SQLAlchemyError as e:
            db.session.rollback()
            return '데이터베이스 에러: {}, 예약이 실패하였습니다.'.format(str(e))
        
    else:
        return render_template('index.html')


@app.route('/database', methods=['GET'])
def database():
    passengers = Passenger.query.all()
    return render_template('database.html', passengers=passengers)

@app.route('/deleteallquery', methods=['GET'])
def delete_all():
    num_rows_deleted = db.session.query(Passenger).delete()
    db.session.commit()
    return '총 {}건의 데이터가 삭제되었습니다.'.format(num_rows_deleted)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # 데이터베이스 초기화
    app.run(debug=True)
