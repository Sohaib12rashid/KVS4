from flask import Flask, request, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Get PostgreSQL URL from environment variable (Render)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define Student table
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    class_name = db.Column(db.String(20))
    section = db.Column(db.String(10))
    admission = db.Column(db.String(50))
    mobile = db.Column(db.String(20))
    address = db.Column(db.String(200))

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()
    student = Student(
        name=data['name'],
        class_name=data['class'],
        section=data['section'],
        admission=data['admission'],
        mobile=data['mobile'],
        address=data['address']
    )
    db.session.add(student)
    db.session.commit()
    return jsonify({"message": "Student data saved to database!"})

@app.route('/view')
def view_data():
    students = Student.query.all()
    return render_template("view.html", students=students)

if __name__ == '__main__':
    app.run(debug=True)
