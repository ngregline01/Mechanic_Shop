from flask import request, jsonify
from sqlalchemy import select
from marshmallow import ValidationError
from Mechanic_App.blueprint.models import Service_Tickets, Customers, Mechanics, db
from Mechanic_App.blueprint.service_tickets.schemas import ticketschema, tickets_schema
from . import tickets_bp
from Mechanic_App.utils.util import token_required

@tickets_bp.route("/", methods=['POST'])
def create_services():
    try:
        # Load JSON into a Service_Tickets object, ignore relationships for now
        service_data = ticketschema.load(
            request.json, 
            partial=("mechanic_services", "customer_service")
        )
    except ValidationError as e:
        return jsonify(e.messages), 400

    # Check if service with same VIN already exists
    existing_service = db.session.execute(
        select(Service_Tickets).where(Service_Tickets.vin == service_data['vin'])
    ).scalars().all()

    if existing_service:
        return jsonify({"Error": "Service already exists"}), 400

    # Fetch existing customer
    customer_id = request.json.get("customer_id")
    customer = db.session.query(Customers).get(customer_id)
    if not customer:
        return jsonify({"Error": "Customer does not exist"}), 400

    # Fetch existing mechanics
    mechanic_ids = request.json.get("mechanic_services", [])
    mechanics = []
    if mechanic_ids:
        mechanics = db.session.query(Mechanics).filter(Mechanics.id.in_(mechanic_ids)).all()
        if len(mechanics) != len(mechanic_ids):
            return jsonify({"Error": "One or more mechanic IDs do not exist"}), 400

    # Create new service ticket and link customer + mechanics
    new_service = Service_Tickets(**service_data)
    new_service.customer_service = customer
    new_service.mechanic_services = mechanics  # link existing mechanics

    db.session.add(new_service)
    db.session.commit()

    return ticketschema.jsonify(new_service), 201

#Retrieve all tickets
@tickets_bp.route("/", methods=['GET'])
def get_services():
    query = select(Service_Tickets)
    services = db.session.execute(query).scalars().all()
    return tickets_schema.jsonify(services)

#Adds a relationship between a service and the mechanic
@tickets_bp.route("/<int:ticket_id>/assign-mechanic/<mechanic_id>", methods=['PUT'])
def assigning_mechanics(ticket_id, mechanic_id):
    mechanic = db.session.get(Mechanics, mechanic_id)
    service = db.session.get(Service_Tickets, ticket_id)
    if not mechanic:
        return jsonify({"Error": "Mechanic does not exist"}), 404
    if not service:
        return jsonify({"Error": "Sorry, service does not exist"}), 404
    
    if mechanic not in service.mechanic_services:
        service.mechanic_services.append(mechanic)
        db.session.commit()
        return jsonify({"Message": "Mechanic successfully added"}), 201
    else:
        return jsonify({"Error": "Unable to add mechanic"})

#Removes a relationship between a service and the mechanic
@tickets_bp.route("/<ticket_id>/remove-mechanic/<mechanic_id>", methods=['PUT'])
def removing_mechanics(ticket_id, mechanic_id):
    service = db.session.get(Service_Tickets, ticket_id)
    mechanic = db.session.get(Mechanics, mechanic_id)
    if not mechanic:
        return jsonify({"Error": "Mechanic does not exist"}), 404
    if not service:
        return jsonify({"Error": "Sorry, service does not exist"}), 404
    
    if mechanic in service.mechanic_services:
        service.mechanic_services.remove(mechanic)
        db.session.commit() #Always remember to commit when you change something to the database
        return jsonify({"Message": "Successfully remove mechanic"}), 200
    else:
        return jsonify({"Error", "Unable to delete mechanic"}), 400
    

   