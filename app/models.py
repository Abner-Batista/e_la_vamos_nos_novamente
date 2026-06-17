from sqlalchemy import Column, Integer, String, Boolean
from app.database import Base


class Livro(Base):
    """Modelo da tabela 'livros' para armazenamento no banco de dados."""

    __tablename__ = "livros"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, nullable=False)
    autor = Column(String, nullable=False)
    paginas = Column(Integer, nullable=False)
    disponivel = Column(Boolean, default=True)
