import os
from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.mysql import VARCHAR
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields.numeric import FloatField
from wtforms.validators import DataRequired, InputRequired, NumberRange, Length
import requests
from dotenv import load_dotenv

load_dotenv()

'''
Red underlines? Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)

# CREATE DB
class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///movie-collection.db"

# CREATE TABLE
db.init_app(app=app)

class Movie(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(VARCHAR(100), unique=True, nullable=False)
    year: Mapped[int] = mapped_column(Integer)
    description: Mapped[str] = mapped_column(VARCHAR(500), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=True)
    ranking: Mapped[int] = mapped_column(Integer, nullable=True)
    review: Mapped[str] = mapped_column(VARCHAR(500))
    img_url: Mapped[str] = mapped_column(VARCHAR(500), nullable=False)

with app.app_context():
    db.create_all()

first_movie = Movie(
    title = "Phone Booth",
    year = 2002,
    description="Publicist Stuart Shepard finds himself trapped in a phone booth, "
                "pinned down by an extortionist's sniper rifle. "
                "Unable to leave or receive outside help, "
                "Stuart's negotiation with the caller leads to a jaw-dropping climax.",
    rating=7.3,
    ranking=10,
    review="My favourite character was the caller.",
    img_url = "https://image.tmdb.org/t/p/w500/tjrX2oWRCM3Tvarz38zlZM7Uc10.jpg"
)

second_movie = Movie(
    title="Avatar The Way of Water",
    year=2022,
    description="Set more than a decade after the events of the first film, learn the story of the Sully family (Jake, Neytiri, and their kids), the trouble that follows them, the lengths they go to keep each other safe, the battles they fight to stay alive, and the tragedies they endure.",
    rating=7.3,
    ranking=9,
    review="I liked the water.",
    img_url="https://image.tmdb.org/t/p/w500/t6HIqrRAclMCA60NsSmeqe9RmNV.jpg"
)

"""
whenever you use db.session you need app context
"""

# with app.app_context():
#     db.session.add(second_movie)
#     # book_to_delete = db.get_or_404(entity=Movie, ident=2)
#     # db.session.delete(book_to_delete)
#     db.session.commit()

class RateMovieForm(FlaskForm):
    rating = FloatField(label="Your Rating Out of 10 e.g. 7.5", validators=[InputRequired(), NumberRange(0, 10)])
    review = StringField("Your Review", validators=[InputRequired(), Length(1, 500)])
    submit = SubmitField("Done")

class AddMovieForm(FlaskForm):
    title = StringField("Movie Title", validators=[InputRequired(), Length(1, 500)])
    submit = SubmitField("Add Movie")

@app.route('/edit', methods=["GET", "POST"])
def edit():
    form = RateMovieForm()
    movie_id = request.args.get("id")
    input_rating = form.rating.data # or request.form['rating']
    input_review = form.review.data
    if form.validate_on_submit():
        movie_to_update = db.get_or_404(entity=Movie, ident=movie_id)
        movie_to_update.rating = input_rating
        movie_to_update.review = input_review
        db.session.commit()

        return redirect(url_for('home'))

    return render_template("edit.html", form=form)

@app.route('/delete')
def delete():
    movie_id = request.args.get("id")
    movie_to_delete = db.get_or_404(entity=Movie, ident=movie_id)
    db.session.delete(movie_to_delete)
    db.session.commit()

    return redirect(url_for('home'))

headers = {
    "Authorization": f"Bearer {os.getenv('TMDB_API')}"
}

@app.route('/add', methods=["POST", "GET"])
def add():
    form = AddMovieForm()
    if form.validate_on_submit():
        movie_title = request.form['title']
        movie_results = requests.get("https://api.themoviedb.org/3/search/movie", params={'query': movie_title},
                                     headers=headers).json()

        return render_template("select.html", results=movie_results['results'])

    movie_id = request.args.get("id")
    if movie_id:
        movie_details = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}", headers=headers).json()
        new_movie = Movie(title=movie_details['title'],
                          description=movie_details['overview'],
                          year=int( movie_details['release_date'].split('-')[0] ) if movie_details['release_date'] else None,
                          review="",
                          img_url=f"https://image.tmdb.org/t/p/original{movie_details['poster_path']}"
                          )
        # print(new_movie.id) #output: None
        db.session.add(new_movie)
        db.session.commit()
        # print(new_movie.id) # after commit() it creates an id
        return redirect(url_for('edit', id=new_movie.id))

    return render_template('add.html', form=form)

@app.route("/")
def home():
    movies = db.session.execute(db.select(Movie).order_by(Movie.rating)).scalars().all()
    movies = list(reversed(movies))
    for index, movie in enumerate(movies):
        movie.ranking = index+1
        # print(movie.rating)

    return render_template("index.html", movies=movies)


if __name__ == '__main__':
    app.run(debug=True)
