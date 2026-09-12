# import random
from flask import Flask

app = Flask(__name__)
# print(random.__name__)
# print(__name__)

def make_bold(function):
    def wrapper_function():
        return f"<b>{function()}</b>"
    return wrapper_function

def make_emphasis(function):
    def wrapper_function():
        return f"<em>{function()}</em>"
    return wrapper_function


def make_underlined(function):
    def wrapper_function():
        return f"<u>{function()}</u>"
    return wrapper_function

@app.route("/")
def hello_world():
    return ("<h1 style='text-align: center'>Hello, World!</h1>"
            "<p> This is a paragraph </p>"
            "<img src='https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExZ3dvNjBzcGJmdDFpaWtyNHl0c3d1dXQ3ZmJjemV1bGtnYjhzMmp2diZlcD12MV9naWZzX3RyZW5kaW5nJmN0PWc/MFsqcBSoOKPbjtmvWz/giphy.gif' width=200>")

@app.route("/bye")
@make_bold
@make_emphasis
@make_underlined
def say_bye():
    return "Bye"

@app.route("/username/<path:name>/<int:number>")
def greet(name, number):
    return f"Hello there {name}, you are {number} years old!"

if __name__ == "__main__":
    app.run(debug=True)

# # TODO: Create the logging_decorator() function 👇
# def logging_decorator(func):
#     def wrapper(*args):
#         print(f"You called {func.__name__}({args})")
#         print(f"it returned: {func(*args)}")
#
#     return wrapper
#
#
# # TODO: Use the decorator 👇
# @logging_decorator
# def a_function(*args):
#     return sum(args)
#
#
# a_function(1, 2, 3)