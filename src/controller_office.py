from os import stat
from models import Office

from config import db
from create_response import create_response

class OfficeController:
    @staticmethod
    def create(body):

        if(("max_percentage_occupation" not in body)or body["max_percentage_occupation"] > 100 or body["max_percentage_occupation"] < 0):
            return create_response(400,"Error",{"field":"max_percentage_occupation Invalid value(0 to 100)"})
    

        if(("max_capacity" not in body) or (body["max_capacity"]<0)):
            return create_response(400,"Error",{"field":"max_capacity need greater than 0"})
        try:
            office = Office(nome=body["nome"], max_capacity=body["max_capacity"], max_percentage_occupation=body["max_percentage_occupation"],company=body["company"])
            db.session.add(office)
            db.session.commit()
            return create_response(201,"Office",office.to_json(),"Create Successful")
        except Exception as e:
            print(e)
            return create_response(400,"Office",{},"Error in create Office")

         
