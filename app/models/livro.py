from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base

class Livro(Base):
    __tablename__ = "livro"

    id = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String(255), nullable=False)
    autor = Column(String(255), nullable=True)
    isbn = Column(String(20), unique=True, nullable=True)
    editora = Column(String(128), nullable=True)
    ano_publicacao = Column(Integer, nullable=True)

    exemplares = relationship("Exemplar", back_populates="livro")
