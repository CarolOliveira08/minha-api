from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Funcionario(Base):
    __tablename__ = "funcionario"

    id = Column(Integer, primary_key=True, autoincrement=True)
    pessoa_id = Column(Integer, ForeignKey("pessoa.id"), nullable=False)
    cargo = Column(String(64), nullable=True)
    data_contratacao = Column(Date, nullable=True)

    pessoa = relationship("Pessoa", back_populates="funcionario")
