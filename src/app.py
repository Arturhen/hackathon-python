from sqlalchemy.dialects.postgresql import UUID
from flask import Flask, Response, request, json
from flask_sqlalchemy import SQLAlchemy
import uuid

from cpf_cnpj.cpf_cnpj import Cnpj


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://root:root@localhost:5432/hackathon'

db = SQLAlchemy(app)


class Companies(db.Model):
    __tablename__ = "companies"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4,)
    nome = db.Column(db.String(200), nullable=False)
    cnpj = db.Column(db.String(200), unique=True, nullable=False)
    senha = db.Column(db.String(255), nullable=False)

    def to_json(self):
        return {"id": self.id, "fantasy-name": self.nome, "cnpj": self.cnpj}

# db.create_all() descomenta se quiser criar o banco

# LIST


@app.route('/companies', methods=["GET"])
def list():
    companies_class = Companies.query.all()
    companies_class_json = [company.to_json() for company in companies_class]

    return create_response(200, "companies", companies_class_json)


# FIND
@app.route('/companies/<cnpj>', methods=["GET"])
def find(cnpj):
    obj_cnpj = Cnpj(cnpj).format()

    company_obj = Companies.query.filter_by(cnpj=obj_cnpj).first()

    if(company_obj is None):
        return Response(status=404)

    company_json = company_obj.to_json()

    return create_response(200, "Company", company_json)


#CREATE
@app.route('/companies', methods=["POST"])
def create():
    body = request.get_json()
    try:
        obj_cpnj = Cnpj(body["cnpj"])
        if(not obj_cpnj.validate()):
            return create_response(400,"Error",{"field":"cnpj invalido"},"No Create")

        company = Companies(nome=body["nome"],
                            cnpj=obj_cpnj.format(), senha=body["senha"])

        db.session.add(company)
        db.session.commit()
        return create_response(201, "Company", company.to_json(), "Create Sucesseful")
    except Exception as e:
        print(e)
        return create_response(400, "Company", {}, "Error in create company")

#Update
@app.route("/companies/<cnpj>",methods=["PUT"])
def update(cnpj):

    obj_cnpj = Cnpj(cnpj).format()

    company_obj= Companies.query.filter_by(cnpj=obj_cnpj).first()

    if(company_obj is None):
        return Response(status=404)

    body = request.get_json()

    try:
        if('nome' in body):
            company_obj.nome = body["nome"]
        if('senha' in body):
            company_obj.senha = body["senha"]
        
        db.session.add(company_obj)
        db.session.commit()

        return create_response(200, "Company", company_obj.to_json(), "Update Sucesseful")
    except Exception as e:
        print(e)
        return create_response(400, "Company", {}, "Error in update company")

@app.route("/companies/<cnpj>",methods=["DELETE"])
def delete(cnpj):
    obj_cnpj = Cnpj(cnpj).format()

    company_obj = Companies.query.filter_by(cnpj=obj_cnpj).first()

    if(company_obj is None):
        return Response(status=404)
    
    try:
        db.session.delete(company_obj)
        db.session.commit()
        return create_response(204,"Company",company_obj.to_json(),"Sucessiful deleted")
    except Exception as e:
        print(e)
        return create_response(400, "Company", {}, "Error in delete company")



def create_response(status, name_content, content, message=False):
    body = {}
    body[name_content] = content

    if(message):
        body[message] = message
    
    return Response(json.dumps(body), status=status, mimetype="application/json")

app.run()
