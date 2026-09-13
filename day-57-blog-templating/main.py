from flask import Flask, render_template
import requests
# from post import Post


app = Flask(__name__)

posts_list = requests.get("https://api.npoint.io/9428afdeb098ff26b695").json()
# for post in posts_list:
#     Post(post['id'], post['title'], post['subtitle'], post['body'])

@app.route('/')
def home():
    return render_template("index.html", posts=posts_list)

@app.route('/post/<int:post_id>')
def post(post_id):
    input_post = next((post for post in posts_list if post['id'] == post_id), None)
    return render_template("post.html", post=input_post)


if __name__ == "__main__":
    app.run(debug=True)
