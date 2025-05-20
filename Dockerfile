FROM python:3.11-slim

# Instalar dependências do sistema necessárias para o WeasyPrint
RUN apt-get update && apt-get install -y \
    build-essential \
    libcairo2 \
    pango1.0-tools \
    libpango-1.0-0 \
    libgdk-pixbuf2.0-0 \
    libffi-dev \
    libssl-dev \
    python3-dev \
    && apt-get clean

# Criar diretório do app
WORKDIR /app

# Copiar arquivos
COPY . /app/

# Instalar dependências Python
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expõe a porta
EXPOSE 8000

# Comando para rodar a aplicação
CMD ["gunicorn", "agendamento.wsgi:application", "--bind", "0.0.0.0:8000"]
