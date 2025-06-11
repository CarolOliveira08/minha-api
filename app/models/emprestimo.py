from sqlalchemy import Column, Integer, String, Date, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func  # For default date
from database import Base


# Association table for Emprestimo and Exemplar
emprestimo_exemplares_table = Table(
    "emprestimo_exemplares",
    Base.metadata,
    Column("emprestimo_id", Integer, ForeignKey("emprestimo.id"), primary_key=True),
    Column("exemplar_id", Integer, ForeignKey("exemplar.id"), primary_key=True),
)


class Emprestimo(Base):
    __tablename__ = "emprestimo"

    id = Column(Integer, primary_key=True, autoincrement=True)
    cliente_id = Column(Integer, ForeignKey("cliente.id"), nullable=False)
    funcionario_id = Column(Integer, ForeignKey("funcionario.id"), nullable=False)
    data_emprestimo = Column(Date, default=func.now(), nullable=False)
    data_devolucao_prevista = Column(Date, nullable=False)
    data_devolucao_real = Column(Date, nullable=True)
    status = Column(String(64), nullable=False, default="ativo")  # e.g., "ativo", "devolvido", "atrasado"

    # Relationships to Cliente and Funcionario
    # These will be filled when Cliente and Funcionario models are updated or if they already exist with back_populates
    # For now, define them simply. The back_populates will be added/checked later.
    cliente = relationship("Cliente", back_populates="emprestimos")
    funcionario = relationship("Funcionario", back_populates="emprestimos")

    exemplares = relationship("Exemplar", secondary=emprestimo_exemplares_table, back_populates="emprestimos")
