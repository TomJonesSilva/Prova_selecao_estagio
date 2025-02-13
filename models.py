from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Empresa(Base):
    __tablename__ = "empresas"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    cnpj = Column(String, unique=True, index=True)
    endereco = Column(String)
    email = Column(String)
    telefone = Column(String)

    # Relacionamento com a tabela de Obrigação Acessória
    obrigacoes_acessorias = relationship("ObrigacaoAcessoria", back_populates="empresa")


class ObrigacaoAcessoria(Base):
    __tablename__ = "obrigacoes_acessorias"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    periodicidade = Column(String)  # mensal, trimestral, anual
    empresa_id = Column(Integer, ForeignKey("empresas.id"))

    # Relacionamento com a tabela Empresa
    empresa = relationship("Empresa", back_populates="obrigacoes_acessorias")
