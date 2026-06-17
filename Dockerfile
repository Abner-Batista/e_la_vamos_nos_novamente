# Usa a imagem oficial do Python, versão enxuta
FROM python:3.12-slim

# Define o diretório de trabalho dentro do container
WORKDIR /codigo

# Copia o arquivo de dependências primeiro (aproveita o cache do Docker)
COPY requirements.txt .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código da aplicação
COPY . .

# Expõe a porta que o uvicorn vai usar
EXPOSE 8000

# Comando para iniciar a aplicação
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
