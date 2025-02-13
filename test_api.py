from fastapi.testclient import TestClient
from main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base

# Configuração do banco de dados em memória para os testes
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

# Cria o engine do banco de dados para os testes
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Cria as tabelas no banco de dados de teste
Base.metadata.create_all(bind=engine)

# Cria a instância do cliente para testar os endpoints
client = TestClient(app)

# obter a sessão do banco de dados de testes
def get_test_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# teste para o endpoint de criação de empresa
def test_criar_empresa():
    response = client.post(
        "/cadastro/empresa/",
        json={"nome": "Empresa Teste", "cnpj": "12345678000195", "endereco": "Rua Teste, 123", "email": "empresa@teste.com", "telefone": "1234567890"},
    )
    assert response.status_code == 200
    assert response.json()["nome"] == "Empresa Teste"
    assert response.json()["cnpj"] == "12345678000195"


# Teste para o endpoint de criação de obrigação acessória
def test_criar_obrigacao_acessoria():
    # cria uma empresa
    response_empresa = client.post(
        "/cadastro/empresa/",
        json={"nome": "Empresa Teste", "cnpj": "123456780001", "endereco": "Rua Teste, 123", "email": "empresa@teste.com", "telefone": "1234567890"},
    )
    empresa_id = response_empresa.json()["id"]

    #cria a obrigação acessória para a empresa
    response_obrigacao = client.post(
        "/cadastro/obrigacao_acessoria/",
        json={"nome": "Obr. Acessória Teste", "periodicidade": "mensal", "empresa_id": empresa_id},
    )
    assert response_obrigacao.status_code == 200
    assert response_obrigacao.json()["nome"] == "Obr. Acessória Teste"
    assert response_obrigacao.json()["empresa_id"] == empresa_id


# Teste para listar todas as empresas
def test_listar_empresas():
    response = client.get("/listar/empresas")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


# Teste para listar as obrigações acessórias de uma empresa
def test_listar_obrigacoes_acessorias():
    # cria uma empresa
    response_empresa = client.post(
        "/cadastro/empresa/",
        json={"nome": "Empresa Teste", "cnpj": "12340", "endereco": "Rua Teste, 123", "email": "empresa@teste.com", "telefone": "1234567890"},
    )
    empresa_id = response_empresa.json()["id"]

    # cria a obrigação acessória
    client.post(
        "/cadastro/obrigacao_acessoria/",
        json={"nome": "Obr. Acessória Teste", "periodicidade": "mensal", "empresa_id": empresa_id},
    )

    # lista as obrigações
    response_obrigacoes = client.get(f"/listar/obrigacao_acessoria/{empresa_id}")
    assert response_obrigacoes.status_code == 200
    assert isinstance(response_obrigacoes.json(), list)
    assert len(response_obrigacoes.json()) > 0

# Teste para o endpoint de atualização de empresa
def test_update_empresa():
    # Cria uma empresa
    response = client.post(
        "/cadastro/empresa/",
        json={"nome": "Empresa Teste", "cnpj": "12341", "endereco": "Rua Teste, 123", "email": "empresa@teste.com", "telefone": "1234567890"},
    )
    empresa_id = response.json()["id"]
    
    # Atualizando a empresa
    update_data = {"nome": "Empresa Atualizada", "cnpj": "12341", "endereco": "Rua Atualizada, 123", "email": "empresa_atualizada@teste.com", "telefone": "0987654321"}
    response_update = client.put(f"/atualizar/empresa/{empresa_id}", json=update_data)

    assert response_update.status_code == 200
    updated_empresa = response_update.json()
    assert updated_empresa["nome"] == "Empresa Atualizada"
    assert updated_empresa["email"] == "empresa_atualizada@teste.com"
    assert updated_empresa["telefone"] == "0987654321"



# Teste para o endpoint de atualização de obrigação acessória
def test_update_obrigacao_acessoria():
    # Cria uma empresa e uma obrigação
    response_empresa = client.post(
        "/cadastro/empresa/",
        json={"nome": "Empresa Teste", "cnpj": "12342", "endereco": "Rua Teste, 123", "email": "empresa@teste.com", "telefone": "1234567890"},
    )
    empresa_id = response_empresa.json()["id"]

    response_obrigacao = client.post(
        "/cadastro/obrigacao_acessoria/",
        json={"nome": "Obr. Acessória Teste", "periodicidade": "mensal", "empresa_id": empresa_id},
    )
    obrigacao_id = response_obrigacao.json()["id"]
    
    # Atualizar a obrigação
    update_data = {"nome": "Obr. Acessória Atualizada", "periodicidade": "trimestral", "empresa_id": empresa_id}
    response_update = client.put(f"/atualizar/obrigacao_acessoria/{obrigacao_id}", json=update_data)

    assert response_update.status_code == 200
    updated_obrigacao = response_update.json()
    assert updated_obrigacao["nome"] == "Obr. Acessória Atualizada"
    assert updated_obrigacao["periodicidade"] == "trimestral"


# Teste para o endpoint de deleção de empresa
def test_delete_empresa():
    # Cria uma empresa
    response = client.post(
        "/cadastro/empresa/",
        json={"nome": "Empresa Teste", "cnpj": "12343", "endereco": "Rua Teste, 123", "email": "empresa@teste.com", "telefone": "1234567890"},
    )
    empresa_id = response.json()["id"]

    # Deletar a empresa
    response_delete = client.delete(f"/excluir/empresa/{empresa_id}")
    assert response_delete.status_code == 200

    # Verificar que a empresa foi excluída
    response_check = client.get(f"/listar/empresas/{empresa_id}")
    assert response_check.status_code == 404  # Não deve encontrar a empresa

    
# Teste para o endpoint de deleção de obrigação acessória
def test_delete_obrigacao_acessoria():
    # Cria uma empresa e uma obrigação
    response_empresa = client.post(
        "/cadastro/empresa/",
        json={"nome": "Empresa Teste", "cnpj": "12344", "endereco": "Rua Teste, 123", "email": "empresa@teste.com", "telefone": "1234567890"},
    )
    empresa_id = response_empresa.json()["id"]

    response_obrigacao = client.post(
        "/cadastro/obrigacao_acessoria/",
        json={"nome": "Obr. Acessória Teste", "periodicidade": "mensal", "empresa_id": empresa_id},
    )
    obrigacao_id = response_obrigacao.json()["id"]
    
    # Deletar a obrigação
    response_delete = client.delete(f"/excluir/obrigacao_acessoria/{obrigacao_id}")
    assert response_delete.status_code == 200

    # Verificar que a obrigação foi excluída
    response_check = client.get(f"/listar/obrigacao_acessoria/{empresa_id}")
    obrigacoes = response_check.json()
    assert len(obrigacoes) == 0  
