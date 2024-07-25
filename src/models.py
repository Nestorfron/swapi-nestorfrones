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
    planets = db.relationship('Planet', backref='user', lazy=True)
    characters = db.relationship('Character', backref='user', lazy=True)


    def serialize(self):
        return {
            'id': self.id,
            'email': self.email,
            'is_active': self.is_active,
            'planets': [planet.serialize() for planet in self.planets],
            'characters': [character.serialize() for character in self.characters]
        }
    
    def __repr__(self):
        return f'<User {self.email}>'

class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'), nullable=False)
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'), nullable=False)
    
    
    def serialize(self):
        return {
            "id": self.id,
        }

    def __repr__(self):
        return f'<Favorite {self.id}>'

class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    name = db.Column(db.String(40), nullable=False)
    gender = db.Column(db.Enum(Gender), nullable=False)
    specie = db.Column(db.Enum(Specie), nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'gender': self.gender.value,
            'specie': self.specie.value
        }

    def __repr__(self):
        return f'<Character {self.name}>'

class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    name = db.Column(db.String(40), nullable=False)
    diameter = db.Column(db.Integer, nullable=False)
    population = db.Column(db.Integer, nullable=False)
    

    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'diameter': self.diameter,
            'population': self.population
        }

    def __repr__(self):
        return f'<Planet {self.name}>'
    
