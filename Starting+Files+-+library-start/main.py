from flask import Flask, render_template, request, redirect, url_for
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
        return f'{self.title}-{self.author}-{self.rating}'

# create
def create_book(title, author, rating):
    with app.app_context():
        book = Book( title=title,author=author,rating=rating)
        db.session.add(book)
        db.session.commit()
    print("clear")

# read
# with app.app_context():
#     # all
#     all_books = db.session.query(Book).all()
#     # particular
#     book = Book.query.filter_by(title="Harry Potter").first()
    

def update(book,rating):
    with app.app_context():
        book_update = Book.query.get(book.id)
        book_update.rating = rating
        db.session.commit()

# delete
def delete(book_id):
    with app.app_context():
        book_to_delete = Book.query.get(book_id)
        db.session.delete(book_to_delete)
        db.session.commit()


@app.route('/')
def home():
    with app.app_context():
        all_books = db.session.query(Book).all()
    return render_template('index.html',books = all_books)

@app.route("/add",methods=["POST","GET"])
def add():
    if request.method == "POST":
        title = request.form["title"]
        author = request.form["author"]
        rating = request.form["rating"]
        create_book(title,author,rating)
        return redirect(url_for('home'))
    
    return render_template('add.html')

@app.route('/edit_book/<int:book_id>', methods=["POST", "GET"])
def edit(book_id):
    # book_id = request.args.get('book_id')
    book = db.session.query(Book).get(book_id)
    if request.method == "POST":
        rating = request.form["rating"]
        if book:
            update(book, rating)
            return redirect(url_for('home'))

    return render_template('edit.html', current_book=book)

# @app.route("/edit", methods=["GET", "POST"])
# def edit():
#     if request.method == "POST":
#         #UPDATE RECORD
#         book_id = request.form["id"]
#         book_to_update = Book.query.get(book_id)
#         book_to_update.rating = request.form["rating"]
#         db.session.commit()
#         return redirect(url_for('home'))
#     book_id = request.args.get('id')
#     book_selected = Book.query.get(book_id)
#     return render_template("edit_rating.html", book=book_selected)




@app.route('/delete/<int:book_id>')
def delete_book(book_id):
    delete(book_id)
    return redirect(url_for('home'))



if __name__ == "__main__":
    app.run(debug=True)

