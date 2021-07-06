from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    favorites = db.relationship('favorite', cascade='all, delete', backref='User') 

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "username": self.username,
            "email": self.email,
            "password": self.password
            "favorites": self.get_favorites()
        }
    
    def get_favorites(self):
        return list(map(lambda favorite: favorite.serialize(), self.favorites))

    def save(self):
        db.session.add(self)
        db.session.commit(self)

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Character(db.Model):
    __tablename__ = 'Character'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(10))
    birth_year = db.Column(db.Integer)
    height = db.Column(db.String(10))
    mass = db.Column(db.String(10))
    hair_color = db.Column(db.String(30))
    eye_color = db.Column(db.String(30))
    homeworld = db.Column(db.Integer, db.ForeignKey('planet.id', ondelete='CASCADE'), primary_key=True)
    specie = db.relationship('specie', cascade='all, delete', backref='specie', uselist=False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "gender": self.gender,
            "birth_year": self.birth_year,
            "height": self.height,
            "mass": self.mass,
            "hair_color": self.hair_color,
            "eye_color": self.eye_color,
            "specie": self.specie,
            "homeworld": self.homeworld
        }

    def save(self):
        db.session.add(self)
        db.session.commit(self)

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
    

class Specie(db.Model):
    __tablename__ = 'Species'
    id = db.Column(db.Integer, primary_key=True)
    classification = db.Column(db.String(50))
    designation = db.Column(db.String(50))
    average_lifespan = db.Column(db.Integer)
    hair_colors = db.Column(db.String(20))
    skin_colors = db.Column(db.String(20))
    language = db.Column(db.String(50))
    homeworld = db.Column(db.String(50), db.ForeignKey('planet.id', ondelete='CASCADE'), primary_key=True)
    specie = db.Column(db.String(50), db.ForeignKey('specie.id', ondelete='CASCADE'), primary_key=True)
    


    def serialize(self):
        return {
            "id": self.id,
            "classification": self.classification,
            "designation": self.designation,
            "average_lifespan": self.average_lifespan,
            "hair_colors": self.hair_colors,
            "skin_colors": self.skin_colors,
            "language": self.language,
            "homeworld": self.homeworld,
            "specie": self.specie,
            "character": self.character.serialize()
        }

    def save(self):
        db.session.add(self)
        db.session.commit(self)

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()



class Planet(db.Model):
    __tablename__ = 'Planet'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    diameter = db.Column(db.Integer)
    rotation_period = db.Column(db.Integer)
    orbital_period = db.Column(db.Integer)
    gravity = db.Column(db.String(50))
    population = db.Column(db.Integer)
    climate = db.Column(db.String(50))
    terrain = db.Column(db.String(50))
    surface_water = db.Column(db.Integer)
    homeworld = db.relationship('homeworld', cascade='all, delete', backref='homeworld', uselist=False)
    specie = db.relationship('specie', cascade='all, delete', backref='contact')
    

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "diameter": self.diameter,
            "rotation_period": self.rotation_period,
            "orbital_period": self.orbital_period,
            "gravity": self.gravity,
            "population": self.population,
            "climate": self.climate,
            "terrain": self.terrain,
            "surface_water": self.surface_water
        }

    def save(self):
        db.session.add(self)
        db.session.commit(self)

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Starship(db.Model):
    __tablename__ = 'Starships'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(100))
    starship_class = db.Column(db.String(100))
    cost_in_credits = db.Column(db.String(100))
    length = db.Column(db.Integer)
    passengers = db.Column(db.Integer)
    max_atmosphering_speed = db.Column(db.Integer)
    cargo_capacity = db.Column(db.Integer)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "model": self.model,
            "starship_class": self.starship_class,
            "cost_in_credits": self.cost_in_credits,
            "length": self.length,
            "passengers": self.passengers,
            "max_atmosphering_speed": self.max_atmosphering_speed,
            "cargo_capacity": self.cargo_capacity
        }

    def save(self):
        db.session.add(self)
        db.session.commit(self)

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Favorite(db.Model):
    __tablename__ = 'favorite'
    id = db.Column(db.Integer, primary_key=True)
    type_favorite = db.Column(db.String(10), nullable=False)
    id_favorite = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))

    def serialize(self):
        return {
            "id": self.id,
            "type_favorite": self.type_favorite,
            "id_favorite": self.id_favorite,
            "user_id": self.user_id
        }
    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
