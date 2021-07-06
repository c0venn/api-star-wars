from flask import Flask, json, jsonify, request, render_template
from flask_migrate import Migrate
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from werkzeug.security import check_password_hash, generate_password_hash
from models import db, Character, Specie, Planet, Starship

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['ENV'] = 'development'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['JWT_SECRET_KEY'] = 'super-secret'  #change this
jwt = JWTManager(app)
db.init_app(app)
Migrate(app, db)  # init, migrate , upgrade 


@app.route('/login', methods=['POST'])
def login ():
    username = request.json.get('username', None)
    password = request.jso.get('password', None)

    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify({"msg": "Incorrect"})

    if (check_password_hash(user.password, password)):
        access_token = create_access_token(identity=user.id)

        datos = {
            "access_token": access_token,
            "user": user.serialize()
        }

        return jsonify(datos), 200


@app.route('api/register', methods=['POST'])
def register():
    if request.method == 'POST':
        username = request.json.get('username')
        password = request.json.get('password')

        user = User()
        user.username = username
        user.password = generate_password_hash(password)
        user.save()

        access_token = create_access_token(identity=user.id)

        datos = {
            "access_token": access_token,
            "user": user.serialize()
        }

        return jsonify(datos), 201

@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as= current_user), 200

@app.route('/api/characters', methods=['GET','POST'])
@app.route('/api/characters/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def characters(id=None):
    if request.method == 'GET':

        if id is not None:
            character = Character.query.get(id)
            return jsonify(character.serialize()), 200

        characters = Character.query.all()
        characters = list(map(lambda character: character.serialize(), characters))
        return jsonify(characters), 200

    if request.method == 'POST':
       name = request.json.get('name', '')
       gender = request.json.get('gender', '')
       birth_year = request.json.get('birth_year', '')
       height = request.json.get('height', '')
       mass = request.json.get('mass', '')
       hair_color = request.json.get('hair_color', '')
       eye_color = request.json.get('eye_color', '')
       specie = request.json.get('specie', '')
       homeworld = request.json.get('homeworld', '')

       character = Character()

       character.name = name
       character.gender = gender
       character.birth_year = birth_year
       character.height = height
       character.mass = mass
       character.hair_color = hair_color
       character.eye_color = eye_color
       character.specie = specie
       character.homeworld = homeworld

       character.save()

       return jsonify(character.serialize()), 201

    if request.method == 'PUT':
        name = request.json.get('name','')
        gender = request.json.get('gender','')
        birth_year = request.json.get('birth_year','')
        height = request.json.get('height','')
        mass = request.json.get('mass','')
        hair_color = request.json.get('hair_color','')
        eye_color = request.json.get('eye_color','')
        specie = request.json.get('specie','')
        homeworld = request.json.get('homeworld','')

        character = Character.query.get(id)

        character.name = name
        character.gender = gender
        character.birth_year = birth_year
        character.height = height
        character.mass = mass
        character.hair_color = hair_color
        character.eye_color = eye_color
        character.specie = specie
        character.homeworld = homeworld

        character.specie.id = id 

        specie = Specie.query.filter_by(character_id=id).first()
        specie.character = character 

        specie.update()

        character.update()

        return jsonify(character.serialize()), 200


    if request.method == 'DELETE':

       character = Character.query.get(id)

       character.delete()

       return jsonify({"success": "character deleted"}), 201

@app.route('/api/specie', methods=['GET', 'POST'])
@app.route('/api/specie/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def specie(id=None):
    if request.method == 'GET':

        if id is not None:
            specie = Specie.query.get(id)
            return jsonify(specie.serialize()), 200

        specie = Specie.query.all()
        specie = list(map(lambda specie: specie.serialize(), specie))
        return jsonify(specie), 200

    if request.method == 'POST':

        classification = request.json.get('classification', '')
        designation = request.json.get('designation', '')
        average_lifespan = request.json.get('average_lifespan', '')
        hair_colors = request.json.get('hair_colors', '')
        skin_colors = request.json.get('skin_colors', '')
        language = request.json.get('language', '')
        homeworld = request.json.get('homeworld', '')
        specie = request.json.get('specie', '')

        specie = Specie()

        specie.classification = classification
        specie.designation = designation
        specie.average_lifespan = average_lifespan
        specie.hair_colors = hair_colors
        specie.skin_colors = skin_colors
        specie.language = language
        specie.homeworld = homeworld
        specie.specie = specie

        specie.save()

        return jsonify(specie.serialize()), 201

    if request.method == 'PUT':

        classification = request.json.get('classification', '')
        designation = request.json.get('designation', '')
        average_lifespan = request.json.get('average_lifespan', '')
        hair_colors = request.json.get('hair_colors', '')
        skin_colors = request.json.get('skin_colors', '')
        language = request.json.get('language', '')
        homeworld = request.json.get('homeworld', '')
        specie = request.json.get('specie', '')

        specie = Specie.query.get(id)

        specie.classification = classification
        specie.designation = designation
        specie.average_lifespan = average_lifespan
        specie.hair_colors = hair_colors
        specie.skin_colors = skin_colors
        specie.language = language
        specie.homeworld = homeworld
        specie.specie = specie

        specie.update()

        return jsonify(specie.serialize()), 200

    if request.method == 'DELETE':

        specie = Specie.query.get(id)

        specie.delete()

        return jsonify({"succes": "specie deleted"}), 201


@app.route('/api/planets', methods=['GET', 'POST'])
@app.route('/api/planets/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def planets(id=None):
    if request.method == 'GET':

        if id is not None:
            planet = Planets.query.get(id)
            return jsonify(planet.serialize()), 200

        planet = Planets.query.all()
        planet = list(map(lambda planet: planet.serialize(), planet))
        return jsonify(planet), 200

    if request.method == 'POST':

        name = request.json.get('name', '')
        diameter = request.json.get('diameter', '')
        rotation_period = request.json.get('rotation_period', '')
        orbital_period = request.json.get('orbital_period', '')
        gravity = request.json.get('gravity', '')
        population = request.json.get('population', '')
        climate = request.json.get('climate', '')
        terrain = request.json.get('terrain', '')
        surface_water = request.json.get('surface_water', '')

        planet = Planets()

        planet.name = name
        planet.diameter = diameter
        planet.rotation_period = rotation_period
        planet.orbital_period = orbital_period
        planet.gravity = gravity
        planet.population = population
        planet.climate = climate
        planet.terrain = terrain
        planet.surface_water = surface_water

        planet.save()

        return jsonify(planet.serialize()), 201

        if request.method == 'PUT':

        name = request.json.get('name', '')
        diameter = request.json.get('diameter', '')
        rotation_period = request.json.get('rotation_period', '')
        orbital_period = request.json.get('orbital_period', '')
        gravity = request.json.get('gravity', '')
        population = request.json.get('population', '')
        climate = request.json.get('climate', '')
        terrain = request.json.get('terrain', '')
        surface_water = request.json.get('surface_water', '')

        planet = Planets.query.get(id)

        planet.name = name
        planet.diameter = diameter
        planet.rotation_period = rotation_period
        planet.orbital_period = orbital_period
        planet.gravity = gravity
        planet.population = population
        planet.climate = climate
        planet.terrain = terrain
        planet.surface_water = surface_water

        planet.update()

        return jsonify(planet.serialize()), 200

    if request.method == 'DELETE':

        planet = Planets.query.get(id)

        planet.delte()

        return jsonify({"succes": "planet deleted"}), 201


@app.route('/api/starship', methods=['GET', 'POST'])
@app.route('/api/starship/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def starship(id=None):
    if request.method == 'GET':

        if id is not None:
            starship = Starship.query.get(id)
            return jsonify(starship.serialize()), 200

        starship = Starship.query.all()
        starship = list(map(lambda starship: starship.serialize(), starship))
        return jsonify(starship), 200

    if request.method == 'POST':

        name = request.json.get('name', '')
        model = request.json.get('model', '')
        starship_class = request.json.get('starship_class', '')
        cost_in_credits = request.json.get('cost_in_credits', '')
        length = request.json.get('length', '')
        passengers = request.json.get('passengers', '')
        max_atmosphering_speed = request.json.get('max_atmosphering_speed', '')
        cargo_capacity = request.json.get('cargo_capacity', '')

        starship = Starship()

        starship.name = name
        starship.model = model
        starship.starship_class = starship_class
        starship.orbital_period = orbital_period
        starship.cost_in_credits = cost_in_credits
        starship.length = length
        starship.climate = climate
        starship.max_atmosphering_speed = max_atmosphering_speed

        starship.save()

        return jsonify(starship.serialize()), 201

        if request.method == 'PUT':

        name = request.json.get('name', '')
        model = request.json.get('model', '')
        starship_class = request.json.get('starship_class', '')
        cost_in_credits = request.json.get('cost_in_credits', '')
        length = request.json.get('length', '')
        passengers = request.json.get('passengers', '')
        max_atmosphering_speed = request.json.get('max_atmosphering_speed', '')
        cargo_capacity = request.json.get('cargo_capacity', '')


        starship = Starship.query.get(id)

        starship.name = name
        starship.model = model
        starship.starship_class = starship_class
        starship.orbital_period = orbital_period
        starship.cost_in_credits = cost_in_credits
        starship.length = length
        starship.climate = climate
        starship.max_atmosphering_speed = max_atmosphering_speed

        starship.update()

        return jsonify(starship.serialize()), 200

    if request.method == 'DELETE':

        starship = Starship.query.get(id)

        starship.delete()

        return jsonify({"succes": "starship deleted"}), 201




if __name__ == '__main__':
    app.run()