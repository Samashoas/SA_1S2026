import grpc
import time
from concurrent import futures
from app.protos import fx_service_pb2
from app.protos import fx_service_pb2_grpc
from app.services.fx_service import fx_service
from app.config import Config
from app.utils.logger import logger

class FXServiceServicer(fx_service_pb2_grpc.FXServiceServicer):    
    def GetExchangeRate(self, request, context):
        logger.info(f"Recibida solicitud gRPC: {request.from_currency} a {request.to_currency}")
        
        # Validaciones
        if not request.from_currency or not request.to_currency:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details('from_currency y to_currency son requeridos')
            return fx_service_pb2.ExchangeRateResponse()
        
        # Obtener tasa de cambio
        result, error = fx_service.get_exchange_rate(
            request.from_currency.upper(),
            request.to_currency.upper()
        )
        
        if error:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(error)
            return fx_service_pb2.ExchangeRateResponse()
        
        response = fx_service_pb2.ExchangeRateResponse(
            from_currency=result['from_currency'],
            to_currency=result['to_currency'],
            rate=result['rate'],
            timestamp=result['timestamp'],
            from_cache=result.get('from_cache', False),
            is_fallback=result.get('is_fallback', False)
        )
        
        logger.info(f"Respuesta enviada: rate={result['rate']}, from_cache={result.get('from_cache')}")
        return response

    def GetMultipleRates(self, request, context):
        logger.info(f"Recibida solicitud de múltiples tasas desde {request.base_currency}")
        
        # Validaciones
        if not request.base_currency or not request.target_currencies:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details('base_currency y target_currencies son requeridos')
            return fx_service_pb2.MultipleRatesResponse()
        
        # Obtener tasas
        result, error = fx_service.get_multiple_rates(
            request.base_currency.upper(),
            [currency.upper() for currency in request.target_currencies]
        )
        
        if error:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(error)
            return fx_service_pb2.MultipleRatesResponse()
        
        # Formar el json de respuesta respuesta
        response = fx_service_pb2.MultipleRatesResponse(
            base_currency=result['base_currency'],
            rates=result['rates'],
            timestamp=result['timestamp'],
            from_cache=result.get('from_cache', False)
        )
        
        logger.info(f"Respuesta enviada con {len(result['rates'])} tasas")
        return response

# Iniciar el servidor gRPC
def serve():
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=Config.GRPC_MAX_WORKERS),
        options=[
            ('grpc.max_send_message_length', 50 * 1024 * 1024),
            ('grpc.max_receive_message_length', 50 * 1024 * 1024),
        ]
    )
    
    fx_service_pb2_grpc.add_FXServiceServicer_to_server(FXServiceServicer(), server)
    
    server.add_insecure_port(f'[::]:{Config.GRPC_PORT}')
    server.start()
    
    logger.info(f"Servidor gRPC iniciado en puerto {Config.GRPC_PORT}")
    
    try:
        while True:
            time.sleep(86400)  # 1 día
            
    except KeyboardInterrupt:
        logger.info("Deteniendo servidor gRPC...")
        server.stop(0)

if __name__ == '__main__':
    serve()