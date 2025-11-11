from . import customers_bp # The "." was used because route and init are in the same folder
from marshmallow import ValidationError
from flask import request, jsonify
from sqlalchemy import select
from Mechanic_App.blueprint.customers.schema import customers_schema, customerschema
from Mechanic_App.blueprint.models import Customers, db 


#Create a Customer
@customers_bp.route( "/", methods=['POST'])
def create_customer():
    try: #put validation on the customer info that is being fire or sent to the server
        customer_data = customerschema.load(request.json)#we use the schema so validation can use on the data seamlessly
    except ValidationError as e:
        return jsonify(e.message), 400 #if the data does not match the expected pattern then it is return as a bad request

    query = select(Customers).where(Customers.email==customer_data['email']) #this to find a specific customer that aligns with the email because this email is actually unique too
    existing_customer = db.session.execute(query).scalars().all() #select all the info that matches the query
    if existing_customer:
        return jsonify({"Error": "Customer already exist"}), 400 #error because the customer exist
    new_customer = Customers(**customer_data) #destructure the customer data to create a new_customer
    db.session.add(new_customer) #add the new customer to the session
    db.session.commit() #commit it
    return customerschema.jsonify(new_customer), 201 #return the new_customer, using customer schema

#Retreive all Customers
@customers_bp.route("/", methods=['GET'] )
def get_customers():
    query = select(Customers) #This is used to get all of the customers
    customers = db.session.execute(query).scalars().all() #then you get all the customers that match the customers
    return customers_schema.jsonify(customers) #this display the customers

#Retrieve a Single Customer
@customers_bp.route("/<int:customer_id>", methods=['GET'])
def get_customer(customer_id):
    #using the get method with path parameter
    customer_data = db.session.get(Customers, customer_id) #getting the exact customer with specific id using path parameter
    if customer_data:
        return customerschema.jsonify(customer_data)
    return jsonify({"Error": "Such customer does not exist"}), 404

#Updating a Single Customer
@customers_bp.route("/<int:customer_id>", methods=['PUT'])
def update_customer(customer_id):
    customer = db.session.get(Customers, customer_id)#update the customer based on their id
    if not customer:
        return jsonify({"Error": "Sorry, customer does not exist"}), 404 #make sure the customer exist
    
    try:
        customer_data = customerschema.load(request.json) #load the request making sure it matches the schema
    except ValidationError as e:
        return jsonify(e.message), 400
    
    for key, value in customer_data.items(): #Go through every customer info
        setattr(customer, key, value) #Update the specific infor you want to
    
    db.session.commit() #commit your request
    return customerschema.jsonify(customer) 
    
#Delete a Customer
@customers_bp.route("/<int:customer_id>", methods=['DELETE'])
def delete_customer(customer_id):
    customer_data = db.session.get(Customers, customer_id) #getting that specific customer
    if not customer_data:
        return jsonify({"Error":"Customer not found"}), 404
    
    db.session.delete(customer_data)
    db.session.commit()
    return customerschema.jsonify({"Message": f'Customer id: {customer_id}, successfully deleted'})

    
