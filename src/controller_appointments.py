from flask.wrappers import Response

from create_response import create_response
from models import Appointments,Office,Users
from config import db

class AppointmentController:
    @staticmethod
    def create(body):
        #Ver se é depois do dia
        if("date" not in body):
            return create_response(400,"Appointment",{"fields":"date is required"},"Not Created")
        
        if(not validate(body["date"])):
            return create_response(400,"Appoitment",{"fields":"Incorrect data format, should be YYYY-MM-DD"},"Not Created")

        try:

            user = Users.query.filter_by(id=body["user"]).first()
            office = Office.query.filter_by(id=body["office"]).first()

            if(user.company != office.company):
                return create_response(400,"Appointment",{},"You do Not Have authorization")

            have_same_appointment = Appointments.query.filter_by(date=body["date"],user=body["user"]).first()
            if(have_same_appointment is not None):
                print(have_same_appointment.date)
                return create_response(400,"Appointment",{"fields":"Another appointment like this one was set"},"Not Created")

            appoitments_in_same_day = len(Appointments.query.filter_by(office=body["office"],date=body["date"]).all())

            if(appoitments_in_same_day>=(office.max_percentage_occupation * office.max_capacity)/100):
                return create_response(400,"Appointment",{},"The Office is full that day")
            
            appoitment = Appointments(date=body["date"],office=body["office"],user=body["user"])
            db.session.add(appoitment)
            db.session.commit()
            return create_response(201, "Appointment", appoitment.to_json(), "Create Successful")
        except Exception as e:
            print(e)
            return create_response(400, "Appointment", {}, "Error in create appointment")

    @staticmethod
    def delete(appointment_id):
        try:
            obj_appointment = Appointments.query.filter_by(id=appointment_id).first()

            if(obj_appointment is None):
                return Response(status=404)

            db.session.delete(obj_appointment)
            db.session.commit()
            return create_response(204, "Appointment", obj_appointment.to_json(), "Successful deleted")
        except Exception as e:
            print(e)
            return create_response(400, "Appointment", {}, "Error in delete appointment")



def validate(date_text):
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
        return True
    except ValueError:
        return False