from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Cria a instância do fastapi
# É esse objeto que o TestClient vai receber

app = FastAPI()

# Banco de dados em memória
tarefas_db: dict[int, dict] = {}
proximo_id: int =1

# modelo pydantic: define a forma dos dados recebidos no POST
# Pydantic valida automaticamente, se o tipo estiver errado, retorna 422
class Tarefa(BaseModel):
    titulo: str
    concluida: bool = False # Valor Padrão: Não concluída

# GET /tarefas - retorna todas as tarefas cadastradas
@app.get("/tarefas")
def listar_tarefas():
    # Converte o dict em lista para retornar como JSON array
    return list(tarefas_db.values())

# POST /tarefas - cria uma nova tarefa
# O fastapi lê o body json e valida contra tarefain automaticamente
@app.post("/tarefas", status_code=201)
def criar_tarefa(tarefa: Tarefa):
    global proximo_id
    nova ={"id": proximo_id, "titulo": tarefa.titulo, "concluida": tarefa.concluida }
    tarefas_db[proximo_id] = nova
    proximo_id +=1
    return nova # retorna a nova tarefa criada com seu id

# GET /tarefas/{id}
# {tarefa_id} na URL vira parâmetro de caminho automaticamente
@app.get("/tarefas/{tarefa_id}")
def obter_tarefa(tarefa_id: int):
    if tarefa_id not in tarefas_db:
        #HTTPEXception gera automaticamente uma resposta 404 com JSON
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return tarefas_db[tarefa_id]

@app.delete("/tarefas/{tarefa_id}", status_code=204)
def deletar_tarefa(tarefa_id: int):
    if tarefa_id not in tarefas_db:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    del tarefas_db[tarefa_id]
    # 204 No content: sucesso, mas sem body de resposta