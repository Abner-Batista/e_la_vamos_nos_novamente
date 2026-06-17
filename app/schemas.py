from pydantic import BaseModel, ConfigDict


class LivroEntrada(BaseModel):
    """Esquema de dados enviado para cadastrar ou editar um livro."""

    titulo: str
    autor: str
    paginas: int
    disponivel: bool = True


class LivroSaida(BaseModel):
    """Esquema de dados retornado pela API contendo o ID do livro."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    titulo: str
    autor: str
    paginas: int
    disponivel: bool
