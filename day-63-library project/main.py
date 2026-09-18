import os
from flask import Flask, render_template, request, redirect, url_for, request
from wtforms import StringField, SubmitField
from flask_wtf import FlaskForm
from wtforms.fields.numeric import IntegerRangeField, IntegerField, FloatField
from wtforms.validators import DataRequired, InputRequired, ValidationError, NumberRange
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Float

'''
Red underlines? Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''

class BookForm(FlaskForm):
    title = StringField("Book Name", [DataRequired()])
    author = StringField("Book Author", [DataRequired()])
    rating = FloatField("Rating", [InputRequired(), NumberRange(min=0, max=10)])

class Rating_Form(FlaskForm):
    rating = FloatField("Rating", [InputRequired(), NumberRange(0, 10)])
    submit = SubmitField("Change Rating")

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(64)

# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///books-collection.db"
# initialize the app with the extension
db.init_app(app)

class Book(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(unique=True, nullable=False, type_=String(250))
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    rating: Mapped[float] = mapped_column(nullable=False, type_=Float())

with app.app_context():
    db.create_all()

"""
.fetchall() returns a list of rows by default
.scalar() returns the first or instance found that matches the criteria, doesnt return a row, returns a scalar
.scalars() returns a sort or set of rows that when you use .fetchall() it returns a list of scalar objects (meaning not rows)
"""

@app.route('/')
def home():
    # query_result = db.session.execute(db.select(Book).order_by(Book.title)).fetchall()[0]
    # print(query_result, type(query_result), query_result)
    results: list[Book] = db.session.execute(db.select(Book).order_by(Book.title)).scalars().fetchall()
    return render_template("index.html", books=results)
    pass


@app.route("/add", methods=["POST", "GET"])
def add():
    book_form = BookForm()
    if book_form.validate_on_submit():
        form_data = {
            field.name: field.data for field in book_form if not field.type in ("CSRFTokenField", "SubmitField")
        }
        # print(form_data)
        new_book = Book(**form_data)
        db.session.add(new_book)
        db.session.commit()

        return redirect(url_for('home'))

    return render_template("add.html", form=book_form)

@app.route("/delete", methods=['GET'])
def delete():
    _id = request.args.get("id", "Flask")
    book_to_delete: Book = db.session.execute(db.select(Book).where(Book.id == _id)).scalar()
    db.session.delete(book_to_delete)
    db.session.commit()

    return redirect("/")


@app.route('/edit', methods=["POST", "GET"])
def edit_rating():
    _id = request.args.get("id", "Flask")
    form = Rating_Form()
    book_to_update:Book = db.session.execute(db.select(Book).where(Book.id == _id)).scalar()
    # request.form
    # print(request.args.to_dict()) #output: {'id': '1'}
    # all_books.

    # if request.method == "POST":

    if form.validate_on_submit():
        input_rating:float = form.rating.data
        # print(input_rating)
        book_to_update.rating = input_rating
        db.session.commit()

        return redirect(url_for('home'))

    return render_template("edit.html", book=book_to_update, form=form)
    pass


if __name__ == "__main__":
    app.run(debug=True)

