from sqlalchemy.orm import Session
import models
import schemas

# Função para criar uma nova empresa
def criar_empresa(db: Session, empresa: schemas.EmpresaCreate):
    db_empresa = models.Empresa(**empresa.dict())
    db.add(db_empresa)
    db.commit()
    db.refresh(db_empresa)
    return db_empresa

# Função para criar uma nova obrigação acessória
def criar_obrigacao_acessoria(db: Session, obrigacao: schemas.ObrigacaoAcessoriaCreate):
    db_obrigacao = models.ObrigacaoAcessoria(**obrigacao.dict())
    db.add(db_obrigacao)
    db.commit()
    db.refresh(db_obrigacao)
    return db_obrigacao

# Função para obter todas as empresas
def get_empresas(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Empresa).offset(skip).limit(limit).all()

# Função para obter todas as obrigações acessórias de uma empresa
def get_obrigacoes_acessorias(db: Session, empresa_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.ObrigacaoAcessoria).filter(models.ObrigacaoAcessoria.empresa_id == empresa_id).offset(skip).limit(limit).all()




# Função para atualizar uma empresa
def atualizar_empresa(db: Session, empresa_id: int, empresa: schemas.EmpresaCreate):
    db_empresa = db.query(models.Empresa).filter(models.Empresa.id == empresa_id).first()
    if db_empresa:
        for key, value in empresa.dict().items():
            setattr(db_empresa, key, value)  
        db.commit()
        db.refresh(db_empresa)
        return db_empresa
    return None


# Função para atualizar uma obrigação acessória
def atualizar_obrigacao_acessoria(db: Session, obrigacao_id: int, obrigacao: schemas.ObrigacaoAcessoriaCreate):
    db_obrigacao = db.query(models.ObrigacaoAcessoria).filter(models.ObrigacaoAcessoria.id == obrigacao_id).first()
    if db_obrigacao:
        for key, value in obrigacao.dict().items():
            setattr(db_obrigacao, key, value)  # Atualiza os campos da obrigação acessória
        db.commit()
        db.refresh(db_obrigacao)
        return db_obrigacao
    return None



# Função para excluir uma empresa
def excluir_empresa(db: Session, empresa_id: int):
    db_empresa = db.query(models.Empresa).filter(models.Empresa.id == empresa_id).first()
    if db_empresa:
        db.delete(db_empresa)
        db.commit()
        return db_empresa
    return None


# Função para excluir uma obrigação acessória
def excluir_obrigacao_acessoria(db: Session, obrigacao_id: int):
    db_obrigacao = db.query(models.ObrigacaoAcessoria).filter(models.ObrigacaoAcessoria.id == obrigacao_id).first()
    if db_obrigacao:
        db.delete(db_obrigacao)
        db.commit()
        return db_obrigacao
    return None

