from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()

# Define the association table for the many-to-many relationship between Hero and Power
hero_power_association = db.Table('hero_power_association',
    db.Column('hero_id', db.Integer, db.ForeignKey('hero.id')),
    db.Column('power_id', db.Integer, db.ForeignKey('power.id'))
)

class Hero(db.Model):
    __tablename__ = 'hero'

    id = db.Column(db.Integer, primary_key=True)
    powers = db.relationship('Power', secondary=hero_power_association, back_populates='heroes')

class Power(db.Model):
    __tablename__ = 'power'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(255), nullable=False)
    heroes = db.relationship('Hero', secondary=hero_power_association, back_populates='powers')

    @validates('description')
    def validate_description(self, key, value):
        if len(value) < 20:
            raise ValueError('Description must be at least 20 characters long.')
        return value

class HeroPower(db.Model):
    __tablename__ = 'hero_power'

    id = db.Column(db.Integer, primary_key=True)
    hero_id = db.Column(db.Integer, db.ForeignKey('hero.id'))
    power_id = db.Column(db.Integer, db.ForeignKey('power.id'))
    hero = db.relationship('Hero', back_populates='hero_powers')
    power = db.relationship('Power', back_populates='power_heroes')
    strength = db.Column(db.String(50), nullable=False)

    @validates('strength')
    def validate_strength(self, key, value):
        allowed_strengths = ['Strong', 'Weak', 'Average']
        if value not in allowed_strengths:
            raise ValueError('Strength must be one of the following values: \'Strong\', \'Weak\', \'Average\'')
        return value

# Add these relationships to the Hero and Power models
Hero.hero_powers = db.relationship('HeroPower', back_populates='hero')
Power.power_heroes = db.relationship('HeroPower', back_populates='power')
