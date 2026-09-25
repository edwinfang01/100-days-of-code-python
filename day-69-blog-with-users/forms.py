from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields.simple import PasswordField, EmailField
from wtforms.validators import URL, InputRequired, Length
from flask_ckeditor import CKEditorField


# WTForm for creating a blog post
class CreatePostForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[InputRequired()])
    subtitle = StringField("Subtitle", validators=[InputRequired()])
    img_url = StringField("Blog Image URL", validators=[InputRequired(), URL()])
    body = CKEditorField("Blog Content", validators=[InputRequired()])
    submit = SubmitField("Submit Post")


# TODO: Create a RegisterForm to register new users
class RegisterForm(FlaskForm):
    email = EmailField("Email", validators=[InputRequired(), Length(1, 50)])
    password = PasswordField("Password", validators=[InputRequired(), Length(1, 50)])
    name = StringField("Name", validators=[InputRequired(), Length(1, 50)])
    submit = SubmitField("SIGN ME UP")

# TODO: Create a LoginForm to login existing users
class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[InputRequired(), Length(1, 50)])
    password = PasswordField("Password", validators=[InputRequired(), Length(1, 50)])
    submit = SubmitField("LET ME IN")

# TODO: Create a CommentForm so users can leave comments below posts
class CommentForm(FlaskForm):
    comment = CKEditorField("Comment", validators=[InputRequired()])
    submit = SubmitField("SUBMIT COMMENT")