from  Mechanic_App.blueprint.models import Service_Tickets, db
from Mechanic_App.blueprint.service_tickets.schemas import tickets_schema, ticketschema
from . import tickets_bp
from marshmallow import ValidationError
from sqlalchemy import select
from flask import request, jsonify

#Create service tickets
@tickets_bp.route("/", methods=['POST'])
def create_services():
    try:
        service_data = ticketschema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    query = select(Service_Tickets).where(Service_Tickets.vin==service_data['vin'])
    service = db.session.execute(query).scalars().all()

    #check if the service already exist
    if service:
        return jsonify({"Error": "Service already exist"}), 400
    new_service = Service_Tickets(**service_data)
    db.session.add(new_service)
    db.session.commit()
    return ticketschema.jsonify(new_service)

#Retrieve all services
#@tickets_bp.route("/", methods=['GET'])
#def get_services():
#    query = select(Service_Tickets)
#    services = db.session.execute(query).scalars().all()
 #   return tickets_schema.jsonify(Service_Tickets)