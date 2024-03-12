from flask import Flask, jsonify, render_template, request, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap5
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean, func
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)

# API Documentation: https://documenter.getpostman.com/view/9502157/2sA2xiWrhE

# CREATE DB
class Base(DeclarativeBase):
    pass


# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)
Bootstrap5(app)

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

    def to_dict(self) -> dict:
        return {
            column.name: getattr(self, column.name) for column in self.__table__.columns
        }


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")


# HTTP GET - Read Record
@app.route("/random", methods=["GET"])
def random():
    cafe = db.session.execute(db.select(Cafe).order_by(func.random())).scalar()
    return jsonify(cafe=cafe.to_dict())


@app.route("/all", methods=["GET"])
def all():
    cafes = db.session.execute(db.select(Cafe)).scalars().all()
    return jsonify(cafes=[cafe.to_dict() for cafe in cafes])


@app.route("/search", methods=["GET"])
def search():
    location = request.args.get("loc")
    cafes = (
        db.session.execute(db.select(Cafe).where(Cafe.location == location))
        .scalars()
        .all()
    )
    if not cafes:
        body = jsonify(
            error={"Not Found": "Sorry, we don't have a cafe at that location."}
        )
        return make_response(body, 404)  # Not Found
    else:
        return jsonify(cafes=[cafe.to_dict() for cafe in cafes])


# HTTP POST - Create Record
@app.route("/add", methods=["POST"])
def add():
    try:
        new_cafe = Cafe(
            name=request.form["name"],
            map_url=request.form["map_url"],
            img_url=request.form["img_url"],
            location=request.form["location"],
            seats=request.form["seats"],
            has_toilet=bool(request.form["has_toilet"]),
            has_wifi=bool(request.form["has_wifi"]),
            has_sockets=bool(request.form["has_sockets"]),
            can_take_calls=bool(request.form["can_take_calls"]),
            coffee_price=request.form["coffee_price"],
        )
        db.session.add(new_cafe)
        db.session.commit()
    except KeyError:
        body = jsonify(
            error={"Invalid Request": "Please provide all the required keys."}
        )
        return make_response(body, 400)  # Bad Request
    except IntegrityError:
        db.session.rollback()
        body = jsonify(
            error={"Invalid Request": "A cafe with that name already exists."}
        )
        return make_response(body, 409)  # Conflict
    else:
        return jsonify(response={"success": "Successfully added the new cafe."})


# HTTP PUT/PATCH - Update Record
@app.route("/update-price/<int:cafe_id>", methods=["PATCH"])
def update_price(cafe_id):
    cafe = db.session.get(Cafe, cafe_id)
    if cafe:
        new_price = request.args.get("coffee_price")
        if new_price:
            cafe.coffee_price = new_price
            db.session.commit()
            return jsonify(response={"success": "Successfully updated the price."})
        else:
            body = jsonify(
                error={"Invalid Request": "Please provide the coffee_price key."}
            )
            return make_response(body, 400)
    else:
        body = jsonify(error={"Not Found": "Sorry, we don't have a cafe with that ID."})
        return make_response(body, 404)

# HTTP DELETE - Delete Record
@app.route("/report-closed/<int:cafe_id>", methods=["DELETE"])
def report_closed(cafe_id):
    cafe = db.session.get(Cafe, cafe_id)
    if cafe:
        api_key = request.args.get("api_key")
        if api_key == "TopSecretAPIKey":
            db.session.delete(cafe)
            db.session.commit()
            return jsonify(response={"success": "Successfully reported the cafe as closed."})
        else:
            body = jsonify(error={"Unauthorized": "Sorry, that is not allowed. Make sure you have the correct api_key"})
            return make_response(body, 401)
    else:
        body = jsonify(error={"Not Found": "Sorry, we don't have a cafe with that ID."})
        return make_response(body, 404)

if __name__ == '__main__':
    app.run(debug=True)
