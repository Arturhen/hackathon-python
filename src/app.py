from flask import   request

from controller_companies import CompanieController
from controller_user import UserController
from controller_office import OfficeController
from config import app

# LIST
@app.route('/companies', methods=["GET"])
def list():
    return CompanieController.list()

# FIND
@app.route('/companies/<cnpj>', methods=["GET"])
def find(cnpj):    
    return CompanieController.find(cnpj)

#CREATE
@app.route('/companies', methods=["POST"])
def create():
    body = request.get_json()
    return CompanieController.create(body)
    
#Update
@app.route("/companies/<cnpj>",methods=["PUT"])
def update_by_cnpj(cnpj):
    body = request.get_json()
    return CompanieController.update_by_cnpj(cnpj,body)

#Delete
@app.route("/companies/<cnpj>",methods=["DELETE"])
def delete(cnpj):
    return CompanieController.delete(cnpj)

@app.route('/users', methods=["POST"])
def create_user():
    body = request.get_json()
    return UserController.create(body)

@app.route('/users/<company>', methods=["GET"])
def list_users_by_company(company):
    return UserController.list_by_company(company)

@app.route('/users/<user_id>', methods=["DELETE"])
def delete_user_id(user_id):
    return UserController.delete(user_id)

@app.route('/users/<user_id>', methods=["PUT"])
def update_user(user_id):
    body = request.get_json()
    return UserController.update(user_id,body)

@app.route('/offices', methods=["POST"])
def create_office():
    body = request.get_json()
    return OfficeController.create(body)

@app.route('/offices/<id_company>', methods=["GET"])
def list_by_company(id_company):
    return OfficeController.list_by_company(id_company)

@app.route('/offices/<id_office>', methods=["DELETE"])
def delete_office(id_office):
    return OfficeController.delete(id_office)

@app.route('/offices/<id_office>', methods=["PUT"])
def upate_office(id_office):
    body = request.get_json()
    return OfficeController.update(id_office,body)

app.run()
