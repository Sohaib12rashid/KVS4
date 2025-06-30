from flask import Flask, request, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Use PostgreSQL URL from Render environment variable
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define the student data model
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    class_name = db.Column(db.String(20))
    section = db.Column(db.String(10))
    admission = db.Column(db.String(50))
    mobile = db.Column(db.String(20))
    address = db.Column(db.String(200))

# Create database tables (only once)
@app.before_first_request
def create_tables():
    db.create_all()

# Home page: form input
@app.route('/')
def index():
    return render_template("index.html")

# API route: save student data to database
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

# Admin view: display saved student records
@app.route('/view')
def view_data():
    students = Student.query.all()
    return render_template("view.html", students=students)

# Run the app locally (not used on Render)
if __name__ == '__main__':
    app.run(debug=True)
