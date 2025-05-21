# Etapa 1 - Builder para instalar dependências
FROM python:3.12-slim AS builder

WORKDIR /app

# Instala dependências do sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copia e instala as dependências
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /wheels -r requirements.txt


# Etapa 2 - Imagem final
FROM python:3.12-slim

WORKDIR /app

# Instala somente as dependências necessárias (a partir dos wheels gerados no builder)
COPY --from=builder /wheels /wheels
RUN pip install --no-cache /wheels/* && rm -rf /wheels

# Copia todo o projeto
COPY . .

# Define a variável de ambiente para produção
ENV PYTHONUNBUFFERED=1
ENV ENVIRONMENT=production

# Expondo a porta
EXPOSE 8000

# Comando para iniciar o servidor uvicorn em modo produção
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]

