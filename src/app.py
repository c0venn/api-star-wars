from flask import Flask, json, jsonify, request, render_template
from flask_migrate import Migrate
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
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


@app.route('login', methods=['POST'])
def login ():
    username = request.json.get('username', None)
    password = request.jso.get('password', None)
    if username != 'test' or password != 'test':
        return jsonify({'msg': 'Bad username or password'}), 401
    
    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)

@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as= curren_user), 200

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







if __name__ == '__main__':
    app.run()