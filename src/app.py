import re
from flask import request
from controller_appointments import AppointmentController

from controller_companies import CompanieController
from controller_user import UserController
from controller_office import OfficeController
from login_controller import LoginController
from config import app, db
from utils.token_required import token_required

db.create_all()


@app.route('/companies', methods=["GET"])
@token_required
def list(current_user):
    return CompanieController.list()


@app.route('/companies/<cnpj>', methods=["GET"])
def find(cnpj):
    return CompanieController.find(cnpj)


@app.route('/companies', methods=["POST"])
def create():
    body = request.get_json()
    return CompanieController.create(body)


@app.route("/companies/<cnpj>", methods=["PUT"])
def update_by_cnpj(cnpj):
    body = request.get_json()
    return CompanieController.update_by_cnpj(cnpj, body)


@app.route("/companies/<cnpj>", methods=["DELETE"])
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
    return UserController.update(user_id, body)


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
    return OfficeController.update(id_office, body)


@app.route('/appointments', methods=["POST"])
def create_appointment():
    body = request.get_json()
    return AppointmentController.create(body)


@app.route('/appointments/<appointment_id>', methods=["DELETE"])
def delete_appointment(appointment_id):
    return AppointmentController.delete(appointment_id)


@app.route('/appointments', methods=["GET"])
def get_appointments():
    user_id = request.args.get("user", None)
    office_id = request.args.get("office", None)
    return AppointmentController.list(user_id, office_id)

@app.route('/login',methods=["POST"])
def login_companie():
    body = request.get_json()
    if 'cnpj' in body:
        return LoginController.login_company(body)

    return LoginController.login_user(body)
    

if __name__ == '__main__':
    app.run(host='0.0.0.0')
