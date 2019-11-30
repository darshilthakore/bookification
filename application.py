import os
import requests
import json

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
	return render_template("register.html")

@app.route("/search/<int:pageno>", methods=["POST","GET"])
def search(pageno):
	if request.method == "POST":
		search_text = request.form.get("search")
		search_text = '%' + search_text + '%'
		page = pageno
		items_per_page = 20
		start_pos = 1 if page == 1 else items_per_page*(page-1)+1
				
		books = db.execute("SELECT *, ROW_NUMBER() OVER() searchid FROM books WHERE (isbn LIKE :search_text OR title LIKE :search_text OR author LIKE :search_text)",{"search_text":search_text}).fetchall()
		total_results = len(books)
		books = books[start_pos-1:start_pos+19]
		return render_template("books.html", books=books,page=page, search_text=search_text,total_results=total_results)
		# books = db.execute("SELECT * from books WHERE isbn LIKE '%:search_text%' OR title LIKE '%:search_text%' OR author LIKE '%:search_text%'", {"search_text": search_text}).fetchall()  



@app.route("/next/<int:pageno>&<search_text>")
def next(pageno,search_text):
	page = pageno
	items_per_page = 20
	start_pos = 1 if page == 1 else items_per_page*(page-1)+1
	books = db.execute("SELECT *, ROW_NUMBER() OVER() searchid FROM books WHERE (isbn LIKE :search_text OR title LIKE :search_text OR author LIKE :search_text)",{"search_text":search_text}).fetchall()
	total_results=len(books)
	books = books[start_pos-1:start_pos+19]
	return render_template("books.html", page=page, books=books, search_text=search_text,total_results=total_results)



@app.route("/review/<isbn>")
def review(isbn):	
	# params = {"isbns":isbn,"key":"2j7EUzQg96bbhWH9tyuv7A"}
	r = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "2j7EUzQg96bbhWH9tyuv7A", "isbns": isbn})
	if r.status_code != 200:
		raise Exception("ERROR: API request unsuccessful.")

	data = r.json()
	book = db.execute("SELECT isbn, title, author, year FROM books WHERE isbn = :isbn", {"isbn":isbn}).fetchone()

	return render_template("review.html",data=data,book=book)


@app.route("/review/<isbn>/success", methods=["POST","GET"])
def post_review(isbn):
	if request.method == "POST":
		review = request.form.get("user_review")
		rating = request.form.get("rating")
		isbn = isbn
		if 'username' in session:
			username = session['username']
			if db.execute("SELECT isbn FROM reviews WHERE username = :username AND isbn = :isbn", {"username":username,"isbn":isbn}).rowcount != 0:
				return render_template("success.html", message="User has already posted a review for this book",isbn=isbn)
			db.execute("INSERT INTO reviews (username, isbn, review, rating) VALUES (:username, :isbn, :review, :rating)", {"username":username,"isbn":isbn,"review":review,"rating":rating})
			db.commit()
			return render_template("success.html", message="Review posted Successfully",isbn=isbn)

@app.route("/review/<isbn>")
def back():
	return redirect(url_for('review',isbn))