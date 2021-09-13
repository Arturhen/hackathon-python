from libraries.cpf_cnpj import Cnpj
from flask import Response
import bcrypt

from models.models import Companies
from utils.create_response import create_response
from config import db


class CompanieController:
    @staticmethod
    def list():
        companies_class = Companies.query.all()

        companies_class_json = [company.to_json()
                                for company in companies_class]

        return create_response(200, "companies", companies_class_json)

    @staticmethod
    def find(cnpj):

        # obj_cnpj = Cnpj(cnpj).format()

        company_obj = Companies.query.filter_by(cnpj=cnpj).first()

        if(company_obj is None):
            return create_response(404, "Company", {})

        company_json = company_obj.to_json()

        return create_response(200, "Company", company_json)

    @staticmethod
    def create(body):

        if(not("cnpj" in body)):
            return create_response(400, "Error", {"field": "cnpj is required"}, "No Create Company")

        obj_cnpj = Cnpj(body["cnpj"])

        if(not obj_cnpj.validate()):
            return create_response(400, "Error", {"field": "Invalid cnpj"}, "No Create")

        cnpj_formated = obj_cnpj.format()

        if(Companies.query.filter_by(cnpj=cnpj_formated).first()):
            return create_response(400, "Error", {"field": "Exist another company with this CNPJ"}, "No Create")

        if(not("password" in body)):
            return create_response(400, "Error", {"field": "password is required"}, "No Create Company")

        password_hash =  bcrypt.hashpw(body["password"].encode('utf-8'), bcrypt.gensalt(8)).decode('utf8')

        try:
            company = Companies(name=body["name"],
                                cnpj=cnpj_formated, password=password_hash)

            db.session.add(company)
            db.session.commit()
            return create_response(201, "Company", company.to_json(), "Create Successful")
        except Exception as e:
            print(e)
            return create_response(400, "Company", {}, "Error in create company")

    @staticmethod
    def update_by_cnpj(cnpj, body):
        # obj_cnpj = Cnpj(cnpj).format()

        company_obj = Companies.query.filter_by(cnpj=cnpj).first()

        if(company_obj is None):
            return create_response(404, "Company", {})

        try:
            if('name' in body):
                company_obj.name = body["name"]
            if('password' in body):
                company_obj.password = bcrypt.hashpw(body["password"].encode('utf-8'), bcrypt.gensalt(8)).decode('utf8')

            db.session.add(company_obj)
            db.session.commit()

            return create_response(200, "Company", company_obj.to_json(), "Update Successful")
        except Exception as e:
            print(e)
            return create_response(400, "Company", {}, "Error in update company")

    @staticmethod
    def delete(cnpj):

        try:
            # obj_cnpj = Cnpj(cnpj).format()

            company_obj = Companies.query.filter_by(cnpj=cnpj).first()

            if(company_obj is None):
                return Response(status=404)

            db.session.delete(company_obj)
            db.session.commit()
            return create_response(204, "Company", company_obj.to_json(), "Successful deleted")
        except Exception as e:
            print(e)
            return create_response(400, "Company", {}, "Error in delete company")
