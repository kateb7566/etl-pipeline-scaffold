# Entry point for the FastAPI app

from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def read_root():
    return {"message": "System Health Monitor API"}
