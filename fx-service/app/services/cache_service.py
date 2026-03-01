import redis
import json
from typing import Optional, Dict, Any
from app.config import Config
from app.utils.logger import logger

class CacheService:
    def __init__(self):
        try:
            self.redis_client = redis.Redis(
                host=Config.REDIS_HOST,
                port=Config.REDIS_PORT,
                db=Config.REDIS_DB,
                password=Config.REDIS_PASSWORD,
                decode_responses=True,
                socket_connect_timeout=5,
                socket_timeout=5
            )

            # Test de conexión
            self.redis_client.ping()
            logger.info(f"Conectado a Redis en {Config.REDIS_HOST}:{Config.REDIS_PORT}")

        except redis.ConnectionError as e:
            logger.error(f"Error conectando a Redis: {e}")
            self.redis_client = None
    
    def _get_cache_key(self, from_currency: str, to_currency: str, is_fallback: bool = False) -> str:
        suffix = ":fallback" if is_fallback else ""
        return f"fx:{from_currency}:{to_currency}{suffix}"
    
    def get_rate(self, from_currency: str, to_currency: str) -> Optional[Dict[str, Any]]:
        if not self.redis_client:
            return None
        
        try:
            cache_key = self._get_cache_key(from_currency, to_currency)
            cached_data = self.redis_client.get(cache_key)
            
            if cached_data:
                logger.info(f"Hay cache: {cache_key}")
                return json.loads(cached_data)
            
            logger.info(f"No hay caché : {cache_key}")
            return None
        except Exception as e:
            logger.error(f"Error obteniendo de caché: {e}")
            return None
    
    def set_rate(self, from_currency: str, to_currency: str, rate: float, timestamp: int, ttl: int = None) -> bool:
        if not self.redis_client:
            return False
        
        try:
            cache_key = self._get_cache_key(from_currency, to_currency)
            fallback_key = self._get_cache_key(from_currency, to_currency, is_fallback=True)
            
            data = {
                'from_currency': from_currency,
                'to_currency': to_currency,
                'rate': rate,
                'timestamp': timestamp,
                'from_cache': True
            }
            
            ttl = ttl or Config.CACHE_TTL
            
            self.redis_client.setex(cache_key, ttl, json.dumps(data))
            self.redis_client.setex(fallback_key, Config.FALLBACK_TTL, json.dumps(data))
            
            logger.info(f"Guardado en caché: {cache_key} (TTL: {ttl}s)")
            return True
        except Exception as e:
            logger.error(f"Error guardando en caché: {e}")
            return False
    
    def get_fallback_rate(self, from_currency: str, to_currency: str) -> Optional[Dict[str, Any]]:
        if not self.redis_client:
            return None
        
        try:
            fallback_key = self._get_cache_key(from_currency, to_currency, is_fallback=True)
            cached_data = self.redis_client.get(fallback_key)
            
            if cached_data:
                logger.warning(f"Usando fallback: {fallback_key}")
                data = json.loads(cached_data)
                data['is_fallback'] = True
                return data
            
            return None
        except Exception as e:
            logger.error(f"Error obteniendo fallback: {e}")
            return None
    
    def set_multiple_rates(self, base_currency: str, rates: Dict[str, float], timestamp: int) -> bool:
        if not self.redis_client:
            return False
        
        try:
            pipe = self.redis_client.pipeline()
            
            for target_currency, rate in rates.items():
                cache_key = self._get_cache_key(base_currency, target_currency)
                fallback_key = self._get_cache_key(base_currency, target_currency, is_fallback=True)
                
                data = {
                    'from_currency': base_currency,
                    'to_currency': target_currency,
                    'rate': rate,
                    'timestamp': timestamp,
                    'from_cache': True
                }
                
                pipe.setex(cache_key, Config.CACHE_TTL, json.dumps(data))
                pipe.setex(fallback_key, Config.FALLBACK_TTL, json.dumps(data))
            
            pipe.execute()
            logger.info(f"Guardadas {len(rates)} tasas en caché para {base_currency}")
            return True
        except Exception as e:
            logger.error(f"Error guardando múltiples tasas: {e}")
            return False
        
    def clear_cache(self, pattern: str = "fx:*") -> int:
        if not self.redis_client:
            return 0
        
        try:
            keys = self.redis_client.keys(pattern)
            if keys:
                deleted = self.redis_client.delete(*keys)
                logger.info(f"🗑️ Eliminadas {deleted} claves de caché")
                return deleted
            return 0
        except Exception as e:
            logger.error(f"Error limpiando caché: {e}")
            return 0

# Instancia singleton
cache_service = CacheService()