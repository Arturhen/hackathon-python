from models import Companies
from flask import Response
from create_response import create_response

from cpf_cnpj.cpf_cnpj import Cnpj
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

        obj_cnpj = Cnpj(cnpj).format()

        company_obj = Companies.query.filter_by(cnpj=obj_cnpj).first()

        if(company_obj is None):
            return create_response(404, "Company", {})

        company_json = company_obj.to_json()

        return create_response(200, "Company", company_json)

    @staticmethod
    def create(body):

        if(not("cnpj" in body)):
            return create_response(400,"Error", {"field": "cnpj is required"}, "No Create Company")

        obj_cnpj = Cnpj(body["cnpj"])

        if(not obj_cnpj.validate()):
            return create_response(400, "Error", {"field": "Invalid cnpj"}, "No Create")

        cnpj_formated = obj_cnpj.format()

        if(Companies.query.filter_by(cnpj=cnpj_formated).first()):
            return create_response(400, "Error", {"field": "Exist another company with this CNPJ"}, "No Create")

        try:
            company = Companies(nome=body["nome"],
                                cnpj=cnpj_formated, senha=body["senha"])

            db.session.add(company)
            db.session.commit()
            return create_response(201, "Company", company.to_json(), "Create Successful")
        except Exception as e:
            print(e)
            return create_response(400, "Company", {}, "Error in create company")

    @staticmethod
    def update_by_cnpj(cnpj, body):
        obj_cnpj = Cnpj(cnpj).format()

        company_obj = Companies.query.filter_by(cnpj=obj_cnpj).first()

        if(company_obj is None):
            return create_response(404, "Company", {})

        try:
            if('nome' in body):
                company_obj.nome = body["nome"]
            if('senha' in body):
                company_obj.senha = body["senha"]

            db.session.add(company_obj)
            db.session.commit()

            return create_response(200, "Company", company_obj.to_json(), "Update Successful")
        except Exception as e:
            print(e)
            return create_response(400, "Company", {}, "Error in update company")

    #TEM QUE DELETAR TODOS USUARIOS E FILIAIS QUANDO FOR DELETADA
    @staticmethod
    def delete(cnpj):
        obj_cnpj = Cnpj(cnpj).format()

        company_obj = Companies.query.filter_by(cnpj=obj_cnpj).first()

        if(company_obj is None):
            return Response(status=404)

        try:
            db.session.delete(company_obj)
            db.session.commit()
            return create_response(204, "Company", company_obj.to_json(), "Successful deleted")
        except Exception as e:
            print(e)
            return create_response(400, "Company", {}, "Error in delete company")
