from flask_sqlalchemy import SQLAlchemy
from enum import Enum as PyEnum, unique
from sqlalchemy.orm import relationship

db = SQLAlchemy()

@unique
class Gender(PyEnum):
    FEMALE = 'Female'
    MALE = 'Male'
    UNDEFINED = 'Undefined'

@unique
class Specie(PyEnum):
    HUMAN = 'Human'
    ALIEN = 'Alien'
    ROBOT = 'Robot'


favorite_planet = db.Table('favorite_planet',
    db.Column('favorite_id', db.Integer, db.ForeignKey('favorite.id'), primary_key=True),
    db.Column('planet_id', db.Integer, db.ForeignKey('planet.id'), primary_key=True)
)

favorite_character = db.Table('favorite_character',
    db.Column('favorite_id', db.Integer, db.ForeignKey('favorite.id'), primary_key=True),
    db.Column('character_id', db.Integer, db.ForeignKey('character.id'), primary_key=True)
)

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
    planets = db.relationship('Planet', secondary=favorite_planet, lazy='subquery', backref=db.backref('favorites', lazy=True))
    characters = db.relationship('Character', secondary=favorite_character, lazy='subquery', backref=db.backref('favorites', lazy=True))

    def serialize(self):
        return {
            'user_id': self.user_id,
            'planets': [planet.serialize() for planet in self.planets],
            'characters': [character.serialize() for character in self.characters]
        }

    def __repr__(self):
        return f'<Favorite {self.user_id}>'

class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    gender = db.Column(db.Enum(Gender), nullable=False)
    specie = db.Column(db.Enum(Specie), nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'gender': self.gender.value,
            'specie': self.specie.value
        }

    def __repr__(self):
        return f'<Character {self.name}>'

class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    diameter = db.Column(db.Integer, nullable=False)
    population = db.Column(db.Integer, nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'diameter': self.diameter,
            'population': self.population
        }

    def __repr__(self):
        return f'<Planet {self.name}>'
