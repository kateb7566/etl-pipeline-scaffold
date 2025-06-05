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
    "main.py": 
        "# Entry point for the FastAPI app\n\nfrom fastapi import FastAPI\n\napp = FastAPI()\n\n@app.get('/')\ndef read_root():\n    return {\"message\": \"System Health Monitor API\"}\n",
    "config.py": "# Configuration via Pydantic or environment variables\n",
    "Dockerfile": "FROM python:3.11-slim\nWORKDIR /app\nCOPY . .\nRUN pip install -r requirements.txt\nCMD [\"uvicorn\", \"app.main:app\", \"--host\", \"0.0.0.0\", \"--port\", \"8000\"]\n",
    "docker-compose.yml": "version: '3.9'\nservices:\n  app:\n    build: .\n    ports:\n      - \"8000:8000\"\n    volumes:\n      - .:/app\n    depends_on:\n      - redis\n  redis:\n    image: redis:alpine\n",
    "requirements.txt": "fastapi\nuvicorn\npsutil\nsqlalchemy[asyncio]\naiofiles\npydantic\nredis\n",
    "README.md": "# System Health Monitor ETL\n\nThis project collects and visualizes system health metrics using FastAPI, SQLAlchemy, and Redis.\n"
}