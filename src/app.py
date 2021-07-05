from flask import Flask, json, jsonify, request, render_template
from flask_migrate import Migrate
from models import db, Character, Specie, Planet, Starship

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['ENV'] = 'development'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db.init_app(app)
Migrate(app, db)  # init, migrate , upgrade 

""" @app.route('/')
def main():
    return render_template('index.html') """

""" @app.route('/api/characters', methods=['GET'])
def list_characters():
    characters = Character.query.all()
    characters = list(map(lambda character: character.serialize(), characters))
    return jsonify(characters), 200

@app.route('/api/characters', methods=['POST'])
def create_characters():
    name = request.json.get('name')
    gender = request.json.get('gender')
    birth_year = request.json.get('birth_year')
    height = request.json.get('height')
    mass = request.json.get('mass')
    hair_color = request.json.get('hair_color')
    eye_color = request.json.get('eye_color')
    specie = request.json.get('specie')
    homeworld = request.json.get('homeworld')

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

    db.session.add(character)
    db.session.commit()

    return jsonify(character.serialize()), 201

@app.route('/api/characters/<int:id>', methods=['PUT'])
def update_character(id):
    name = request.json.get('name')
    gender = request.json.get('gender')
    birth_year = request.json.get('birth_year')
    height = request.json.get('height')
    mass = request.json.get('mass')
    hair_color = request.json.get('hair_color')
    eye_color = request.json.get('eye_color')
    specie = request.json.get('specie')
    homeworld = request.json.get('homeworld')

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

    db.session.commit()

    return jsonify(character.serialize()), 200

@app.route('/api/characters/<int:id>', methods=['DELETE'])
def delete_character(id):

    character = Character.query.get(id)
    db.session.delete(character)
    db.session.commit()

    return jsonify({"success": "character deleted"}), 200 """


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