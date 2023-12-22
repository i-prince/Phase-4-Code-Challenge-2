from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from models import db, Hero, Power, HeroPower

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

# Define routes

@app.route('/heroes', methods=['GET'])
def get_heroes():
    heroes = Hero.query.all()
    hero_list = [{'id': hero.id, 'name': hero.name, 'super_name': hero.super_name} for hero in heroes]
    return jsonify(hero_list)

@app.route('/heroes/<int:hero_id>', methods=['GET'])
def get_hero(hero_id):
    hero = Hero.query.get(hero_id)
    if hero:
        powers = [{'id': power.id, 'name': power.name, 'description': power.description} for power in hero.powers]
        hero_data = {'id': hero.id, 'name': hero.name, 'super_name': hero.super_name, 'powers': powers}
        return jsonify(hero_data)
    else:
        return jsonify({'error': 'Hero not found'}), 404

@app.route('/powers', methods=['GET'])
def get_powers():
    powers = Power.query.all()
    power_list = [{'id': power.id, 'name': power.name, 'description': power.description} for power in powers]
    return jsonify(power_list)

@app.route('/powers/<int:power_id>', methods=['GET'])
def get_power(power_id):
    power = Power.query.get(power_id)
    if power:
        power_data = {'id': power.id, 'name': power.name, 'description': power.description}
        return jsonify(power_data)
    else:
        return jsonify({'error': 'Power not found'}), 404

@app.route('/powers/<int:power_id>', methods=['PATCH'])
def update_power(power_id):
    power = Power.query.get(power_id)
    if power:
        data = request.get_json()
        power.description = data.get('description', power.description)

        try:
            db.session.commit()
            return jsonify({'id': power.id, 'name': power.name, 'description': power.description})
        except Exception as e:
            db.session.rollback()
            return jsonify({'errors': ['validation errors']}), 400
    else:
        return jsonify({'error': 'Power not found'}), 404

@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    data = request.get_json()
    hero_id = data.get('hero_id')
    power_id = data.get('power_id')
    strength = data.get('strength')

    # Validate input
    if not hero_id or not power_id or not strength:
        return jsonify({'errors': ['validation errors']}), 400

    hero = Hero.query.get(hero_id)
    power = Power.query.get(power_id)

    if not hero or not power:
        return jsonify({'errors': ['validation errors']}), 400

    hero_power = HeroPower(hero_id=hero_id, power_id=power_id, strength=strength)

    try:
        db.session.add(hero_power)
        db.session.commit()
        return jsonify({'id': hero.id, 'name': hero.name, 'super_name': hero.super_name, 'powers': [{'id': power.id, 'name': power.name, 'description': power.description}]})
    except Exception as e:
        db.session.rollback()
        return jsonify({'errors': ['validation errors']}), 400

if __name__ == '__main__':
    app.run(port=5555)
