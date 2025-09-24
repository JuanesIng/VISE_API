# ===== Base de ejecución =====
FROM python:3.11-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Paquetes del sistema (build/runtime mínimos)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
 && rm -rf /var/lib/apt/lists/*

# Carpeta de la app
WORKDIR /app

# Primero requirements para aprovechar caché
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copiar código
COPY app /app/app

# Crear usuario no root
RUN useradd -m -u 10001 appuser
USER appuser

# Exponer puerto
EXPOSE 8000

# Comando de arranque (Uvicorn)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]