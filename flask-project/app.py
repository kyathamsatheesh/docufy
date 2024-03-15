from flask_cors import CORS, cross_origin
from flask import Flask, render_template, request, make_response, jsonify, redirect, url_for
from werkzeug.utils import secure_filename
import os
import sqlite3
from docx import Document

# Database setup
conn = sqlite3.connect('test.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS test (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER NOT NULL,
        grade INTEGER NOT NULL
    )
''')
conn.commit()
conn.close()

app = Flask(__name__)
# Use SQLite as the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
# Configure upload folder and allowed extensions
app.config["UPLOAD_FOLDER"] = "uploads/"
ALLOWED_EXTENSIONS = {"doc", "docx"}

# Configure CORS
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# db = SQLAlchemy(app)


def allowed_file(filename):
    """
    Checks if the filename has an allowed extension.
    """
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# class ExampleModel(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     data = db.Column(db.String(100), nullable=False)

@app.route('/')
def index():
    # Query data from the database
    # data_from_db = ExampleModel.query.all()
    # return render_template('index.html', data_from_db=data_from_db)
    return render_template('index.html')


@app.route('/api/upload', methods=['POST'])
def upload_file():
    if "file" not in request.files:
        return make_response(jsonify({"message": "No file uploaded"}), 400)
    file = request.files["file"]

    # Check if the file is allowed
    if file.filename == "":
        return make_response(jsonify({"message": "No selected file"}), 400)


    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)

        data = query_db()
        doc = Document(filepath)
        doc.add_paragraph(f"Additional Data: {data}")
        doc.save(filepath)

        return jsonify({"message": "File uploaded successfully"})
    else:
        return make_response(jsonify({"message": "Invalid file format"}), 400)


def query_db():
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM test')
    students = cursor.fetchall()
    conn.close()
    return students

def add_student():
    data = [
        ("Keshav", "24", "A"),
        ("Satish", "28", "A"),
        ("Test", "20", "B"),
        ("Joe", "42", "A+")
    ]

    # name = request.form.get('name')
    # age = request.form.get('age')
    # grade = request.form.get('grade')

    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    for each in data:
        cursor.execute(
            'INSERT INTO test (name, age, grade) VALUES (?, ?, ?)', each)
    conn.commit()
    conn.close()

    return redirect('index')


if __name__ == '__main__':
    with app.app_context():
        add_student()
    # Create tables within the application context
    # with app.app_context():
    # db.create_all()

    app.run(debug=True)
