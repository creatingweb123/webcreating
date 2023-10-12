# import sqlite3

# db = sqlite3.connect("books-collection.db")

# cursor = db.cursor()

# cursor.execute("CREATE TABLE books (id INTEGER PRIMARY KEY, title varchar(250) NOT NULL UNIQUE, author varchar(250) NOT NULL, rating FLOAT NOT NULL)")

# cursor.execute("INSERT INTO books VALUES(1, 'Harry Potter', 'J. K. Rowling', '9.3')")

# db.commit()
# ////////////////////////////////////////////

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///new-books-collection.db"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(250),unique=True, nullable=False)
    author=db.Column(db.String(250), nullable=False)
    rating=db.Column(db.Float, nullable=False)
    
    def __repr__(self):
        return f'<Book {self.title}>'


with app.app_context():
    db.create_all()
with app.app_context():
    book = Book(id=1, title='Columbus and Other Cannibals',author='Jack D.Forbes',rating=7.1)
    db.session.add(book)
    db.session.commit()