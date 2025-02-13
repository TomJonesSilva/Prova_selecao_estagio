from pydantic import BaseModel

# Modelo para Empresa
class EmpresaBase(BaseModel):
    nome: str
    cnpj: str
    endereco: str
    email: str
    telefone: str

class EmpresaCreate(EmpresaBase):
    pass

class Empresa(EmpresaBase):
    id: int

    class Config:
        orm_mode = True


# Modelo para Obrigação Acessória
class ObrigacaoAcessoriaBase(BaseModel):
    nome: str
    periodicidade: str  # mensal, trimestral, anual

class ObrigacaoAcessoriaCreate(ObrigacaoAcessoriaBase):
    empresa_id: int

class ObrigacaoAcessoria(ObrigacaoAcessoriaBase):
    id: int
    empresa_id: int

    class Config:
        orm_mode = True
