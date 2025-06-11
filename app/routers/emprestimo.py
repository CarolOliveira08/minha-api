from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from datetime import date
from pydantic import BaseModel

from app.database import get_db
from app.models.emprestimo import Emprestimo
from app.models.cliente import Cliente
from app.models.funcionario import Funcionario
from app.models.exemplar import Exemplar # To fetch exemplars by ID
# Assuming Livro model might be needed for more detailed ExemplarInfoSchema later, but not for current definition
# from app.models.livro import Livro

router = APIRouter(prefix="/emprestimos", tags=["emprestimos"])

# Schemas
class ExemplarInfoSchema(BaseModel):
    id: int
    codigo_exemplar: str
    # To include Livro details, you'd need to resolve relationships and potentially have a LivroInfoSchema
    # e.g., livro_titulo: Optional[str] = None

    class Config:
        orm_mode = True


@router.get("/", response_model=List[EmprestimoResponse])
def list_emprestimos(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    try:
        emprestimos = (
            db.query(Emprestimo)
            .options(joinedload(Emprestimo.exemplares)) # Eager load exemplares
            .offset(skip)
            .limit(limit)
            .all()
        )
        return emprestimos
    except Exception as e:
        # Log the error e for debugging
        raise HTTPException(status_code=500, detail="An error occurred while fetching emprestimos.")


@router.get("/{emprestimo_id}", response_model=EmprestimoResponse)
def get_emprestimo(emprestimo_id: int, db: Session = Depends(get_db)):
    try:
        emprestimo = (
            db.query(Emprestimo)
            .options(joinedload(Emprestimo.exemplares)) # Eager load exemplares
            .filter(Emprestimo.id == emprestimo_id)
            .first()
        )
        if not emprestimo:
            raise HTTPException(status_code=404, detail=f"Emprestimo with id {emprestimo_id} not found")
        return emprestimo
    except HTTPException:
        raise
    except Exception as e:
        # Log the error e for debugging
        raise HTTPException(status_code=500, detail="An error occurred while fetching the emprestimo.")


@router.post("/", response_model=EmprestimoResponse, status_code=201)
def create_emprestimo(emprestimo_data: EmprestimoCreate, db: Session = Depends(get_db)):
    try:
        # Fetch Cliente
        cliente = db.query(Cliente).filter(Cliente.id == emprestimo_data.cliente_id).first()
        if not cliente:
            raise HTTPException(status_code=404, detail=f"Cliente with id {emprestimo_data.cliente_id} not found")

        # Fetch Funcionario
        funcionario = db.query(Funcionario).filter(Funcionario.id == emprestimo_data.funcionario_id).first()
        if not funcionario:
            raise HTTPException(status_code=404, detail=f"Funcionario with id {emprestimo_data.funcionario_id} not found")

        # Fetch Exemplares
        if not emprestimo_data.exemplar_ids:
            raise HTTPException(status_code=400, detail="At least one exemplar ID must be provided")

        exemplares_db = []
        for exemplar_id in emprestimo_data.exemplar_ids:
            exemplar = db.query(Exemplar).filter(Exemplar.id == exemplar_id).first()
            if not exemplar:
                raise HTTPException(status_code=404, detail=f"Exemplar with id {exemplar_id} not found")
            if not exemplar.disponivel:
                raise HTTPException(status_code=400, detail=f"Exemplar with id {exemplar_id} is not available")
            exemplares_db.append(exemplar)

        # Create Emprestimo instance
        new_emprestimo = Emprestimo(
            cliente_id=emprestimo_data.cliente_id,
            funcionario_id=emprestimo_data.funcionario_id,
            data_devolucao_prevista=emprestimo_data.data_devolucao_prevista,
            status=emprestimo_data.status
            # data_emprestimo is set by default in the model
        )

        # Associate exemplares and mark them as unavailable
        for exemplar in exemplares_db:
            new_emprestimo.exemplares.append(exemplar)
            exemplar.disponivel = False
            db.add(exemplar) # Add exemplar to session to track changes

        db.add(new_emprestimo)
        db.commit()
        db.refresh(new_emprestimo)
        # Need to refresh exemplares as well if their changes need to be immediately reflected from DB
        # For now, new_emprestimo contains the relationships correctly populated for the response

        return new_emprestimo

    except HTTPException:
        # Re-raise HTTPException to let FastAPI handle it
        raise
    except Exception as e:
        db.rollback()
        # Log the error e for debugging
        raise HTTPException(status_code=500, detail="An error occurred while creating the emprestimo.")

class EmprestimoBase(BaseModel):
    cliente_id: int
    funcionario_id: int
    data_devolucao_prevista: date
    status: Optional[str] = "ativo"

class EmprestimoCreate(EmprestimoBase):
    exemplar_ids: List[int]

class EmprestimoResponse(EmprestimoBase):
    id: int
    data_emprestimo: date
    data_devolucao_real: Optional[date] = None
    exemplares: List[ExemplarInfoSchema]

    class Config:
        orm_mode = True
