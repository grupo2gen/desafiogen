from sqlalchemy.orm import Session
from backend.controller import estrutura
from fastapi import HTTPException
from backend.controller import regras_token
from backend.controller import tabelas 

def create_funcionario(db: Session, funcionario: estrutura.FuncionarioCreate):
    existing_funcionario = db.query(tabelas.Funcionario).filter(tabelas.Funcionario.email == funcionario.email).first()
    if existing_funcionario:
        raise HTTPException(status_code=400, detail="Já existe um funcionário cadastrado com este e-mail.")
    
    existing_aluno = db.query(tabelas.Aluno).filter(tabelas.Aluno.email == funcionario.email).first()
    if existing_aluno:
        raise HTTPException(status_code=400, detail="Este e-mail já está sendo utilizado por um aluno.")
    
    hashed_password = regras_token.get_password_hash(funcionario.senha)
    db_funcionario = tabelas.Funcionario(**funcionario.dict())
    db_funcionario.senha = hashed_password 

    db.add(db_funcionario)
    db.commit()
    db.refresh(db_funcionario)
    return db_funcionario

def update_funcionario(db: Session, funcionario_id: int, funcionario: estrutura.FuncionarioCreate):
    db_funcionario = db.query(tabelas.Funcionario).filter(tabelas.Funcionario.id == funcionario_id).first()
    if not db_funcionario:
        raise HTTPException(status_code=404, detail="Funcionário não encontrado")
    
    existing_funcionario = db.query(tabelas.Funcionario).filter(tabelas.Funcionario.email == funcionario.email).first()
    if existing_funcionario and existing_funcionario.id != funcionario_id:
        raise HTTPException(status_code=400, detail="Já existe um funcionário com este e-mail.")
    
    existing_aluno = db.query(tabelas.Aluno).filter(tabelas.Aluno.email == funcionario.email).first()
    if existing_aluno:
        raise HTTPException(status_code=400, detail="Este e-mail já está sendo utilizado por um aluno.")
    
    for key, value in funcionario.dict().items():
        setattr(db_funcionario, key, value)
    
    db.commit()
    db.refresh(db_funcionario)
    return db_funcionario

def delete_funcionario(db: Session, funcionario_id: int):
    db_funcionario = db.query(tabelas.Funcionario).filter(tabelas.Funcionario.id == funcionario_id).first()
    if not db_funcionario:
        raise HTTPException(status_code=404, detail="Funcionário não encontrado")
    
    db.delete(db_funcionario)
    db.commit()
    return db_funcionario

def get_funcionario(db: Session, funcionario_id: int):
    return db.query(tabelas.Funcionario).filter(tabelas.Funcionario.id == funcionario_id).first()

def get_all_funcionarios(db: Session):
    return db.query(tabelas.Funcionario).all()

def get_funcionario_by_email(db: Session, email: str):
    return db.query(tabelas.Funcionario).filter(tabelas.Funcionario.email == email).first()
