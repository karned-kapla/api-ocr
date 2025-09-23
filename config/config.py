import os

# API Configuration
API_NAME = os.environ.get('API_NAME', 'api-ocr')
API_TAG_NAME = os.environ.get('API_TAG_NAME', 'ocr')
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
URL_API_GATEWAY = os.environ.get('URL_API_GATEWAY', 'http://localhost:8000')
UNPROTECTED_PATHS = ['/favicon.ico', '/docs', '/ocr/openapi.json', '/ocr/v1/tasks/results']
UNLICENSED_PATHS = []
MS_SECRET_TTL = os.environ.get("MS_SECRET_TTL", 3600)

# Keycloak Configuration
KEYCLOAK_HOST = os.environ.get('KEYCLOAK_HOST', 'http://localhost:8080')
KEYCLOAK_REALM = os.environ.get('KEYCLOAK_REALM', 'master')
KEYCLOAK_CLIENT_ID = os.environ.get('KEYCLOAK_CLIENT_ID', 'test-client')
KEYCLOAK_CLIENT_SECRET = os.environ.get('KEYCLOAK_CLIENT_SECRET', 'test-secret')

# Redis Configuration
REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.environ.get('REDIS_PORT', '6379'))
REDIS_DB = int(os.environ.get('REDIS_DB', '0'))
REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD', 'test-password')

# Kafka Configuration
KAFKA_HOST = os.environ.get('KAFKA_HOST', 'localhost')
KAFKA_PORT = int(os.environ.get('KAFKA_PORT', '9092'))
KAFKA_TOPIC = os.environ.get('KAFKA_TOPIC', 'ocr')

# ocr Response Configuration
OCR_RESPONSE_CHANNELS = [
    {
        "canal": "kafka",
        "topic": "ocr_done"
    },
    {
        "canal": "api",
        "url": "http://karned-api-ocr:8000/ocr/v1/tasks/results"
    }
]
