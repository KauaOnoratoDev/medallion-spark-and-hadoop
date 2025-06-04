FROM bitnami/spark:latest

# Define diretório de trabalho
WORKDIR /app

# Atualiza o repositório e instala dependências do sistema
USER root
RUN apt-get update && \
    apt-get install -y gcc libffi-dev libssl-dev python3-dev build-essential && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN curl -L -o /opt/bitnami/spark/jars/postgresql-42.6.0.jar https://jdbc.postgresql.org/download/postgresql-42.6.0.jar

# Instala poetry
RUN pip install poetry

# Copia arquivos de dependência
COPY pyproject.toml poetry.lock ./

# Instala as dependências com poetry (sem criar virtualenv)
RUN poetry config virtualenvs.create false && \
    poetry install --no-root

# Copia o restante da aplicação
COPY . .

# Comando padrão
CMD ["sh", "-c", "\
    poetry run python3 orchestrator/scheduler.py && \
    poetry run python3 excel/df_to_excel.py && \
    poetry run python3 email/send_email.py"]
