import pytest
from unittest.mock import Mock, patch, MagicMock
from app.services.fx_service import FXService

class TestFXService:
    @pytest.fixture
    def fx_service(self):
        return FXService()
    
    @patch('app.services.fx_service.requests.get')
    @patch('app.services.fx_service.cache_service')
    def test_get_exchange_rate_success(self, mock_cache, mock_requests, fx_service):
        """Prueba obtener tasa de cambio exitosamente desde la API"""
        # Mock de caché sin datos
        mock_cache.get_rate.return_value = None
        
        # Mock de respuesta de la API
        mock_response = Mock()
        mock_response.json.return_value = {
            'result': 'success',
            'rates': {'USD': 0.13},
            'time_last_update_unix': 1234567890
        }
        mock_response.raise_for_status = Mock()
        mock_requests.return_value = mock_response
        
        # Ejecutar
        result, error = fx_service.get_exchange_rate('GTQ', 'USD')
        
        # Verificar
        assert error is None
        assert result is not None
        assert result['from_currency'] == 'GTQ'
        assert result['to_currency'] == 'USD'
        assert result['rate'] == 0.13
        assert result['from_cache'] is False
    
    @patch('app.services.fx_service.cache_service')
    def test_get_exchange_rate_from_cache(self, mock_cache, fx_service):
        """Prueba obtener tasa de cambio desde caché"""
        # Mock de caché con datos
        cached_data = {
            'from_currency': 'GTQ',
            'to_currency': 'USD',
            'rate': 0.13,
            'timestamp': 1234567890,
            'from_cache': True
        }
        mock_cache.get_rate.return_value = cached_data
        
        # Ejecutar
        result, error = fx_service.get_exchange_rate('GTQ', 'USD')
        
        # Verificar
        assert error is None
        assert result is not None
        assert result['from_cache'] is True
        assert result['rate'] == 0.13