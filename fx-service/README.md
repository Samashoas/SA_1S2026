# Microservicio fx-service


## Definición del Proto y sus archivos creados.
Para poder definir el esquema del proto que generará los dos archivos de python se debe hacer lo siguiente:

1. Ir a la carpeta /services/fx-service
2. Ejecutar el comando: `python -m grpc_tools.protoc -I./app/protos --python_out=./app/protos --grpc_python_out=./app/protos ./app/protos/fx_service.proto`

## Ejecución del servicio desde local

Para poder ejecutar este micro servicio de manera local lo que deben de hacer es:

1. Irse a la carpeta /services/fx-service
2. Ejecutar el comando: `python -m app.main`

## Requests:

En **POSTMAN** se debe de importar el proto del microservicio, este tiene 2 métodos (parte del contrato), los cuales serán el `GetExchangeRate` y `GetMultipleRates`.

Ambas peticiones se deben de realizar con "localhost:50051" y elegir la que corresponda, a continuación se encontrarán el body de cada una y el mensaje de respuesta en JSON.

- GetExchangeRate:

Body:
```json
{
    "from_currency": "GTQ",
    "to_currency": "USD"
}
```

Respuesta:
```json
{
    "from_currency": "GTQ",
    "to_currency": "USD",
    "rate": 0.130455,
    "timestamp": "1765152151",
    "from_cache": true,
    "is_fallback": false
}
```

- GetMultipleRates:

Body:
```json
{
    "base_currency": "GTQ",
    "target_currencies": ["USD", "MXN", "JPY"]
}
```

Respuesta:
```json
{
    "rates": {
        "JPY": 20.255469,
        "USD": 0.130455,
        "MXN": 2.372892
    },
    "base_currency": "GTQ",
    "timestamp": "1765152151",
    "from_cache": false
}
```

Los "from_cache" y "is_fallback" cambiarán dependiendo de si se ejecuta de forma repetida, ahí se almacenará en la caché para no saturar la llamada a la API, en caso de que la API se caiga estará el "is_fallback" que almacenará el cambio por 24 horas, el "from_cache" dura 6 minutos (360 segunds).

## Herramientas utilizadas

### Extraído desde el requirements.txt
Flask==3.0.0
flask-cors==4.0.0
grpcio==1.60.0
grpcio-tools==1.60.0
redis==5.0.1
requests==2.31.0
python-dotenv==1.0.0
pytest==7.4.3
pytest-mock==3.12.0

# Pruebas unitarias

## fx-service
cd services/fx-service
pytest -v

## payments-wallet-service
cd services/payments-wallet-service
pytest -v

## orders-service
cd services/orders-service
pytest -v