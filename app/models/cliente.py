from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Cliente(Base):
    __tablename__ = "cliente"

    id = Column(Integer, primary_key=True, autoincrement=True)
    pessoa_id = Column(Integer, ForeignKey("pessoa.id"), nullable=False)
    codigo = Column(String(64), unique=True, nullable=True)
    observacoes = Column(String(255), nullable=True)

    pessoa = relationship("Pessoa", back_populates="cliente")
