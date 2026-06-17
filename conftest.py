# fixtures disponíveis para TODOS os testes e os arquivos de teste
import pytest
from fastapi.testclient import TestClient
import main
from main import app

# @pytest.fixture marca uma função como fixture
# Toda a função de teste que declare client como parâmetro receberá automaticamente o valor que esta no fixture yield
@pytest.fixture
def client():
    # Código de setup de preparação
    # Limpa o estado global da API antes de cada teste
    main.tarefas_db.clear()
    main.proximo_id = 1

    # yiel entre o clinte para teste
    # A execução pausa aqui enquanto o teste roda.
    yield TestClient(app)

    # Depois do yield códio (limpeza)
    # Executar mesmo se o teste falhar
    main.tarefas_db.clear()
    main.proximo_id = 1
# Porque usamos o yield ao inves do return? O yield ele permite que você defina o código de limpeza após o teste terminar. Com o return vc teria apenas o setup e nunca rodaria a limpeza.