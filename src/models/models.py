from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import ForeignKey
import uuid

from config import db


class Companies(db.Model):
    __tablename__ = "companies"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(200), nullable=False)
    cnpj = db.Column(db.String(200), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    users = db.relationship("Users", cascade="all, delete")
    offices = db.relationship("Office", cascade="all, delete")

    def to_json(self):
        return {"id": self.id, "name": self.name, "cnpj": self.cnpj}


class Users(db.Model):
    __tablename__ = "users"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    company = db.Column(ForeignKey(Companies.id), nullable=False)
    appointments = db.relationship("Appointments", cascade="all, delete")

    def to_json(self):
        return {"id": self.id, "name": self.name, "email": self.email}


class Office(db.Model):
    __tablename__ = "office"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(255), nullable=False)
    max_capacity = db.Column(db.Integer, nullable=False)
    max_percentage_occupation = db.Column(db.Integer, default=100)
    company = db.Column(ForeignKey(Companies.id), nullable=False)
    appointments = db.relationship("Appointments", cascade="all, delete")

    def to_json(self):
        return {"id": self.id, "name": self.name, "max_capacity": self.max_capacity, "max_percentage_occupation": self.max_percentage_occupation}


class Appointments(db.Model):
    __tablename__ = "appointments"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    date = db.Column(db.Date, nullable=False)
    office = db.Column(ForeignKey(Office.id), nullable=False)
    user = db.Column(ForeignKey(Users.id), nullable=False)

    def to_json(self):
        return {"id": self.id, "date": self.date, "office": self.office, "user": self.user}

# db.drop_all() #Descomente se quiser apagar todos
# db.create_all() # descomenta se quiser criar o banco
