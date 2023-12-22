from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import pymongo

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# MongoDB connection
with pymongo.MongoClient("mongodb+srv://monikgowda21:nbM0WoXK2IUQGLcq@cluster0.oiyfvc4.mongodb.net/") as mongo_client:
    mongo_db = mongo_client["resumes"]
    collection = mongo_db["resumes"]

# In-memory database (replace this with an actual database in production)
users = {'hr': {'password': 'hr123'},
         'hiring_manager': {'password': 'manager123'},
         'interviewer': {'password': 'interviewer123'},
         'user1': {'password': 'user123'},
         'user2': {'password': 'user123'},
         'user3': {'password': 'user123'}}

resumes = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    if username in users and users[username]['password'] == password:
        return redirect(url_for('dashboard', user_type=username))
    else:
        flash('Invalid credentials. Please try again.')
        return redirect(url_for('index'))

@app.route('/upload_resume')
def upload_resume():
    # Your logic for uploading a resume
    return render_template('upload_resume.html')

@app.route('/hr_dashboard')
def hr_dashboard():
    # Retrieve data from MongoDB
    cursor = collection.find()
    processed_data = [document for document in cursor]

    # Render the template with the data
    return render_template('hr_dashboard.html', mongo_data=processed_data)

@app.route('/dashboard/<user_type>', methods=['GET', 'POST'])
def dashboard(user_type):
    if request.method == 'POST':
        # Handle resume upload
        resume_data = {
            'name': request.form['name'],
            'job_description': request.form['job_description'],
            'deadline': request.form['deadline']
        }

        # Implement AI/ML logic here to shortlist and delete duplicates

        resumes.append(resume_data)
        flash('Resume added successfully.')

    if user_type == 'hr':
        return render_template('hr_dashboard.html', resumes=resumes)
    elif user_type == 'hiring_manager':
        return render_template('hiring_manager_dashboard.html', resumes=resumes)
    else:
        return render_template('user_dashboard.html', resumes=resumes)

if __name__ == '__main__':
    app.run(debug=True)
