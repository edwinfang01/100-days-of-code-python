import os
import smtplib
from flask import Flask, render_template, request
import requests
from datetime import datetime
from dotenv import load_dotenv

app = Flask(__name__)
blog_posts: list[dict] = requests.get("https://api.npoint.io/9428afdeb098ff26b695").json()

CACTUS_IMAGE_LINK = "https://images.unsplash.com/photo-1517025423291-770fb99ae547?q=80&w=774&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
FISHING_IMAGE_LINK = "https://images.unsplash.com/photo-1787869200926-d8f1d923d3c1?q=80&w=770&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
SMOOTHIE_IMAGE_LINK = "https://images.unsplash.com/photo-1610970881699-44a5587cabec?q=80&w=774&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"

load_dotenv()
MY_EMAIL = os.getenv("MY_EMAIL")
MY_PASSWORD = os.getenv("MY_PASSWORD")

post_image_dict = {
    1: CACTUS_IMAGE_LINK,
    2: FISHING_IMAGE_LINK,
    3: SMOOTHIE_IMAGE_LINK
}

@app.route('/')
def home():
    return render_template("index.html", blog_posts=blog_posts)

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/contact')
def contact(method=None):
    return render_template("contact.html", method=method)

@app.route('/post/<int:post_id>')
def get_post(post_id):
    current_year = datetime.today().year
    input_post = next((post for post in blog_posts if post['id'] == post_id), None)
    return render_template("post.html", input_post=input_post, year=current_year, header_image=post_image_dict[post_id])

@app.route("/contact", methods=["POST", "GET"])
def receive_data():
    if request.method == "POST":
        request_info = request.form
        message = ""
        for key, value in request_info.items():
            # print(f"{key}: {value}")
            message += f"{key.title()}: {value}\n"

        with smtplib.SMTP('smtp.gmail.com') as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=MY_PASSWORD)
            connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs=MY_EMAIL,
                msg=f'Subject: New Message\n\n{message}'
            )

        return contact(method="POST")

    return contact()

if __name__ == "__main__":
    app.run(debug=True)