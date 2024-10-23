from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend import banco, crud, estrutura, regras_token
from backend.regras_token import create_access_token
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()

@router.get("/funcionarios", response_model=list[estrutura.Funcionario])
def read_all_funcionarios(db: Session = Depends(banco.get_db)):
    return crud.get_all_funcionarios(db)

@router.post("/cadastro", response_model=estrutura.Funcionario)
def create_funcionario(funcionario: estrutura.FuncionarioCreate, db: Session = Depends(banco.get_db)):
    return crud.create_funcionario(db, funcionario)

@router.post("/login")
def login_funcionario(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(banco.get_db)):
    funcionario = crud.get_funcionario_by_email(db, form_data.username)
    if not funcionario or not regras_token.verify_password(form_data.password, funcionario.senha):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciais inválidas")
    
    access_token = regras_token.create_access_token(data={"sub": funcionario.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/{funcionario_id}", response_model=estrutura.Funcionario)
def get_funcionario(funcionario_id: int, db: Session = Depends(banco.get_db), current_user: estrutura.Funcionario = Depends(regras_token.get_current_user)):
    db_funcionario = crud.get_funcionario(db, funcionario_id=funcionario_id)
    if db_funcionario is None:
        raise HTTPException(status_code=404, detail="Funcionário não encontrado")
    return db_funcionario

@router.put("/{funcionario_id}", response_model=estrutura.Funcionario)
def update_funcionario(funcionario_id: int, funcionario: estrutura.FuncionarioCreate, db: Session = Depends(banco.get_db), current_user: estrutura.Funcionario = Depends(regras_token.get_current_user)):
    return crud.update_funcionario(db, funcionario_id, funcionario)

@router.delete("/{funcionario_id}", response_model=estrutura.Funcionario)
def delete_funcionario(funcionario_id: int, db: Session = Depends(banco.get_db), current_user: estrutura.Funcionario = Depends(regras_token.get_current_user)):
    return crud.delete_funcionario(db, funcionario_id)
