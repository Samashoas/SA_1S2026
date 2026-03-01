import os
from dotenv import load_dotenv

load_dotenv()

class Config:    
    # API Externa de Exchange Rate
    FX_API_BASE_URL = os.getenv('FX_API_BASE_URL')
    FX_API_TIMEOUT = int(os.getenv('FX_API_TIMEOUT'))
    
    # Redis Configuration
    REDIS_HOST = os.getenv('REDIS_HOST')
    REDIS_PORT = int(os.getenv('REDIS_PORT'))
    REDIS_DB = int(os.getenv('REDIS_DB'))
    REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')
    
    # Cache TTL (Time To Live) en segundos
    CACHE_TTL = int(os.getenv('CACHE_TTL'))  # 6 minutos por defecto
    FALLBACK_TTL = int(os.getenv('FALLBACK_TTL'))  # 24 horas
    
    # gRPC Configuration
    GRPC_PORT = os.getenv('GRPC_PORT')
    GRPC_MAX_WORKERS = int(os.getenv('GRPC_MAX_WORKERS'))
    
    # Flask Configuration (Health check)
    FLASK_HOST = os.getenv('FLASK_HOST')
    FLASK_PORT = int(os.getenv('FLASK_PORT'))
    FLASK_DEBUG = os.getenv('FLASK_DEBUG').lower()
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL')