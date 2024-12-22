from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from prometheus_client import Counter, Histogram, generate_latest
import random
import httpx
from typing import Optional
from src.dtos.ISayHelloDto import ISayHelloDto

app = FastAPI()
messages = []
DEFAULT_SERVICES = [
    "https://stagging-api.upflame.org",
    "https://dev-api.upflame.org",
    "https://production-api.upflame.org",
]

@app.get("/")
async def root():
    """Root endpoint showing the 'devbranch' under development message."""
    return {"message": "This application is in 'devbranch' view - Currently under development. Stay tuned!"}

@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.post("/hello")
async def hello_message(dto: ISayHelloDto):
    return {"message": f"Hello {dto.message}"}
