from sqlalchemy.orm import Session
from backend.controller import estrutura
from fastapi import HTTPException
from backend.controller import regras_token
from backend.controller import tabelas 

def create_aluno(db: Session, aluno: estrutura.AlunoCreate):

    existing_aluno = db.query(tabelas.Aluno).filter(tabelas.Aluno.email == aluno.email).first()
    if existing_aluno:
        raise HTTPException(status_code=400, detail="Já existe um aluno cadastrado com este e-mail.")

    if aluno.turma_id:
        db_turma = db.query(tabelas.Turma).filter(tabelas.Turma.id == aluno.turma_id).first()
        if not db_turma:
            raise HTTPException(status_code=404, detail="Turma não encontrada")

    media = (aluno.nota_primeiro_modulo + aluno.nota_segundo_modulo) / 2
    db_aluno = tabelas.Aluno(**aluno.dict(), media=media)
    db.add(db_aluno)
    db.commit()
    db.refresh(db_aluno)
    return db_aluno

def update_aluno(db: Session, aluno_id: int, aluno: estrutura.AlunoCreate):
    db_aluno = db.query(tabelas.Aluno).filter(tabelas.Aluno.id == aluno_id).first()
    if not db_aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    
    existing_aluno = db.query(tabelas.Aluno).filter(tabelas.Aluno.email == aluno.email).first()
    if existing_aluno and existing_aluno.id != aluno_id:
        raise HTTPException(status_code=400, detail="Já existe um aluno com este e-mail.")
    
    existing_funcionario = db.query(tabelas.Funcionario).filter(tabelas.Funcionario.email == aluno.email).first()
    if existing_funcionario:
        raise HTTPException(status_code=400, detail="Este e-mail já está sendo utilizado por um funcionário.")
    
    for key, value in aluno.dict().items():
        setattr(db_aluno, key, value)
    
    db.commit()
    db.refresh(db_aluno)
    return db_aluno

def delete_aluno(db: Session, aluno_id: int):
    db_aluno = db.query(tabelas.Aluno).filter(tabelas.Aluno.id == aluno_id).first()
    if not db_aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    
    db.delete(db_aluno)
    db.commit()
    return db_aluno

def get_aluno(db: Session, aluno_id: int):
    return db.query(tabelas.Aluno).filter(tabelas.Aluno.id == aluno_id).first()

def get_all_alunos(db: Session):
    return db.query(tabelas.Aluno).all()

