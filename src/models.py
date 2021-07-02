from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


Base = declarative_base()

class User(Base):
    __tablename__ = 'User'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    username = Column(String(100))
    email = Column(String(100), nullable=False)
    password = Column(String(100), nullable=False)

class Characters(Base):
    __tablename__ = 'Character'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    gender = Column(String(10))
    birth_year = Column(20)
    height = Column(String(10))
    mass = Column(String(10))
    hair_color = Column(String(30))
    eye_color = Column(String(30))
    specie = Column(String(50), ForeignKey('species.id'))
    homeworld = Column(Integer, ForeignKey('planet.id'))
    species= relationship(Species)
    planet = relationship(Planet)

class Species(Base):
    __tablename__ = 'Species'
    id = Column(Integer, primary_key=True)
    classification = Column(String(50))
    designation = Column(String(50))
    average_lifespan = Column(Integer)
    hair_colors = Column(String(20))
    skin_colors = Column(String(20))
    homeworld = Column(String(50))
    language = Column(string(50))


class Planet(Base):
    __tablename__ = 'Planet'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    diameter = Column(Integer)
    rotation_period = Column(Integer)
    orbital_period = Column(Integer)
    gravity = Column(String(50))
    population = Column(Integer)
    climate = Column(String(50))
    terrain = Column(String(50))
    surface_water = Column(Integer)

class Starships(Base):
    __tablename__ = 'Starships'
    id = Column(integer, primary_key=True)
    name = Column(String(50), nullable=False)
    model = Column(String(100))
    starship_class = Column(string(100))
    cost_in_credits = Column(String(100))
    length = Column(Integer)
    passengers = Column(Integer)
    max_atmosphering_speed = Column(Integer)
    cargo_capacity = Column(Integer)

class Favorites(Base):
    __tablename__ = 'Favorite'
    id = Column(Integer, primary_key=True)
    id_user = Column(Integer, ForeignKey('user.id'))
    name = Column(String(100), nullable=False)
    user = relationship(User)

## Draw from SQLAlchemy base
render_er(Base, 'diagram.png')