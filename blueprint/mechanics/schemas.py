from Mechanic_App.blueprint.models import Mechanics
from Mechanic_App.blueprint.extensions import ma

#Create the mechanic 
class MechanicSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Mechanics
mechanicschema = MechanicSchema()
mechanics_schema = MechanicSchema(many = True)