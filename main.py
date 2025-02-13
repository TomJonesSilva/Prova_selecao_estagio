from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import crud, schemas
from database import SessionLocal, engine
import models
from typing import List

# Cria tabelas no banco
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Função para obter a sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Rota para criar uma empresa
@app.post("/cadastro/empresa/", response_model=schemas.Empresa)
def criar_empresa(empresa: schemas.EmpresaCreate, db: Session = Depends(get_db)):
    return crud.criar_empresa(db=db, empresa=empresa)


# Rota para criar uma obrigação acessória
@app.post("/cadastro/obrigacao_acessoria/", response_model=schemas.ObrigacaoAcessoria)
def criar_obrigacao_acessoria(obrigacao: schemas.ObrigacaoAcessoriaCreate, db: Session = Depends(get_db)):
    return crud.criar_obrigacao_acessoria(db=db, obrigacao=obrigacao)


# Rota para listar todas as empresas
@app.get("/listar/empresas", response_model=List[schemas.Empresa])
def listar_empresas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_empresas(db=db, skip=skip, limit=limit)


# Rota para listar as obrigações acessórias de uma empresa
@app.get("/listar/obrigacao_acessoria/{empresa_id}", response_model=List[schemas.ObrigacaoAcessoria])
def listar_obrigacoes_acessorias(empresa_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_obrigacoes_acessorias(db=db, empresa_id=empresa_id, skip=skip, limit=limit)


# Rota para atualizar uma empresa
@app.put("/atualizar/empresa/{empresa_id}", response_model=schemas.Empresa)
def atualizar_empresa(empresa_id: int, empresa: schemas.EmpresaCreate, db: Session = Depends(get_db)):
    db_empresa = crud.atualizar_empresa(db=db, empresa_id=empresa_id, empresa=empresa)
    if db_empresa is None:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")
    return db_empresa


# Rota para atualizar uma obrigação acessória
@app.put("/atualizar/obrigacao_acessoria/{obrigacao_id}", response_model=schemas.ObrigacaoAcessoria)
def atualizar_obrigacao_acessoria(obrigacao_id: int, obrigacao: schemas.ObrigacaoAcessoriaCreate, db: Session = Depends(get_db)):
    db_obrigacao = crud.atualizar_obrigacao_acessoria(db=db, obrigacao_id=obrigacao_id, obrigacao=obrigacao)
    if db_obrigacao is None:
        raise HTTPException(status_code=404, detail="Obrigação Acessória não encontrada")
    return db_obrigacao


# Rota para excluir uma empresa
@app.delete("/excluir/empresa/{empresa_id}", response_model=schemas.Empresa)
def excluir_empresa(empresa_id: int, db: Session = Depends(get_db)):
    db_empresa = crud.excluir_empresa(db=db, empresa_id=empresa_id)
    if db_empresa is None:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")
    return db_empresa


# Rota para excluir uma obrigação acessória
@app.delete("/excluir/obrigacao_acessoria/{obrigacao_id}", response_model=schemas.ObrigacaoAcessoria)
def excluir_obrigacao_acessoria(obrigacao_id: int, db: Session = Depends(get_db)):
    db_obrigacao = crud.excluir_obrigacao_acessoria(db=db, obrigacao_id=obrigacao_id)
    if db_obrigacao is None:
        raise HTTPException(status_code=404, detail="Obrigação Acessória não encontrada")
    return db_obrigacao

