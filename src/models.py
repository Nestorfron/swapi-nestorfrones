from flask_sqlalchemy import SQLAlchemy
from enum import Enum as PyEnum
from sqlalchemy.orm import relationship

db = SQLAlchemy()


class Gender(PyEnum):
    FEMALE = 'Female'
    MALE = 'Male'
    UNDEFINED = 'Undefined'


class Specie(PyEnum):
    HUMAN = 'Human'
    ALIEN = 'Alien'
    ROBOT = 'Robot'



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    is_active = db.Column(db.Boolean(), nullable=False, default=True)
    favorites = db.relationship('Favorite', backref='user', lazy=True)

    def serialize(self):
        return {
            'id': self.id,
            'email': self.email,
            'is_active': self.is_active,
            'favorites': [favorite.serialize() for favorite in self.favorites]
        }
    
    def __repr__(self):
        return f'<User {self.email}>'

class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    characters = db.relationship("Character", backref="favorite", lazy=True)
    planets = db.relationship("Planet", backref="favorite", lazy=True)


    def serialize(self):
        return {
            "id": self.id,
            'planets': [planet.serialize() for planet in self.planets],
            'characters': [character.serialize() for character in self.characters]
        }

    def __repr__(self):
        return f'<Favorite {self.id}>'

class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    favorite_id = db.Column(db.Integer, db.ForeignKey('favorite.id'), nullable=True)
    name = db.Column(db.String(40), nullable=False)
    gender = db.Column(db.Enum(Gender), nullable=False)
    specie = db.Column(db.Enum(Specie), nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'favorite_id': self.favorite_id,
            'name': self.name,
            'gender': self.gender.value,
            'specie': self.specie.value
        }

    def __repr__(self):
        return f'<Character {self.name}>'

class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    favorite_id = db.Column(db.Integer, db.ForeignKey('favorite.id'), nullable=True)
    name = db.Column(db.String(40), nullable=False)
    diameter = db.Column(db.Integer, nullable=False)
    population = db.Column(db.Integer, nullable=False)
    

    def serialize(self):
        return {
            'id': self.id,
            'favorite_id': self.favorite_id,
            'name': self.name,
            'diameter': self.diameter,
            'population': self.population
        }

    def __repr__(self):
        return f'<Planet {self.name}>'
    
