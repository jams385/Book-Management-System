import os

from flask import Flask, redirect
from flask import render_template
from flask import request

from flask_sqlalchemy import SQLAlchemy

executable_path = os.path.abspath(__file__)
project_dir = os.path.dirname(executable_path)

database_file = "sqlite:///{}".format(os.path.join(project_dir, "bookdatabase.db"))

app = Flask(__name__) 
app.config["SQLALCHEMY_DATABASE_URI"] = database_file 

db = SQLAlchemy(app) 

class Book(db.Model):
    __tablename__ = "Book Library"

    title = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)
    author = db.Column(db.String(50), nullable=False)
    publisher = db.Column(db.String(100), nullable=False)
    publication_date = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return "<Title: {}>".format(self.title)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.form:
        try:
            book = Book(title=request.form.get("title"),
                        author=request.form.get("author"),
                        publisher=request.form.get("publisher"),
                        publication_date=request.form.get("publication_date") )
            db.session.add(book)
            db.session.commit()

        except Exception as e:
            print("Failed to add book")
            print(e)

    books = Book.query.all()
    return render_template("home.html", books=books)

@app.route("/update", methods=["POST"])
def update():
    try:
        # update title

        old_title = request.form.get("old_title")
        book = Book.query.filter_by(title=old_title).first()

        new_title = request.form.get("new_title")
        new_author = request.form.get("new_author")
        new_publisher = request.form.get("new_publisher")

        if new_title is not '':
            book.title = new_title

        if new_author is not '':
            book.author = new_author
        
        if new_publisher is not '':
            book.publisher = new_publisher
        
        db.session.commit()

    except Exception as e:
        print("Cannot update book title")
    
    return redirect("/")

@app.route("/delete", methods=["POST"])
def delete():
    try:
        title = request.form.get("title")
        book = Book.query.filter_by(title=title).first()

        if book:
            db.session.delete(book)
            db.session.commit()
    except Exception as e:
        print("Cannot Delete Book")

    return redirect("/")