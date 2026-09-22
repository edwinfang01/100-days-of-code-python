from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_ckeditor.utils import cleanify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text
from flask_wtf import FlaskForm
from sqlalchemy.orm.attributes import set_attribute
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL, InputRequired
from flask_ckeditor import CKEditor, CKEditorField
from datetime import datetime as dt
from flask_ckeditor.utils import cleanify

'''
Make sure the required packages are installed: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from the requirements.txt for this project.
'''

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)

# CREATE DATABASE
class Base(DeclarativeBase):
    pass
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)
ckeditor = CKEditor(app)


# CONFIGURE TABLE
class BlogPost(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    subtitle: Mapped[str] = mapped_column(String(250), nullable=False)
    date: Mapped[str] = mapped_column(String(250), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)

with app.app_context():
    db.create_all()

class CreatePostForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[InputRequired()])
    subtitle = StringField("Subtitle", validators=[InputRequired()])
    author = StringField("Your Name", validators=[InputRequired()])
    img_url = StringField("Blog Image URL", validators=[InputRequired(), URL()])
    body = CKEditorField("Blog Content", validators=[InputRequired()])
    submit = SubmitField("Submit Post")

@app.route('/')
def get_all_posts():
    # TODO: Query the database for all the posts. Convert the data to a python list.
    posts:list[BlogPost] = db.session.query(BlogPost)
    return render_template("index.html", all_posts=posts)

# TODO: Add a route so that you can click on individual posts.
@app.route('/post/<int:post_id>')
def show_post(post_id):
    # TODO: Retrieve a BlogPost from the database based on the post_id
    print(post_id)
    requested_post = db.get_or_404(BlogPost, post_id)
    return render_template("post.html", post=requested_post)


# TODO: add_new_post() to create a new blog post
@app.route('/new-post', methods=["GET", "POST"])
def add_new_post():
    form = CreatePostForm()
    if request.method == "POST" or form.validate_on_submit():
        blog_data = request.form.to_dict()
        [blog_data.pop(key) for key in ('csrf_token', 'submit')]
        blog_body = cleanify(request.form.get('body'))
        blog_data.update({'body': blog_body, 'date': dt.today().strftime("%B %d %Y")})

        new_blog = BlogPost(**blog_data)
        db.session.add(new_blog)
        db.session.commit()
        return redirect(url_for('get_all_posts'))

    return render_template("make-post.html", form=form)


# TODO: edit_post() to change an existing blog post
@app.route("/edit-post/<int:post_id>", methods=["GET", "POST"])
def edit_post(post_id):
    post_to_edit = db.get_or_404(entity=BlogPost, ident=post_id)
    post_to_edit_data = post_to_edit.__dict__.copy()
    del post_to_edit_data['_sa_instance_state']
    form = CreatePostForm(**post_to_edit_data)

    if form.validate_on_submit() or request.method == "POST":
        for field in form:
            if field.name not in ('submit', 'csrf_token'):
                post_to_edit_data.update({field.name: field.data})

        for attribute, value in post_to_edit_data.items():
            if attribute == '_sa_instance_state':
                continue
            setattr(post_to_edit, attribute, value)

        db.session.commit()
        return redirect(url_for("show_post", post_id=post_id))

    return render_template("make-post.html", form=form)

# TODO: delete_post() to remove a blog post from the database
@app.route('/delete/<int:post_id>')
def delete_post(post_id):
    db.session.query(BlogPost).where(BlogPost.id == post_id).delete()
    db.session.commit()
    return redirect(url_for('get_all_posts'))

# Below is the code from previous lessons. No changes needed.
@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True, port=5003)
