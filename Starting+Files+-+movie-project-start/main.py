from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import FloatField, StringField, SubmitField
from wtforms.validators import DataRequired
import requests

url = "https://api.themoviedb.org/3/search/movie"
headers = {
    "accept": "application/json",
    "Authorization": "Bearer your key"
}



app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///my-top-10-movies.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Movie(db.Model):
    id      = db.Column(db.Integer, primary_key=True)
    title   = db.Column(db.String(30), nullable=False)
    year    = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(250), nullable=False)
    rating  = db.Column(db.Float, nullable=False)
    ranking = db.Column(db.Integer)
    review  = db.Column(db.String(100))
    img_url = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Movie {self.title}>'

class RateMovieForm(FlaskForm):
    rating = FloatField('Your Rating Out of 10 e.g. 7.5',validators=[DataRequired()])
    review = StringField('Your Review',validators=[DataRequired()])
    submit = SubmitField('Done')

class RegisterMovieForm(FlaskForm):
    title  = StringField('Movie Title',validators=[DataRequired()])
    submit = SubmitField('Add Movie')


@app.route("/")
def home():
    with app.app_context():
        all_movies = Movie.query.order_by(Movie.rating).all()
        for i in range(len(all_movies)):
            all_movies[i].ranking = len(all_movies) - i
    return render_template("index.html",movies=all_movies)

@app.route("/edit_movie",methods=["POST","GET"])
def edit_movie():
    movie_form = RateMovieForm()
    movie_id = request.args.get('movie_id')
    movie = db.session.query(Movie).get(movie_id)
    if movie_form.validate_on_submit():
        movie.rating = float(movie_form.rating.data)
        movie.review = movie_form.review.data
        db.session.commit()
        return redirect(url_for('home'))

    return render_template("edit.html",movie=movie,form=movie_form)

@app.route("/delete")
def delete_movie():
    movie_id = request.args.get('movie_id')
    movie = db.session.query(Movie).get(movie_id)
    db.session.delete(movie)
    db.session.commit()
    return redirect(url_for('home'))

@app.route("/add",methods=["POST","GET"])
def add_movie():
    form = RegisterMovieForm()
    if form.validate_on_submit():
        param = {'query':f'{form.title.data}','page':1}
        response = requests.get(url, headers=headers,params=param)
        return render_template("select.html",movies=response.json()["results"])

    return render_template("add.html",form=form)

@app.route("/select")
def select_movie():
    title = request.args.get('title')
    year = request.args.get('year').split('-')[0]
    description = request.args.get('description')
    rating = request.args.get('rating')
    img_url = "https://image.tmdb.org/t/p/w500"+request.args.get('img_url')
    movie= Movie(title=title,year=year,description=description,rating=rating,img_url=img_url)
    db.session.add(movie)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
