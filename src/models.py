from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import ForeignKey
import uuid

from sqlalchemy.sql.sqltypes import Integer
from config import db

# db.drop_all() Descomente se quiser apagar todos

class Companies(db.Model):
    __tablename__ = "companies"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome = db.Column(db.String(200), nullable=False)
    cnpj = db.Column(db.String(200), unique=True, nullable=False)
    senha = db.Column(db.String(255), nullable=False)

    def to_json(self):
        return {"id": self.id, "fantasy-name": self.nome, "cnpj": self.cnpj}

class Users(db.Model):
    __tablename__ = "users"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome = db.Column(db.String(200),nullable=False)
    email = db.Column(db.String(255),nullable=False,unique=True)
    senha = db.Column(db.String(255),nullable=False) 
    company = db.Column(ForeignKey(Companies.id),nullable=False)

    def to_json(self):
        return {"id": self.id, "name": self.nome, "email": self.email}

class Office(db.Model):
    __tablename__ = "office"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome = db.Column(db.String(255),nullable=False)
    max_capacity= db.Column(db.Integer,nullable=False)
    max_percentage_occupation= db.Column(db.Integer,default=100)
    company = db.Column(ForeignKey(Companies.id),nullable=False)

    def to_json(self):
        return {"id": self.id,"name":self.nome,"max-capacity":self.max_capacity,"max-percentage-occupation":self.max_percentage_occupation}

# db.create_all() # descomenta se quiser criar o banco
