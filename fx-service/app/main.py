from flask import Flask, jsonify
from flask_cors import CORS
from app.config import Config
from app.utils.logger import logger
from app.grpc_server import serve as grpc_serve
import threading

app = Flask(__name__)
CORS(app)

# Saber si esta levantado el servicio.
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'service': 'fx-service',
        'version': '1.0.0'
    }), 200

# Endpoint raíz
@app.route('/', methods=['GET'])
def index():
    return jsonify({
        'service': 'fx-service',
        'description': 'Servicio de conversión de monedas con caché y fallback',
        'endpoints': {
            'health': '/health',
            'grpc_port': Config.GRPC_PORT
        }
    }), 200

def start_grpc_server():
    logger.info("Iniciando servidor gRPC en thread separado...")
    grpc_serve()

if __name__ == '__main__':
    grpc_thread = threading.Thread(target=start_grpc_server, daemon=True)
    grpc_thread.start()
    
    # Iniciar Flask
    logger.info(f"Iniciando servidor Flask en {Config.FLASK_HOST}:{Config.FLASK_PORT}")
    app.run(
        host=Config.FLASK_HOST,
        port=Config.FLASK_PORT,
        debug=Config.FLASK_DEBUG
    )