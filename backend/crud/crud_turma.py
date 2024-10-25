from sqlalchemy.orm import Session
from backend.controller import estrutura
from fastapi import HTTPException
from backend.controller import regras_token
from backend.controller import tabelas 

def create_turma(db: Session, turma: estrutura.TurmaCreate):
    db_turma = tabelas.Turma(nome=turma.nome, instrutor=turma.instrutor)
    db.add(db_turma)
    db.commit()
    db.refresh(db_turma)
    return db_turma

def get_turma(db: Session, turma_id: int):
    db_turma = db.query(tabelas.Turma).filter(tabelas.Turma.id == turma_id).first()
    if db_turma is None:
        raise HTTPException(status_code=404, detail="Turma não encontrada")
    return db_turma


def update_turma(db: Session, turma_id: int, turma: estrutura.TurmaCreate):
    db_turma = db.query(tabelas.Turma).filter(tabelas.Turma.id == turma_id).first()
    if not db_turma:
        raise HTTPException(status_code=404, detail="Turma não encontrada")
    
    for key, value in turma.dict().items():
        setattr(db_turma, key, value)
    
    db.commit()
    db.refresh(db_turma)
    return db_turma

def delete_turma(db: Session, turma_id: int):
    db_turma = db.query(tabelas.Turma).filter(tabelas.Turma.id == turma_id).first()
    if not db_turma:
        raise HTTPException(status_code=404, detail="Turma não encontrada")
    
    db.delete(db_turma)
    db.commit()
    return db_turma

def get_all_turmas(db: Session):
    return db.query(tabelas.Turma).all()
