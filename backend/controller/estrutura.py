from pydantic import BaseModel, EmailStr, Field, constr, validator
from pydantic import BaseModel, EmailStr, Field, constr
from typing import Optional, List
from typing import Optional
import re

EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")

class AlunoBase(BaseModel):
    nome: constr(min_length=3)
    email: EmailStr
    idade: int
    nota_primeiro_modulo: float = Field(..., le=10.0)
    nota_segundo_modulo: float = Field(..., le=10.0)
    turma_id: Optional[int]  

class AlunoCreate(AlunoBase):
    pass

class Aluno(AlunoBase):
    id: int
    media: float

    class Config:
        from_attributes = True

class TurmaBase(BaseModel):
    nome: constr(min_length=3)
    instrutor: constr(min_length=3)

class TurmaCreate(TurmaBase):
    pass

class Turma(TurmaBase):
    id: int
    alunos: List[Aluno] 

    class Config:
        from_attributes = True

class FuncionarioBase(BaseModel):
    nome: constr(min_length=3)
    email: EmailStr
    senha: constr(min_length=6)
    cargo: str

    @validator('email')
    def validar_email(cls, v):
        if not EMAIL_REGEX.match(v):
            raise ValueError('E-mail inválido')
        return v

class FuncionarioCreate(FuncionarioBase):
    pass

class Funcionario(FuncionarioBase):
    id: int

    class Config:
        from_attributes = True
