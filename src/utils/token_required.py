from functools import wraps
from flask import request
import jwt

from create_response import create_response
from models import Companies, Users


def token_required(f):
    @wraps(f)
    def decorated(*args,**kwargs):
        secret ='4b6d207afe3bcc9381b1f0301733861277bca526ad029b2a'

        token = None
        if 'x-acess-token' in request.headers:
            token = request.headers['x-acess-token']
        if not token:
            return create_response(401,"Fail Request",{"message":"Token is Missing"})

        try:
            data = jwt.decode(token,secret)
            if(data["type"] =="company"):
                current_user = Companies.query.filter_by(id=data["id"]).first()
            if(data["type"] =="user"):
                current_user = Users.query.filter_by(id=data["id"]).first()
        except Exception:
            return create_response(401,"Fail Request",{"message": "token is invalid"})

        return f(current_user,*args,**kwargs)
    return decorated
