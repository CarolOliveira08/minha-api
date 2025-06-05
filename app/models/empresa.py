from sqlalchemy import Column, Integer, String, Boolean, Float
from database import Base
class Empresa(Base):
    __tablename__ = "empresa"

    id = Column(Integer, primary_key=True, autoincrement=True)
    cnpj = Column(String(14), nullable=False)#(14) delimita a quant. de dados que
    # pode ser armazenado para não usar espaço desnecessário
    razao_social = Column(String(128), nullable=False)
    nome_fantasia = Column(String(128), nullable=True)
    numero_contato = Column(String(11), nullable=True)
    email_contato = Column(String(128), nullable=True)
    website = Column(String(128), nullable=True)