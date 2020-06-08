import os

from flask import Flask, session, request, render_template, redirect, url_for
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

@app.route("/")
def index():
    if 'username' in session:
        return render_template('books.html', username=session['username'])
    return redirect(url_for('signin'))

@app.route("/signin", methods=['GET', 'POST'])
def signin():
    errors = []
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if db.execute("SELECT * FROM users WHERE username = :username AND password = :password", {"username":username, "password":password}).rowcount == 0:
            errors.append('Username or password incorrect')
            return render_template('sign-in.html', errors=errors)
        session['username'] = username
        return redirect(url_for('index'))
    return render_template('sign-in.html', errors=errors)

@app.route('/sign-up', methods=['GET', 'POST'])
def signup():
    errors = []
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        password_conf = request.form.get('password_conf')
        if password != password_conf:
            errors.append('Passwords do not concuerd')
            return render_template('sign-up.html', errors=errors)
        if db.execute("SELECT * FROM users WHERE username = :username", {"username":username}).rowcount != 0:
            errors.append('User already exists')
            return render_template('sign-up.html', errors=errors)
        db.execute("INSERT INTO users (username, password) VALUES (:username, :password)",{"username":username, "password":password})
        db.commit()
        session['username'] = username
        return redirect(url_for('index'))
    return render_template('sign-up.html', errors=errors)
