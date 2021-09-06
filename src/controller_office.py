from flask.wrappers import Response

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

    @staticmethod
    def list_by_company(company):
        offices_by_company = Office.query.filter_by(company=company)
        
        offices_json = [office.to_json()
                        for office in offices_by_company]

        return  create_response(200,"Offices",offices_json)
      
    @staticmethod
    def delete(office_id):

        try:
            office_obj = Office.query.filter_by(id=office_id).first()

            if(office_obj is None):
                return Response(status=404)
            db.session.delete(office_obj)
            db.session.commit()
            return create_response(204,"Office",office_obj.to_json(), "Successful deleted")
        except Exception as e:
            print(e)
            return create_response(400,"Office",{},"Error in delete user")

    @staticmethod
    def update(office_id,body):
        office_obj = Office.query.filter_by(id=office_id).first()

        if(office_obj is None):
            return create_response(404, "Office", {})

        try:
            if('nome' in body):
                office_obj.nome = body["nome"]
            
            if('max_capacity' in body):
                if(body["max_capacity"]<0):
                    return create_response(400,"Error",{"field":"max_capacity need greater than 0"})
                office_obj.max_capacity = body["max_capacity"]
            
            if('max_percentage_occupation' in body):
                if(body["max_percentage_occupation"] > 100 or body["max_percentage_occupation"] < 0):
                    return create_response(400,"Error",{"field":"max_percentage_occupation Invalid value(0 to 100)"})
                office_obj.max_percentage_occupation = body["max_percentage_occupation"]
            
            db.session.add(office_obj)
            db.session.commit()
            return create_response(200,"Office",office_obj.to_json(),"Update Successful")
        except Exception as e:
            print(e)
            return create_response(400, "Office", {}, "Error in update office")
    
