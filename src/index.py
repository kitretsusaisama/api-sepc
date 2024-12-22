from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from prometheus_client import Counter, Histogram, generate_latest
import random
import httpx
from typing import Optional

# Prometheus Metrics
REQUESTS = Counter("requests_total", "Total number of requests processed", ["method", "route"])
LATENCY = Histogram("request_latency_seconds", "Request latency in seconds", ["method", "route"])

# App Initialization
app = FastAPI()

# Sample in-memory data store (temporary storage)
messages = []
DEFAULT_SERVICES = [
    "https://stagging-api.upflame.org",
    "https://dev-api.upflame.org",
    "https://production-api.upflame.org",
]

# DTOs
class HelloMessage(BaseModel):
    message: str

class ProxyRequest(BaseModel):
    path: str
    method: Optional[str] = "GET"

# Middleware for Metrics and Logging
@app.middleware("http")
async def log_and_measure(request: Request, call_next):
    method = request.method
    route = request.url.path
    REQUESTS.labels(method, route).inc()

    start_time = LATENCY.labels(method, route).time()
    response = await call_next(request)
    start_time()
    return response

# Routes

@app.get("/")
async def root():
    """Root endpoint showing the 'devbranch' under development message."""
    return {"message": "This application is in 'devbranch' view - Currently under development. Stay tuned!"}

@app.get("/hello/{name}")
async def say_hello(name: str):
    """Greets the user."""
    return {"message": f"Hello {name}"}

@app.post("/hello")
async def hello_message(dto: HelloMessage):
    """Receives and returns a custom message."""
    messages.append(dto.message)
    return {"message": f"Hello {dto.message}"}

@app.post("/proxy")
async def proxy_request(proxy: ProxyRequest):
    """Proxies a request to one of the backend services."""
    backend_service = random.choice(DEFAULT_SERVICES)
    target_url = f"{backend_service}/{proxy.path.lstrip('/')}"
    
    async with httpx.AsyncClient() as client:
        if proxy.method.upper() == "GET":
            response = await client.get(target_url)
        elif proxy.method.upper() == "POST":
            response = await client.post(target_url)
        else:
            raise HTTPException(status_code=405, detail="Method not allowed")

    return JSONResponse(content=response.json(), status_code=response.status_code)

@app.get("/metrics")
async def get_metrics():
    """Returns Prometheus metrics."""
    return JSONResponse(content=generate_latest().decode("utf-8"))
