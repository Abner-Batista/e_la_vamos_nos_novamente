import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, obter_conexao

# Banco de dados SQLite isolado para a execução dos testes automatizados
SQLITE_TESTE_URL = "sqlite:///./acervo_teste.db"

engine_teste = create_engine(
    SQLITE_TESTE_URL, connect_args={"check_same_thread": False}
)

SessaoTeste = sessionmaker(autocommit=False, autoflush=False, bind=engine_teste)


@pytest.fixture
def client():
    # Cria as tabelas do acervo no início de cada caso de teste
    Base.metadata.create_all(bind=engine_teste)

    # Injeta a dependência local simulando a sessão do SQLite
    def simular_conexao():
        sessao = SessaoTeste()
        try:
            yield sessao
        finally:
            sessao.close()

    app.dependency_overrides[obter_conexao] = simular_conexao

    yield TestClient(app)

    # Apaga as tabelas do teste para limpar o ambiente
    Base.metadata.drop_all(bind=engine_teste)
    app.dependency_overrides.clear()
