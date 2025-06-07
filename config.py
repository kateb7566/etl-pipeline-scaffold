PROJECT_STRUCTURE = {
    "app":
        {
            "api": ["__init__.py", "routes.py"],
            "ingest": ["__init__.py", "fetcher.py"],
            "models": ["__init__.py", "models.py"],
            "storage": ["__init__.py", "storage.py", "database.py", "cache_bucket.py"],
            "transformation": ["__init__.py", "transformer.py"],
            "utils": ["__init__.py", "logger.py"],
            "__files__": ["main.py", "config.py", "__init__.py"]
        },
    "test":
        [
            "__init__.py",
            "fetcher_test.py",
            "routes_test.py",
            "storage_test.py",
            "database_test.py",
            "cache_bucket_test.py",
            "transform_test.py"
        ]
    ,
    "__files__": ["dockerfile", "docker-compose.yml", "requirements.txt", "README.md", "pytest.ini", ".dockerignore", ".gitignore"]
    }

TEMPLATE_FILES = {
    "main.py": "from app.ingest.fetcher import Fetcher\nfrom app.storage.storage import Storage\nfrom app.storage.database import get_db_session\n\nfrom app.transformation.transformer import Transformer\nfrom app.utils.logger import get_logger\nimport asyncio\n\nlogger = get_logger(__name__)\n\nasync def main():\n    fetcher = Fetcher()\n    transformer = Transformer()\n    storage = Storage()\n    \n    try:\n        logger.info(\"Starting async data pipeline...\")\n        data = await fetcher.run() # Fetch Data\n        if data: # if data object does exist!\n            transformed_data = transformer.transform(data) # Transform data\n            # treat your code over here!\n            ####\n            ## your code!\n            ####\n            logger.info(\"something happened successfully!\")\n        else:\n            logger.warning(\"No data fetched.\")\n            \n    except Exception as e:\n        logger.exception(f\"Pipeline failed: {e}\")\n\nif __name__ == \"__main__\":\n    asyncio.run(main())",
    "config.py": "# manage API URLS and secrets\n\n\nfrom dotenv import load_dotenv\nimport os\n\n\nload_dotenv()\n\nclass Settings:\n    def __init__(self):\n        self.API_ENDPOINT = os.getenv(\"API_ENDPOINT\", \"\")\n        self.API_KEY = os.getenv(\"API_KEY\", \"\")\n        self.REQUEST_TIMEOUT = int(os.getenv(\"REQUEST_TIMEOUT\", 10)) # seconds\n        self.MAX_RETRIES = int(os.getenv(\"MAX_RETRIES\", 3))\n        self.RETRY_BACKOFF = float(os.getenv(\"RETRY_BACKOFF\", 1.5)) # seconds\n        self.OUTPUT_DIR = os.getenv(\"OUTPUT_DIR\")\n        self.LOG_LEVEL = os.getenv(\"LOG_LEVEL\", \"INFO\")\n        self.REDIS_URL = os.getenv(\"REDIS_URL\", \"redis://localhost:6379/0\")\n        self.DB_URL = os.getenv(\"DB_URL\", \"\")\n        \n        \nsettings = Settings()",
    "dockerfile": "FROM python:3.12-slim as build-stage\n\nWORKDIR /app\n\nCOPY requirements.txt .\n\nRUN pip install --no-cache-dir -r requirements.txt\n\nFROM python:3.12-slim as final-stage\n\nWORKDIR /app\n\nCOPY requirements.txt .\n\nRUN pip install --no-cache-dir -r requirements.txt\n\nCOPY /app/__main__.py .\n\nEXPOSE 5000\n\nCMD [\"python\", \"main.py\"]",
    "docker-compose.yml": "version: '3.8'\n\nservices:\n  health_monitor:\n    build: .\n    container_name: health_monitor\n    ports:\n      - \"5000:5000\"\n    depends_on:\n      - redis:\n        condition: service_started\n      - postgres:\n        condition: service_healthy\n    environment:\n      - REDIS_URL=redis://redis:6379/0\n      - DB_URL=\n\n  postgres:\n    image: postgres:17.5-bookworm\n    container_name: postgres_health_pipeline\n    restart: always\n    environment:\n      - POSTGRES_USER=DUMB_NAME\n      - POSTGRES_PASSWORD=123456\n      - POSTGRES_DB=health_monitor_db\n    healthcheck:\n      test: [\"CMD-SHELL\", \"pg-isready -U kateb7566\"]\n      interval: 5s\n      timeout: 5s\n      retries: 10\n      start_period: 30s\n    ports:\n      - \"5432:5432\"\n    volumes:\n      - postgres_data: /var/lib/postgresql/postgres_data\n  \n  redis:\n    image: redis:7-alpine\n    container_name: redis_health_cache\n    restart: always\n    ports:\n      - \"6379:6379\"\nvolumes:\n  postgres_data:",
    "pytest.ini": "[pytest]\npythonpath = .",
    ".env": "# .env\n\nAPI_ENDPOINT=website_url\nAPI_KEY=key_here\nREQUEST_TIMEOUT=10\nMAX_RETRIES=3\nRETRY_BACKOFF=1.5\nLOG_LEVEL=INFO\nOUTPUT_DIR=.\\output_dir\nREDIS_URL=REDIS_PATH\nDB_URL=",
    "requirements.txt": "fastapi\nuvicorn\npsutil\nsqlalchemy[asyncio]\naiofiles\npydantic\nredis\n",
    "README.md": "# System Health Monitor ETL\n\nThis project collects and visualizes system health metrics using FastAPI, SQLAlchemy, and Redis.\n"
}