from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy.orm import Session

from database import get_db
from app.models.empresa import Empresa

router = APIRouter(prefix="/empresas")

class CompanyResponse(BaseModel):
    id: int
    cnpj: str
    razao_social: str
    nome_fantasia: Optional[str] = None
    numero_contato: Optional[str] = None
    email_contato: Optional[str] = None
    website: Optional[str] = None

    class Config:
        orm_mode = True


class CompanyCreate(BaseModel):
    cnpj: str
    razao_social: str
    nome_fantasia: Optional[str] = None
    numero_contato: Optional[str] = None
    email_contato: Optional[str] = None
    website: Optional[str] = None


@router.get("/", response_model=List[CompanyResponse], response_description="Essa rota lista todas as bibliotecas que existem")
def lista_empresas(db: Session = Depends(get_db)):
    try:
        empresas = db.query(Empresa).all()
        return empresas
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while fetching companies.")

@router.post("/", response_model=CompanyResponse, status_code=201)
def criar_empresas(empresa_data: CompanyCreate, db: Session = Depends(get_db)):
    try:
        new_empresa = Empresa(**empresa_data.dict())
        db.add(new_empresa)
        db.commit()
        db.refresh(new_empresa)
        return new_empresa
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="An error occurred while creating the company.")
