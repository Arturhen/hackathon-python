from os import error
import bcrypt
from create_response import create_response
from libraries.cpf_cnpj import Cnpj
from check_email import check_email

from models import Companies,Users

class LoginController:
    @staticmethod
    def login_company(body):
          
        try:

            if not 'password'in body:
                return create_response(400,'Missing password',{})
            
            if not 'cnpj' in body:
                return create_response(400,'Missing cnpj',{})

            obj_cnpj = Cnpj(body["cnpj"])

            if(not obj_cnpj.validate()):
                return create_response(400, "Error", {"field": "Invalid cnpj"}, "No Create")

            cnpj_formated = obj_cnpj.format()

            company = Companies.query.filter_by(cnpj=cnpj_formated).first()

            if not company:
                return f'Company Not Found!', 404
            
            if bcrypt.checkpw(body["password"].encode('utf-8'), company.password.encode('utf-8')):
                return f'Logged in, Welcome {cnpj_formated}!', 200
            else:
                return 'Invalid Login Info!', 400
        except AttributeError:
            return create_response(400,'Provide an Cnpj and Password in JSON format in the request body',{"cnpj":"","password":""})
    
    @staticmethod
    def login_user(body):
        try:
            if not 'password'in body:
                return create_response(400,'Missing password',{})
            
            if not 'email' in body:
                return create_response(400,'Missing email',{})
            
            if(not check_email(body['email'])):
                    return create_response(400, "Error", {"field": "Email invalid format"})
            
            user = Users.query.filter_by(email=body["email"]).first()

            if not user:
                return create_response(404,"User not Found",{})


            if bcrypt.checkpw(body["password"].encode('utf-8'), user.password.encode('utf-8')):
                return f'Logged in, Welcome {user.name}!', 200
            else:
                return 'Invalid Login Info!', 400
        except AttributeError:
            return create_response(400,'Provide an Cnpj and Password in JSON format in the request body',{"cnpj":"","password":""})


