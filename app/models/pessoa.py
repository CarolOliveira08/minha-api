from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base

class Pessoa(Base):
    __tablename__ = "pessoa"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(128), nullable=False)
    sobrenome = Column(String(128), nullable=True)
    email = Column(String(128), unique=True, nullable=True)
    telefone = Column(String(32), nullable=True)
    endereco = Column(String(255), nullable=True)

    cliente = relationship("Cliente", back_populates="pessoa", uselist=False)
    funcionario = relationship("Funcionario", back_populates="pessoa", uselist=False)
