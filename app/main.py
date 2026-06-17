import time
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import OperationalError

from app.database import engine, Base, obter_conexao
from app.models import Livro
from app.schemas import LivroEntrada, LivroSaida

# Tenta estabelecer a estrutura do banco com retentativas para evitar falhas do Docker
maximo_tentativas = 12
for loop in range(maximo_tentativas):
    try:
        Base.metadata.create_all(bind=engine)
        break
    except OperationalError as falha:
        if loop == maximo_tentativas - 1:
            raise falha
        time.sleep(2)

app = FastAPI(title="Gerenciador de Biblioteca")


@app.get("/livros", response_model=list[LivroSaida])
def listar_todos_livros(db: Session = Depends(obter_conexao)):
    """Retorna a listagem completa dos livros cadastrados."""
    return db.query(Livro).all()


@app.post("/livros", response_model=LivroSaida, status_code=201)
def adicionar_novo_livro(corpo: LivroEntrada, db: Session = Depends(obter_conexao)):
    """Insere um novo livro no acervo."""
    novo = Livro(
        titulo=corpo.titulo,
        autor=corpo.autor,
        paginas=corpo.paginas,
        disponivel=corpo.disponivel,
    )
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo


@app.get("/livros/{livro_id}", response_model=LivroSaida)
def obter_livro_especifico(livro_id: int, db: Session = Depends(obter_conexao)):
    """Busca os detalhes de um livro específico através do ID."""
    livro = db.query(Livro).filter(Livro.id == livro_id).first()
    if not livro:
        raise HTTPException(status_code=404, detail="Livro não foi encontrado")
    return livro


@app.put("/livros/{livro_id}", response_model=LivroSaida)
def alterar_livro_existente(
    livro_id: int, corpo: LivroEntrada, db: Session = Depends(obter_conexao)
):
    """Modifica os dados de um livro já registrado."""
    livro = db.query(Livro).filter(Livro.id == livro_id).first()
    if not livro:
        raise HTTPException(status_code=404, detail="Livro não foi encontrado")

    livro.titulo = corpo.titulo
    livro.autor = corpo.autor
    livro.paginas = corpo.paginas
    livro.disponivel = corpo.disponivel

    db.commit()
    db.refresh(livro)
    return livro


@app.delete("/livros/{livro_id}", status_code=204)
def remover_livro_do_acervo(livro_id: int, db: Session = Depends(obter_conexao)):
    """Exclui permanentemente um livro do acervo."""
    livro = db.query(Livro).filter(Livro.id == livro_id).first()
    if not livro:
        raise HTTPException(status_code=404, detail="Livro não foi encontrado")

    db.delete(livro)
    db.commit()
