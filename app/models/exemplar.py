from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey, Table
from sqlalchemy.orm import relationship
from database import Base
from .emprestimo import emprestimo_exemplares_table # Import the association table

class Exemplar(Base):
    __tablename__ = "exemplar"

    id = Column(Integer, primary_key=True, autoincrement=True)
    livro_id = Column(Integer, ForeignKey("livro.id"), nullable=False)
    codigo_exemplar = Column(String(64), unique=True, nullable=False)
    data_aquisicao = Column(Date, nullable=True)
    situacao = Column(String(64), nullable=True)
    disponivel = Column(Boolean, default=True)

    livro = relationship("Livro", back_populates="exemplares")
    emprestimos = relationship("Emprestimo", secondary=emprestimo_exemplares_table, back_populates="exemplares")
