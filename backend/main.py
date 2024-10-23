from fastapi import FastAPI
from backend.entidades import aluno, funcionario, turma
from backend.banco import engine
from backend.tabelas import Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Bem-vindo à API das GATAS do python da Generation!"}

app.include_router(aluno.router, prefix="/alunos", tags=["Alunos"])
app.include_router(turma.router, prefix="/turmas", tags=["Turmas"])
app.include_router(funcionario.router, prefix="/funcionarios", tags=["Funcionários"])

def reset_database():
    print("Dropping all tables...")
    Base.metadata.drop_all(bind=engine)  
    print("Recreating all tables...")
    Base.metadata.create_all(bind=engine)  # parte não funcional
    print("All tables recreated successfully.")