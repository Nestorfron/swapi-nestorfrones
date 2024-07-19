"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Gender, Specie, Planet, Favorite


app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


#Get All Users:

@app.route('/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    serialize_user = [user.serialize() for user in users]
    return jsonify({
        "users": serialize_user
    }), 200

#Get User by ID

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    try:
        user= User.query.get(user_id)
        if user is None:
            return  jsonify({"error": "user not found!"}),404
        return jsonify({
            "user": user.serialize()
        }), 200
    except Exception as error:
        return jsonify({"error": f"{error}!"}),500

#Create User:

@app.route('/users', methods=['POST'])
def create_user():
    body = request.json 
    email = body.get("email", None)
    password = body.get("password", None)
    is_active = body.get("is_active", None)
    if email is None or password is None or is_active is None:
        return jsonify({"error": "missing fields"}), 400
    user = User(email=email, password=password, is_active=is_active)
    try:
        db.session.add(user)
        db.session.commit()
        db.session.refresh(user)
        return jsonify({"message": f"User craterd {user.email}!"}),201
    except Exception as error:
        return jsonify({"error": f"{error}!"}),500

#Get All People:

@app.route('/people', methods=['GET'])
def get_all_people():
    people = Character.query.all()
    serialize_character = [character.serialize() for character in people]
    return jsonify({
        "people": serialize_character
    }), 200

#Get People by ID:

@app.route('/people/<int:people_id>', methods=['GET'])
def get_character(people_id):
    try:
        character = Character.query.get(people_id)
        if character is None:
            return  jsonify({"error": "character not found!"}),404
        return jsonify({
            "character": character.serialize()
        }), 200
    except Exception as error:
        return jsonify({"error": f"{error}!"}),500

#Create character:

@app.route('/people', methods=['POST'])
def create_character():
    body = request.json 
    name = body.get("name", None)
    gender = body.get("gender", None)
    specie = body.get("specie", None)
    if name is None or gender is None or specie is None:
        return jsonify({"error": "missing fields"}), 400
    character = Character(name=name, gender=Gender(gender), specie=Specie(specie))
    try:
        db.session.add(character)
        db.session.commit()
        db.session.refresh(character)
        return jsonify({"message": f"Character craterd {character.name}!"}),201
    except Exception as error:
        return jsonify({"error": f"{error}!"}),500

#Get All Planets

@app.route('/planets', methods=['GET'])
def get_all_planets():
    planets = Planet.query.all()
    serialize_planet = [planet.serialize() for planet in planets]
    return jsonify({
        "planets": serialize_planet
    }), 200

#Get Planet by ID:

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    try:
        planet = Planet.query.get(planet_id)
        if planet is None:
            return  jsonify({"error": "planet not found!"}),404
        return jsonify({
            "planet": planet.serialize()
        }), 200
    except Exception as error:
        return jsonify({"error": f"{error}!"}),500

#Create Planet:

@app.route('/planets', methods=['POST'])
def create_planet():
    body = request.json 
    name = body.get("name", None)
    diameter = body.get("diameter", None)
    population = body.get("population", None)
    if name is None or diameter is None or population is None:
        return jsonify({"error": "missing fields"}), 400
    planet = Planet(name=name, diameter=diameter, population=population)
    try:
        db.session.add(planet)
        db.session.commit()
        db.session.refresh(planet)
        return jsonify({"message": f"Planet craterd {planet.name}!"}),201
    except Exception as error:
        return jsonify({"error": f"{error}!"}),500

#Get User Favorites

@app.route('/users/<int:user_id>/favorites', methods=['GET'])
def get_user_favorites(user_id):
    try:
        user = User.query.get(user_id)
        if user_id is None:

            return  jsonify({"error": "user not found"}),404
        favorites = [favorite.serialize() for favorite in user.favorites]
        return jsonify({
            "favorites": favorites
        }), 200
    except Exception as error:
        return jsonify({"error": f"{error}!"}),500
    

#Get favorites planets of user  
    
@app.route('/users/<int:user_id>/favorites/planets', methods=['GET'])
def get_user_favorite_planets(user_id):
    try:
        user = User.query.get(user_id)
        if user_id is None:
            return  jsonify({"error": "user not found"}),404
        planets = [planet.serialize() for planet in user.favorites]
        return jsonify({
            "planets": planets
        }), 200
    except Exception as error:
        return jsonify({"error": f"{error}!"}),500

#Post Planet in favorite User

@app.route('/users/<int:user_id>/favorites/planets/<int:planet_id>', methods=['POST'])
def add_planet_favorite(user_id, planet_id):
    user = User.query.get(user_id)
    planet = Planet.query.get(planet_id)
    favorite = Favorite( user_id=user.id, planet=[planet])
    try:
        db.session.add(favorite)
        db.session.commit()
        db.session.refresh(favorite)
        return jsonify({"message": f"Favorite added!"}),201
    except Exception as error:
        return jsonify({"error": f"{error}!"}),500


@app.route('/users/<int:user_id>/favorites/planets/<int:planet_id>', methods=['DELETE'])
def delete_planet_favorite(user_id, planet_id):
    user = User.query.get(user_id)
    favorite = Favorite.query.filter_by(user_id=user_id, planet_id=planet_id).first()
    if favorite is None:
        return jsonify({"error": f"El planeta con ID {planet_id} no es un favorito del usuario con ID {user_id}"}), 404
    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"message": f"Se eliminó el planeta favorito con ID {planet_id} del usuario con ID {user_id}"}), 200








   



    
    
    
    
    
    



















# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
