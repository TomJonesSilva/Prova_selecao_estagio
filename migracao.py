from sqlalchemy import create_engine
from database import Base
import os
from dotenv import load_dotenv

# Carregar variáveis do .env
load_dotenv()

# URL de conexão com o PostgreSQL
DATABASE_URL = os.getenv("DATABASE_URL",  "postgresql://usuario:senha@localhost:5432/seu_banco")

# Criar engine do SQLAlchemy
engine = create_engine(DATABASE_URL)

# Criar as tabelas no banco
Base.metadata.create_all(bind=engine)
