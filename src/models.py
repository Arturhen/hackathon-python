from sqlalchemy.dialects.postgresql import UUID
import uuid
from config import db


class Companies(db.Model):
    __tablename__ = "companies"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4,)
    nome = db.Column(db.String(200), nullable=False)
    cnpj = db.Column(db.String(200), unique=True, nullable=False)
    senha = db.Column(db.String(255), nullable=False)

    def to_json(self):
        return {"id": self.id, "fantasy-name": self.nome, "cnpj": self.cnpj}

# db.create_all() descomenta se quiser criar o banco
