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

@app.route("/", methods=['GET', 'POST'])
def index():
    if 'username' in session:
        if request.method == 'POST':
            search = request.form.get('search')
            books = db.execute(f"SELECT * FROM books WHERE CAST(year AS VARCHAR) LIKE '%{search}%' OR isbn LIKE '%{search}%' OR UPPER(title) LIKE UPPER('%{search}%') OR UPPER(author) LIKE UPPER('%{search}%')").fetchall()
        else:
            books = db.execute("SELECT * FROM books").fetchmany(30)
        return render_template('books.html', username=session['username'], books=books)
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
            errors.append('Passwords do not match')
            return render_template('sign-up.html', errors=errors)
        if db.execute("SELECT * FROM users WHERE username = :username", {"username":username}).rowcount != 0:
            errors.append('User already exists')
            return render_template('sign-up.html', errors=errors)
        db.execute("INSERT INTO users (username, password) VALUES (:username, :password)",{"username":username, "password":password})
        db.commit()
        session['username'] = username
        return redirect(url_for('index'))
    return render_template('sign-up.html', errors=errors)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/<string:book_isbn>', methods=['POST', 'GET'])
def book(book_isbn):
    errors = []
    if db.execute("SELECT * FROM books WHERE isbn = :book_isbn", {"book_isbn":book_isbn}).rowcount == 0:
        return 'Error 404: Not found', 404
    book = db.execute("SELECT * FROM books WHERE isbn = :book_isbn", {"book_isbn":book_isbn}).fetchone()
    if request.method == "POST":
        try:
            user_id = db.execute("SELECT id FROM users WHERE username = :username", {"username":session['username']}).fetchone().id
            if db.execute("SELECT * FROM reviews WHERE user_id = :user_id AND book_id = :book_id", {"user_id":user_id, "book_id":book.id}).rowcount == 0:
                rate = request.form.get('rate')
                title = request.form.get('title')
                opinion = request.form.get('opinion')
                db.execute("INSERT INTO reviews (rate, opinion, user_id, book_id, title) VALUES (:rate, :opinion, :user_id, :book_id, :title)", {"rate":rate, "opinion":opinion, "user_id":user_id, "book_id":book.id, "title":title})
                db.commit()
            errors.append("Error: You already reviewed this book!")
        except KeyError:
            errors.append("Error: Empty fields")
    if db.execute("SELECT * FROM reviews WHERE book_id = :book_id", {"book_id":book.id}).rowcount==0:
        return render_template('book.html', book=book, errors=errors)
    n_reviews = db.execute("SELECT COUNT(*) FROM reviews WHERE book_id = :book_id", {"book_id":book.id}).fetchone().count
    rating = round(float(db.execute("SELECT AVG(rate) FROM reviews WHERE book_id = :book_id", {"book_id":book.id}).fetchone().avg), 2)
    reviews = db.execute("SELECT reviews.rate, reviews.opinion, users.username, reviews.title FROM reviews INNER JOIN users ON reviews.user_id = users.id WHERE book_id = :book_id;", {"book_id":book.id}).fetchall()
    return render_template('book.html', book=book, n_reviews=n_reviews, rating=rating, reviews=reviews, errors=errors)
