import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine("postgres://ranpflhaqmbzqy:42001e5fc1ba560ca03f1b063a4ac2cee61666009cf4e83b4ce28f99bf9a6d07@ec2-174-129-254-235.compute-1.amazonaws.com:5432/df30u59pp5l3lc")
db = scoped_session(sessionmaker(bind=engine))

def main():
	f = open("books.csv")
	reader = csv.reader(f)
	for isbn, title, author, year in reader:
		db.execute("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)",{"isbn": isbn, "title": title, "author": author, "year": year})
	db.commit()    

if __name__ == "__main__":
	main()