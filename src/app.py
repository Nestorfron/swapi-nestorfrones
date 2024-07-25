#This module takes care of starting the API Server, Loading the DB and Adding the endpoints

import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Gender, Specie, Planet, Favorite
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity


app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv('DATABASE_URL')
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace('postgres://', 'postgresql://')
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['JWt_SECRET_KEY'] = os.environ.get("FLASK_APP_KEY")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = 3600 # 1 hora en segundos

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)
JWTManager(app)


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


#register User (create user)

@app.route('/register', methods=['POST'])
def user_register():
    try:
        body = request.json
        email = body.get("email", None)
        password = body.get("password", None)
        is_active = body.get("is_active", None)
        if email is None or password is None:
            return jsonify({"error": "email and password requred"}), 400
        email_is_taken = User.query.filter_by(email=email).first()
        if email_is_taken:
            return jsonify({"error": "Email already exist"}), 400
        password_hash = generate_password_hash(password)
        user = User(email = email, password = password_hash, is_active = is_active)
        db.session.add(user)
        db.session.commit()
        return jsonify({"message": "User created"}), 201
    except Exception as error:
        return jsonify({"error": f'{error}'}),500
    
    
# login User

@app.route('/login', methods=['POST'])
def login():
    try:
        body = request.json
        email = body.get("email", None)
        password = body.get("password", None)
        if email is None or password is None:
            return jsonify({"error": "email and password requred"}), 400
        user = User.query.filter_by(email=email).first()
        if user is None:
            return jsonify({"error": "User not exist"}), 404
        if not check_password_hash(user.password, password):
            return jsonify({"error":"Try again later"}), 400
        auth_token = create_access_token({"id" : user.id, "email" : user.email})
        return auth_token
    except Exception as error:
        return jsonify({"error": f'{error}'}),500
    

#Get User loged
    
@app.route('/me', methods=['GET'])
@jwt_required()
def get_user_data():
    user_data = get_jwt_identity()
    return jsonify(user_data), 200 
       
#Get All Users:

@app.route('/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    serialize_user = [user.serialize() for user in users]
    return jsonify({
        'users': serialize_user
    }), 200

#Get User by ID

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    try:
        user= User.query.get(user_id)
        if user is None:
            return  jsonify({'error': 'user not found!'}),404
        return jsonify({
            'user': user.serialize()
        }), 200
    except Exception as error:
        return jsonify({'error': f'{error}!'}),500

#Get All People:

@app.route('/people', methods=['GET'])
def get_all_people():
    people = Character.query.all()
    serialize_character = [character.serialize() for character in people]
    return jsonify({
        'people': serialize_character
    }), 200

#Get People by ID:

@app.route('/people/<int:people_id>', methods=['GET'])
def get_character(people_id):
    try:
        character = Character.query.get(people_id)
        if character is None:
            return  jsonify({'error': 'character not found!'}),404
        return jsonify({
            'character': character.serialize()
        }), 200
    except Exception as error:
        return jsonify({'error': f'{error}!'}),500

#Create character:

@app.route('/people', methods=['POST'])
@jwt_required()
def create_character():
    body = request.json 
    name = body.get('name', None)
    gender = body.get('gender', None)
    specie = body.get('specie', None)
    if name is None or gender is None or specie is None:
        return jsonify({'error': 'missing fields'}), 400
    character = Character(name=name, gender=Gender(gender), specie=Specie(specie))
    try:
        db.session.add(character)
        db.session.commit()
        db.session.refresh(character)
        return jsonify({'message': f'Character craterd {character.name}!'}),201
    except Exception as error:
        return jsonify({'error': f'{error}!'}),500

#Get All Planets

@app.route('/planets', methods=['GET'])
def get_all_planets():
    planets = Planet.query.all()
    serialize_planet = [planet.serialize() for planet in planets]
    return jsonify({
        'planets': serialize_planet
    }), 200

#Get Planet by ID:

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    try:
        planet = Planet.query.get(planet_id)
        if planet is None:
            return  jsonify({'error': 'planet not found!'}),404
        return jsonify({
            'planet': planet.serialize()
        }), 200
    except Exception as error:
        return jsonify({'error': f'{error}!'}),500

#Create Planet:

@app.route('/planets', methods=['POST'])
@jwt_required()
def create_planet():
    body = request.json 
    name = body.get('name', None)
    diameter = body.get('diameter', None)
    population = body.get('population', None)
    if name is None or diameter is None or population is None:
        return jsonify({'error': 'missing fields'}), 400
    planet = Planet(name=name, diameter=diameter, population=population)
    try:
        db.session.add(planet)
        db.session.commit()
        db.session.refresh(planet)
        return jsonify({'message': f'Planet craterd {planet.name}!'}),201
    except Exception as error:
        return jsonify({'error': f'{error}!'}),500

#Get User Favorites

@app.route('/user/favorites', methods=['GET'])
@jwt_required()
def get_user_favorites():
    try:
        current_user = get_jwt_identity()
        user_id = current_user.get("id")
        user = User.query.get(user_id)
        if user is None:
            return  jsonify({'error': 'user not found'}),404
        characters = [character.serialize() for character in user.characters]
        planets = [planet.serialize() for planet in user.planets]
        return jsonify({
            'Characters': characters,
            'Planets': planets
        }), 200
    except Exception as error:
        return jsonify({'error': f'{error}!'}),500

#Post Planet favorite in User

@app.route('/favorites/planets/<int:planet_id>', methods=['POST'])
@jwt_required()
def add_favorite_planet(planet_id):
    current_user = get_jwt_identity()
    user_id = current_user.get("id")
    planet = Planet.query.get(planet_id)
    if planet is None:
        return jsonify({"error": "Planet not found"}),404
    planet = Planet(name=planet.name, diameter=planet.diameter, population=planet.population, user_id=user_id )
    try:
        db.session.add(planet)
        db.session.commit()
        return jsonify({"message": "Planet added to favorites"}), 201
    except Exception as error:
        db.session.rollback()
        return jsonify({"error": {error}}), 500
    
#Delete Planet  favorite of User

@app.route('/favorites/planets/<int:planet_id>', methods=['DELETE'])
@jwt_required()
def delete_favorite_planet(planet_id):
    try:
        current_user = get_jwt_identity()
        user_id = current_user.get("id")
        planet = Planet.query.get(planet_id)        
        if planet is None:
            return jsonify({"error": "Planet not found"}),404
        db.session.delete(planet)
        db.session.commit()
        return jsonify({"message": f"Planet removed from favorites"}), 200
    except Exception as error:
        return jsonify({"error": {error}}), 500

    
#Post Character favorite in User

@app.route('/favorites/people/<int:people_id>', methods=['POST'])
@jwt_required()
def add_favorite_character(people_id):
    try:
        current_user = get_jwt_identity()
        user_id = current_user.get("id")
        character = Character.query.get(people_id)
        if character is None:
            return jsonify({"error": f"Character not found"}), 404
        character = Character(name=character.name, gender=character.gender, specie=character.specie, user_id=user_id)
        db.session.add(character)
        db.session.commit() 
        return jsonify({"message": f"Character added to favorites"}), 201
    except Exception as error:
        return jsonify({"error": {error}}), 500
    
#Delete Character favorite of User    

@app.route('/favorites/people/<int:people_id>', methods=['DELETE'])
@jwt_required()
def delete_favorite_character(people_id):
    try:
        current_user = get_jwt_identity()
        user_id = current_user.get("id")
        character = Character.query.get(people_id)        
        if character is None:
            return jsonify({"error": "Character not found"}),404
        db.session.delete(character)
        db.session.commit()
        return jsonify({"message": f"Character removed from favorites"}), 200
    except Exception as error:
        return jsonify({"error": {error}}), 500
    
    
# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
