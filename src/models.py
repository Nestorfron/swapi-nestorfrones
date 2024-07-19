from flask_sqlalchemy import SQLAlchemy
from enum import Enum as PyEnum 

db = SQLAlchemy()


class Gender(PyEnum):
    FEMALE = "Female"
    MALE = "Male"
    UNDEFINED = "Undefined"

class Specie(PyEnum):
    HUMAN = "Human"
    ALIEN = "Alien"
    ROBOT = "Robot"


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    favorites = db.relationship('Favorite', backref='user', lazy=True)

    def __repr__(self):
        return f"<user{self.name}>"

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "is_active": self.is_active,
            "favorites": [favorite.serialize() for favorite in self.favorites]
            # do not serialize the password, its a security breach
        }


class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    gender = db.Column(db.Enum(Gender), nullable=False)
    specie = db.Column(db.Enum(Specie), nullable=False)
    favorite_id = db.Column(db.Integer, db.ForeignKey("favorite.id"))

    def serialize(self):
        return {
            "id": self.id,
            "name":self.name,
            "gender": self.gender.value,
            "specie": self.specie.value
        }

    def __repr__(self):
        return f"<character{self.name}>"


class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    diameter = db.Column(db.Integer, nullable=False)
    population = db.Column(db.Integer, nullable=False)
    favorite_id = db.Column(db.Integer, db.ForeignKey("favorite.id"))


    def serialize(self):
        return {
            "id": self.id,
            "name":self.name,
            "diameter": self.diameter,
            "population": self.population,
        }

    def __repr__(self):
        return f"<planet{self.name}>"


class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    planet = db.relationship("Planet", backref="favorite")
    character = db.relationship("Character", backref="favorite")
    
    def serialize(self):
        return {
            "id": self.id,
            "planet": [planet.serialize() for planet in self.planet],
            "character": [character.serialize() for character in self.character]
        }

    def __repr__(self):
        return f"<favorite{self.number}>"
    











