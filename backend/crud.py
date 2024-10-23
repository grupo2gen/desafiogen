from sqlalchemy.orm import Session
from backend import estrutura, tabelas
from fastapi import HTTPException
from backend import regras_token 

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
