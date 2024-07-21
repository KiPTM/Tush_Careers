from flask import Flask, render_template, redirect, url_for, flash, request, jsonify, session
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_migrate import Migrate
from extensions import db
from models import User, Job
import logging

app = Flask(__name__)
app.config['SECRET_KEY'] = 'M!@#$t33178250'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    jobs = Job.query.all()
    return render_template('home.html', jobs=jobs, company_name='Kratos')

@app.route("/api/jobs")
def list_jobs():
    jobs = Job.query.all()
    return jsonify([job.as_dict() for job in jobs])

@app.route("/api/jobs/<int:job_id>")
def get_job(job_id):
    job = Job.query.get_or_404(job_id)
    return jsonify(job.as_dict())

@app.route("/apply/<int:job_id>")
def apply(job_id):
    if not current_user.is_authenticated:
        session['next_job_id'] = job_id
        return redirect(url_for('login'))
    job = Job.query.get_or_404(job_id)
    return render_template('application.html', job=job)

@app.route("/register", methods=['GET', 'POST'])
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

@app.route("/login", methods=['GET', 'POST'])
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

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    app.run(host='0.0.0.0', debug=True)
