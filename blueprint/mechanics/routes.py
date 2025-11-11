from Mechanic_App.blueprint.models import Mechanics, db 
from Mechanic_App.blueprint.mechanics.schemas import mechanics_schema, mechanicschema
from . import mechanics_bp
from sqlalchemy import select
from marshmallow import ValidationError
from flask import request, jsonify

#Create a mechanic
@mechanics_bp.route("/", methods=['POST'])
def create_mechanic():
    try:
        mechanic_data = mechanicschema.load(request.json)
    except ValidationError as e:
        return (e.message), 400
    
    query = select(Mechanics).where(Mechanics.email==mechanic_data['email'])
    existing_mechanic = db.session.execute(query).scalars().all()

    if existing_mechanic:
        return ({"Error": "Mechanic exists"}), 400
    
    new_mechanic=Mechanics(**mechanic_data)
    db.session.add(new_mechanic)
    db.session.commit()
    return mechanicschema.jsonify(new_mechanic), 201
    
#Retrieve all mechanics
@mechanics_bp.route("/", methods=['GET'])
def get_mechanics():
    query=select(Mechanics)
    mechanics = db.session.execute(query).scalars().all()
    return mechanics_schema.jsonify(mechanics)

#Update a mechanic
@mechanics_bp.route("/<int:mechanic_id>", methods=['PUT'])
def update_mechanic(mechanic_id):
    mechanic = db.session.get(Mechanics, mechanic_id)

    if not mechanic:
        return jsonify({"Error": "Mechanic not found"}), 404
    try:
        mechanic_data = mechanicschema.load(request.json)
    except ValidationError as e:
        return (e.message), 400
    
    for key, value in mechanic_data.items():
        setattr(mechanic, key, value)

    db.session.commit()
    return mechanicschema.jsonify(mechanic)

#Delete a mechanic
@mechanics_bp.route("/<int:mechanic_id>", methods=['DELETE'])
def delete_mechanic(mechanic_id):
    mechanic = db.session.get(Mechanics, mechanic_id)
    if not mechanic:
        return jsonify({"Error": "Sorry, mechanic does not exist"})
    
    db.session.delete(mechanic)
    db.session.commit()
    return mechanicschema.jsonify({"Message": f'Mechanice id: {mechanic_id} deleted successfully'}), 200