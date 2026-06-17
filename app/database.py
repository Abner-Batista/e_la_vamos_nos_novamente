import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Obtém o endereço de conexão com o banco de dados
CAMINHO_BANCO = os.getenv("DATABASE_URL", "sqlite:///./biblioteca.db")

# Inicializa o mecanismo de conexão do SQLAlchemy
engine = create_engine(CAMINHO_BANCO)

# Configura a sessão local para interagir com o banco
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declarativo base para os modelos do banco
Base = declarative_base()


def obter_conexao():
    """Gera uma sessão de banco de dados e finaliza ao terminar a requisição."""
    conexao = SessionLocal()
    try:
        yield conexao
    finally:
        conexao.close()
