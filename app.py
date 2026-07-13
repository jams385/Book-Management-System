import os

from flask import Flask
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
    title = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)

    def __repr__(self):
        return "<Title: {}>".format(self.title)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.form:
        book = Book(title=request.form.get("title"))
        db.session.add(book)
        db.session.commit()

    books = Book.query.all()
    return render_template("home.html", books=books)
