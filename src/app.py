from sqlalchemy.dialects.postgresql import UUID
from flask import   request

from controller_user import UserController
from controller_companies import CompanieController
from config import app,db

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


@app.route('/users',methods=["POST"])
def create_user():
    body = request.get_json()
    return UserController.create(body)

app.run()
