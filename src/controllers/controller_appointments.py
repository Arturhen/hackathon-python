import datetime
from flask.wrappers import Response

from utils.create_response import create_response
from models.models import Appointments, Office, Users
from config import db


class AppointmentController:
    @staticmethod
    def create(body,user_id,company_id):
        if("date" not in body):
            return create_response(400, "Appointment", {"fields": "date is required"}, "Not Created")

        if(not validate(body["date"])):
            return create_response(400, "Appoitment", {"fields": "Incorrect data format, should be YYYY-MM-DD"}, "Not Created")

        try:

            user = Users.query.filter_by(id=user_id,company=company_id).first()
            office = Office.query.filter_by(id=body["office"],company=company_id).first()

            if(user.company != office.company):
                return create_response(400, "Appointment", {}, "You do Not Have authorization")

            have_same_appointment = Appointments.query.filter_by(
                date=body["date"], user=user_id).first()
            if(have_same_appointment is not None):
                print(have_same_appointment.date)
                return create_response(400, "Appointment", {"fields": "Another appointment like this one was set"}, "Not Created")

            appoitments_in_same_day = len(Appointments.query.filter_by(
                office=body["office"], date=body["date"]).all())

            if(appoitments_in_same_day >= (office.max_percentage_occupation * office.max_capacity)/100):
                return create_response(400, "Appointment", {}, "The Office is full that day")

            appoitment = Appointments(
                date=body["date"], office=body["office"], user=user_id)
            db.session.add(appoitment)
            db.session.commit()
            return create_response(201, "Appointment", appoitment.to_json(), "Create Successful")
        except Exception as e:
            print(e)
            return create_response(400, "Appointment", {}, "Error in create appointment")

    @staticmethod
    def delete(appointment_id,user_id):
        try:
            obj_appointment = Appointments.query.filter_by(
                id=appointment_id,user=user_id).first()

            if(obj_appointment is None):
                return Response(status=404)

            db.session.delete(obj_appointment)
            db.session.commit()
            return create_response(204, "Appointment", obj_appointment.to_json(), "Successful deleted")
        except Exception as e:
            print(e)
            return create_response(400, "Appointment", {}, "Error in delete appointment")

    @staticmethod
    def list(user_id, office_id,company_id):
        try:
            if(user_id is not None):
                user_valid = Users.query.filter_by(id=user_id,company=company_id).first()
                if(user_valid is None):
                    return create_response(401, "appointments", {"message":"Unauthorized"})

                appointments_by_user = Appointments.query.filter_by(
                    user=user_id).all()
                appointments_by_user_json = [
                    appointment.to_json() for appointment in appointments_by_user]
                if(office_id is None):
                    return create_response(200, "appointments", appointments_by_user_json)

            if(office_id is not None):
                office_valid = Office.query.filter_by(id=office_id,company=company_id).first()
                if(office_valid is None):
                    return create_response(401, "appointments", {"message":"Unauthorized"})

                appointments_by_office = Appointments.query.filter_by(
                    office=office_id).all()
                appointments_by_office_json = [
                    appointment.to_json() for appointment in appointments_by_office]
                if(user_id is None):
                    return create_response(200, "appointments", appointments_by_office_json)

            appointments_json = []
            for appointment in appointments_by_user_json:
                if(appointment in appointments_by_office_json):
                    appointments_json.append(appointment)

            return create_response(200, "appointments", appointments_json)

        except Exception as e:
            print(e)
            return create_response(400, "Appointment", {}, "Error in list appointments")


def validate(date_text):
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
        return True
    except ValueError:
        return False
