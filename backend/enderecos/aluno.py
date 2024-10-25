from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.crud import crud_aluno

from backend.controller import banco, estrutura, regras_token

router = APIRouter()

@router.get("/alunos", response_model=list[estrutura.Aluno])
def read_all_alunos(db: Session = Depends(banco.get_db)):
    return crud_aluno.get_all_alunos(db)

@router.post("/", response_model=estrutura.Aluno)
def create_aluno(aluno: estrutura.AlunoCreate, db: Session = Depends(banco.get_db), current_user: estrutura.Funcionario = Depends(regras_token.get_current_user)):
    return crud_aluno.create_aluno(db, aluno)

@router.get("/{aluno_id}", response_model=estrutura.Aluno)
def get_aluno(aluno_id: int, db: Session = Depends(banco.get_db), current_user: estrutura.Funcionario = Depends(regras_token.get_current_user)):
    db_aluno = crud_aluno.get_aluno(db, aluno_id=aluno_id)
    if db_aluno is None:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    return db_aluno

@router.put("/{aluno_id}", response_model=estrutura.Aluno)
def update_aluno(aluno_id: int, aluno: estrutura.AlunoCreate, db: Session = Depends(banco.get_db), current_user: estrutura.Funcionario = Depends(regras_token.get_current_user)):
    return crud_aluno.update_aluno(db, aluno_id, aluno)

@router.delete("/{aluno_id}", response_model=estrutura.Aluno)
def delete_aluno(aluno_id: int, db: Session = Depends(banco.get_db), current_user: estrutura.Funcionario = Depends(regras_token.get_current_user)):
    return crud_aluno.delete_aluno(db, aluno_id)
