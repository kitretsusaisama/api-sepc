from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
#from src.DB_Connection import DB_Connection
import logging
from src.dtos.ISayHelloDto import ISayHelloDto
#connection = DB_Connection()

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def createLogger():
    #Formerly __name__  now uvicorn
    logger = logging.getLogger("uvicorn")
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler())
    return logger


@app.get("/")
async def root():
    log = createLogger()
    log.info("TEST CASE")
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.post("/hello")
async def hello_message(dto: ISayHelloDto):
    return {"message": f"Hello {dto.message}"}
