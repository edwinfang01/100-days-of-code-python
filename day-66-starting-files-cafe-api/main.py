from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean, select, func

'''
Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''

app = Flask(__name__)

# CREATE DB
class Base(DeclarativeBase):
    pass
# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# Cafe TABLE Configuration
class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")

def to_dict(cafe):
    dictionary = cafe.__dict__
    dictionary.pop("_sa_instance_state")
    return dictionary

@app.route('/random')
def random():
    random_cafe = db.session.query(Cafe).order_by(func.random()).first()
    dictionary = to_dict(random_cafe)
    json_result = jsonify(dictionary) or jsonify(**dictionary) #both works ive tested them
    return json_result
    pass

@app.route('/get')
def get_all_cafes():
    all_cafes = db.session.query(Cafe)
    all_cafes = [to_dict(cafe) for cafe in all_cafes]
    return jsonify(all_cafes)

@app.route('/search')
def search():
    cafe_location = request.args.get("loc")
    result = db.session.query(Cafe).where(Cafe.location == cafe_location).all()
    result = [to_dict(cafe) for cafe in result]

    if not result:
        return jsonify(error={"Not found": "sorry we couldn't find any cafe at such location"}), 404

    return jsonify(result)

@app.route('/add', methods=["POST"])
def add():
    new_cafe = Cafe(
        name=request.form.get("name"),
        map_url=request.form.get("map_url"),
        img_url=request.form.get("img_url"),
        location=request.form.get("loc"),
        has_sockets=bool(request.form.get("sockets")),
        has_toilet=bool(request.form.get("toilet")),
        has_wifi=bool(request.form.get("wifi")),
        can_take_calls=bool(request.form.get("calls")),
        seats=request.form.get("seats"),
        coffee_price=request.form.get("coffee_price"),
    )
    db.session.add(new_cafe)
    db.session.commit()
    return jsonify(response={"success": "Successfully added the new cafe."})

@app.route('/update-price/<int:cafe_id>', methods=["PATCH"])
def update_price(cafe_id):
    cafe_to_patch = db.session.query(Cafe).where(Cafe.id == cafe_id).first()
    if not cafe_to_patch:
        return jsonify(error={"Not Found": "Sorry a cafe with that id was not found in the database."}), 404

    new_price = request.form.get("new_price")
    cafe_to_patch.coffee_price = new_price
    db.session.commit()
    return jsonify(success="Successfully updated the price.")

@app.route('/report-closed/<cafe_id>', methods=["DELETE"])
def delete_cafe(cafe_id):
    cafe_to_delete = db.session.query(Cafe).where(Cafe.id == cafe_id).first()
    if not cafe_to_delete:
        return jsonify(error={"Not Found": "Sorry a cafe with that id was not found in the database."}), 404

    api_key = request.args.get("api-key")
    if api_key != "TopSecretAPIKey":
        return jsonify(error={"Forbidden": "Sorry, that's not allowed. Make sure you have the correct api_key."}), 403

    db.session.delete(cafe_to_delete)
    db.session.commit()
    return jsonify(Success="Successfully deleted the cafe.")


# HTTP GET - Read Record

# HTTP POST - Create Record

# HTTP PUT/PATCH - Update Record

# HTTP DELETE - Delete Record


if __name__ == '__main__':
    app.run(debug=True)
