from .models import db
from flask import Flask
from Mechanic_App.blueprint.extensions import ma
from Mechanic_App.blueprint.customers import customers_bp
from Mechanic_App.blueprint.mechanics import mechanics_bp
from Mechanic_App.blueprint.service_tickets import tickets_bp

#Create the app
def create_app(config_name):
    mechanics_shop = Flask(__name__)
    mechanics_shop.config.from_object(f'config.{config_name}')

    #Add the app to the db connections
    db.init_app(mechanics_shop)
    ma.init_app(mechanics_shop)

#Register the blueprint
    mechanics_shop.register_blueprint(customers_bp, url_prefix="/customers")
    mechanics_shop.register_blueprint(mechanics_bp, url_prefix="/mechanics")
    mechanics_shop.register_blueprint(tickets_bp, url_prefix="/service_tickets")
    return mechanics_shop


