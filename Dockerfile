FROM python:3.10-slim

ENV FLASK_CONTEXT=production
ENV PYTHONDONTWRITEBYTECODE=1 
ENV PYTHONUNBUFFERED=1
ENV PATH=$PATH:/home/sysacad/.venv/bin

# Creamos un usuario no-root por seguridad y establecemos el directorio de trabajo
RUN useradd --create-home --home-dir /home/sysacad sysacad

#Dependencias necesarias para psycopg2 / uv
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-dev \
    build-essential \
    libpq-dev \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /home/sysacad

RUN curl -fsSL https://astral.sh/uv/install.sh | sh \
    && install -m 0755 /root/.local/bin/uv /usr/local/bin/uv

    # Copiamos primero el archivo de dependencias para aprovechar el cache de Docker
COPY pyproject.toml uv.lock ./

#creamos el venv e instalamos dependencias versiones
RUN uv sync --locked

COPY app ./app 
COPY app.py .

# Cambiamos al usuario no-root ANTES de instalar dependencias
RUN chown -R sysacad:sysacad /home/sysacad
USER sysacad

ENV VIRTUAL_ENV="/home/sysacad/.venv"

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "app:app"]


#Migré de requirements.txt a uv con lockfile 
#para asegurar builds reproducibles, eliminé 
#dependencias innecesarias, dejé solo las requeridas 
#para PostgreSQL, uso usuario no-root .