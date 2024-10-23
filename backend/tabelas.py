from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from backend.banco import Base

class Aluno(Base):
    __tablename__ = "alunos"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome = Column(String, index=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    idade = Column(Integer, nullable=False)
    nota_primeiro_modulo = Column(Integer, nullable=False)
    nota_segundo_modulo = Column(Integer, nullable=False)
    media = Column(Integer)
    turma_id = Column(Integer, ForeignKey('turmas.id'))  

    turma = relationship('Turma', back_populates='alunos')

class Turma(Base):
    __tablename__ = "turmas"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome = Column(String, nullable=False)
    instrutor = Column(String, nullable=False)

    alunos = relationship('Aluno', back_populates='turma') 
    
class Funcionario(Base):
    __tablename__ = "funcionarios"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    senha = Column(String, nullable=False)
    cargo = Column(String, nullable=False)
