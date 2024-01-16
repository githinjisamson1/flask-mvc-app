from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate
from models import db, Hero, HeroPower, Power
from flask_restful import Api, Resource

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)


class Index(Resource):
    def get(self):
        return make_response("<h1>Welcome to Superheroes API</h1>", 200)


api.add_resource(Index, "/")


class Heroes(Resource):
    # !GET heroes
    def get(self):
        heroes_lc = [hero.to_dict() for hero in Hero.query.all()]

        response = make_response(jsonify(heroes_lc), 200)

        response.headers["Content-Type"] = "application/json"

        return response

    # !POST heroes
    def post(self):
        data = request.get_json()

        new_hero = Hero(
            name=data["name"],
            super_name=data["super_name"]
        )

        db.session.add(new_hero)
        db.session.commit()

        new_hero_dict = new_hero.to_dict()

        response = make_response(jsonify(new_hero_dict), 201)

        response.headers["Content-Type"] = "application/json"

        return response


api.add_resource(Heroes, "/heroes")


# !if hero not in database/DRY
def hero_not_found():

    response_body = {
        "error": "Hero not found"
    }

    response = make_response(jsonify(response_body), 400)

    response.headers["Content-Type"] = "application/json"

    return response


class HeroById(Resource):
    # !GET hero
    def get(self, hero_id):
        hero = Hero.query.filter_by(id=hero_id).first()

        if not hero:
            return hero_not_found()

        hero_dict = hero.to_dict()

        response = make_response(jsonify(hero_dict), 200)

        response.headers["Content-Type"] = "application/json"

        return response

    # !PATCH hero
    def patch(self, hero_id):
        data = request.get_json()

        hero = Hero.query.filter_by(id=hero_id).first()

        if not hero:
            return hero_not_found()

        for attr in data:
            setattr(hero, attr, data.get(attr))

        db.session.commit()

        hero_dict = hero.to_dict()

        response = make_response(jsonify(hero_dict), 200)

        response.headers["Content-Type"] = "application/json"

        return response

    # !DELETE hero
    def delete(self, hero_id):
        hero = Hero.query.filter_by(id=hero_id).first()

        if not hero:
            return hero_not_found()

        db.session.delete(hero)
        db.session.commit()

        response_body = {
            "success": True,
            "message": "Hero deleted"
        }

        response = make_response(jsonify(response_body), 200)

        response.headers["Content-Type"] = "application/json"

        return response


api.add_resource(HeroById, "/heroes/<int:hero_id>")


class Powers(Resource):
    # !GET powers
    def get(self):
        powers_lc = [power.to_dict() for power in Power.query.all()]

        response = make_response(jsonify(powers_lc), 200)

        response.headers["Content-Type"] = "application/json"

        return response


api.add_resource(Powers, "/powers")


def power_not_found():

    response_body = {
        "error": "Power not found"
    }

    response = make_response(jsonify(response_body), 400)

    response.headers["Content-Type"] = "application/json"

    return response


class PowerById(Resource):
    # !GET power
    def get(self, power_id):
        power = Power.query.filter_by(id=power_id).first()

        if not power:
            return power_not_found()

        power_dict = power.to_dict()

        response = make_response(jsonify(power_dict), 200)

        response.headers["Content-Type"] = "application/json"

        return response

    # !PATCH power
    def patch(self, power_id):
        power = Power.query.filter_by(id=power_id).first()

        if not power:
            return power_not_found()

        data = request.get_json()

        for attr in data:
            setattr(power, attr, data.get(attr))

        db.session.commit()

        power_dict = power.to_dict()

        response = make_response(jsonify(power_dict), 200)

        response.headers["Content-Type"] = "application/json"

        return response


api.add_resource(PowerById, "/powers/<int:power_id>")


class HeroPowers(Resource):
    # !POST heropowers
    def post(self):
        data = request.get_json()

        # validate

        new_heropower = HeroPower(
            strength=data.get("strength"),
            hero_id=data.get("hero_id"),
            power_id=data.get("power_id")
        )

        db.session.add(new_heropower)
        db.session.commit()

        new_heropower_dict = new_heropower.to_dict()

        response = make_response(jsonify(new_heropower_dict), 201)

        response.headers["Content-Type"] = "application/json"

        return response


api.add_resource(HeroPowers, "/heropowers")

if __name__ == "__main__":
    app.run(port=5555, debug=True)
