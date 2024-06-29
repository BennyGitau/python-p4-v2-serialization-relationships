# server/models.py

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(metadata=metadata)


class Zookeeper(db.Model):
    __tablename__ = 'zookeepers'

    serialize_rules = ('-animals.zookeeper',)
    #this can be used when you want to specify specific fields to serialize
    #serialize_only = ('id', 'name', 'animals.name', 'animals.species',)


    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    birthday = db.Column(db.Date)

    animals = db.relationship('Animal', back_populates='zookeeper')

    def __repr__(self):
        return f'<Zookeeper {self.name} {self.birthday}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'birthday': self.birthday,
            'animals': [animal.to_dict() for animal in self.animals]
        }


class Enclosure(db.Model):
    __tablename__ = 'enclosures'
    
    serialize_rules = ('-animals.enclosure',)

    id = db.Column(db.Integer, primary_key=True)
    environment = db.Column(db.String)
    open_to_visitors = db.Column(db.Boolean)

    animals = db.relationship('Animal', back_populates='enclosure')

    def to_dict(self):
        return {
            'id': self.id,
            'environment': self.environment,
            'open_to_visitors': self.open_to_visitors,
            'animlas': [animal.to_dict() for animal in self.animals]
        }


class Animal(db.Model):
    __tablename__ = 'animals'

    serilaize_rules= ('-zookeeper.animals', '-enclosure.animals',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    species = db.Column(db.String)

    zookeeper_id = db.Column(db.Integer, db.ForeignKey('zookeepers.id'))
    enclosure_id = db.Column(db.Integer, db.ForeignKey('enclosures.id'))

    enclosure = db.relationship('Enclosure', back_populates='animals')
    zookeeper = db.relationship('Zookeeper', back_populates='animals')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'species': self.species
        }

    def __repr__(self):
        return f'<Animal {self.name}, a {self.species}>'
