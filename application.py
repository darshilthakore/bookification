import os

from flask import Flask, session, render_template, request, redirect, url_for, flash
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


@app.route("/", methods=["POST","GET"])
def index():
	# if request.method == "POST":
	# 	name = request.form.get("name")
	# 	username = request.form.get("username")
	# 	password = request.form.get("password")
	return render_template("index.html")

@app.route("/newuser", methods=["POST"])
def newuser():
	name = request.form.get("name")
	username = request.form.get("username")
	password = request.form.get("password")
	if db.execute("SELECT username FROM users WHERE username = :username", {"username": username}).rowcount != 0:
		return render_template("error.html", message="Username already exists, try another", prompt="alert alert-danger")

	db.execute("INSERT INTO users (name, username, password) VALUES (:name, :username, :password)", {"name": name, "username": username, "password": password})
	db.commit()
	return render_template("error.html", message="Successfull registered", prompt="alert alert-success")



@app.route("/home", methods=["POST","GET"])
def home():
	page = 1
	return render_template("home.html", page=page)



@app.route("/login", methods=["POST"])
def login():

	username = request.form.get("username")
	password = request.form.get("password")
	res = db.execute("SELECT username FROM users WHERE username=:username AND password=:password", {"username": username, "password": password}).fetchone()
	if res:
		if res[0] == username:
			session['username'] = username
			return redirect(url_for('home'))
		return render_template("error.html", message="username or password is incorrect",prompt="alert alert-warning")
	# flash("Login unsucessful!")
	# return redirect(url_for('index'))		
	return render_template("error.html", message="username or password is incorrect",prompt="alert alert-warning")


@app.route("/logout")
def logout():
	session.pop('username',None)
	return redirect(url_for('index'))

@app.route("/register", methods=["POST"])
def register():
	return redirect(url_for('newuser'))



@app.route("/search/<int:pageno>", methods=["POST","GET"])
def search(pageno):
	if request.method == "POST":
		search_text = request.form.get("search")
		items_per_page = 20
		page = pageno
		if search_text == '':
			books = db.execute("SELECT * FROM books").fetchall()
			start_pos = 0 if page == 1 else items_per_page*(page-1)
			return render_template("books.html", page=page, books=books, start_pos=start_pos, items_per_page=items_per_page)
		books = db.execute("SELECT * from books WHERE isbn LIKE '%:search_text%' OR title LIKE '%:search_text%' OR author LIKE '%:search_text%'", {"search_text": search_text})  

@app.route("/next/<int:pageno>")
def next(pageno):
	page = pageno
	items_per_page = 20
	books = db.execute("SELECT * FROM books").fetchall()
	start_pos = 0 if page == 1 else items_per_page*(page-1)
	return render_template("books.html", page=page, books=books, start_pos=start_pos, items_per_page=items_per_page)

@app.route("/review", methods=["POST","GET"])
def review():
	return render_template("review.html")


