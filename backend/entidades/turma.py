from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend import banco, crud, estrutura, regras_token

router = APIRouter()

@router.get("/turmas", response_model=list[estrutura.Turma])
def read_all_turmas(db: Session = Depends(banco.get_db)):
    return crud.get_all_turmas(db)

@router.post("/", response_model=estrutura.Turma)
def create_turma(turma: estrutura.TurmaCreate, db: Session = Depends(banco.get_db), current_user: estrutura.Funcionario = Depends(regras_token.get_current_user)):
    return crud.create_turma(db, turma)

@router.get("/{turma_id}", response_model=estrutura.Turma)
def get_turma(turma_id: int, db: Session = Depends(banco.get_db), current_user: estrutura.Funcionario = Depends(regras_token.get_current_user)):
    return crud.get_turma(db, turma_id)

@router.put("/{turma_id}", response_model=estrutura.Turma)
def update_turma(turma_id: int, turma: estrutura.TurmaCreate, db: Session = Depends(banco.get_db), current_user: estrutura.Funcionario = Depends(regras_token.get_current_user)):
    return crud.update_turma(db, turma_id, turma)

@router.delete("/{turma_id}", response_model=estrutura.Turma)
def delete_turma(turma_id: int, db: Session = Depends(banco.get_db), current_user: estrutura.Funcionario = Depends(regras_token.get_current_user)):
    return crud.delete_turma(db, turma_id)
