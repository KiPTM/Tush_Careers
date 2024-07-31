from flask import Flask, render_template, redirect, url_for, flash, request, jsonify, session
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_migrate import Migrate
from extensions import db
from models import User, Job
import logging
import os
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
from itsdangerous import URLSafeTimedSerializer

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Use environment variables for configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default_secret_key')  # Default value in case .env is not loaded
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://admin:your_password@localhost/site_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configuration for file uploads
app.config['UPLOAD_FOLDER'] = '/home/vagrant/Tush_Careers/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB limit

db.init_app(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

# Initialize the URLSafeTimedSerializer
serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    jobs = Job.query.all()
    return render_template('home.html', jobs=jobs, company_name='Kratos')

@app.route('/job/<int:job_id>')
def job_detail(job_id):
    job = Job.query.get_or_404(job_id)
    return render_template('job_detail.html', job=job)

@app.route('/apply/<int:job_id>', methods=['GET', 'POST'])
@login_required
def apply(job_id):
    job = Job.query.get_or_404(job_id)
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        highest_education = request.form.get('highest_education')
        institution = request.form.get('institution')
        company_name = request.form.get('company_name')
        job_title_experience = request.form.get('job_title_experience')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        cover_letter = request.form.get('cover_letter')

        if 'resume' not in request.files:
            flash('No resume part', 'danger')
            return redirect(request.url)
        resume = request.files['resume']
        if resume.filename == '':
            flash('No selected file', 'danger')
            return redirect(request.url)
        if resume and allowed_file(resume.filename):
            filename = secure_filename(resume.filename)
            resume.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # Save the form data to the database or perform other actions
        # Example: Save to a new Application model (you would need to create this model)
        # application = Application(first_name=first_name, last_name=last_name, ...)
        # db.session.add(application)
        # db.session.commit()

        flash('Your application has been submitted!', 'success')
        return redirect(url_for('home'))
    return render_template('application.html', job=job)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password != confirm_password:
            flash('Passwords do not match', 'danger')
            return redirect(url_for('register'))

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username=username, email=email, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = request.form.get('remember') is not None
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user, remember=remember)
            next_job_id = session.pop('next_job_id', None)
            if next_job_id:
                return redirect(url_for('apply', job_id=next_job_id))
            else:
                return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        if user:
            token = serializer.dumps(user.email, salt='password-reset-salt')
            reset_url = url_for('reset_password', token=token, _external=True)
            # Send the reset link via email
            # Example: send_email(user.email, reset_url)
            flash('A password reset link has been sent to your email address.', 'info')
        else:
            flash('Email address not found.', 'danger')
        return redirect(url_for('forgot_password'))
    return render_template('forgot_password.html')

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    try:
        email = serializer.loads(token, salt='password-reset-salt', max_age=3600)
    except:
        flash('The password reset link is invalid or has expired.', 'danger')
        return redirect(url_for('forgot_password'))
    
    if request.method == 'POST':
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password != confirm_password:
            flash('Passwords do not match', 'danger')
            return redirect(url_for('reset_password', token=token))

        user = User.query.filter_by(email=email).first()
        if user:
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            user.password = hashed_password
            db.session.commit()
            flash('Your password has been updated!', 'success')
            return redirect(url_for('login'))
        else:
            flash('User not found.', 'danger')
            return redirect(url_for('forgot_password'))
    
    return render_template('reset_password.html', token=token)

@app.route('/debug')
def debug():
    jobs = Job.query.all()
    return jsonify([job.as_dict() for job in jobs])

@app.route('/api/jobs')
def list_jobs():
    jobs = Job.query.all()
    return jsonify([job.as_dict() for job in jobs])

@app.route('/api/jobs/<int:job_id>')
def get_job(job_id):
    job = Job.query.get_or_404(job_id)
    return jsonify(job.as_dict())

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'pdf', 'doc', 'docx'}

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    app.run(host='0.0.0.0', debug=True)

