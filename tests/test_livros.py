def test_obter_acervo_vazio(client):
    """GET /livros deve responder com lista vazia no início."""
    retorno = client.get("/livros")

    assert retorno.status_code == 200
    assert retorno.json() == []


def test_cadastrar_livro(client):
    """POST /livros deve inserir um livro com sucesso e retornar status 201."""
    retorno = client.post(
        "/livros",
        json={"titulo": "Dom Casmurro", "autor": "Machado de Assis", "paginas": 256, "disponivel": True},
    )
    dados = retorno.json()

    assert retorno.status_code == 201
    assert dados["titulo"] == "Dom Casmurro"
    assert dados["autor"] == "Machado de Assis"
    assert dados["paginas"] == 256
    assert dados["disponivel"] is True
    assert "id" in dados


def test_cadastrar_livro_padrao_disponivel(client):
    """POST /livros deve configurar a disponibilidade como True por padrão se omitida."""
    retorno = client.post(
        "/livros",
        json={"titulo": "O Cortiço", "autor": "Aluísio Azevedo", "paginas": 320},
    )
    dados = retorno.json()

    assert retorno.status_code == 201
    assert dados["disponivel"] is True


def test_listar_acervo_com_livros(client):
    """GET /livros deve listar todos os registros salvos."""
    client.post("/livros", json={"titulo": "Livro A", "autor": "Autor A", "paginas": 100})
    client.post("/livros", json={"titulo": "Livro B", "autor": "Autor B", "paginas": 200})

    retorno = client.get("/livros")
    dados = retorno.json()

    assert retorno.status_code == 200
    assert len(dados) == 2


def test_localizar_livro_id(client):
    """GET /livros/{id} deve trazer os dados do livro correspondente."""
    criacao = client.post("/livros", json={"titulo": "O Guarani", "autor": "José de Alencar", "paginas": 400})
    id_gerado = criacao.json()["id"]

    retorno = client.get(f"/livros/{id_gerado}")
    dados = retorno.json()

    assert retorno.status_code == 200
    assert dados["id"] == id_gerado
    assert dados["titulo"] == "O Guarani"


def test_localizar_livro_inexistente(client):
    """GET /livros/{id} deve retornar 404 caso o livro não conste no banco."""
    retorno = client.get("/livros/12345")

    assert retorno.status_code == 404
    assert retorno.json()["detail"] == "Livro não foi encontrado"


def test_modificar_livro(client):
    """PUT /livros/{id} deve alterar os atributos do livro indicado."""
    criacao = client.post("/livros", json={"titulo": "Nome Errado", "autor": "Autor", "paginas": 10})
    id_gerado = criacao.json()["id"]

    retorno = client.put(
        f"/livros/{id_gerado}",
        json={"titulo": "Nome Certo", "autor": "Autor Oficial", "paginas": 150, "disponivel": False},
    )
    dados = retorno.json()

    assert retorno.status_code == 200
    assert dados["titulo"] == "Nome Certo"
    assert dados["autor"] == "Autor Oficial"
    assert dados["paginas"] == 150
    assert dados["disponivel"] is False


def test_modificar_livro_inexistente(client):
    """PUT /livros/{id} deve retornar 404 ao tentar atualizar um livro inexistente."""
    retorno = client.put(
        "/livros/12345",
        json={"titulo": "Invisível", "autor": "Desconhecido", "paginas": 100},
    )

    assert retorno.status_code == 404
    assert retorno.json()["detail"] == "Livro não foi encontrado"


def test_remover_livro(client):
    """DELETE /livros/{id} deve excluir o livro e retornar status 204."""
    criacao = client.post("/livros", json={"titulo": "Descartável", "autor": "Ninguém", "paginas": 50})
    id_gerado = criacao.json()["id"]

    retorno = client.delete(f"/livros/{id_gerado}")
    assert retorno.status_code == 204

    # Confirmação da remoção
    busca = client.get(f"/livros/{id_gerado}")
    assert busca.status_code == 404


def test_remover_livro_inexistente(client):
    """DELETE /livros/{id} deve responder com 404 se o livro não for encontrado."""
    retorno = client.delete("/livros/12345")

    assert retorno.status_code == 404
    assert retorno.json()["detail"] == "Livro não foi encontrado"
