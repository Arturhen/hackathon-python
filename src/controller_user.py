import bcrypt

from flask.wrappers import Response

from config import db
from models import Users
from create_response import create_response
from check_email import check_email

class UserController:
    @staticmethod
    def create(body):

        if(("email" not in body) or (not check_email(body["email"]))):
            return create_response(400, "Error", {"field": "Email invalid format"}, "Usuario não Cadastrado")

        if(Users.query.filter_by(email=body["email"]).first()):
            return create_response(400, "Error", {"field": "Exist another user with this Email"})

        password_hash =  bcrypt.hashpw(body["password"].encode('utf-8'), bcrypt.gensalt(8)).decode('utf8')

        try:
            user = Users(name=body["name"], email=body["email"],
                         password=password_hash, company=body["company"])
            db.session.add(user)
            db.session.commit()
            return create_response(201, "User", user.to_json(), "Create Successful")

        except Exception as e:
            print(e)
            return create_response(400, "Error", {}, "Error in create User")

    @staticmethod
    def list_by_company(company):
        users_by_company = Users.query.filter_by(company=company)

        users_json = [user.to_json()
                      for user in users_by_company]

        return create_response(200, "users", users_json)

    @staticmethod
    def delete(user_id):

        try:
            user_obj = Users.query.filter_by(id=user_id).first()

            if(user_obj is None):
                return Response(status=404)
            db.session.delete(user_obj)
            db.session.commit()
            return create_response(204, "User", user_obj.to_json(), "Successful deleted")
        except Exception as e:
            print(e)
            return create_response(400, "User", {}, "Error in delete user")

    @staticmethod
    def update(user_id, body):

        try:
            user_obj = Users.query.filter_by(id=user_id).first()

            if(user_obj is None):
                return Response(status=404)

            if('name' in body):
                user_obj.name = body["name"]

            if('password' in body):
                user_obj.password = bcrypt.hashpw(body["password"].encode('utf-8'), bcrypt.gensalt(8)).decode('utf8')

            if('email' in body):
                if(not check_email(body['email'])):
                    return create_response(400, "Error", {"field": "Email invalid format"}, "Usuario não Cadastrado")

                user_by_email = Users.query.filter_by(
                    email=body["email"]).first()
                if((user_by_email is not None) and (user_by_email.id != user_obj.id)):
                    return create_response(400, "Error", {"field": "Exist another user with this Email"})

                user_obj.email = body["email"]

            db.session.add(user_obj)
            db.session.commit()
            return create_response(200, "User", user_obj.to_json(), "Update Successful")
        except Exception as e:
            print(e)
            return create_response(400, "User", {}, "Error in update User")

