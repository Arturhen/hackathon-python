import re   

from config import db
from models import Users 
from create_response import create_response  

class UserController:
    @staticmethod
    def create(body):
        email = body["email"]
        
        if(not check_email(email)):
            return  create_response(400,"Error", {"field":"Email invalid format"},"Usuario não Cadastrado")

        if(Users.query.filter_by(email=email).first()):
            return create_response(400,"Error",{"field":"Exist another user with this Email"})        

        try:
            user = Users(nome=body["nome"], email=body["email"], senha=body["senha"], company=body["company"])
            db.session.add(user)
            db.session.commit()
            return create_response(201, "User",user.to_json(),"Create Successful")

        except Exception as e:
            print(e)
            return create_response(400, "Error",{}, "Error in create User")

  
def check_email(email):  
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'  

    if(re.search(regex,email)):   
        return True   

    return False
              