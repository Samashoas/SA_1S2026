FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código
COPY . .

# Compilar archivos .proto
RUN python -m grpc_tools.protoc \
    -I./app/protos \
    --python_out=./app/protos \
    --grpc_python_out=./app/protos \
    ./app/protos/fx_service.proto \
 && sed -i 's/^import fx_service_pb2 as fx__service__pb2/from app.protos import fx_service_pb2 as fx__service__pb2/' app/protos/fx_service_pb2_grpc.py

# Exponer puertos
EXPOSE 5000 50052

HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Comando de inicio
CMD ["python", "-m", "app.main"]