import datetime
from create_response import create_response
from models import Appointments
from config import db

class AppointmentController:
    @staticmethod
    def create(body):
        #verificar se ta cheio, verificar se ambos sao o mesmo id de company, verificar se a pessoa ja marcou
        if("date" not in body):
            return create_response(400,"Appointment",{"fields":"date is required"},"Not Created")
        
        if(not validate(body["date"])):
            return create_response(400,"Appoitment",{"fields":"Incorrect data format, should be YYYY-MM-DD"},"Not Created")

        try:
            appoitment = Appointments(date=body["date"],office=body["office"],user=body["user"])
            db.session.add(appoitment)
            db.session.commit()
            return create_response(201, "Appointment", appoitment.to_json(), "Create Successful")
        except Exception as e:
            print(e)
            return create_response(400, "Appointment", {}, "Error in create appointment")

    @staticmethod
    def delete():
        return True

def validate(date_text):
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
        return True
    except ValueError:
        return False